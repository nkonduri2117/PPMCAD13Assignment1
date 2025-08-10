import psutil
import time

# Define CPU usage threshold (in percentage)
CPU_THRESHOLD = 80

def monitor_cpu(threshold):
    print("Monitoring CPU usage... Press Ctrl+C to stop.\n")
    try:
        while True:
            # Measure CPU usage over 1-second interval
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Alert if CPU usage exceeds threshold
            if cpu_usage > threshold:
                print(f"Alert! CPU usage exceeds threshold: {cpu_usage}%\n")

            time.sleep(1)  # Optional: Add delay to reduce log spam
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred while monitoring CPU: {e}")

if __name__ == "__main__":
    monitor_cpu(CPU_THRESHOLD)
