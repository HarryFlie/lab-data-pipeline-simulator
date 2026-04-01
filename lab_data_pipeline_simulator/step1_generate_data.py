"""
Step 1 — Equipment Data Generator
===================================
Simulates a laboratory instrument (biosensor / pressure sensor)
generating real-time measurement data and saving it locally.

Mirrors: SHL Medical lab equipment writing data to a local folder
on a Windows lab PC before the pipeline picks it up.

Author : Haris Khan
Project: Automated Lab Data Pipeline Simulator
Date   : April 2026
"""

import csv
import random
import datetime
import os

# ── Configuration ─────────────────────────────────────────────────────────────
OUTPUT_FOLDER = "Local_Lab_PC"
OUTPUT_FILE   = os.path.join(OUTPUT_FOLDER, "sensor_data.csv")
NUM_READINGS  = 20   # number of simulated measurements

# ── Ensure output folder exists ───────────────────────────────────────────────
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ── Generate simulated sensor readings ───────────────────────────────────────
# Simulates a CMOS MEMS biosensor measuring:
#   - Temperature (°C)   — biological assay environment
#   - Pressure (kPa)     — microfluidic channel pressure
#   - Signal Voltage (mV)— biosensor output signal
#   - Status             — pass/fail flag (ALCOA+ data quality)

readings = []
base_time = datetime.datetime.now()

for i in range(NUM_READINGS):
    timestamp   = base_time + datetime.timedelta(seconds=i * 30)
    temperature = round(random.uniform(36.5, 38.0), 3)   # body-temp range
    pressure    = round(random.uniform(101.0, 103.5), 3)  # near-atmospheric
    voltage     = round(random.uniform(2.80, 3.30), 4)    # sensor output mV
    status      = "PASS" if 36.8 <= temperature <= 37.8 else "FLAG"

    readings.append({
        "timestamp"    : timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature_C": temperature,
        "pressure_kPa" : pressure,
        "voltage_mV"   : voltage,
        "status"       : status,
        "operator_id"  : "HK-001",   # Attributable — ALCOA+ principle
        "instrument_id": "BIOSENSOR-01"
    })

# ── Write CSV ─────────────────────────────────────────────────────────────────
fieldnames = ["timestamp", "temperature_C", "pressure_kPa",
              "voltage_mV", "status", "operator_id", "instrument_id"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(readings)

print(f"[OK] Generated {NUM_READINGS} sensor readings")
print(f"[OK] Saved to: {OUTPUT_FILE}")
print(f"[OK] PASS readings : {sum(1 for r in readings if r['status'] == 'PASS')}")
print(f"[OK] FLAG readings : {sum(1 for r in readings if r['status'] == 'FLAG')}")
