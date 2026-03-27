#!/usr/bin/env python3
import re
from collections import defaultdict

# Define personalities
personalities = ["Scout", "Leech", "Parasite", "Mimic", "Hunter"]
log_path = "/data/data/com.termux/files/home/LANIMORPH/logs/inject_silent.log"

# Init heatmap
heatmap = defaultdict(lambda: defaultdict(int))

# Open log with fallback for encoding errors
with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        match = re.search(r"(\d+\.\d+\.\d+\.\d+).*?using\s+(.*)", line)
        if match:
            host = match.group(1).strip()
            payload = match.group(2).strip()
            for p in personalities:
                if p.lower() in payload.lower():
                    heatmap[host][p] += 1

# === Visualize ===
print("\n🧬 LANIMORPH :: Mutation Personality Heatmap")
print("=" * 66)
print("Legend: ▓ = 1+, █ = 3+, ░ = 0")
header = "HOST".ljust(18) + " ".join([p[:4].upper().ljust(6) for p in personalities])
print(header)
print("-" * len(header))

for host in sorted(heatmap.keys()):
    row = host.ljust(18)
    for p in personalities:
        count = heatmap[host][p]
        if count == 0:
            cell = "░".ljust(6)
        elif count >= 3:
            cell = "█".ljust(6)
        else:
            cell = "▓".ljust(6)
        row += cell
    print(row)

print("=" * 66)
print(f"[✓] Personality map generated from: inject_silent.log\n")
