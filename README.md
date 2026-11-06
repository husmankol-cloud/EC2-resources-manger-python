# EC2 Resource Manager

A Python-based Linux server monitoring and resource management project built on an Amazon EC2 Linux instance.

The project monitors CPU usage, RAM consumption, disk space, and running processes. It also evaluates server health using predefined warning and critical thresholds and generates a consolidated monitoring report.

## Table of Contents

1. Project Overview
2. Problem Statement
3. Project Objectives
4. Solution
5. Architecture
6. Features
7. Technology Stack
8. Project Structure
9. Prerequisites
10. Installation
11. Running the Project
12. Monitoring Components
13. Health Check Thresholds
14. Generated Reports
15. Limitations
16. Future Improvements
17. Security Considerations
18. Learning Outcomes
19. Project Status

## 1. Project Overview

EC2 Resource Manager is a Linux server monitoring tool developed with Python.

It collects system resource information directly from the Linux operating system and produces reports that help an administrator understand the condition of an EC2 instance.

The project demonstrates practical Linux system administration, Python scripting, process monitoring, resource management, and automation.

## 2. Problem Statement

Cloud servers require continuous monitoring to ensure that their resources are being used efficiently.

Without proper monitoring, an administrator may not easily identify:

- High CPU utilization.
- Excessive memory consumption.
- Low available disk space.
- Processes consuming significant memory.
- Potential server resource problems.

This project provides a simple automated way to collect and review these resource measurements.

## 3. Project Objectives

The objectives are to:

- Monitor CPU utilization.
- Monitor RAM usage.
- Monitor disk utilization.
- Identify processes consuming the most memory.
- Evaluate server resource health.
- Generate individual monitoring reports.
- Combine monitoring results into one consolidated report.
- Practise Linux administration and Python automation.

## 4. Solution

The project uses Python scripts to collect resource information from Linux system interfaces and generate readable reports.

A central dashboard executes the monitoring scripts, checks their execution results, runs the health checker when the required resource reports are available, and saves the consolidated report.

## 5. Architecture

The monitoring workflow is:

```text
              EC2 Linux Server
                     |
                     v
                dashboard.py
                     |
        +------------+------------+
        |            |            |
        v            v            v
   cpu_monitor  ram_monitor  disk_monitor
        |            |            |
        +------------+------------+
                     |
              process_monitor.py
                     |
                     v
              Monitoring Reports
                     |
                     v
               health_check.py
                     |
                     v
             Server Health Status
                     |
                     v
             ec2_full_report.txt
```

The dashboard executes the four monitoring scripts sequentially.

The health checker evaluates CPU, RAM, and disk health after their monitoring scripts succeed.

The dashboard then combines the available monitoring reports and health-check results into a consolidated report.

## 6. Features

### CPU Monitoring

- Reads CPU statistics from `/proc/stat`.
- Collects five CPU samples.
- Calculates CPU utilization.
- Records CPU measurements in a CSV file.
- Generates a CPU summary containing average, maximum, and minimum utilization.

### RAM Monitoring

- Reads memory information from `/proc/meminfo`.
- Uses total memory and available memory to calculate RAM utilization.
- Generates a RAM summary report.

### Disk Monitoring

- Uses Python's `shutil.disk_usage()` to inspect filesystem usage.
- Calculates used and available disk space.
- Generates a disk summary report.

### Process Monitoring

- Inspects Linux process information under `/proc`.
- Collects process IDs, names, states, and resident memory usage.
- Sorts processes by memory consumption.
- Displays the top 10 processes by resident memory usage.

### Server Health Checker

- Reads CPU, RAM, and disk monitoring reports.
- Classifies resource usage as HEALTHY, WARNING, CRITICAL, or UNKNOWN.
- Determines an overall server health status.
- Reports missing or invalid resource measurements as UNKNOWN.

### Automated Dashboard

- Executes all four monitoring scripts.
- Handles failed scripts and execution timeouts.
- Runs the health checker when CPU, RAM, and disk monitoring succeed.
- Combines monitoring results into one report.
- Saves the final report as `ec2_full_report.txt`.

## 7. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Monitoring and automation |
| Linux | Operating system |
| Amazon EC2 | Cloud server environment |
| `/proc/stat` | CPU statistics |
| `/proc/meminfo` | Memory statistics |
| `/proc` | Process information |
| pathlib | File and directory handling |
| subprocess | Executing monitoring scripts |
| shutil | Disk usage information |
| re | Reading measurements from reports |
| datetime | Report timestamps |

The project currently uses Python's standard library and does not require external Python packages.

## 8. Project Structure

```text
ec2-resource-manager/
│
├── cpu_monitor.py
├── ram_monitor.py
├── disk_monitor.py
├── process_monitor.py
├── health_check.py
├── dashboard.py
├── README.md
├── .gitignore
│
├── cpu_usage.csv
├── cpu_summary.txt
├── ram_summary.txt
├── disk_summary.txt
├── process_summary.txt
└── ec2_full_report.txt
```

The monitoring output files are generated when the scripts run. They are excluded from Git tracking through `.gitignore`.

## 9. Prerequisites

- A Linux server or Linux virtual machine.
- An Amazon EC2 instance or equivalent Linux environment.
- Python 3.
- Terminal or SSH access.
- Basic knowledge of Linux commands.

The monitoring scripts depend on Linux system information available through `/proc`.

## 10. Installation

Clone the repository:

```bash
git clone git@github.com:husmankol-cloud/EC2-resources-manger-python.git
```

Enter the project directory:

```bash
cd EC2-resources-manger-python
```

Check the Python version:

```bash
python3 --version
```

No external Python packages are required.

## 11. Running the Project

### Run the complete monitoring dashboard

```bash
python3 dashboard.py
```

This executes the monitoring scripts, performs the health check when possible, and generates the consolidated report.

### Run individual monitoring scripts

CPU:

```bash
python3 cpu_monitor.py
```

RAM:

```bash
python3 ram_monitor.py
```

Disk:

```bash
python3 disk_monitor.py
```

Processes:

```bash
python3 process_monitor.py
```

Health checker:

```bash
python3 health_check.py
```

The standalone health checker expects the CPU, RAM, and disk summary reports to exist.

### View the consolidated report

```bash
cat ec2_full_report.txt
```

## 12. Monitoring Components

| Component | Data Source | Main Output |
|---|---|---|
| CPU Monitor | `/proc/stat` | CPU usage and summary |
| RAM Monitor | `/proc/meminfo` | RAM summary |
| Disk Monitor | `shutil.disk_usage()` | Disk summary |
| Process Monitor | `/proc/[pid]/status` | Top memory-consuming processes |
| Health Checker | Monitoring reports | Server health status |
| Dashboard | All monitoring components | Consolidated report |

## 13. Health Check Thresholds

The health checker uses predefined thresholds in `health_check.py`.

| Resource | Warning | Critical |
|---|---:|---:|
| CPU | 70% | 90% |
| RAM | 75% | 90% |
| Disk | 80% | 90% |

Classification:

- HEALTHY: Usage is below the warning threshold.
- WARNING: Usage has reached the warning threshold.
- CRITICAL: Usage has reached the critical threshold.
- UNKNOWN: The measurement is missing or invalid.

For CPU, the health checker classifies usage using the maximum CPU utilization recorded during the monitoring period.

The overall server health is UNKNOWN if any required resource measurement is unavailable or invalid. Otherwise, the highest severity determines the overall status.

## 14. Generated Reports

The project generates the following reports:

| File | Description |
|---|---|
| `cpu_usage.csv` | Recorded CPU measurements |
| `cpu_summary.txt` | Average, maximum, and minimum CPU usage |
| `ram_summary.txt` | RAM usage information |
| `disk_summary.txt` | Disk usage information |
| `process_summary.txt` | Top 10 memory-consuming processes |
| `ec2_full_report.txt` | Consolidated monitoring and health report |

These files are generated locally when the monitoring scripts execute.

## 15. Limitations

Current project limitations include:

- Disk monitoring currently checks the root filesystem only.
- CPU monitoring uses a short five-sample measurement period.
- Process monitoring focuses on resident memory usage.
- Health thresholds are currently defined directly in the Python source code.
- Monitoring runs when manually started; continuous background monitoring has not yet been implemented.
- The project does not currently send email or external alerts.
- Historical monitoring data is not yet stored in a database.

## 16. Future Improvements

Planned improvements include:

- Make health thresholds configurable through a configuration file.
- Add automated scheduled monitoring.
- Introduce email or notification alerts.
- Add historical resource tracking.
- Build a web-based monitoring dashboard.
- Add monitoring for network traffic.
- Support monitoring multiple EC2 instances.
- Integrate CloudWatch metrics.
- Add automated testing.

## 17. Security Considerations

- The project does not require AWS access keys to collect local Linux resource information.
- No passwords, private keys, or AWS credentials should be committed to GitHub.
- Generated monitoring reports are excluded from version control.
- The scripts read Linux system information and generate local reports.
- Monitoring should be performed with appropriate server permissions.

## 18. Learning Outcomes

Building this project provided practical experience with:

- Linux system administration.
- Amazon EC2 server management.
- Python scripting and automation.
- CPU and memory monitoring.
- Linux process inspection.
- Filesystem monitoring.
- Python file handling.
- Regular expressions.
- Python subprocess management.
- Error handling and execution timeouts.
- Server health evaluation.
- Git and GitHub project documentation.

## 19. Project Status

**Current status: Core monitoring functionality implemented and tested.**

Completed:

- CPU monitoring.
- RAM monitoring.
- Disk monitoring.
- Process monitoring.
- Server health checker.
- Automated monitoring dashboard.
- Consolidated report generation.
- GitHub project documentation.

Future improvements are listed above and have not yet been implemented.

---

**Project:** EC2 Resource Manager
**Platform:** Amazon EC2/Linux
**Language:** Python3
