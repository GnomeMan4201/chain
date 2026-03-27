#!/usr/bin/env python3
# LANIMORPH :: Payload Evolution Engine

import os
from collections import Counter

XP_FILE = os.path.expanduser("~/LANIMORPH/logs/unlocked_payloads.txt")
VAULT = os.path.expanduser("~/LANIMORPH/vault")
EVOLVE_MAP = {
    "Scout": ("lan_worm.py", 10),
    "Exfil": ("encrypted_exfil.py", 3),
    "Recon": ("fingerprint_dump.py", 5),
    "Persist": ("polymorph_mutator.py", 4),
}

if not os.path.isfile(XP_FILE):
    print("[!] No XP log found.")
    exit(1)

counts = Counter()
with open(XP_FILE) as f:
    for line in f:
        parts = line.strip().split("→")
        if len(parts) == 2:
            role = parts[1].strip()
            counts[role] += 1

print("======================================")
print("🔓 LANIMORPH :: Payload Evolution")
print("======================================")

for role, (filename, threshold) in EVOLVE_MAP.items():
    xp = counts.get(role, 0)
    unlocked = os.path.exists(os.path.join(VAULT, filename))
    bar = "█" * xp + " " * max(0, threshold - xp)
    status = "✅ UNLOCKED" if unlocked else "🔒 LOCKED"
    print(f"{role:<10} | {bar:<{threshold}} {xp}/{threshold}  {status}")

print("======================================")
