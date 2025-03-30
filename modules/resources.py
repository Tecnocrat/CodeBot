import psutil
import time
import json
import os
from datetime import datetime

def monitor_resources(log_file="resource_log.json", cpu_threshold=90, memory_threshold=90, disk_threshold=90):
    """
    Monitors system resource usage (CPU, memory, and disk) and logs warnings if usage exceeds thresholds.
    Logs resource usage to a JSON file for historical tracking.

    Args:
        log_file (str): Path to the log file where resource usage will be recorded.
        cpu_threshold (int): CPU usage percentage threshold for warnings.
        memory_threshold (int): Memory usage percentage threshold for warnings.
        disk_threshold (int): Disk usage percentage threshold for warnings.
    """
    print("Starting resource monitoring...")
    while True:
        # Get system resource usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent

        # Log resource usage to the console
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")

        # Check thresholds and log warnings
        warnings = []
        if cpu_usage > cpu_threshold:
            warning = "High CPU usage detected!"
            print(f"Warning: {warning}")
            warnings.append(warning)
        if memory_usage > memory_threshold:
            warning = "High memory usage detected!"
            print(f"Warning: {warning}")
            warnings.append(warning)
        if disk_usage > disk_threshold:
            warning = "High disk usage detected!"
            print(f"Warning: {warning}")
            warnings.append(warning)

        # Log resource usage and warnings to a file
        log_resource_usage(cpu_usage, memory_usage, disk_usage, warnings, log_file)

        # Sleep for a short interval before the next check
        time.sleep(5)


def log_resource_usage(cpu_usage, memory_usage, disk_usage, warnings, log_file):
    """
    Logs resource usage and warnings to a JSON file.

    Args:
        cpu_usage (float): CPU usage percentage.
        memory_usage (float): Memory usage percentage.
        disk_usage (float): Disk usage percentage.
        warnings (list): List of warning messages.
        log_file (str): Path to the log file where resource usage will be recorded.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "warnings": warnings
    }

    # Append the log entry to the JSON file
    if not log_file.endswith(".json"):
        raise ValueError("Log file must have a .json extension.")
    
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Resource usage logged to {log_file}")


def get_average_usage(log_file="resource_log.json"):
    """
    Calculates the average CPU, memory, and disk usage from the log file.

    Args:
        log_file (str): Path to the log file where resource usage is recorded.

    Returns:
        dict: A dictionary containing the average CPU, memory, and disk usage.
    """
    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist.")
        return {}

    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Log file is empty.")
        return {}

    total_cpu = sum(entry["cpu_usage"] for entry in data)
    total_memory = sum(entry["memory_usage"] for entry in data)
    total_disk = sum(entry["disk_usage"] for entry in data)
    count = len(data)

    return {
        "average_cpu_usage": total_cpu / count,
        "average_memory_usage": total_memory / count,
        "average_disk_usage": total_disk / count
    }


if __name__ == "__main__":
    # Example usage of monitor_resources
    monitor_resources(
        log_file="C:\\dev\\adn_trash_code\\resource_log.json",
        cpu_threshold=85,
        memory_threshold=80,
        disk_threshold=90
    )

    # Example usage of get_average_usage
    averages = get_average_usage("C:\\dev\\adn_trash_code\\resource_log.json")
    print("Average Resource Usage:", averages)


# CodeBot_Tracking