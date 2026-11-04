
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
REPORT_FILE = PROJECT_DIR / "process_summary.txt"


def read_processes():
    """Read process information from Linux /proc."""

    processes = []

    for entry in Path("/proc").iterdir():

        if not entry.name.isdigit():
            continue

        pid = int(entry.name)
        status_file = entry / "status"

        try:
            process = {
                "pid": pid,
                "name": "",
                "state": "",
                "memory_kb": 0
            }

            with open(status_file, "r") as file:
                for line in file:
                    if line.startswith("Name:"):
                        process["name"] = line.split(":", 1)[1].strip()

                    elif line.startswith("State:"):
                        process["state"] = line.split(":", 1)[1].strip()

                    elif line.startswith("VmRSS:"):
                        process["memory_kb"] = int(line.split()[1])

            processes.append(process)

        except (FileNotFoundError, PermissionError, ProcessLookupError):
            # A process may disappear or become inaccessible while we inspect it.
            continue

    return processes


def main():
    print("EC2 PROCESS MONITOR")
    print("-------------------")

    processes = read_processes()

    # Show processes using the most physical RAM.
    processes.sort(
        key=lambda process: process["memory_kb"],
        reverse=True
    )

    timestamp = datetime.now().isoformat(timespec="seconds")

    print(f"Timestamp: {timestamp}")
    print(f"Processes inspected: {len(processes)}")
    print("\nTOP 10 MEMORY-USING PROCESSES")
    print("-----------------------------------------------")
    print(f"{'PID':<10}{'NAME':<25}{'MEMORY (MB)':>12}")
    print("-----------------------------------------------")

    for process in processes[:10]:
        memory_mb = process["memory_kb"] / 1024

        print(
            f"{process['pid']:<10}"
            f"{process['name']:<25}"
            f"{memory_mb:>12.2f}"
        )

    with open(REPORT_FILE, "w") as file:
        file.write("EC2 PROCESS SUMMARY\n")
        file.write("-------------------\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Processes inspected: {len(processes)}\n\n")

        file.write("TOP 10 MEMORY-USING PROCESSES\n")
        file.write("-----------------------------------------------\n")

        for process in processes[:10]:
            memory_mb = process["memory_kb"] / 1024

            file.write(
                f"PID: {process['pid']} | "
                f"Name: {process['name']} | "
                f"State: {process['state']} | "
                f"Memory: {memory_mb:.2f} MB\n"
            )

    print("-----------------------------------------------")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()

