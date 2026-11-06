from pathlib import Path
import re


PROJECT_DIR = Path(__file__).resolve().parent

CPU_REPORT = PROJECT_DIR / "cpu_summary.txt"
RAM_REPORT = PROJECT_DIR / "ram_summary.txt"
DISK_REPORT = PROJECT_DIR / "disk_summary.txt"

THRESHOLDS = {
    "CPU": {"warning": 70, "critical": 90},
    "RAM": {"warning": 75, "critical": 90},
    "DISK": {"warning": 80, "critical": 90},
}


def read_percentage(report_file, pattern):
    """Read a percentage from a monitoring report."""

    if not report_file.exists():
        return None

    content = report_file.read_text()

    match = re.search(pattern, content)

    if not match:
        return None

    try:
        value = float(match.group(1))
    except ValueError:
        return None

    if not 0 <= value <= 100:
        return None

    return value


def check_resource(name, usage):
    """Classify a resource based on its usage."""

    if usage is None:
        return "UNKNOWN"

    limits = THRESHOLDS[name]

    if usage >= limits["critical"]:
        return "CRITICAL"

    if usage >= limits["warning"]:
        return "WARNING"

    return "HEALTHY"


def main():
    print("\nEC2 SERVER HEALTH CHECK")
    print("=" * 45)

    cpu_average = read_percentage(
        CPU_REPORT,
        r"Average CPU usage:\s*([\d.]+)%"
    )

    cpu_maximum = read_percentage(
        CPU_REPORT,
        r"Maximum CPU usage:\s*([\d.]+)%"
    )

    ram_usage = read_percentage(
        RAM_REPORT,
        r"RAM Usage:\s*([\d.]+)%"
    )

    disk_usage = read_percentage(
        DISK_REPORT,
        r"Disk Usage:\s*([\d.]+)%"
    )

    resources = {
        "CPU": cpu_maximum,
        "RAM": ram_usage,
        "DISK": disk_usage,
    }

    statuses = {}

    for name, usage in resources.items():
        status = check_resource(name, usage)
        statuses[name] = status

        if usage is None:
            print(f"{name}: UNKNOWN - Report missing or invalid")
        elif name == "CPU":
            print(
                f"{name}: {status} | "
                f"Average: {cpu_average}% | "
                f"Maximum: {cpu_maximum}%"
            )
        else:
            print(f"{name}: {status} | Usage: {usage}%")

    if "UNKNOWN" in statuses.values():
        overall = "UNKNOWN"
    elif "CRITICAL" in statuses.values():
        overall = "CRITICAL"
    elif "WARNING" in statuses.values():
        overall = "WARNING"
    else:
        overall = "HEALTHY"

    print("=" * 45)
    print(f"OVERALL SERVER HEALTH: {overall}")
    print("=" * 45)


if __name__ == "__main__":
    main()
