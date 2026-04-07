from agent.collectors.process_monitor import monitor_processes

def main():
    print("=" * 40)
    print("   EDR Endpoint Agent Started")
    print("=" * 40)
    print("Monitoring system activity...\n")

    try:
        monitor_processes()
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

if __name__ == "__main__":
    main()
