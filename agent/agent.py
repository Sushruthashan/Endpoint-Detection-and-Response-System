import threading
from agent.collectors.process_monitor import monitor_processes
from agent.collectors.auth_monitor import monitor_auth

def main():
    print("=" * 40)
    print("    EDR Endpoint Agent Started")
    print("=" * 40)

    # Define the threads
    process_thread = threading.Thread(target=monitor_processes, daemon=True)
    auth_thread = threading.Thread(target=monitor_auth, daemon=True)

    # Start the threads
    print("[+] Starting Process Monitor...")
    process_thread.start()
    
    print("[+] Starting Auth Monitor...")
    auth_thread.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

if __name__ == "__main__":
    import time
    main()
