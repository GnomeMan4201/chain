#!/usr/bin/env python3
import os, re
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
GLYPHS = ["🧬", "🦠", "🔗", "🐛", "👾", "🪱", "💉", "💀"]

def parse_log():
    entries = []
    if not os.path.exists(LOG):
        print("[!] mutation_chain.log not found.")
        return entries

    with open(LOG) as f:
        for line in f:
            match = re.match(r"\[(.*?)\] (\d+\.\d+\.\d+\.\d+) -> (.*?) :: PORT (\d+)", line)
            if match:
                ts_raw, src, mid, port = match.groups()
                try:
                    ts = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M:%S")
                except:
                    ts = ts_raw
                entries.append((ts, src, mid, port))
    return sorted(entries, key=lambda x: x[0])

def render(entries):
    print("\n╭─ LANIMORPH DNA TIMELINE ───────────────────────────────╮")
    for i, (ts, src, mid, port) in enumerate(entries):
        glyph = GLYPHS[i % len(GLYPHS)]
        print(f"│ {glyph} [{ts}] {src} => {mid} on PORT {port}")
    print("╰────────────────────────────────────────────────────────╯")
    print(f"[✓] Rendered {len(entries)} mutation entries.\n")

if __name__ == "__main__":
    render(parse_log())
