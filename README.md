# API Ingestion Pipeline

A Python-based data ingestion pipeline that extracts product data from an API,
transforms and validates the data, and loads it into ClickHouse.

## Architecture

```text
API
 ↓
Extraction with retry
 ↓
Validation & transformation
 ↓
Generators & batching
 ↓
ClickHouse
```

The pipeline processes data incrementally using generators and batches instead
of loading the entire dataset into memory.

## Features
API pagination
HTTP error handling and retries with exponential backoff

- Data validation using dataclasses
- Product and review transformation
- Generator-based processing
- Batch loading
- Checkpoint-based restartability
- Structured logging

## Tech Stack
- Python
- Requests
- Tenacity
- ClickHouse
- clickhouse-connect

## Project Status
The core ingestion pipeline is implemented, including retry handling,
transformation, batching, and checkpoint-based restartability.
