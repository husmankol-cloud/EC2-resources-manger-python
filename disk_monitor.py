
import shutil
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SUMMARY_FILE = PROJECT_DIR / "disk_summary.txt"


def read_disk_stats():
    """Read disk space information from the root filesystem."""

    total, used, free = shutil.disk_usage("/")

    return total, used, free


def calculate_disk_usage(total, used, free):
    """Calculate disk usage percentage."""

    percentage = (used / total) * 100

    return round(percentage, 2)


def main():
    print("EC2 DISK MONITOR")
    print("----------------")

    total, used, free = read_disk_stats()

    percentage = calculate_disk_usage(total, used, free)

    timestamp = datetime.now().isoformat(timespec="seconds")

    # Convert bytes into gigabytes
    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)

    print(f"Timestamp: {timestamp}")
    print(f"Total Disk: {total_gb:.2f} GB")
    print(f"Used Disk: {used_gb:.2f} GB")
    print(f"Free Disk: {free_gb:.2f} GB")
    print(f"Disk Usage: {percentage}%")

    with open(SUMMARY_FILE, "w") as file:
        file.write("EC2 DISK SUMMARY\n")
        file.write("----------------\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Total Disk: {total_gb:.2f} GB\n")
        file.write(f"Used Disk: {used_gb:.2f} GB\n")
        file.write(f"Free Disk: {free_gb:.2f} GB\n")
        file.write(f"Disk Usage: {percentage}%\n")

    print("----------------")
    print(f"Report saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()

