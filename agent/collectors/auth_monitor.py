import time
import subprocess
import re
import os
from datetime import datetime
from agent.sender import send_event
from agent.config import HOSTNAME, AGENT_ID

def monitor_auth():
    """
    Tails system authentication logs and reports failed login attempts.
    """
    # Detect log location based on OS distribution
    log_file = "/var/log/auth.log" if os.path.exists("/var/log/auth.log") else "/var/log/secure"
    
    if not os.path.exists(log_file):
        print(f"[!] CRITICAL: No authentication log found at {log_file}")
        return

    print(f"[*] Monitoring Authentication logs at: {log_file}")

    # -F (Follow) keeps the pipe open even if the log file is rotated by the OS
    cmd = ["tail", "-F", log_file]
    
    try:
        # We use bufsize=1 for line-buffered output to ensure real-time processing
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1 
        )
        
        for line in process.stdout:
            # Match common failure strings for SSH, Sudo, and PAM
            if any(x in line for x in ["Failed password", "authentication failure", "FAILED LOGIN"]):
                
                # Robust Regex to find IP regardless of 'from' or 'rhost=' labels
                ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
                source_ip = ip_match.group(1) if ip_match else "127.0.0.1"

                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "hostname": HOSTNAME,
                    "agent_id": AGENT_ID,
                    "event_type": "auth",
                    "success": False,  # Explicit boolean False
                    "source_ip": source_ip
                }
                
                # This will appear in 'sudo journalctl -u agent.service -f'
                print(f"[!] AUTH FAILURE: Reporting attempt from {source_ip}")
                
                try:
                    send_event(event)
                except Exception as e:
                    print(f"[!] Network Error: Could not send event to server: {e}")
                
    except Exception as e:
        print(f"[!] Auth Monitor Thread crashed: {e}")

if __name__ == "__main__":
    monitor_auth()
