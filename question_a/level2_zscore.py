import csv
import numpy as np

# Load data
hr = []
acc = []
labels = []
anomaly_types = []

with open("../setup/readings.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        hr.append(float(row["hr"]))
        acc.append(float(row["acc"]))
        labels.append(int(row["label"]))
        anomaly_types.append(row["anomaly_type"])

hr = np.array(hr)
acc = np.array(acc)
labels = np.array(labels)

# Rolling z-score detector
window = 120
threshold = 3.0

predictions = np.zeros(len(hr), dtype=int)

for i in range(window, len(hr)):
    previous = hr[i - window:i]

    mean = np.mean(previous)
    std = np.std(previous)

    if std > 0:
        z_score = abs((hr[i] - mean) / std)

        if z_score > threshold:
            predictions[i] = 1


# Calculate metrics from scratch
def calculate_metrics(true, predicted):
    tp = np.sum((true == 1) & (predicted == 1))
    fp = np.sum((true == 0) & (predicted == 1))
    fn = np.sum((true == 1) & (predicted == 0))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return precision, recall, f1


print("Rolling Z-Score Detector")
print("Window:", window)
print("Threshold:", threshold)

precision, recall, f1 = calculate_metrics(labels, predictions)

print("\nOverall:")
print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"F1-score:  {f1:.3f}")


print("\nPerformance by Anomaly Type:")

for anomaly_type in ["spike", "dropout", "silent_drift"]:

    true_type = np.array([
        1 if t == anomaly_type else 0
        for t in anomaly_types
    ])

    precision, recall, f1 = calculate_metrics(
        true_type,
        predictions
    )

    print(
        f"{anomaly_type}: "
        f"precision={precision:.3f}, "
        f"recall={recall:.3f}, "
        f"f1={f1:.3f}"
    )


# False alarms during walking
walking = (acc > 0.5) & (labels == 0)
false_alarms = np.sum((predictions == 1) & walking)

print("\nFalse alarms during walking:", false_alarms)

from sklearn.metrics import precision_score, recall_score, f1_score

print("\nScikit-learn Verification:")

print(f"Precision: {precision_score(labels, predictions, zero_division=0):.3f}")
print(f"Recall:    {recall_score(labels, predictions, zero_division=0):.3f}")
print(f"F1-score:  {f1_score(labels, predictions, zero_division=0):.3f}")