#!/usr/bin/env python3
# LANIMORPH :: Mutation Personality Bar Graph + Summary

import re
from collections import Counter
from termcolor import colored

log_path = "/data/data/com.termux/files/home/LANIMORPH/logs/inject_silent.log"
personalities = ["Scout", "Leech", "Parasite", "Mimic", "Hunter"]

counts = Counter()

with open(log_path, "r", errors="ignore") as f:
    for line in f:
        match = re.search(r"(\d+\.\d+\.\d+\.\d+).*?using\s+(.*)", line)
        if match:
            payload = match.group(2).strip()
            for p in personalities:
                if p.lower() in payload.lower():
                    counts[p] += 1

# === Visual ===
print("\n🧬 LANIMORPH :: Personality Spread Summary")
print("=".ljust(50, "="))
max_bar = 40
total = sum(counts.values()) or 1

for p in personalities:
    count = counts[p]
    bar_len = int((count / total) * max_bar)
    bar = colored("█" * bar_len, "cyan")
    print(f"{p.ljust(10)} | {bar} {count}")

print("=".ljust(50, "="))
print(f"[✓] Total personality mutations: {total}\n")
