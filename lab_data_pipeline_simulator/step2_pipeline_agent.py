"""
Step 2 — Windows Automation: Metadata Tagging & File Migration
================================================================
Monitors the Local_Lab_PC folder, renames CSV files with a
standardized timestamp (metadata tagging), and migrates them
to the Central_Server folder — simulating a data pipeline
from lab equipment to a centralized server.

Mirrors: SHL Medical's need for automated upload tools to
bridge local equipment folders to server-side storage,
with consistent naming conventions and data path design.

ALCOA+ Principles applied:
  - Attributable : operator_id embedded in filename
  - Contemporaneous: timestamp reflects actual transfer time
  - Original      : raw file moved, not modified
  - Accurate      : checksum logged to verify file integrity

Author : Haris Khan
Project: Automated Lab Data Pipeline Simulator
Date   : April 2026
"""

import os
import shutil
import datetime
import hashlib
import json

# ── Configuration ─────────────────────────────────────────────────────────────
SOURCE_FOLDER = "Local_Lab_PC"
DEST_FOLDER   = "Central_Server"
LOG_FILE      = os.path.join(DEST_FOLDER, "transfer_log.json")
OPERATOR_ID   = "HK-001"
INSTRUMENT_ID = "BIOSENSOR-01"

# ── Ensure destination exists ─────────────────────────────────────────────────
os.makedirs(DEST_FOLDER, exist_ok=True)

# ── Helper: compute MD5 checksum for data integrity verification ──────────────
def md5_checksum(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# ── Helper: load existing transfer log ───────────────────────────────────────
def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ── Helper: save transfer log ─────────────────────────────────────────────────
def save_log(log_entries):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, indent=2)

# ── Main pipeline logic ───────────────────────────────────────────────────────
def run_pipeline():
    print("=" * 60)
    print("  SHL Lab Data Pipeline — Transfer Agent")
    print("=" * 60)

    # Scan source folder for CSV files
    csv_files = [
        f for f in os.listdir(SOURCE_FOLDER)
        if f.endswith(".csv")
    ]

    if not csv_files:
        print("[INFO] No CSV files found in Local_Lab_PC. Nothing to transfer.")
        return

    log_entries = load_log()
    transferred = 0

    for filename in csv_files:
        source_path = os.path.join(SOURCE_FOLDER, filename)

        # ── Step A: Metadata Tagging — build standardized filename ────────────
        # Format: YYYYMMDD_HHMMSS_<INSTRUMENT>_<OPERATOR>_<original_name>
        # This is the naming convention / metadata tagging standard
        now         = datetime.datetime.now()
        date_tag    = now.strftime("%Y%m%d")
        time_tag    = now.strftime("%H%M%S")
        tagged_name = f"{date_tag}_{time_tag}_{INSTRUMENT_ID}_{OPERATOR_ID}_{filename}"
        dest_path   = os.path.join(DEST_FOLDER, tagged_name)

        # ── Step B: Compute checksum BEFORE move (data integrity) ─────────────
        checksum_before = md5_checksum(source_path)

        # ── Step C: Copy file to Central_Server (preserve original) ──────────
        shutil.copy2(source_path, dest_path)

        # ── Step D: Verify checksum AFTER copy ───────────────────────────────
        checksum_after = md5_checksum(dest_path)
        integrity_ok   = checksum_before == checksum_after

        # ── Step E: Remove source file only if integrity verified ─────────────
        if integrity_ok:
            os.remove(source_path)
            transfer_status = "SUCCESS"
        else:
            transfer_status = "INTEGRITY_FAIL — source file retained"

        # ── Step F: Log the transfer (ALCOA+ audit trail) ────────────────────
        log_entry = {
            "transfer_timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "original_filename"  : filename,
            "tagged_filename"    : tagged_name,
            "source_folder"      : SOURCE_FOLDER,
            "destination_folder" : DEST_FOLDER,
            "operator_id"        : OPERATOR_ID,
            "instrument_id"      : INSTRUMENT_ID,
            "checksum_md5"       : checksum_after,
            "integrity_verified" : integrity_ok,
            "status"             : transfer_status,
        }
        log_entries.append(log_entry)

        print(f"[{transfer_status}] {filename}")
        print(f"         -> {tagged_name}")
        print(f"         -> MD5: {checksum_after} | Integrity: {integrity_ok}")
        transferred += 1

    # Save updated log
    save_log(log_entries)

    print("-" * 60)
    print(f"[DONE] Transferred {transferred} file(s)")
    print(f"[DONE] Audit log saved to: {LOG_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
