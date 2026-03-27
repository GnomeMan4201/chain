#!/usr/bin/env python3
import re, os
from collections import defaultdict

logfile = os.path.expanduser("~/LANIMORPH/chain/logs/inject_silent.log")
if not os.path.exists(logfile):
    print("[x] No silent log found.")
    exit(1)

edges = defaultdict(set)
hosts = set()

with open(logfile) as f:
    for line in f:
        match = re.search(r"silent: Host compromised by (\d+\.\d+\.\d+\.\d+) \[ (\d+\.\d+\.\d+\.\d+) \]", line)
        if match:
            source = match.group(1)
            target = match.group(2)
            edges[source].add(target)
            hosts.update([source, target])

# Build ASCII graph
out = ["LANIMORPH :: SUBNET MESH MAP\n"]
for src in sorted(edges):
    targets = sorted(edges[src])
    line = f"{src:<15} → " + ", ".join(targets)
    out.append(line)

output_path = os.path.expanduser("~/LANIMORPH/chain/replays/lan_subnet_meshmap.txt")
with open(output_path, "w") as f:
    f.write("\n".join(out))

print(f"[✓] Mesh map saved to: {output_path}")
