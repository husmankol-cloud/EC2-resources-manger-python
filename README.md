# EC2 Resource Manager

**A lightweight Linux server monitoring and resource reporting tool built with Python.**

EC2 Resource Manager is a Python-based monitoring application designed to collect and report essential system resource information from a Linux server running on Amazon EC2.

The project uses Python's standard library and Linux system interfaces to monitor CPU utilization, memory usage, disk capacity, and running processes. A central dashboard coordinates the monitoring scripts and generates a consolidated resource report.

The goal is to demonstrate practical skills in Linux system monitoring, Python automation, process management, and cloud server operations.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Architecture](#architecture)
5. [Features](#features)
6. [Technology Stack](#technology-stack)
7. [Project Structure](#project-structure)
8. [Prerequisites](#prerequisites)
9. [Installation and Setup](#installation-and-setup)
10. [Running the Application](#running-the-application)
11. [Monitoring Components](#monitoring-components)
12. [Generated Reports](#generated-reports)
13. [Limitations](#limitations)
14. [Future Improvements](#future-improvements)
15. [Security Considerations](#security-considerations)
16. [Learning Outcomes](#learning-outcomes)

---

## Project Overview

Cloud servers require regular monitoring to understand how system resources are being consumed.

This project provides a simple monitoring solution that collects information about:

- CPU utilization
- RAM utilization
- Disk space usage
- Running processes and their memory consumption

Each monitoring component is implemented as an independent Python script. A central dashboard executes the components, checks their execution results, and combines their summaries into one report.

The application is designed for Linux-based EC2 environments.

## Problem Statement

A server administrator needs visibility into the condition of a running server.

Without monitoring, it can be difficult to identify:

- Whether CPU utilization is unusually high.
- How much memory is currently available.
- Whether disk space is running low.
- Which processes are consuming significant memory.

The objective of this project is to build a lightweight tool that collects these resource measurements and presents them in an organised report.

## Solution

The EC2 Resource Manager uses four independent monitoring scripts and one dashboard application.

Each monitoring script collects a specific category of system information and saves a summary.

The dashboard coordinates the scripts using Python's `subprocess` module. It captures execution results, handles failures and timeouts, and combines the generated summaries into a single report.

This modular approach makes the application easier to understand, maintain, and extend.

## Architecture

The application follows a simple modular monitoring architecture:

```text
                 EC2 Linux Server
                        |
                        v
                  dashboard.py
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     CPU Monitor    RAM Monitor   Disk Monitor
     cpu_monitor.py ram_monitor.py disk_monitor.py
          |
          +-----------------------------+
                                        |
                                        v
                                Process Monitor
                                process_monitor.py
                                        |
                                        v
                              Individual Summaries
                                        |
                                        v
                              Combined Full Report
                              ec2_full_report.txt
```

The dashboard runs the monitoring scripts sequentially and creates a consolidated report from their output files.

## Features

### 1. CPU Monitoring

- Reads CPU statistics from Linux `/proc/stat`.
- Collects five measurements at one-second intervals.
- Calculates CPU utilization percentages.
- Appends timestamped readings to a CSV file.
- Produces a summary containing average, maximum, and minimum CPU utilization.

### 2. RAM Monitoring

- Reads memory information from `/proc/meminfo`.
- Calculates total memory, used memory, and available memory.
- Calculates memory utilization as a percentage.
- Saves the latest memory summary.

### 3. Disk Monitoring

- Uses Python's `shutil.disk_usage()` to inspect disk capacity.
- Reports total, used, and available disk space.
- Calculates disk utilization percentage.
- Currently monitors the root filesystem.

### 4. Process Monitoring

- Inspects numeric process directories under `/proc`.
- Reads process information from their status files.
- Collects process names and memory usage.
- Sorts processes by resident memory usage.
- Displays the ten processes with the highest memory consumption.

### 5. Central Monitoring Dashboard

- Executes all four monitoring scripts.
- Uses Python's `subprocess` module.
- Captures command output and execution errors.
- Applies a timeout to individual monitoring tasks.
- Checks whether each monitoring script completed successfully.
- Combines monitoring summaries into one report.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Monitoring logic and automation |
| Linux | Operating system environment |
| Amazon EC2 | Cloud server environment |
| `/proc/stat` | CPU statistics |
| `/proc/meminfo` | Memory information |
| `/proc` | Process information |
| `shutil` | Disk usage information |
| `subprocess` | Running monitoring scripts |
| `csv` | Recording CPU measurements |
| `pathlib` | Managing project file paths |
| Git | Source code version control |
| GitHub | Source code hosting and collaboration |

The application currently uses Python's standard library and does not require third-party Python packages.

## Project Structure

```text
ec2-resource-manager/
│
├── cpu_monitor.py
├── ram_monitor.py
├── disk_monitor.py
├── process_monitor.py
├── dashboard.py
├── README.md
└── .gitignore
```

### Generated files

The application creates the following files when it runs:

```text
cpu_usage.csv
cpu_summary.txt
ram_summary.txt
disk_summary.txt
process_summary.txt
ec2_full_report.txt
```

These are runtime output files. They are excluded from the Git repository through `.gitignore` because they may contain server-specific monitoring information.

## Prerequisites

Before running the application, ensure you have:

- A Linux-based system.
- Python 3 installed.
- Terminal or SSH access to the server.
- Permission to read the required Linux system information.

The project was developed and tested on a Linux EC2 environment.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

### 2. Enter the project directory

```bash
cd ec2-resource-manager
```

### 3. Verify Python installation

```bash
python3 --version
```

No additional package installation is required for the current implementation.

## Running the Application

Run the central dashboard:

```bash
python3 dashboard.py
```

The dashboard will:

1. Start the CPU monitoring script.
2. Start the RAM monitoring script.
3. Start the disk monitoring script.
4. Start the process monitoring script.
5. Collect the results.
6. Generate a consolidated report.

### Running individual monitoring scripts

Each component can also be executed independently:

```bash
python3 cpu_monitor.py
```

```bash
python3 ram_monitor.py
```

```bash
python3 disk_monitor.py
```

```bash
python3 process_monitor.py
```

## Monitoring Components

| Component | Data source | Main output |
|---|---|---|
| CPU Monitor | `/proc/stat` | CPU usage and statistics |
| RAM Monitor | `/proc/meminfo` | Memory usage summary |
| Disk Monitor | `shutil.disk_usage()` | Filesystem usage summary |
| Process Monitor | `/proc/[PID]/status` | Process memory information |
| Dashboard | Monitoring summaries | Consolidated report |

## Generated Reports

After successful execution, the dashboard generates:

`ec2_full_report.txt`

The consolidated report contains:

- Report generation timestamp.
- CPU monitoring summary.
- RAM monitoring summary.
- Disk monitoring summary.
- Process monitoring summary.
- Execution status for each monitoring component.

CPU readings are also recorded in `cpu_usage.csv` for historical reference across runs.

## Limitations

This is an initial lightweight monitoring implementation. It is not yet a full production monitoring platform.

Current limitations include:

- Monitoring is designed for Linux systems.
- Disk monitoring currently checks only the root filesystem.
- CPU monitoring uses a short five-sample window.
- Monitoring scripts execute sequentially rather than simultaneously.
- Process monitoring reports resident memory usage, not per-process CPU utilization.
- No automatic alerts or notifications are implemented.
- No graphical monitoring interface is currently available.
- Monitoring data is stored locally rather than sent to a central monitoring service.

## Future Improvements

Planned improvements include:

- Add configurable CPU, RAM, and disk usage thresholds.
- Implement email or SNS alerts for resource thresholds.
- Add structured application logging.
- Introduce automated tests.
- Add historical trend analysis.
- Build a web-based monitoring dashboard.
- Integrate Prometheus and Grafana.
- Explore automated deployment using GitHub Actions.
- Extend monitoring to multiple EC2 instances.

These are planned enhancements, not features currently implemented.

## Security Considerations

- Generated monitoring reports are excluded from source control.
- Private keys and environment files should never be committed.
- Credentials should not be hardcoded into application files.
- Access to the EC2 instance should follow the server owner's security policies.
- Monitoring should remain read-only unless additional permissions and changes are explicitly authorised.

## Learning Outcomes

This project provides practical experience with:

- Python scripting and automation.
- Linux system resource inspection.
- Reading information from the Linux `/proc` filesystem.
- CPU, memory, disk, and process monitoring.
- Python subprocess execution and error handling.
- CSV data collection.
- Modular application design.
- Git and GitHub version control.
- Basic AWS EC2 server operations.

---

## Project Status

**Current status:** Initial monitoring application implemented.

The application successfully executes its four monitoring components and generates a consolidated resource report.

Further development will focus on testing, alerting, improved reporting, and integration with modern DevOps monitoring tools.

---

*Built as a hands-on Linux, Python automation, and AWS EC2 learning project.*
