#!/usr/bin/env python3
import re, os
from collections import Counter, defaultdict

logfile = os.path.expanduser("~/LANIMORPH/chain/logs/inject_silent.log")
if not os.path.exists(logfile):
    print("[x] No inject_silent.log found.")
    exit(1)

sources = Counter()
targets = Counter()
chains = defaultdict(set)

with open(logfile) as f:
    for line in f:
        match = re.search(r"silent: Host compromised by (\d+\.\d+\.\d+\.\d+) \[ (\d+\.\d+\.\d+\.\d+) \]", line)
        if match:
            src = match.group(1)
            tgt = match.group(2)
            sources[src] += 1
            targets[tgt] += 1
            chains[src].add(tgt)

out_path = os.path.expanduser("~/LANIMORPH/chain/reports/lan_replay_stats.txt")
with open(out_path, "w") as f:
    f.write("LANIMORPH :: REPLAY STATS\n\n")
    f.write("Top Spreaders:\n")
    for s, c in sources.most_common(5):
        f.write(f"  {s:<15} → {c} injections\n")

    f.write("\nMost Targeted Hosts:\n")
    for t, c in targets.most_common(5):
        f.write(f"  {t:<15} ← {c} times\n")

    f.write("\nPossible Chain Loops:\n")
    for src, tgts in chains.items():
        if src in tgts:
            f.write(f"  [!] {src} re-injected into itself\n")

print(f"[✓] Replay stats report saved to: {out_path}")
