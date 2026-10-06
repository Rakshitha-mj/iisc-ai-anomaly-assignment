# Question C — Scalable Storage Architecture

## Level 1

For 1000 users sending 1 reading per second, the system receives:

- 1000 writes/second
- 86.4 million readings/day

Architecture:

Users → Ingestion API → Message Queue → Time-Series Database

The database stores:
- user_id
- timestamp
- heart_rate
- acceleration
- label
- anomaly_type

Data is partitioned by time and indexed by user_id and timestamp.

Older data can be moved to cheaper object storage for long-term retention.