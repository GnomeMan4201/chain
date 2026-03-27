#!/usr/bin/env python3
import os, re
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")

def parse_log():
    entries = []
    if not os.path.exists(LOG):
        print("[!] No inject_silent.log found.")
        return entries

    with open(LOG) as f:
        for line in f:
            match = re.match(r"\[(.*?)\] (\d+\.\d+\.\d+\.\d+) -> (.*?) :: PORT (\d+)", line)
            if match:
                ts_raw, src, tgt, port = match.groups()
                try:
                    ts = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M:%S")
                except:
                    ts = ts_raw
                entries.append((ts, src, tgt, port))
    return sorted(entries, key=lambda x: x[0])

def replay(entries):
    print("\n=== LANIMORPH :: Chronological Infection Replay ===\n")
    for ts, src, tgt, port in entries:
        print(f"[{ts}] {src} ➜ {tgt}  (port {port})")
    print(f"\nTotal injections: {len(entries)}")

if __name__ == "__main__":
    replay(parse_log())
