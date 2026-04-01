# Automated Lab Data Pipeline Simulator

**Author:** Haris Khan  
**Date:** April 2026  
**Tech Stack:** Python · SQLite · Windows Task Scheduler · pandas · os · shutil

---

## Overview

A Windows-based automated data pipeline that bridges local laboratory equipment output to a centralized data ecosystem — simulating exactly the infrastructure required in regulated medical device laboratory environments (e.g. SHL Medical, pharmaceutical labs).

Built to demonstrate practical skills in:
- **Data pipeline automation** (Windows-based Python scripting)
- **Data Lake architecture** (SQLite as a lightweight local data lake)
- **ALCOA+ data integrity** (Attributable, Legible, Contemporaneous, Original, Accurate)
- **Data lineage tracking** (full audit trail from instrument → server → database)
- **Metadata tagging** (standardized filename conventions with timestamp + operator + instrument ID)
- **Windows automation** (Task Scheduler for hourly execution)

---

## Architecture

```
[Lab Instrument / Biosensor]
         |
         | generates CSV every session
         v
[Local_Lab_PC/]                  ← Step 1: sensor_data.csv
         |
         | step2_pipeline_agent.py (runs hourly via Task Scheduler)
         | - Renames file with timestamp + metadata tag
         | - Verifies MD5 checksum (data integrity)
         | - Moves file to Central_Server
         | - Writes ALCOA+ audit log
         v
[Central_Server/]                ← Step 2: 20250401_143022_BIOSENSOR-01_HK-001_sensor_data.csv
         |                                  transfer_log.json
         | step3_data_lake.py
         | - Reads all CSV files
         | - Inserts into SQLite database
         | - Records full data lineage
         v
[Central_Server/lab_data_lake.db] ← Step 3: queryable, structured, traceable
```

---

## Project Structure

```
lab_pipeline_project/
│
├── step1_generate_data.py      # Simulates lab instrument — generates CSV sensor data
├── step2_pipeline_agent.py     # Windows automation — metadata tag, migrate, verify
├── step3_data_lake.py          # SQLite data lake — ingest, structure, lineage tracking
├── step4_scheduler_setup.py    # Generates Windows Task Scheduler XML config
├── run_pipeline.py             # Runs all steps end-to-end (demo runner)
│
├── Local_Lab_PC/               # Simulated local lab PC folder (equipment output)
├── Central_Server/             # Simulated central server (receives migrated data)
│   ├── *.csv                   # Timestamped, tagged data files
│   ├── transfer_log.json       # ALCOA+ audit trail
│   └── lab_data_lake.db        # SQLite data lake database
│
└── README.md
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install pandas

# 2. Run the full pipeline end-to-end
python run_pipeline.py

# 3. Set up hourly Windows automation
python step4_scheduler_setup.py
# Then import the generated XML into Windows Task Scheduler
```

---

## Key Features

### ALCOA+ Data Integrity
Every record is:
- **Attributable** — operator_id and instrument_id embedded in filename and database
- **Legible** — standardized CSV format with clear column headers
- **Contemporaneous** — transfer and ingestion timestamps recorded at time of action
- **Original** — MD5 checksum verified before and after transfer; source removed only after integrity confirmed
- **Accurate** — PASS/FLAG status assigned at generation; anomalies preserved, not corrected

### Data Lineage Tracking
The `data_lineage` table in SQLite records:
- Original filename → tagged filename
- Transfer timestamp → ingestion timestamp
- Operator and instrument identifiers
- MD5 checksum for integrity verification
- Number of rows ingested per file

Every record in `sensor_measurements` references its source file, enabling complete traceability from the database record back to the original instrument reading.

### Metadata Tagging
Files are renamed using a standardized convention:
```
YYYYMMDD_HHMMSS_<INSTRUMENT_ID>_<OPERATOR_ID>_<original_filename>.csv
Example: 20260401_143022_BIOSENSOR-01_HK-001_sensor_data.csv
```

### Windows Task Scheduler Integration
Step 4 generates a ready-to-import XML configuration for Windows Task Scheduler. Once imported, the pipeline runs automatically every hour without any manual intervention.

---

## Database Schema

### sensor_measurements
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| record_id | TEXT | Globally unique record identifier |
| source_file | TEXT | Original CSV filename (lineage) |
| tagged_file | TEXT | Timestamped filename (lineage) |
| ingestion_time | TEXT | When inserted into database |
| timestamp | TEXT | When reading was taken by instrument |
| temperature_C | REAL | Temperature measurement |
| pressure_kPa | REAL | Pressure measurement |
| voltage_mV | REAL | Biosensor signal voltage |
| status | TEXT | PASS / FLAG |
| operator_id | TEXT | Who ran the instrument (ALCOA+) |
| instrument_id | TEXT | Which instrument (ALCOA+) |

### data_lineage
| Column | Type | Description |
|---|---|---|
| source_filename | TEXT | Original file from Local_Lab_PC |
| tagged_filename | TEXT | Renamed file in Central_Server |
| transfer_timestamp | TEXT | When file was moved |
| ingestion_timestamp | TEXT | When data entered database |
| checksum_md5 | TEXT | File integrity verification hash |
| rows_ingested | INTEGER | Number of records processed |

---

## Relevance to Regulated Laboratory Environments

This project directly addresses the data management challenges in regulated laboratory environments such as medical device companies, pharmaceutical labs, and semiconductor fabs:

1. **Eliminates data silos** — automated pipeline ensures no data stays trapped on local lab PCs
2. **Ensures compliance** — ALCOA+ principles built into every transfer and storage step
3. **Enables audit readiness** — complete lineage from instrument to database, queryable at any time
4. **Scalable architecture** — swap SQLite for a cloud database (Azure Blob, AWS S3) with minimal code changes
5. **Zero manual intervention** — Windows Task Scheduler ensures continuous operation

---

## Skills Demonstrated

| Skill | Where |
|---|---|
| Python automation scripting | step1, step2 |
| Windows-based file operations (os, shutil) | step2 |
| Metadata tagging & naming conventions | step2 |
| MD5 integrity verification | step2 |
| SQLite database design & queries | step3 |
| pandas CSV processing | step3 |
| Data lineage tracking | step3 |
| ALCOA+ compliance principles | step2, step3 |
| Windows Task Scheduler XML | step4 |
| Structured technical documentation | README |

---

*Built as part of Haris Khan's data engineering portfolio — April 2026*
