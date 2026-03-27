#!/usr/bin/env python3
import os, time, subprocess

PARENT_IP = "192.168.1.33"  # You can make this dynamic if needed
MUTATOR = os.path.expanduser("~/LANIMORPH/chain/dna_mutator.py")
TRACKER = os.path.expanduser("~/LANIMORPH/chain/payload_family_tracker.py")
LOG = os.path.expanduser("~/LANIMORPH/chain/rotator.log")

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def rotate():
    log("Starting chain rotation")
    subprocess.run(["python3", MUTATOR, PARENT_IP])
    subprocess.run(["python3", TRACKER])
    log("Rotation complete")

def loop_forever():
    log("Chain rotator initialized")
    while True:
        rotate()
        time.sleep(3600)  # 1 hour

if __name__ == "__main__":
    loop_forever()
