#!/usr/bin/env python3
import os, time, random, subprocess

ROTATE_INTERVAL = 60 * 5  # Rotate every 5 minutes
PARENT_IP = os.popen("ip route get 1 | awk '{print $7; exit}'").read().strip()
MUTATOR = os.path.expanduser("~/LANIMORPH/chain/dna_mutator.py")
DASHBOARD = os.path.expanduser("~/LANIMORPH/chain/dna_timeline.py")

def rotate():
    print(f"[🌀] Starting mutation rotation loop (interval: {ROTATE_INTERVAL}s)")
    while True:
        try:
            print(f"[+] Mutating from parent IP: {PARENT_IP}")
            subprocess.run(["python3", MUTATOR, PARENT_IP], check=True)
            subprocess.run(["python3", DASHBOARD], check=True)
            sleep = ROTATE_INTERVAL + random.randint(-60, 60)
            print(f"[⏳] Sleeping {sleep} seconds until next rotation...\n")
            time.sleep(sleep)
        except KeyboardInterrupt:
            print("[!] Rotation manually stopped.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    rotate()
