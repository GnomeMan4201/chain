#!/usr/bin/env python3
import os, time
LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
def replay():
    if not os.path.exists(LOG): return print("No chain to replay.")
    with open(LOG) as f:
        entries = f.readlines()
    print("=== LANIMORPH :: INFECTION REPLAY ===")
    for line in entries:
        print("->", line.strip())
        time.sleep(0.3)
if __name__ == "__main__":
    replay()
