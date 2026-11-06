import subprocess
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent

FULL_REPORT = PROJECT_DIR / "ec2_full_report.txt"

MONITORS = [
    ("CPU", "cpu_monitor.py"),
    ("RAM", "ram_monitor.py"),
    ("DISK", "disk_monitor.py"),
    ("PROCESSES", "process_monitor.py"),
]

REPORTS = [
    ("CPU", "cpu_summary.txt"),
    ("RAM", "ram_summary.txt"),
    ("DISK", "disk_summary.txt"),
    ("PROCESSES", "process_summary.txt"),
]


def run_monitor(name, script):
    print(f"\nRunning {name} monitor...")

    script_path = PROJECT_DIR / script

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

        if result.returncode == 0:
            print(f"{name} monitor completed successfully.")
            return True

        print(f"{name} monitor FAILED.")
        print(result.stderr)
        return False

    except subprocess.TimeoutExpired:
        print(f"{name} monitor timed out.")
        return False

    except OSError as error:
        print(f"Could not run {name} monitor: {error}")
        return False


def run_health_check(results):
    print("\nRunning server health check...")

    required = ["CPU", "RAM", "DISK"]

    if not all(results.get(name, False) for name in required):
        message = (
            "OVERALL SERVER HEALTH: UNKNOWN\n"
            "Health check skipped because a resource monitor failed."
        )
        print(message)
        return message

    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_DIR / "health_check.py")],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

        if result.returncode == 0:
            print(result.stdout)
            return result.stdout

        message = "OVERALL SERVER HEALTH: UNKNOWN\nHealth checker failed."
        print(message)
        print(result.stderr)
        return message

    except (subprocess.TimeoutExpired, OSError) as error:
        message = f"OVERALL SERVER HEALTH: UNKNOWN\nHealth check error: {error}"
        print(message)
        return message


def build_report(results, health_report):
    timestamp = datetime.now().isoformat(timespec="seconds")

    lines = [
        "EC2 RESOURCE MANAGER",
        "=" * 50,
        f"Report generated: {timestamp}",
        "FRESH SERVER MONITORING",
    ]

    for name, filename in REPORTS:
        lines.append("\n" + "=" * 50)
        lines.append(f"{name} REPORT")
        lines.append("=" * 50)

        if not results.get(name):
            lines.append("Monitor failed. Report unavailable.")
            continue

        report_path = PROJECT_DIR / filename

        if report_path.exists():
            lines.append(report_path.read_text())
        else:
            lines.append("Report file not found.")

    lines.append("\n" + "=" * 50)
    lines.append("SERVER HEALTH CHECK")
    lines.append("=" * 50)
    lines.append(health_report)

    lines.append("\n" + "=" * 50)
    lines.append("MONITORING RESULTS")

    for name, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        lines.append(f"{name}: {status}")

    lines.append("=" * 50)
    lines.append("DASHBOARD COMPLETE")

    return "\n".join(lines) + "\n"


def main():
    print("\nEC2 RESOURCE MANAGER")
    print("=" * 50)
    print("FRESH SERVER MONITORING")

    results = {}

    for name, script in MONITORS:
        results[name] = run_monitor(name, script)

    health_report = run_health_check(results)

    report = build_report(results, health_report)

    print("\n" + report)

    FULL_REPORT.write_text(report)

    print(f"Full report saved to: {FULL_REPORT}")


if __name__ == "__main__":
    main()
