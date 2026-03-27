#!/usr/bin/env python3
# LANIMORPH :: XP SVG Generator

import os
from collections import Counter

XP_FILE = os.path.expanduser("~/LANIMORPH/logs/unlocked_payloads.txt")
SVG_FILE = os.path.expanduser("~/LANIMORPH/vault/vault_xp_graph.svg")

count = Counter()
with open(XP_FILE) as f:
    for line in f:
        if "→" in line:
            _, role = map(str.strip, line.strip().split("→", 1))
            count[role] += 1

bar_height = 20
bar_gap = 10
bar_width_scale = 10
width = 500
height = (bar_height + bar_gap) * len(count)

svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']

y = 0
for role, val in count.items():
    svg.append(f'<rect x="0" y="{y}" width="{val*bar_width_scale}" height="{bar_height}" fill="#66ccff" />')
    svg.append(f'<text x="{val*bar_width_scale + 5}" y="{y + 15}" font-size="14" fill="#000">{role} ({val})</text>')
    y += bar_height + bar_gap

svg.append("</svg>")
with open(SVG_FILE, "w") as f:
    f.write("\n".join(svg))

print(f"[✓] SVG chart saved to: {SVG_FILE}")
