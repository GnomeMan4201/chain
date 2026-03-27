#!/usr/bin/env python3
import os, re
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def parse_log():
    timeline = []
    if not os.path.exists(LOG): return timeline

    with open(LOG) as f:
        for line in f:
            match = re.match(r"\[(.*?)\]\s+(.*?)\s+->\s+(mut_\d+)\s+::\s+PORT\s+(\d+)", line)
            if match:
                ts, ip, mut, port = match.groups()
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                timeline.append((dt, ip, mut, int(port)))
    return sorted(timeline, key=lambda x: x[0])

def render_timeline(timeline):
    if not timeline:
        print("No timeline data.")
        return

    print("\n== LANIMORPH :: Payload Mutation Timeline ==")
    print("-" * 70)
    prev_time = None
    chain_depth = 0

    for dt, ip, mut, port in timeline[-25:]:  # Limit to last 25
        if prev_time:
            delta = (dt - prev_time).total_seconds()
            if delta > 90:
                print(" " * chain_depth + "⋮")
                chain_depth = 0
        indent = " " * (chain_depth * 2)
        print(f"{indent}↳ [{dt.strftime('%H:%M:%S')}] {ip} -> {mut} (:{port})")
        prev_time = dt
        chain_depth += 1
    print("-" * 70)

if __name__ == "__main__":
    render_timeline(parse_log())
