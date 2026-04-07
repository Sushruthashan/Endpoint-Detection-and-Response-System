import psutil
import time
from datetime import datetime
from agent.sender import send_event
from agent.config import HOSTNAME, AGENT_ID

seen = set()

def monitor_processes():
    while True:
        for proc in psutil.process_iter(['pid','name']):
            if proc.info['pid'] not in seen:
                seen.add(proc.info['pid'])

                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "hostname": HOSTNAME,
                    "agent_id": AGENT_ID,
                    "event_type": "process",
                    "process_name": proc.info['name'],
                    "pid": proc.info['pid']
                }

                send_event(event)

        time.sleep(0.01)


if __name__ == "__main__":
    monitor()
