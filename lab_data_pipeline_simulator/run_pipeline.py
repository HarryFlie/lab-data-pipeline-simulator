"""
run_pipeline.py — Full Pipeline Runner
========================================
Runs all 4 steps of the Automated Lab Data Pipeline in sequence.
Use this to demonstrate the complete system end-to-end.

Author : Haris Khan
Project: Automated Lab Data Pipeline Simulator
Date   : April 2026
"""

import subprocess
import sys
import os

def run_step(script, step_name):
    print(f"\n{'='*60}")
    print(f"  STEP: {step_name}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=False,
        text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] {step_name} failed.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + "█"*60)
    print("  AUTOMATED LAB DATA PIPELINE SIMULATOR")
    print("  SHL Medical — Data Integration Project")
    print("  Author: Haris Khan | April 2026")
    print("█"*60)

    run_step("step1_generate_data.py",  "1/4 — Generate sensor data (CSV)")
    run_step("step2_pipeline_agent.py", "2/4 — Metadata tag & migrate to Central_Server")
    run_step("step3_data_lake.py",      "3/4 — Ingest into SQLite Data Lake")

    print(f"\n{'='*60}")
    print("  ALL STEPS COMPLETE")
    print(f"{'='*60}")
    print()
    print("  What was demonstrated:")
    print("  [1] Equipment data generated → Local_Lab_PC/sensor_data.csv")
    print("  [2] File tagged with timestamp & moved → Central_Server/")
    print("  [3] MD5 integrity verified before & after transfer")
    print("  [4] ALCOA+ audit trail written → transfer_log.json")
    print("  [5] All records ingested into SQLite data lake")
    print("  [6] Full data lineage tracked: instrument → server → DB")
    print()
    print("  For automated hourly scheduling, run:")
    print("  python step4_scheduler_setup.py")
    print("="*60)
