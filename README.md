# ⚔️ D.ATHENA

```
▓█████▄       ▄▄▄     ▄▄▄█████▓ ██░ ██ ▓█████  ███▄    █  ▄▄▄      
▒██▀ ██▌     ▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    
░██   █▌     ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  
░▓█▄   ▌     ░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██ 
░▒████▓  ██▓  ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓░▒████▒▒██░   ▓██░ ▓█   ▓██▒
 ▒▒▓  ▒  ▒▓▒  ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░
 ░ ▒  ▒  ░▒    ▒   ▒▒ ░   ░     ▒ ░▒░ ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░
 ░ ░  ░  ░     ░   ▒    ░       ░  ░░ ░   ░      ░   ░ ░   ░   ▒   
   ░      ░        ░  ░         ░  ░  ░   ░  ░         ░       ░  ░
 ░        ░
```

> **Digital Autonomous Threat Hunting & Exploit Navigation Agent**  
> AI-powered penetration testing agent for Kali Linux

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=kali-linux)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-red?style=for-the-badge)

---

## 🧠 What is D.ATHENA?

D.ATHENA is an autonomous AI penetration testing agent that runs on Kali Linux.  
Tell it what you want to do in natural language — it figures out which tools to use and executes them automatically.

It supports **two modes**:
- **Normal Mode** — AI chat for cybersecurity questions
- **Pentest Mode** — Fully automatic tool execution with AI analysis

---

## ⚡ Features

- 🤖 Natural language → automatic tool execution
- 🔧 Supports **all Kali Linux tools** (nmap, metasploit, sqlmap, hydra, aircrack-ng, and more)
- 🧩 Interactive tool handler (metasploit, gdb, radare2 via pexpect)
- 📡 Wireless attack support (auto monitor mode)
- 🔍 AI analyzes tool output and suggests next steps
- 🔑 Supports **any AI API** (Groq, Gemini, OpenAI, OpenRouter, Custom)
- 💾 Session logging

---

## 📦 Installation

```bash
# Clone repo
git clone https://github.com/SONICZY-RAWR/D.ATHENA.git
cd D.ATHENA

# Install dependencies
pip install colorama pexpect --break-system-packages

# Run as sudo (REQUIRED for full tool access)
sudo python3 dathena.py
```

> ⚠️ **Must run with `sudo`** — many Kali Linux tools require root privileges to function properly.

---

## 🔑 API Key Setup

D.ATHENA supports multiple AI providers. Get a **free API key** from any of these:

| Provider | Free? | Get Key |
|----------|-------|---------|
| **Groq** ⭐ | ✅ Free | [console.groq.com/keys](https://console.groq.com/keys) |
| Gemini | ✅ Free tier | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| OpenAI | ❌ Paid | [platform.openai.com](https://platform.openai.com/api-keys) |
| OpenRouter | ✅ Free models | [openrouter.ai/keys](https://openrouter.ai/keys) |

> Groq is recommended — it's fast, free, and works great with D.ATHENA.

---

## 🎮 How To Use

```bash
sudo python3 dathena.py
```

1. First launch — choose API provider and enter API key
2. Select **Mode 1** (chat) or **Mode 2** (pentest auto)
3. In Pentest Mode, just describe what you want:

```
[PENTEST] scan 192.168.1.1
[PENTEST] full port scan 10.0.0.1
[PENTEST] vuln scan 192.168.1.1
[PENTEST] web scan example.com
[PENTEST] exploit android
[PENTEST] exploit ms17_010 192.168.1.1
[PENTEST] brute ssh 192.168.1.1
[PENTEST] crack hash /path/to/hash.txt
[PENTEST] enumerate smb 192.168.1.1
[PENTEST] subdomains example.com
[PENTEST] osint example.com
[PENTEST] sniff traffic
[PENTEST] crack wifi
```

---

## 🔧 Troubleshooting

### ❌ Error: model decommissioned (Groq)

Groq sometimes decommissions old models. Fix:

```bash
# Step 1 - Delete old config
sudo rm /root/.dathena/config.json
rm ~/.dathena/config.json

# Step 2 - Update model in script
sed -i 's/llama3-70b-8192/llama-3.3-70b-versatile/g' dathena.py

# Step 3 - Run again
sudo python3 dathena.py
```

Current working Groq models (as of 2025):
```
llama-3.3-70b-versatile    ← recommended
llama-3.1-8b-instant       ← fastest
mixtral-8x7b-32768         ← good for technical tasks
```

Check latest models at: [console.groq.com/docs/models](https://console.groq.com/docs/models)

---

### ❌ Error: 429 Too Many Requests

You've hit the API rate limit. D.ATHENA will auto-retry, but if it persists:
- Wait 1-2 minutes and try again
- Switch to a different API provider (option 4 in main menu)

---

### ❌ Tool not found

D.ATHENA will offer to install missing tools automatically.  
Or install manually:
```bash
sudo apt install <toolname> -y
```

---

### ❌ Permission denied on tools

Always run D.ATHENA with sudo:
```bash
sudo python3 dathena.py
```

---

## ⚠️ Disclaimer

> D.ATHENA is intended for **educational purposes** and **authorized penetration testing** only.  
> Only use on systems you have **explicit permission** to test.  
> The developer is not responsible for any misuse or damage caused by this tool.

---

## 👤 Author

Made with ❤️ by **[SONICZY-RAWR](https://github.com/SONICZY-RAWR)**

> *"From Termux dreams to real tools — this is just the beginning."* 🔥

---

## ⭐ Support

If you find this useful, give it a **star** ⭐ on GitHub!

```bash
git clone https://github.com/SONICZY-RAWR/D.ATHENA.git
```
