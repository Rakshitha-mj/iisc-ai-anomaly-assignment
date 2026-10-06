import sqlite3

conn = sqlite3.connect("readings.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    timestamp TEXT,
    hr REAL,
    acc REAL,
    label INTEGER,
    anomaly_type TEXT
)
""")

data = [
    (1, "2026-10-06 10:00:01", 72, 0.2, 0, None),
    (2, "2026-10-06 10:00:02", 80, 0.3, 0, None),
    (3, "2026-10-06 10:00:03", 125, 0.1, 1, "spike")
]

cur.executemany("""
INSERT INTO readings (user_id, timestamp, hr, acc, label, anomaly_type)
VALUES (?, ?, ?, ?, ?, ?)
""", data)

print("Query 1: All readings")
for row in cur.execute("SELECT * FROM readings"):
    print(row)

print("\nQuery 2: Anomalies")
for row in cur.execute(
    "SELECT * FROM readings WHERE label = 1"
):
    print(row)

print("\nQuery 3: Average HR by user")
for row in cur.execute(
    "SELECT user_id, AVG(hr) FROM readings GROUP BY user_id"
):
    print(row)

conn.commit()
conn.close()