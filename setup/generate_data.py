import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

S = 2513
np.random.seed(S)

# 2 hours, 1 reading/second
n = 7200

timestamps = pd.date_range(
    "2026-10-06 00:00:00",
    periods=n,
    freq="s"
)

t = np.arange(n)

# -----------------------------
# Normal heart rate
# -----------------------------
resting_hr = 60 + (S % 20)

hr = (
    resting_hr
    + 2 * np.sin(2 * np.pi * t / 3600)
    + 1.5 * np.sin(2 * np.pi * t / 10)
    + np.random.normal(0, 1.5, n)
)

# -----------------------------
# Movement
# -----------------------------
acc = np.abs(np.random.normal(0.05, 0.02, n))

# Three normal walking periods
walking_periods = [
    (800, 1200),
    (2800, 3250),
    (5000, 5400)
]

for start, end in walking_periods:
    acc[start:end] = np.abs(
        np.random.normal(0.8, 0.15, end - start)
    )

    hr[start:end] += np.random.uniform(20, 30)

# -----------------------------
# 20 anomaly EVENTS
# 7 spikes + 7 dropouts + 6 silent drifts
# -----------------------------
anomalies = [
    (300, "spike"),
    (600, "dropout"),

    (1200, "silent_drift"),
    (1600, "spike"),
    (1900, "dropout"),
    (2000, "silent_drift"),
    (2400, "spike"),
    (2600, "dropout"),

    (3300, "silent_drift"),
    (3700, "spike"),
    (3900, "dropout"),
    (4100, "silent_drift"),
    (4500, "spike"),
    (4700, "dropout"),

    (5500, "silent_drift"),
    (5900, "spike"),
    (6100, "dropout"),
    (6250, "silent_drift"),
    (6650, "spike"),
    (6900, "dropout")
]

label = np.zeros(n, dtype=int)
anomaly_type = np.array(["normal"] * n, dtype=object)

for start, kind in anomalies:

    if kind == "spike":
        duration = np.random.randint(3, 11)
        end = start + duration

        hr[start:end] += np.random.uniform(40, 55)
        acc[start:end] = 0

    elif kind == "dropout":
        duration = np.random.randint(10, 31)
        end = start + duration

        hr[start:end] = 0

    else:  # silent drift
        duration = 300
        end = start + duration

        hr[start:end] += np.linspace(0, 15, duration)
        acc[start:end] = 0

    label[start:end] = 1
    anomaly_type[start:end] = kind

# -----------------------------
# Create dataframe
# -----------------------------
df = pd.DataFrame({
    "timestamp": timestamps,
    "hr": hr,
    "acc": acc,
    "label": label,
    "anomaly_type": anomaly_type
})

# Save dataset
df.to_csv("readings.csv", index=False)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(16, 6))

plt.plot(
    df["timestamp"],
    df["hr"],
    linewidth=0.8
)

anomaly_rows = df[df["label"] == 1]

plt.scatter(
    anomaly_rows["timestamp"],
    anomaly_rows["hr"],
    s=5,
    label="Anomalies"
)

plt.xlabel("Timestamp")
plt.ylabel("Heart Rate (bpm)")
plt.title("Wearable Heart Rate Signal with Anomalies")
plt.legend()
plt.tight_layout()

plt.savefig("signal_plot.png", dpi=150)
plt.close()

print("Dataset generated successfully.")
print("Seed:", S)
print("Rows:", len(df))
print("Anomaly EVENTS:", len(anomalies))
print("Anomaly readings:", df["label"].sum())
print("\nAnomaly types:")
print(df[df["label"] == 1]["anomaly_type"].value_counts())