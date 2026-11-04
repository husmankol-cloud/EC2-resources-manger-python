
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SUMMARY_FILE = PROJECT_DIR / "ram_summary.txt"


def read_memory_stats():
    """Read memory information provided by Linux."""

    memory = {}

    with open("/proc/meminfo", "r") as file:
        for line in file:
            parts = line.split()

            name = parts[0].rstrip(":")
            value = int(parts[1])

            memory[name] = value

    return memory


def calculate_memory_usage(memory):
    """Calculate RAM usage and percentage."""

    total = memory["MemTotal"]
    available = memory["MemAvailable"]

    used = total - available

    percentage = (used / total) * 100

    return total, used, available, round(percentage, 2)


def main():
    print("EC2 RAM MONITOR")
    print("----------------")

    memory = read_memory_stats()

    total, used, available, percentage = (
        calculate_memory_usage(memory)
    )

    timestamp = datetime.now().isoformat(timespec="seconds")

    print(f"Timestamp: {timestamp}")
    print(f"Total RAM: {total / 1024:.2f} MB")
    print(f"Used RAM: {used / 1024:.2f} MB")
    print(f"Available RAM: {available / 1024:.2f} MB")
    print(f"RAM Usage: {percentage}%")

    with open(SUMMARY_FILE, "w") as file:
        file.write("EC2 RAM SUMMARY\n")
        file.write("----------------\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Total RAM: {total / 1024:.2f} MB\n")
        file.write(f"Used RAM: {used / 1024:.2f} MB\n")
        file.write(f"Available RAM: {available / 1024:.2f} MB\n")
        file.write(f"RAM Usage: {percentage}%\n")

    print("----------------")
    print(f"Report saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()

