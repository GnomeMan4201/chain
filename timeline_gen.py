#!/usr/bin/env python3
import os, re
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
OUT = os.path.expanduser("~/LANIMORPH/chain/mutation_timeline.txt")

def load_log():
    if not os.path.exists(LOG): return []
    with open(LOG) as f:
        lines = f.readlines()
    entries = []
    for line in lines:
        m = re.search(r"\[(.*?)\] (.*?) -> (mut_\d+) :: PORT (\d+)", line)
        if m:
            ts, parent, mut, port = m.groups()
            entries.append({
                "time": ts,
                "parent": parent,
                "mutation": mut,
                "port": port
            })
    return entries

def render_ascii(entries):
    lines = ["LANIMORPH :: ASCII MUTATION TIMELINE\n"]
    for e in entries:
        lines.append(f"{e['time']} | {e['parent']} ──▶ {e['mutation']} (port {e['port']})")
    return "\n".join(lines)

def save_out(text):
    with open(OUT, "w") as f:
        f.write(text)
    print(f"[✓] ASCII timeline saved to: {OUT}")

def main():
    entries = load_log()
    if not entries:
        print("[!] No mutation log entries found.")
        return
    timeline = render_ascii(entries[::-1])  # Newest on bottom
    print(timeline)
    save_out(timeline)

if __name__ == "__main__":
    main()
