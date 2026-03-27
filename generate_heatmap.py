#!/usr/bin/env python3
# LANIMORPH :: Payload Heatmap Generator (ASCII CLI)

import os
from collections import defaultdict
from datetime import datetime

log_path = os.path.expanduser("~/LANIMORPH/logs/inject_silent.log")

# Initialize host → family map
heatmap = defaultdict(lambda: defaultdict(int))
families = ["exfil", "scanner", "prank", "lateral", "polymorph", "other"]

# Parse log
if os.path.exists(log_path):
    with open(log_path, "r", errors="ignore") as f:
        for line in f:
            if "silent:" not in line or "using" not in line:
                continue
            try:
                parts = line.strip().split()
                host = parts[-3]
                payload = parts[-1]
                fam = "other"
                if any(x in payload for x in ["exfil", "dump", "token", "cookie"]):
                    fam = "exfil"
                elif any(x in payload for x in ["map", "scan", "finger", "bluetooth"]):
                    fam = "scanner"
                elif any(x in payload for x in ["prank", "fake", "flash", "scream"]):
                    fam = "prank"
                elif any(x in payload for x in ["worm", "crawl", "chain"]):
                    fam = "lateral"
                elif any(x in payload for x in ["mirror", "mimic", "polymorph", "skin"]):
                    fam = "polymorph"
                heatmap[host][fam] += 1
            except:
                continue
else:
    print("[✘] inject_silent.log not found.")
    exit(1)

# Print ASCII heatmap
print("\n🔥 LANIMORPH :: Payload Heatmap")
print("=".ljust(60, "="))
print("Legend: ▓ = 1+, █ = 3+, ░ = 0")
header = "HOST".ljust(18) + " ".join([f[:3].upper().ljust(6) for f in families])
print(header)
print("-" * len(header))

for host in sorted(heatmap.keys()):
    row = host.ljust(18)
    for fam in families:
        count = heatmap[host][fam]
        if count == 0:
            cell = "░".ljust(6)
        elif count >= 3:
            cell = "█".ljust(6)
        else:
            cell = "▓".ljust(6)
        row += cell
    print(row)

print("=" * 60)
print(f"[✓] Heatmap generated from: inject_silent.log\n")
