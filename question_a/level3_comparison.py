import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../setup/readings.csv")

# Recreate the two detectors
def zscore_detector(hr, window, threshold=3.0):
    predictions = [0] * len(hr)

    for i in range(window, len(hr)):
        previous = hr[i - window:i]
        mean = previous.mean()
        std = previous.std()

        if std > 0:
            z = abs((hr[i] - mean) / std)

            if z > threshold:
                predictions[i] = 1

    return predictions


hr = df["hr"].to_numpy()

pred_60 = zscore_detector(hr, 60)
pred_120 = zscore_detector(hr, 120)

# Find missed silent-drift readings
silent = df["anomaly_type"] == "silent_drift"

missed_60 = silent & (pd.Series(pred_60) == 0)
missed_120 = silent & (pd.Series(pred_120) == 0)

# Choose one missed reading from each method
idx_60 = df.index[missed_60][0]
idx_120 = df.index[missed_120][0]

# Plot 60-second missed anomaly
plt.figure(figsize=(10, 5))
start = max(0, idx_60 - 60)
end = min(len(df), idx_60 + 60)

plt.plot(df.index[start:end], df["hr"].iloc[start:end])
plt.axvline(idx_60, linestyle="--")
plt.title("Silent Drift Missed by 60-Second Z-Score Detector")
plt.xlabel("Reading")
plt.ylabel("Heart Rate (bpm)")
plt.tight_layout()
plt.savefig("missed_silent_drift_60s.png")
plt.close()

# Plot 120-second missed anomaly
plt.figure(figsize=(10, 5))
start = max(0, idx_120 - 60)
end = min(len(df), idx_120 + 60)

plt.plot(df.index[start:end], df["hr"].iloc[start:end])
plt.axvline(idx_120, linestyle="--")
plt.title("Silent Drift Missed by 120-Second Z-Score Detector")
plt.xlabel("Reading")
plt.ylabel("Heart Rate (bpm)")
plt.tight_layout()
plt.savefig("missed_silent_drift_120s.png")
plt.close()

print("60-second missed anomaly:", idx_60)
print("120-second missed anomaly:", idx_120)
print("Plots created successfully.")