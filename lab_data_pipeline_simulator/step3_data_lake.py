"""
Step 3 — Data Lake: SQLite Database Integration
=================================================
Reads all migrated CSV files from Central_Server and
inserts the data into a local SQLite database — simulating
a Data Lake architecture with structured storage, full
data lineage tracking, and queryable experimental records.

Mirrors: SHL Medical's need to move data from local equipment
folders into server-side or cloud-based Data Lake architectures
with organized, searchable, and scalable data structures.

Data Lineage: every record tracks its full journey from
instrument → local folder → central server → database,
with timestamps at each stage — full traceability per ALCOA+.

Author : Haris Khan
Project: Automated Lab Data Pipeline Simulator
Date   : April 2026
"""

import sqlite3
import pandas as pd
import os
import datetime
import json

# ── Configuration ─────────────────────────────────────────────────────────────
CENTRAL_SERVER = "Central_Server"
DB_FILE        = os.path.join(CENTRAL_SERVER, "lab_data_lake.db")
LOG_FILE       = os.path.join(CENTRAL_SERVER, "transfer_log.json")

# ── Connect to SQLite database (creates file if not exists) ───────────────────
conn   = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ── Create tables ─────────────────────────────────────────────────────────────

# Main measurements table — stores all sensor readings
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_measurements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id       TEXT UNIQUE,          -- globally unique ID per reading
    source_file     TEXT NOT NULL,        -- original filename (data lineage)
    tagged_file     TEXT NOT NULL,        -- timestamped filename (data lineage)
    ingestion_time  TEXT NOT NULL,        -- when inserted into DB (ALCOA+)
    timestamp       TEXT NOT NULL,        -- when reading was taken
    temperature_C   REAL NOT NULL,
    pressure_kPa    REAL NOT NULL,
    voltage_mV      REAL NOT NULL,
    status          TEXT NOT NULL,        -- PASS / FLAG
    operator_id     TEXT NOT NULL,        -- Attributable (ALCOA+)
    instrument_id   TEXT NOT NULL
)
""")

# Data lineage table — tracks every file's journey
cursor.execute("""
CREATE TABLE IF NOT EXISTS data_lineage (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    source_filename     TEXT NOT NULL,
    tagged_filename     TEXT NOT NULL,
    transfer_timestamp  TEXT NOT NULL,
    ingestion_timestamp TEXT NOT NULL,
    operator_id         TEXT NOT NULL,
    instrument_id       TEXT NOT NULL,
    checksum_md5        TEXT NOT NULL,
    rows_ingested       INTEGER NOT NULL,
    status              TEXT NOT NULL
)
""")

conn.commit()
print("[OK] Database schema ready")

# ── Load transfer log to get lineage metadata ─────────────────────────────────
transfer_log = []
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        transfer_log = json.load(f)

# Build lookup: tagged_filename -> log entry
log_lookup = {entry["tagged_filename"]: entry for entry in transfer_log}

# ── Find all CSV files in Central_Server ─────────────────────────────────────
csv_files = [
    f for f in os.listdir(CENTRAL_SERVER)
    if f.endswith(".csv")
]

if not csv_files:
    print("[INFO] No CSV files found in Central_Server to ingest.")
    conn.close()
    exit()

total_rows = 0
ingestion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for tagged_filename in csv_files:
    filepath = os.path.join(CENTRAL_SERVER, tagged_filename)

    # Check if already ingested (avoid duplicates — ALCOA+ Original)
    cursor.execute(
        "SELECT COUNT(*) FROM data_lineage WHERE tagged_filename = ?",
        (tagged_filename,)
    )
    if cursor.fetchone()[0] > 0:
        print(f"[SKIP] Already ingested: {tagged_filename}")
        continue

    # Read CSV into DataFrame
    df = pd.read_csv(filepath)

    # Get lineage metadata from transfer log
    log_entry       = log_lookup.get(tagged_filename, {})
    source_filename = log_entry.get("original_filename", "unknown")
    operator_id     = log_entry.get("operator_id", "unknown")
    instrument_id   = log_entry.get("instrument_id", "unknown")
    checksum_md5    = log_entry.get("checksum_md5", "unknown")

    rows_ingested = 0

    for idx, row in df.iterrows():
        # Generate unique record ID: instrument + date + row index
        record_id = f"{instrument_id}_{tagged_filename[:15]}_{idx:04d}"

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO sensor_measurements
                (record_id, source_file, tagged_file, ingestion_time,
                 timestamp, temperature_C, pressure_kPa, voltage_mV,
                 status, operator_id, instrument_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_id,
                source_filename,
                tagged_filename,
                ingestion_time,
                row["timestamp"],
                row["temperature_C"],
                row["pressure_kPa"],
                row["voltage_mV"],
                row["status"],
                row["operator_id"],
                row["instrument_id"],
            ))
            rows_ingested += 1
        except Exception as e:
            print(f"  [WARN] Row {idx} skipped: {e}")

    # Record data lineage entry
    cursor.execute("""
        INSERT INTO data_lineage
        (source_filename, tagged_filename, transfer_timestamp,
         ingestion_timestamp, operator_id, instrument_id,
         checksum_md5, rows_ingested, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source_filename,
        tagged_filename,
        log_entry.get("transfer_timestamp", "unknown"),
        ingestion_time,
        operator_id,
        instrument_id,
        checksum_md5,
        rows_ingested,
        "INGESTED",
    ))

    conn.commit()
    total_rows += rows_ingested
    print(f"[OK] Ingested: {tagged_filename} → {rows_ingested} rows")

# ── Summary query — prove the data lake works ─────────────────────────────────
print("\n" + "=" * 60)
print("  DATA LAKE SUMMARY")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM sensor_measurements")
print(f"  Total records in database : {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM data_lineage")
print(f"  Total files ingested      : {cursor.fetchone()[0]}")

cursor.execute("""
    SELECT status, COUNT(*) as count
    FROM sensor_measurements
    GROUP BY status
""")
for row in cursor.fetchall():
    print(f"  Status [{row[0]}]            : {row[1]} readings")

cursor.execute("""
    SELECT AVG(temperature_C), MIN(temperature_C), MAX(temperature_C)
    FROM sensor_measurements
""")
avg, mn, mx = cursor.fetchone()
print(f"  Temp avg / min / max      : {avg:.2f} / {mn:.2f} / {mx:.2f} °C")

print("=" * 60)
print(f"[DONE] Data Lake database: {DB_FILE}")
print(f"[DONE] Full data lineage tracked for all {total_rows} new records")

conn.close()
