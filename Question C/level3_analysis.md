# Question C — Level 3 Analysis

## Prediction

For 1000 users sending 1 reading per second:

- Writes per second = 1000
- Readings per day = 86,400,000
- Readings per 30-day month = 2,592,000,000

At 100,000 users:

- Writes per second = 100,000
- Readings per day = 8,640,000,000
- The system would need distributed ingestion, partitioned/time-series storage, message queues, and horizontal scaling.

## Storage

Assuming approximately 50 bytes per reading:

2,592,000,000 × 50 bytes ≈ 129.6 GB/month.

Actual storage will be higher after database indexes, metadata, replication, and overhead.

## Changes at 100,000 users

At this scale, a single database server would not be sufficient. I would use:

- Multiple ingestion servers
- Load balancing
- Message queue/stream processing
- Distributed time-series database
- Time-based partitioning
- Retention and archival policies