#!/usr/bin/env python3
import os
import sys
import time
import json
import subprocess
import re
import urllib.request
import urllib.error
import pexpect
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
P = Fore.MAGENTA
W = Fore.WHITE
C = Fore.CYAN
RESET = Style.RESET_ALL

API_PROVIDERS = {
    '1': {
        'name': 'Groq',
        'type': 'openai', 
        'url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.3-70b-versatile', 
        'info': 'Laju gila (Groq LPU)'
    },
    '2': {
        'name': 'Gemini',
        'type': 'gemini',
        'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash',
        'model': 'gemini-1.5-flash',
        'info': 'Percuma & Context besar'
    },
    
}

CONFIG_DIR = os.path.expanduser("~/.dathena")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LOG_FILE = os.path.join(CONFIG_DIR, "session.log")

# ══════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════

def banner():
    print(RESET)
    print(f"""{R}
▓█████▄       ▄▄▄     ▄▄▄█████▓ ██░ ██ ▓█████  ███▄    █  ▄▄▄      
▒██▀ ██▌     ▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    
░██   █▌     ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  
░▓█▄   ▌     ░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██ 
░▒████▓  ██▓  ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓░▒████▒▒██░   ▓██░ ▓█   ▓██▒
 ▒▒▓  ▒  ▒▓▒  ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░
 ░ ▒  ▒  ░▒    ▒   ▒▒ ░   ░     ▒ ░▒░ ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░
 ░ ░  ░  ░     ░   ▒    ░       ░  ░░ ░   ░      ░   ░ ░   ░   ▒   
   ░      ░        ░  ░         ░  ░  ░   ░  ░         ░       ░  ░
 ░        ░{RESET}
{W}        Digital Autonomous Threat Hunting & Exploit Navigation Agent{RESET}
{R}                     [ Kali Linux Edition v2.1 ]{RESET}

                        git:https://github.com/SONICZY-RAWR

""")

# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════

def clear():
    os.system("clear")

def slowprint(s, delay=0.02):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)

def log_session(cmd, output):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n[{datetime.now()}] CMD: {cmd}\n")
        f.write(f"OUTPUT: {str(output)[:500]}\n")
        f.write("─" * 50 + "\n")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(data):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ══════════════════════════════════════════════════════
# API SETUP - SUPPORT ANY API
# ══════════════════════════════════════════════════════

API_PROVIDERS = {
    '1': {
        'name': 'Groq',
        'url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.3-70b-versatile',
        'type': 'openai',
        'info': 'Free, fast - console.groq.com/keys'
    },
    '2': {
        'name': 'Gemini',
        'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
        'model': 'gemini-2.0-flash',
        'type': 'gemini',
        'info': 'Free tier - aistudio.google.com/apikey'
    },
    '3': {
        'name': 'OpenAI',
        'url': 'https://api.openai.com/v1/chat/completions',
        'model': 'gpt-4o-mini',
        'type': 'openai',
        'info': 'Paid - platform.openai.com/api-keys'
    },
    '4': {
        'name': 'OpenRouter',
        'url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'meta-llama/llama-3-8b-instruct:free',
        'type': 'openai',
        'info': 'Free models available - openrouter.ai/keys'
    },
    '5': {
        'name': 'Custom',
        'url': '',
        'model': '',
        'type': 'openai',
        'info': 'Any OpenAI-compatible API'
    }
}

def setup_api():
    clear()
    banner()
    print(f"{R}╔══════════════════════════════════════╗{RESET}")
    print(f"{R}║{Y}         FIRST TIME SETUP             {R}║{RESET}")
    print(f"{R}╚══════════════════════════════════════╝{RESET}\n")

    slowprint(f"{W}  Pilih API provider untuk D.ATHENA:\n")

    
    for k, v in API_PROVIDERS.items():
        print(f"{R}  [{k}] {Y}{v['name']:<12}{W} - {v['info']}{RESET}")

    print()
    choice = input(f"{R}  Pilihan (1-5): {W}").strip()

    if choice not in API_PROVIDERS:
        choice = '1'

    
    provider = API_PROVIDERS[choice].copy()

    if choice == '5':
        provider['url'] = input(f"{R}  API URL: {W}").strip()
        provider['model'] = input(f"{R}  Model name: {W}").strip()
        provider['name'] = input(f"{R}  Provider name: {W}").strip()
        provider['type'] = 'openai' 

    api_key = input(f"\n{R}  Masukkan API Key untuk {provider['name']}: {W}").strip()

    if not api_key:
        print(f"{R}  [!] API Key tidak boleh kosong!")
        sys.exit(1)

    
    config = {
        'api_key': api_key,
        'provider': provider,  
        'setup_date': str(datetime.now())
    }

    save_config(config)
    slowprint(f"\n{G}  [+] Config disimpan! Sila restart D.ATHENA.")
    time.sleep(1.5)
    return config
# ══════════════════════════════════════════════════════
# UNIVERSAL AI CALL
# ══════════════════════════════════════════════════════
def ask_ai(config, prompt, system_prompt="", retries=3):
    provider = config['provider']
    api_key = config.get('api_key')
    api_type = provider.get('type', 'openai')

    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'D.ATHENA-Security-Agent/1.0'
    }

    for attempt in range(retries):
        try:
            # --- LOGIK GEMINI ---
            if api_type == 'gemini':
                url = f"{provider['url']}:generateContent?key={api_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
                }).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers=headers)

            # --- LOGIK OPENAI / GROQ / OPENROUTER ---
            else:
                url = provider['url']
                headers['Authorization'] = f'Bearer {api_key}'
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                payload = json.dumps({
                    "model": provider['model'],
                    "messages": messages,
                    "temperature": 0.6
                }).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers=headers)

            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
                # Cara ambil jawapan ikut provider
                if api_type == 'gemini':
                    return res_data['candidates'][0]['content']['parts'][0]['text']
                else:
                    return res_data['choices'][0]['message']['content']

        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8')
            # Kalau 400, mungkin sebab model name salah kat Groq
            if e.code == 400:
                return f"[ERROR] Bad Request: Check model name atau JSON format.\nDetail: {error_msg}"
            return f"[ERROR] HTTP {e.code}: {e.reason}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return f"[ERROR] {str(e)}"

    return "[ERROR] Gagal hubungi AI."
# ══════════════════════════════════════════════════════
# EXECUTION ENGINE
# ══════════════════════════════════════════════════════

WIRELESS_TOOLS = ['aircrack-ng', 'airodump-ng', 'aireplay-ng', 'airmon-ng',
                  'wifite', 'reaver', 'bully', 'pixiewps', 'hcxdumptool',
                  'hcxtools', 'wash', 'cowpatty', 'fern-wifi-cracker']

GUI_ALTERNATIVES = {
    'burpsuite': 'curl -v -k {}',
    'wireshark': 'tshark -i eth0 -c 200',
    'maltego': 'theharvester -d {} -b all',
    'autopsy': 'volatility3 -f {} windows.info',
    'zenmap': 'nmap -sV -sC -T4 {}',
}

INTERACTIVE_TOOLS = {
    'msfconsole': 'msf',
    'metasploit': 'msf',
    'gdb': 'gdb',
    'radare2': 'r2',
    'r2': 'r2',
}

def check_tool(tool):
    r = subprocess.run(f"which {tool} 2>/dev/null", shell=True, capture_output=True, text=True)
    return r.returncode == 0

def execute_simple(cmd, timeout=120):
    print(f"\n{R}  ╔═ EXECUTING ══════════════════════════╗{RESET}")
    print(f"{R}  ║ {Y}{cmd[:45]:<45}{R} ║{RESET}")
    print(f"{R}  ╚══════════════════════════════════════╝{RESET}\n")

    try:
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True, bufsize=1,
            env={**os.environ, 'TERM': 'xterm'}
        )
        output_lines = []
        line_count = 0
        for line in iter(process.stdout.readline, ''):
            
            print(f"  {line}", end='')
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            output_lines.append(clean_line)
            line_count += 1
            if line_count >= 400:
                print(f"\n{Y}  ... [output truncated at 400 lines]{RESET}")
                break

        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"\n{R}  [!] Timeout after {timeout}s{RESET}")

        print(f"\n{R}  ══════════════════════════════════════{RESET}")
        return ''.join(output_lines)

    except Exception as e:
        return f"ERROR: {str(e)}"

def execute_msf(msf_commands, config):
    print(f"\n{R}  ╔═ METASPLOIT ═════════════════════════╗{RESET}")
    print(f"{R}  ║ {Y}Launching msfconsole...               {R}║{RESET}")
    print(f"{R}  ╚══════════════════════════════════════╝{RESET}\n")

    output_all = ""
    try:
        child = pexpect.spawn('msfconsole -q', timeout=90, encoding='utf-8')
        child.expect(['msf6', 'msf5', 'msf'], timeout=90)
        print(f"{G}  [+] Metasploit ready!{RESET}\n")

        for cmd in msf_commands:
            print(f"{Y}  msf > {W}{cmd}{RESET}")
            child.sendline(cmd)
            try:
                child.expect(['msf6', 'msf5', 'msf'], timeout=45)
                out = child.before
                output_all += out
                lines = out.split('\n')
                for line in lines[:30]:
                    if line.strip():
                        print(f"{W}  {line}{RESET}")
                if len(lines) > 30:
                    print(f"{Y}  ... [{len(lines)} lines total]{RESET}")
            except pexpect.TIMEOUT:
                print(f"{Y}  [~] Timeout on: {cmd}{RESET}")
            except pexpect.EOF:
                break

        child.sendline('exit -y')
        try:
            child.close()
        except:
            pass

    except Exception as e:
        output_all = f"MSF Error: {str(e)}"
        print(f"{R}  [!] {output_all}{RESET}")

    print(f"\n{R}  ══════════════════════════════════════{RESET}")
    return output_all

def execute_gdb(binary):
    if not binary or not os.path.exists(binary):
        binary = input(f"{R}  [D.ATHENA] Binary path to analyze: {W}").strip()
    cmd = f'gdb -batch -ex "file {binary}" -ex "info functions" -ex "disassemble main" -ex "info security" -ex "quit" 2>/dev/null'
    return execute_simple(cmd, timeout=30)

def execute_r2(binary):
    if not binary or not os.path.exists(binary):
        binary = input(f"{R}  [D.ATHENA] Binary path to analyze: {W}").strip()
    cmd = f'r2 -q -c "aaa;afl;pdf @main;iI;quit" {binary} 2>/dev/null'
    return execute_simple(cmd, timeout=60)

def execute_wireless(cmd):
    print(f"\n{Y}  [!] Wireless tool detected - checking monitor mode...{RESET}")

    result = subprocess.run("iwconfig 2>/dev/null | grep Monitor", shell=True, capture_output=True, text=True)

    if not result.stdout:
        print(f"{R}  [!] No interface in monitor mode!{RESET}")
        ifaces = subprocess.run("iwconfig 2>/dev/null", shell=True, capture_output=True, text=True)
        print(f"{W}{ifaces.stdout[:400]}{RESET}")
        iface = input(f"{R}  [D.ATHENA] Interface to use (e.g. wlan0): {W}").strip()
        if iface:
            print(f"{Y}  [*] Enabling monitor mode on {iface}...{RESET}")
            subprocess.run(f"sudo airmon-ng start {iface}", shell=True)
            time.sleep(3)
            # Update command with mon interface
            cmd = cmd.replace(iface, f"{iface}mon")

    return execute_simple(cmd, timeout=300)

def execute_sqlmap(cmd):
    if '--batch' not in cmd:
        cmd += ' --batch'
    if '--level' not in cmd:
        cmd += ' --level=3'
    if '--risk' not in cmd:
        cmd += ' --risk=2'
    return execute_simple(cmd, timeout=300)

def execute_hydra(cmd):
    return execute_simple(cmd, timeout=300)

def execute_john(cmd):
    return execute_simple(cmd, timeout=300)

def execute_hashcat(cmd):
    return execute_simple(cmd, timeout=300)

def execute_aircrack(cmd):
    return execute_simple(cmd, timeout=600)

def smart_execute(cmd, config):
    cmd = cmd.strip()
    if not cmd:
        return ""

    cmd_lower = cmd.lower()
    # Get first real command (skip sudo)
    parts = cmd.split()
    tool = parts[0]
    if tool == 'sudo' and len(parts) > 1:
        tool = parts[1]
    tool_lower = tool.lower()

    # ── GUI tools → terminal alternative ──
    for gui, alt in GUI_ALTERNATIVES.items():
        if gui in cmd_lower:
            print(f"{Y}  [~] GUI tool detected → using terminal mode{RESET}")
            return execute_simple(alt, timeout=60)

    # ── Wireless tools ──
    for wtool in WIRELESS_TOOLS:
        if wtool in cmd_lower:
            return execute_wireless(cmd)

    # ── Metasploit ──
    if any(t in cmd_lower for t in ['msfconsole', 'metasploit']):
        msf_cmds = []
        match = re.search(r'-x\s+"([^"]+)"', cmd)
        if match:
            msf_cmds = [c.strip() for c in match.group(1).split(';') if c.strip()]
        if not msf_cmds:
            print(f"{Y}  [?] What to do in Metasploit?{RESET}")
            print(f"{W}  Examples: search ms17_010 | use exploit/multi/handler | show options{RESET}")
            intent = input(f"{R}  >> {W}").strip()
            if intent:
                response = ask_ai(config,
                    f"List msfconsole commands for: {intent}. One command per line only.",
                    "Expert metasploit user. Return only msfconsole commands, one per line, no explanation.")
                msf_cmds = [l.strip() for l in response.split('\n')
                           if l.strip() and not l.startswith('#') and not l.startswith('[')][:10]
        return execute_msf(msf_cmds, config)

    # ── SQLmap ──
    if 'sqlmap' in cmd_lower:
        return execute_sqlmap(cmd)

    # ── Hydra ──
    if 'hydra' in cmd_lower or 'medusa' in cmd_lower or 'crowbar' in cmd_lower:
        return execute_hydra(cmd)

    # ── John / Hashcat ──
    if 'john' in cmd_lower:
        return execute_john(cmd)
    if 'hashcat' in cmd_lower:
        return execute_hashcat(cmd)

    # ── GDB ──
    if tool_lower == 'gdb':
        binary = parts[-1] if len(parts) > 1 and parts[-1] != 'gdb' else ''
        return execute_gdb(binary)

    # ── Radare2 ──
    if tool_lower in ['r2', 'radare2']:
        binary = parts[-1] if len(parts) > 1 else ''
        return execute_r2(binary)

    # ── Nmap - ensure flags ──
    if tool_lower == 'nmap' and len(parts) < 3:
        cmd += ' -sV -sC -T4'

    # ── Volatility ──
    if 'volatility' in cmd_lower:
        return execute_simple(cmd, timeout=180)

    # ── Aircrack ──
    if 'aircrack' in cmd_lower:
        return execute_aircrack(cmd)

    # ── Check tool exists, offer install ──
    if not check_tool(tool):
        pkg = tool_lower
        print(f"{R}  [!] Tool '{tool}' not found!{RESET}")
        install = input(f"{R}  [D.ATHENA] Install '{pkg}'? (y/n): {W}").strip().lower()
        if install == 'y':
            print(f"{Y}  [*] Installing {pkg}...{RESET}")
            execute_simple(f"sudo apt install {pkg} -y", timeout=120)
        else:
            return f"Tool '{tool}' not installed."

    # ── Default execution ──
    return execute_simple(cmd, timeout=120)

# ══════════════════════════════════════════════════════
# AI SYSTEM PROMPTS
# ══════════════════════════════════════════════════════

PENTEST_SYSTEM = """You are D.ATHENA, an autonomous penetration testing AI running on Kali Linux.

Analyze the user's pentest request and return ONLY valid JSON with NO markdown, NO backticks, NO extra text:

{
  "intent": "brief description of what user wants",
  "commands": ["bash_command_1", "bash_command_2"],
  "explanation": "what these commands do",
  "next_steps": "recommended next steps after seeing results"
}

CRITICAL RULES:
- Return ONLY the JSON object, nothing else
- Use real Kali Linux commands that work in bash
- Extract IP/domain/URL/file from user input exactly as given
- For nmap: use -sV -sC -T4 by default
- For metasploit: msfconsole -q -x "search term;exit"
- For sqlmap: include full target URL with http://
- For gobuster: use /usr/share/wordlists/dirb/common.txt
- For hashcat/john: user must provide hash file path
- Multiple commands allowed for complex tasks

Examples:
"scan 192.168.1.1" → nmap -sV -sC -O -T4 192.168.1.1
"full scan 10.0.0.1" → nmap -sV -sC -p- -T4 10.0.0.1
"vuln scan 192.168.1.1" → nmap --script vuln -T4 192.168.1.1
"web scan example.com" → nikto -h http://example.com
"find dirs example.com" → gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt -t 50
"exploit android" → msfconsole -q -x "search android/meterpreter;show options;exit"
"exploit ms17_010" → msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue;show options;exit"
"crack hash file.txt" → john --wordlist=/usr/share/wordlists/rockyou.txt file.txt
"brute ssh 192.168.1.1" → hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1
"enumerate smb 192.168.1.1" → enum4linux -a 192.168.1.1
"subdomains example.com" → sublist3r -d example.com
"osint example.com" → theharvester -d example.com -b all
"check ssl example.com" → sslscan example.com
"sniff traffic" → tshark -i eth0 -c 500
"arp scan" → arp-scan --localnet
"nikto example.com" → nikto -h http://example.com
"dirb example.com" → dirb http://example.com /usr/share/wordlists/dirb/common.txt"""

NORMAL_SYSTEM = """You are D.ATHENA, expert AI cybersecurity assistant on Kali Linux.
Deep expertise: penetration testing, web security, network security, exploit development,
reverse engineering, malware analysis, OSINT, bug bounty, CTF, Active Directory attacks.
Be direct, technical, practical. Give real working examples with actual commands."""

ANALYSIS_SYSTEM = """You are D.ATHENA analyzing pentest tool output.
Be concise, technical, and actionable.
Format:
FINDINGS: [what was discovered]
RISKS: [vulnerabilities/issues found]  
NEXT: [specific recommended commands/steps]"""

# ══════════════════════════════════════════════════════
# PARSE INTENT
# ══════════════════════════════════════════════════════

def parse_intent(config, user_input):
    response = ask_ai(config, user_input, PENTEST_SYSTEM)
    try:
        clean = response.strip()
        clean = re.sub(r'```json\s*', '', clean)
        clean = re.sub(r'```\s*', '', clean)
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        pass
    return {"intent": user_input, "commands": [], "explanation": response, "next_steps": ""}

# ══════════════════════════════════════════════════════
# MODE 1 - NORMAL CHAT
# ══════════════════════════════════════════════════════

def normal_mode(config):
    clear()
    banner()
    print(f"{R}╔══════════════════════════════════════╗{RESET}")
    print(f"{R}║{W}      MODE 1 : NORMAL AI CHAT         {R}║{RESET}")
    print(f"{R}╚══════════════════════════════════════╝{RESET}\n")
    print(f"{W}  Provider : {G}{config['provider']['name']}{RESET}")
    print(f"{W}  Model    : {C}{config['provider']['model']}{RESET}")
    slowprint(f"\n{W}  Tanya apa sahaja! Type 'exit' untuk keluar.\n")

    chat_history = []

    while True:
        try:
            user_input = input(f"\n{R}[YOU] {W}").strip()
            print(RESET, end='')

            if not user_input:
                continue
            if user_input.lower() in ['exit', 'back', 'quit']:
                break

            context = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-8:]])
            full_prompt = f"Previous:\n{context}\n\nUser: {user_input}" if context else user_input

            print(f"\n{R}[D.ATHENA]{RESET}")
            response = ask_ai(config, full_prompt, NORMAL_SYSTEM)

            for line in response.split('\n'):
                print(f"{W}  {line}{RESET}")

            chat_history.append({'role': 'User', 'content': user_input})
            chat_history.append({'role': 'D.ATHENA', 'content': response})

        except KeyboardInterrupt:
            break

# ══════════════════════════════════════════════════════
# MODE 2 - PENTEST AUTO
# ══════════════════════════════════════════════════════

def pentest_mode(config):
    clear()
    banner()
    print(f"{R}╔══════════════════════════════════════╗{RESET}")
    print(f"{R}║{R}    MODE 2 : PENTEST AUTO MODE         {R}║{RESET}")
    print(f"{R}╚══════════════════════════════════════╝{RESET}\n")

    print(f"{R}  [!] GUNAKAN HANYA PADA SISTEM YANG ADE KEBENARAN!{RESET}")
    print(f"{W}  Provider : {G}{config['provider']['name']}{RESET}\n")

    print(f"{Y}  Examples:{RESET}")
    examples = [
        "scan 192.168.1.1",
        "full port scan 10.0.0.1",
        "vuln scan 192.168.1.1",
        "web scan example.com",
        "find dirs example.com",
        "exploit android",
        "exploit ms17_010 192.168.1.1",
        "brute ssh 192.168.1.1",
        "crack hash /path/hash.txt",
        "enumerate smb 192.168.1.1",
        "subdomains example.com",
        "osint example.com",
        "sniff traffic",
        "crack wifi",
        "reverse shell 192.168.1.1 4444",
    ]
    for ex in examples:
        print(f"{W}  • {C}{ex}{RESET}")

    print(f"\n{R}  Commands: 'log' = history | 'clear' = clear screen | 'exit' = keluar{RESET}\n")

    session_log = []

    while True:
        try:
            user_input = input(f"\n{R}[PENTEST] {W}").strip()
            print(RESET, end='')

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'back', 'quit']:
                break

            if user_input.lower() == 'log':
                print(f"\n{Y}  ═══ SESSION LOG ═══{RESET}")
                if not session_log:
                    print(f"{W}  No commands executed yet.{RESET}")
                for e in session_log:
                    print(f"{W}  [{e['time']}] {C}{e['command']}{RESET}")
                continue

            if user_input.lower() == 'clear':
                clear()
                banner()
                continue

            print(f"\n{R}  [D.ATHENA] Analyzing request...{RESET}\n")
            parsed = parse_intent(config, user_input)

            print(f"{R}  ┌─ ANALYSIS ──────────────────────────────────┐{RESET}")
            print(f"{R}  │ {Y}Intent  : {W}{str(parsed.get('intent',''))[:48]}{RESET}")
            print(f"{R}  │ {Y}Explain : {W}{str(parsed.get('explanation',''))[:48]}{RESET}")
            print(f"{R}  └─────────────────────────────────────────────┘{RESET}")

            commands = parsed.get('commands', [])

            if not commands:
                print(f"{R}  [!] No commands generated. Try being more specific.{RESET}")
                print(f"{W}  AI says: {parsed.get('explanation','')}{RESET}")
                continue

            print(f"\n{Y}  Commands to execute:{RESET}")
            for i, cmd in enumerate(commands):
                print(f"{W}  [{i+1}] {C}{cmd}{RESET}")

            confirm = input(f"\n{R}  Execute? (y=all / n=cancel / number=select): {W}").strip().lower()
            print(RESET, end='')

            if confirm == 'n':
                print(f"{Y}  [~] Cancelled.{RESET}")
                continue
            elif confirm == 'y':
                exec_commands = commands
            elif confirm.isdigit():
                idx = int(confirm) - 1
                exec_commands = [commands[idx]] if 0 <= idx < len(commands) else []
                if not exec_commands:
                    print(f"{R}  [!] Invalid selection.{RESET}")
                    continue
            else:
                continue

            for cmd in exec_commands:
                output = smart_execute(cmd, config)
                log_session(cmd, output)
                session_log.append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'command': cmd
                })

                # AI Analysis
                output_str = str(output)
                if (output_str and
                    output_str not in ['TIMEOUT'] and
                    not output_str.startswith('ERROR') and
                    not output_str.startswith('Tool') and
                    len(output_str) > 30):

                    print(f"\n{R}  [D.ATHENA] Analyzing output...{RESET}\n")
                    analysis_prompt = f"Command: {cmd}\nOutput:\n{output_str[:1000]}"
                    analysis = ask_ai(config, analysis_prompt, ANALYSIS_SYSTEM)

                    print(f"{R}  ┌─ AI ANALYSIS ───────────────────────────────┐{RESET}")
                    for line in analysis.split('\n')[:25]:
                        print(f"{R}  │ {W}{line[:56]}{RESET}")
                    print(f"{R}  └─────────────────────────────────────────────┘{RESET}")

            next_steps = parsed.get('next_steps', '')
            if next_steps:
                print(f"\n{Y}  [NEXT] {W}{next_steps}{RESET}")

        except KeyboardInterrupt:
            print(f"\n{R}  [!] Interrupted.{RESET}")
            break

# ══════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════

def main_menu(config):
    while True:
        clear()
        banner()
        print(f"{R}╔══════════════════════════════════════╗{RESET}")
        print(f"{R}║{W}           SELECT MODE                {R}║{RESET}")
        print(f"{R}╠══════════════════════════════════════╣{RESET}")
        print(f"{R}║  {W}[1] Normal Mode  {R}─{W} AI Chat            {R}║{RESET}")
        print(f"{R}║  {W}[2] Pentest Mode {R}─{W} Full Auto Execute  {R}║{RESET}")
        print(f"{R}║  {W}[3] View Session Log                 {R}║{RESET}")
        print(f"{R}║  {W}[4] Change API / Provider            {R}║{RESET}")
        print(f"{R}║  {W}[0] Exit                             {R}║{RESET}")
        print(f"{R}╚══════════════════════════════════════╝{RESET}")
        print(f"\n{W}  Provider : {G}{config['provider']['name']}{W} | Model: {C}{config['provider']['model']}{RESET}\n")

        choice = input(f"{R}  [D.ATHENA] {W}").strip()
        print(RESET, end='')

        if choice == '1':
            normal_mode(config)
        elif choice == '2':
            pentest_mode(config)
        elif choice == '3':
            clear()
            if os.path.exists(LOG_FILE):
                os.system(f"tail -150 {LOG_FILE} | less")
            else:
                print(f"{Y}  No session logs yet.{RESET}")
                time.sleep(1.5)
        elif choice == '4':
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            config = setup_api()
        elif choice == '0':
            clear()
            slowprint("  D.ATHENA shutting down...")
            slowprint("  Stay ethical. Stay sharp. ⚔️")
            slowprint("  babaaaaaaaaaaaaaai...tq for using me")
            slowprint("  make by:soniczy :)")
            sys.exit(0)

# ══════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════

def main():
    try:
        clear()
        config = load_config()
        if config is None:
            config = setup_api()
        main_menu(config)
    except KeyboardInterrupt:
        print(f"\n{R}  [!] D.ATHENA terminated.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
