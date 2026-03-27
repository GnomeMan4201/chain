#!/usr/bin/env python3
import os, time
LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
def draw():
    if not os.path.exists(LOG): return print("No timeline available.")
    with open(LOG) as f:
        entries = f.readlines()[-20:]
    print("\n=== LANIMORPH :: Last 20 Injections ===")
    for i, line in enumerate(entries, 1):
        ts = line.split("]")[0].strip("[")
        details = line.split("]")[1].strip()
        print(f"{i:02d} [{ts}] → {details}")
if __name__ == "__main__":
    draw()
