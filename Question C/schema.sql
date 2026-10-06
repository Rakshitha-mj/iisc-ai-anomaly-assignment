CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    hr REAL NOT NULL,
    acc REAL NOT NULL,
    label INTEGER NOT NULL,
    anomaly_type TEXT
);