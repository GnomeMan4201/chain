#!/usr/bin/env python3
# LANIMORPH :: Infection Graph JSON Export

import os, re, json
from datetime import datetime

logfile = os.path.expanduser("~/LANIMORPH/logs/inject_silent.log")
outfile = os.path.expanduser("~/LANIMORPH/chain/map_data.json")

with open(logfile, encoding="utf-8", errors="ignore") as f:
    lines = [l.strip() for l in f if "silent:" in l]

edges = []
seen = set()
for line in lines:
    match = re.search(r"\[(.*?)\] silent: Host compromised by (\S+) \[ (\S+) \]", line)
    if match:
        _, src, dst = match.groups()
        if (src, dst) not in seen:
            edges.append({"source": src, "target": dst})
            seen.add((src, dst))

with open(outfile, "w") as f:
    json.dump(edges, f, indent=2)

print(f"[✓] Infection map exported → {outfile}")
