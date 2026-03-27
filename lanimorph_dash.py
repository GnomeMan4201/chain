#!/usr/bin/env python3
import os, subprocess, socket, time
from datetime import datetime

LOG_PATH = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")
MUTATION_PATH = os.path.expanduser("~/LANIMORPH/chain/mutation.txt")
AI_SCAN_DIR = os.path.expanduser("~/LANIMORPH/ai_scans")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.45", 80))
        return s.getsockname()[0]
    except:
        return "unknown"

def get_current_mutation():
    if os.path.exists(MUTATION_PATH):
        with open(MUTATION_PATH) as f:
            return f.read().strip()
    return "(none)"

def get_last_injection():
    if not os.path.exists(LOG_PATH):
        return "(none)"
    with open(LOG_PATH) as f:
        lines = f.readlines()
    for line in reversed(lines):
        if "silent: Host compromised" in line:
            return line.strip()
    return "(none)"

def score_payload_ai():
    payload_path = input("[?] Path to payload: ").strip()
    if not os.path.exists(payload_path):
        print("[!] Payload not found.")
        time.sleep(2)
        return
    with open(payload_path) as f:
        payload_code = f.read()
    prompt = f"""
You are a stealth evaluation AI.

Analyze the following payload and score it for stealthiness on a scale from 0 (highly detectable) to 10 (extremely stealthy).

Also identify:
- Obfuscation method (e.g., base64, string reversal, PowerShell obfuscation)
- Risk level (Low / Medium / High)
- Suggest one stealth upgrade

Payload:
{payload_code}
    """.strip()
    result = subprocess.run(["llama-cli", "--prompt", prompt], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_path = os.path.join(AI_SCAN_DIR, f"score_{ts}.md")
    with open(out_path, "w") as f:
        f.write(output)
    print(f"[✓] Saved AI score to: {out_path}")
    input("[Enter] to return...")

def draw_menu():
    os.system("clear")
    print("="*60)
    print("🧠  LANIMORPH :: LIVE OPERATION DASHBOARD")
    print("="*60)
    print(f"[+] Local IP            : {get_local_ip()}")
    print(f"[+] Current Mutation    : {get_current_mutation()}")
    print(f"[+] Last Injection      : {get_last_injection()}")
    print(f"[+] Time                : {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    print("Choose an option:\n")
    print(" [1] View Live Subnet Infection Map")
    print(" [2] Score Payload Stealth (Offline AI)")
    print(" [3] Replay Infection Timeline")
    print(" [4] Rotate Payload Vault")
    print(" [5] Open QR Flyer")
    print(" [0] Exit")

def main():
    while True:
        draw_menu()
    try:
    try:
        try:
        try:
            choice = input("\n>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Exiting dashboard.")
            break
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Exiting dashboard.")
            break
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Exiting dashboard.")
        break
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Exiting dashboard.")
        return
        if choice == "1":
            subprocess.run(["python3", os.path.expanduser("~/LANIMORPH/chain/lan_mesh_map.py")])
        elif choice == "2":
            score_payload_ai()
        elif choice == "3":
            subprocess.run(["python3", os.path.expanduser("~/LANIMORPH/chain/lan_replay_stats.py")])
        elif choice == "4":
            subprocess.run(["bash", os.path.expanduser("~/LANIMORPH/chain/lan_rotate_mutation.sh")])
        elif choice == "5":
            subprocess.run(["bash", os.path.expanduser("~/LANIMORPH/chain/lan_flyer_trigger.sh")])
        elif choice == "0":
            break
        else:
            print("[!] Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    main()
