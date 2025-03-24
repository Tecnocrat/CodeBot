import psutil
import time

def monitor_resources():
    """
    Monitors system resource usage and logs warnings if usage exceeds thresholds.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")

    if cpu_usage > 90:
        print("Warning: High CPU usage detected!")
    if memory_usage > 90:
        print("Warning: High memory usage detected!")

# CodeBot_Tracking
