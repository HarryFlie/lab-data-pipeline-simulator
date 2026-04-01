# 🧪 Automated Lab Data Pipeline Simulator

## 📌 Overview

This project simulates a real-world laboratory data pipeline used in medical and semiconductor industries.

It demonstrates how sensor data is:

* Generated from lab equipment
* Transferred securely to a central server
* Verified using MD5 integrity checks
* Logged for audit compliance (ALCOA+)
* Stored in a structured SQLite data lake

---

## ⚙️ Pipeline Architecture

1. **Data Generation**

   * Simulated sensor readings (temperature, pressure, status)

2. **Data Transfer**

   * File renaming with timestamp + metadata
   * Secure migration to central server

3. **Data Integrity**

   * MD5 checksum verification

4. **Audit Logging**

   * JSON-based transfer logs

5. **Data Storage**

   * SQLite database (data lake)
   * Full data lineage tracking

---

## 🚀 How to Run

```bash
pip install pandas
python run_pipeline.py
```

---

## 📂 Project Structure

```
lab_data_pipeline_simulator/
│
├── step1_generate_data.py
├── step2_pipeline_agent.py
├── step3_data_lake.py
├── run_pipeline.py
└── step4_scheduler_setup.py
```

---

## 📊 Output

* CSV files with sensor data
* Transfer logs (JSON)
* SQLite database with structured records

---

## 🎯 Applications

* Medical device data pipelines (SHL Medical)
* Semiconductor data processing (TSMC, ASML)
* Industrial IoT systems
* Data engineering workflows

---

## 👨‍💻 Author

Haris Khan
Graduate Institute of Mechatronics Engineering
Taipei Tech, Taiwan
