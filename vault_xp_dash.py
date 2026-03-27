#!/usr/bin/env python3
# LANIMORPH :: XP Dashboard (TUI)

import os
from collections import Counter

XP_FILE = os.path.expanduser("~/LANIMORPH/logs/unlocked_payloads.txt")
if not os.path.isfile(XP_FILE):
    print("[!] XP log missing.")
    exit(1)

count = Counter()
with open(XP_FILE) as f:
    for line in f:
        if "→" in line:
            _, role = map(str.strip, line.strip().split("→", 1))
            count[role] += 1

print("=" * 40)
print("📊 LANIMORPH :: XP Dashboard")
print("=" * 40)
for role, xp in count.most_common():
    print(f"{role:<12} | {'█' * xp} {xp}")
print("=" * 40)
