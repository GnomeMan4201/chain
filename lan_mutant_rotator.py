#!/usr/bin/env python3
import os, time, random
from datetime import datetime

# Ensure LANIMORPH is in path
import sys
sys.path.append(os.path.expanduser("~/LANIMORPH"))

from core.mutators.lanimorph_mutator import mutate_payload

PAYLOAD_PATH = os.path.expanduser("~/LANIMORPH/chain/payload_template.py")
OUT_DIR = os.path.expanduser("~/LANIMORPH/chain/mutants")
os.makedirs(OUT_DIR, exist_ok=True)

def mutate_and_save():
    if not os.path.exists(PAYLOAD_PATH):
        print("[!] Base payload not found.")
        return
    with open(PAYLOAD_PATH) as f:
        base = f.read()

    fake_ip = f"192.168.0.{random.randint(100, 250)}"
    try:
        mutated = mutate_payload(base, fake_ip)
        fname = f"mutant_{fake_ip.replace('.', '_')}_{int(time.time())}.sh"
        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w") as f:
            f.write(mutated)
        print(f"[✓] Mutated payload saved: {out_path}")
    except Exception as e:
        print(f"[!] Mutation failed: {e}")

if __name__ == "__main__":
    mutate_and_save()
