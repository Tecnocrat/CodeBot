import psutil
import time

def monitor_resources(interval=10, cpu_limit=80, memory_limit=80):
    """
    Monitors CPU and memory usage periodically. Pauses if usage exceeds specified thresholds.
    """
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        print(f"CPU: {cpu_usage}% | Memory: {memory_info.percent}%")
        if cpu_usage > cpu_limit or memory_info.percent > memory_limit:
            print("High resource usage detected. Pausing...")
            time.sleep(5)
        else:
            time.sleep(interval)
