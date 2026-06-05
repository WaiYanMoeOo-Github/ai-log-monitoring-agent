# 🛡️ AI-Powered Security Log Monitoring Agent

An intelligent, cross-platform security agent that monitors system logs in real-time, detects brute-force attacks or unauthorized access, and sends AI-analyzed alerts via Telegram. 

## ✨ Features
- **Cross-Platform:** Works seamlessly on both Windows (Event Viewer) and Linux (auth.log/journalctl).
- **Real-Time Threat Detection:** Instantly detects failed logons and suspicious activities.
- **AI Threat Analysis:** Integrates Google Gemini AI to analyze threats and assign severity scores.
- **Instant Alerts:** Sends critical alerts directly to Telegram with OS, User, IP, and AI summary.
- **Interactive Dashboard:** Built with Streamlit to visualize attack logs, timestamps, and threat levels.

## 🛠️ Technologies Used
- **Python** (Watchdog, Pandas, SQLite)
- **Google GenAI** (Gemini API)
- **Telegram Bot API**
- **Streamlit** (Data Visualization)

## 📸 Screenshots
### 📊 Dashboard
<img width="1280" height="601" alt="Image" src="https://github.com/user-attachments/assets/9edb198f-2a0a-44c0-bf48-08452bee208d" />

### 🚨 Telegram Alert
<img width="435" height="312" alt="Image" src="https://github.com/user-attachments/assets/774aabdd-23cb-4532-8bad-1c20ca9ef5e0" />

## 🚀 Installation & Setup
```bash
🔑 1. Create API Key
Step 1: Go to https://aistudio.google.com/  
Step 2: Enter get API key page  
Step 3: Create API key  
Step 4: Give API key name  
Step 5: Copy API key into notepad

🤖 2. Create Telegram Bot
Step 1: Open Telegram  
Step 2: Search "@BotFather"  
Step 3: Click "Start"  
Step 4: Write /newbot and click "enter"  
Step 5: Give a name for bot (Eg. My Security Agent)  
Step 6: Give username. Username must end "bot". (Eg. alice_security_bot)  
Step 7: Copy HTTP API token into notepad (If the bot created successfully @BotFather will send HTTP API Token)
Step 8: Click created bot link and then "Start"  

🆔 3. Get Telegram UserID
Step 1: Search "@userinfobot"  
Step 2: Click "Start"  
Step 3: Copy UserID into notepad  

🪟 Setup For Windows
📥 Clone & Install Dependencies
Step 1: git clone [https://github.com/WaiYanMoeOo-Github/ai-log-monitoring-agent.git](https://github.com/WaiYanMoeOo-Github/ai-log-monitoring-agent.git)
Step 2: cd ai-log-monitoring-agent
Step 3: pip install -r requirements.txt
Step 4: Insert API Key, Bot API Token and UserID into log_agent.py  

⚙️ Setup In Windows (Task Scheduler)
Step 1: Search Task Scheduler  
Step 2: Click "Action" Tab  
Step 3: Click "Create Task..."  
Step 4: Give task name (Eg. AI Security Agent)  
Step 5: Click "Change User or Group..."  
Step 6: Enter "SYSTEM" into the object name to select (examples) box and then click "OK"  
Step 7: Check "Run with highest privileges"  
Step 8: Check "Hidden"  
Step 9: Click "Trigger" Tab  
Step 10: Select "At startup" in Begin the task  
Step 11: Choose "30 seconds" in Delay task for. And then click "OK"  
Step 12: Click "Action" Tab  
Step 13: Choose "Start a program" in Action  
Step 14: Browse python.exe in Program/script """If you didn't know the location, open cmd and enter where python. And then, copy the path into the Program/script box. And change python.exe to pythonw.exe."""
Step 15: Write log_agent.py in Add arguments box.  
Step 16: Write the path that the log_agent.py script existed in Start in box.  
Step 17: Click "Ok". (If appear warning box to change the path click "NO")  
Step 18: Click "OK"  
Step 19: Restart your device.  

📊 Run Dashboard
Step 1: py -m streamlit run dashboard.py 

🧪 Test by Runas
Step 1: Open cmd by administrator  
Step 2: Enter runas /user:hacker cmd (Replace any name in hacker)  

🐧 Setup For Linux  
📥 Clone & Install Dependencies
Step 1: git clone [https://github.com/WaiYanMoeOo-Github/ai-log-monitoring-agent.git](https://github.com/WaiYanMoeOo-Github/ai-log-monitoring-agent.git)
Step 2: cd ai-log-monitoring-agent
Step 3: python3 -m venv venv_name (Create Virtual Environment) 
Step 4: source venv_name/bin/activate` (Activate Environment)
Step 5: pip install -r requirements.txt
Step 6: Insert API Key, Bot API Token and UserID into log_agent.py  
 

⚙️ Setup In Linux (Systemd Service)
Step 1: Open Terminal  
Step 2: Enter sudo nano /etc/systemd/system/log_agent.service  

In nano...  
[Unit]
Description=AI Security Log Monitoring Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=Enter downloaded folder path (Eg. /home/username/Download/Log_Monitoring_Agent/)
ExecStart=Enter log_agent.py path by venv (Eg. /home/username/Download/Log_Monitoring_Agent/log_monitor/bin/python log_agent.py)
Restart=on-failure

[Install]
WantedBy=multi-user.target

Step 3: sudo systemctl daemon-reload  
Step 4: sudo systemctl enable log_agent.service  
Step 5: sudo systemctl start log_agent.service  
Step 6: Restart device  

📊 Run Dashboard
Step 1: Open Terminal  
Step 2: source venv_name/bin/activate (Activate Virtual Environment)  
Step 3: streamlit run dashboard.py (Run Dashboard)  

🧪 Test by Hydra
Step 1: Open Terminal  
Step 2: Enter sudo hydra -l root -p wrongpassword ssh://127.0.0.1 -t 7 (Attack)  