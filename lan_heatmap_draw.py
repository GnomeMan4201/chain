#!/usr/bin/env python3
import os, re
from collections import defaultdict
from datetime import datetime

logfile = "/data/data/com.termux/files/home/LANIMORPH/chain/silent_timeline.log"
heatmap = defaultdict(int)

if not os.path.exists(logfile):
    print("No timeline log yet."); exit(0)

with open(logfile) as f:
    for line in f:
        m = re.search(r"\[(.*?)\].*?\[(.*?)\]", line)
        if m:
            host = m.group(2).strip()
            heatmap[host] += 1

rows = []
for ip in sorted(heatmap):
    count = heatmap[ip]
    bar = "█" * min(count, 20)
    rows.append(f"{ip:<15} | {bar:<20} {count}")

with open("/data/data/com.termux/files/home/LANIMORPH/chain/lan_infection_heatmap.txt", "w") as out:
    out.write("LANIMORPH INFECTION HEATMAP\n")
    out.write("Generated: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    for row in rows:
        out.write(row + "\n")

print("[✓] ASCII heatmap saved to: ~/LANIMORPH/chain/lan_infection_heatmap.txt")
