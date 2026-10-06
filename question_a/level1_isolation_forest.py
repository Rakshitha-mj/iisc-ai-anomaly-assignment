import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("../setup/readings.csv")

# Features
X = df[["hr", "acc"]]

# True anomaly labels
y_true = (df["label"] == 1).astype(int)

# Isolation Forest
model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=2513
)

# Predict
y_pred = model.fit_predict(X)

# Convert: -1 = anomaly, 1 = normal
y_pred = (y_pred == -1).astype(int)

print("\nClassification Report:")
print(classification_report(
    y_true,
    y_pred,
    target_names=["Normal", "Anomaly"],
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

# Performance by anomaly type
from sklearn.metrics import precision_score, recall_score, f1_score

print("\nPerformance by Anomaly Type:")

for anomaly_type in ["spike", "dropout", "silent_drift"]:
    y_type_true = (df["anomaly_type"] == anomaly_type).astype(int)

    precision = precision_score(y_type_true, y_pred, zero_division=0)
    recall = recall_score(y_type_true, y_pred, zero_division=0)
    f1 = f1_score(y_type_true, y_pred, zero_division=0)

    print(
        f"{anomaly_type}: "
        f"precision={precision:.3f}, "
        f"recall={recall:.3f}, "
        f"f1={f1:.3f}"
    )
    
# False alarms during walking
walking = (df["acc"] > 0.5) & (df["label"] == 0)
false_alarms = ((y_pred == 1) & walking).sum()

print("\nFalse alarms during walking:", false_alarms)