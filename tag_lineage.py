#!/usr/bin/env python3
# LANIMORPH :: Auto-Lineage Tagger

import os
import json
from collections import defaultdict

log_file = os.path.expanduser("~/LANIMORPH/logs/inject_silent.log")
output_file = os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")

tree = defaultdict(list)
data = {}

# Step 1: Parse
with open(log_file, "r", errors="ignore") as f:
    for line in f:
        if "using" not in line: continue
        parts = line.strip().split("using")
        if len(parts) != 2: continue
        source = parts[0].split()[-1].strip("[]")
        payload = parts[1].strip()
        tree[source].append(payload)
        data[payload] = {"parent": source}

# Step 2: Recurse and Tag
def tag_chain(node, lineage=[], depth=0):
    if node not in data: return
    data[node]["lineage"] = lineage + [node]
    data[node]["depth"] = depth
    for child in tree.get(node, []):
        tag_chain(child, data[node]["lineage"], depth + 1)

roots = [k for k in tree if all(k != v for sub in tree.values() for v in sub)]
for r in roots:
    tag_chain(r)

# Step 3: Save
with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"[✓] Lineage data saved to: {output_file}")
