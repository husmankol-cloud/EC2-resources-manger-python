
import csv
import time
from datetime import datetime
from pathlib import Path


# Keep our reports inside this project directory
PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_FILE = PROJECT_DIR / "cpu_usage.csv"
SUMMARY_FILE = PROJECT_DIR / "cpu_summary.txt"


def read_cpu_stats():
    """Read CPU counters provided by the Linux kernel."""

    with open("/proc/stat", "r") as file:
        cpu_line = file.readline()

    values = list(map(int, cpu_line.split()[1:]))

    total_time = sum(values)
    idle_time = values[3] + values[4]

    return total_time, idle_time


def calculate_cpu_usage(previous, current):
    """Calculate CPU usage between two measurements."""

    total_difference = current[0] - previous[0]
    idle_difference = current[1] - previous[1]

    if total_difference == 0:
        return 0.0

    usage = (
        (total_difference - idle_difference)
        / total_difference
    ) * 100

    return round(usage, 2)


def save_summary(readings):
    """Calculate and save CPU statistics."""

    average = sum(readings) / len(readings)
    maximum = max(readings)
    minimum = min(readings)

    with open(SUMMARY_FILE, "w") as file:
        file.write("EC2 CPU SUMMARY\n")
        file.write("----------------\n")
        file.write(f"Number of samples: {len(readings)}\n")
        file.write(f"Average CPU usage: {average:.2f}%\n")
        file.write(f"Maximum CPU usage: {maximum:.2f}%\n")
        file.write(f"Minimum CPU usage: {minimum:.2f}%\n")

    print("\nCPU SUMMARY")
    print("----------------")
    print(f"Number of samples: {len(readings)}")
    print(f"Average CPU usage: {average:.2f}%")
    print(f"Maximum CPU usage: {maximum:.2f}%")
    print(f"Minimum CPU usage: {minimum:.2f}%")
    print(f"Summary saved to: {SUMMARY_FILE}")


def main():
    print("EC2 CPU MONITOR")
    print("----------------")

    previous = read_cpu_stats()
    readings = []

    with open(RESULTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if RESULTS_FILE.stat().st_size == 0:
            writer.writerow(["timestamp", "cpu_usage_percent"])

        for sample in range(5):
            time.sleep(1)

            current = read_cpu_stats()
            usage = calculate_cpu_usage(previous, current)

            timestamp = datetime.now().isoformat(timespec="seconds")

            print(f"{timestamp} | CPU Usage: {usage}%")

            readings.append(usage)
            writer.writerow([timestamp, usage])
            file.flush()

            previous = current

    save_summary(readings)


if __name__ == "__main__":
    main()

