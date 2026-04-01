"""
Step 4 — Windows Task Scheduler: Automated Execution
======================================================
This script generates the exact XML configuration for
Windows Task Scheduler to run your pipeline automatically
every hour — simulating production-grade scheduled automation.

HOW TO USE:
1. Run this script to generate 'pipeline_scheduler.xml'
2. Import it into Windows Task Scheduler (instructions below)

Author : Haris Khan
Project: Automated Lab Data Pipeline Simulator
Date   : April 2026
"""

import os
import datetime

# ── Detect current Python path and script directory ───────────────────────────
python_exe  = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"),
                            "Programs", "Python", "Python311", "python.exe")
script_dir  = os.getcwd()
script_path = os.path.join(script_dir, "step2_pipeline_agent.py")

# ── Generate Task Scheduler XML ───────────────────────────────────────────────
xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">

  <!-- TASK METADATA -->
  <RegistrationInfo>
    <Date>{datetime.datetime.now().isoformat()}</Date>
    <Author>Haris Khan</Author>
    <Description>
      SHL Medical Lab Data Pipeline — Automated hourly transfer
      of sensor data from Local_Lab_PC to Central_Server.
      Runs step2_pipeline_agent.py every hour automatically.
      Project: Automated Lab Data Pipeline Simulator, April 2026.
    </Description>
    <URI>\\SHL_Lab_Pipeline</URI>
  </RegistrationInfo>

  <!-- TRIGGER: Run every hour, starting now -->
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT1H</Interval>       <!-- PT1H = every 1 hour -->
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>{datetime.datetime.now().strftime('%Y-%m-%dT%H:00:00')}</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>

  <!-- SETTINGS -->
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>  <!-- max 10 min run time -->
    <Priority>7</Priority>
    <Enabled>true</Enabled>
  </Settings>

  <!-- ACTION: Run Python pipeline script -->
  <Actions Context="Author">
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>"{script_path}"</Arguments>
      <WorkingDirectory>{script_dir}</WorkingDirectory>
    </Exec>
  </Actions>

</Task>"""

# Save XML file
xml_path = "pipeline_scheduler.xml"
with open(xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print("=" * 60)
print("  Windows Task Scheduler Configuration Generated")
print("=" * 60)
print(f"[OK] XML saved: {xml_path}")
print()
print("HOW TO IMPORT INTO WINDOWS TASK SCHEDULER:")
print("-" * 60)
print("  1. Press Windows + S → search 'Task Scheduler' → Open it")
print("  2. In the right panel click 'Import Task...'")
print(f"  3. Select this file: {os.path.abspath(xml_path)}")
print("  4. Click OK — the task is now scheduled!")
print()
print("ALTERNATIVE (Command Line — run as Administrator):")
print("-" * 60)
print(f'  schtasks /create /xml "{os.path.abspath(xml_path)}" /tn "SHL_Lab_Pipeline"')
print()
print("VERIFY IT IS RUNNING:")
print("-" * 60)
print('  schtasks /query /tn "SHL_Lab_Pipeline"')
print("=" * 60)
print()
print("WHAT THIS AUTOMATES:")
print("  Every hour Windows will automatically run your pipeline.")
print("  No manual action needed — fully automated data flow.")
print("  This is exactly what SHL Medical needs for their lab.")
