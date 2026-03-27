#!/usr/bin/env python3
import os
import sys

mem_path = os.path.expanduser("~/LANIMORPH/chain/mutation_memory.db")
family = sys.argv[1] if len(sys.argv) > 1 else ""
host = sys.argv[2] if len(sys.argv) > 2 else ""

if not family or not host:
    print("Usage: avoid_repeats.py <family> <host>")
    sys.exit(1)

used = {}

if os.path.exists(mem_path):
    with open(mem_path) as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2:
                used[parts[0].strip()] = parts[1].strip().split(",")

if host in used and family in used[host]:
    print(f"[✘] Skipping {host} — already injected with {family}")
    sys.exit(2)

print(f"[✓] Host {host} has not seen family: {family}. Proceed.")
sys.exit(0)
