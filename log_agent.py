import platform
import time
import re
import json
import sqlite3
import requests
from google import genai
from google.genai import types

# Replace with your actual credentials
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# Setup SQLite Database
def setup_database():
    conn = sqlite3.connect('security_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alerts 
                 (id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  ip_address TEXT, username TEXT, threat_type TEXT, severity INTEGER)''')
    conn.commit()
    conn.close()

# Send Telegram Alert
def send_telegram_alert(threat_type, severity, ip, user, os_source):
    message = f"🚨 **CRITICAL ALERT** 🚨\n💻 **OS/Source:** {os_source}\n⚠️ **Threat:** {threat_type}\n🔴 **Severity:** {severity}/10\n🌐 **IP:** {ip}\n👤 **User:** {user}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

# Analyze Threat using AI (Gemini)
def analyze_threat(username, ip_address, os_name):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"Target Username: {username}, Source IP: {ip_address}, Event: Failed login attempts on {os_name}. Return JSON with 'threat_type' and 'severity_score' (1-10)."
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)
    except Exception as e:
        print("AI Error:", e)
        return {"threat_type": "Unknown", "severity_score": 5}

# ==========================================
# WINDOWS MONITORING SECTION (Updated with win32evtlog)
# ==========================================
def monitor_windows():
    print("🛡️ Detected OS: Windows. Starting Native Event Log Monitoring...")
    try:
        import win32evtlog
    except ImportError:
        print("❌ Error: 'pywin32' library is required. Please run (py -m pip install pywin32).")
        return

    server = 'localhost'
    logtype = 'Security'
    
    try:
        # Connect for the first time and remember the last record number
        hand = win32evtlog.OpenEventLog(server, logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        last_record_number = events[0].RecordNumber if events else 0
        win32evtlog.CloseEventLog(hand)
    except Exception as e:
        print(f"\n❌ Error accessing Security Log: {e}")
        print("Please make sure to run the Command Prompt as 'Administrator'.")
        return

    print("✅ Successfully connected. Listening for Failed Logons (Event ID: 4625)...")
    
    while True:
        time.sleep(2) # Check every 2 seconds
        try:
            hand = win32evtlog.OpenEventLog(server, logtype)
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            
            if events:
                for event in events:
                    # Stop if we reach previously checked logs
                    if event.RecordNumber <= last_record_number:
                        break
                        
                    event_id = event.EventID & 0xFFFF
                    
                    # 4625 is the Event ID for Failed Logon
                    if event_id == 4625:
                        strings = event.StringInserts
                        if strings:
                            # Extract Username and IP from Windows Event
                            user = strings[5] if len(strings) > 5 else "Unknown User"
                            ip = strings[19] if len(strings) > 19 else "Unknown IP"
                            
                            if ip != "-" and user != "-":
                                print(f"\n[!] Windows Threat Detected! User: '{user}', IP: '{ip}'")
                                process_threat(user, ip, "Windows")
                                
                # Update the last checked record number
                last_record_number = events[0].RecordNumber
            win32evtlog.CloseEventLog(hand)
        except Exception:
            pass # Skip temporary errors

# ==========================================
# LINUX MONITORING SECTION
# ==========================================
def monitor_linux():
    LOG_FILE_PATH = "/var/log/auth.log"
    print(f"🛡️ Detected OS: Linux. Monitoring '{LOG_FILE_PATH}'...")
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ Error: 'watchdog' library is required for Linux. Please run (pip install watchdog).")
        return

    class LogHandler(FileSystemEventHandler):
        def __init__(self, filename):
            self.filename = filename
            try:
                with open(filename, 'r') as f:
                    f.seek(0, 2)
                    self.last_pos = f.tell()
            except FileNotFoundError:
                print(f"❌ Error: {filename} not found. No security logs exist yet on this machine.")
                self.last_pos = 0

        def on_modified(self, event):
            if not event.src_path.endswith("auth.log"):
                return
            with open(self.filename, 'r') as f:
                f.seek(self.last_pos)
                new_lines = f.readlines()
                self.last_pos = f.tell()

            for line in new_lines:
                if "Failed password" in line:
                    ip_match = re.search(r'from\s+(\d+\.\d+\.\d+\.\d+)', line)
                    user_match = re.search(r'for\s+(invalid user\s+)?(\w+)\s+from', line)
                    if ip_match and user_match:
                        ip = ip_match.group(1)
                        user = user_match.group(2)
                        print(f"\n[!] Linux Threat Detected! User: '{user}', IP: '{ip}'")
                        process_threat(user, ip, "Linux")

    event_handler = LogHandler(LOG_FILE_PATH)
    observer = Observer()
    # Monitor the directory containing auth.log (/var/log)
    observer.schedule(event_handler, path='/var/log', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ==========================================
# CORE THREAT PROCESSING FUNCTION
# ==========================================
def process_threat(user, ip, os_name):
    ai_result = analyze_threat(user, ip, os_name)
    threat = ai_result.get('threat_type', f'{os_name} Logon Failure')
    severity = int(ai_result.get('severity_score', 8))
    
    print(f"[*] AI Analysis -> Threat: {threat}, Severity: {severity}")
    
    conn = sqlite3.connect('security_logs.db')
    conn.execute("INSERT INTO alerts (ip_address, username, threat_type, severity) VALUES (?, ?, ?, ?)", (ip, user, threat, severity))
    conn.commit()
    conn.close()
    
    if severity >= 4:
        send_telegram_alert(threat, severity, ip, user, os_name)

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    setup_database()
    
    # Automatically detect the Operating System
    current_os = platform.system()
    try:
        if current_os == "Windows":
            monitor_windows()
        elif current_os == "Linux":
            monitor_linux()
        else:
            print(f"❌ Unsupported OS Detected: {current_os}. Only Windows and Linux are supported.")
    except KeyboardInterrupt:
        print("\n Agent has been stopped!")