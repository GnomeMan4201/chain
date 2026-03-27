#!/usr/bin/env python3
# LANIMORPH :: Personality Mutation Tree (CLI)

import os, json
from collections import defaultdict
from termcolor import colored

meta_dir = os.path.expanduser("~/LANIMORPH/vault/metadata")
lineage_file = os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")

# Load metadata by filename
meta = {}
for f in os.listdir(meta_dir):
    if f.endswith(".meta"):
        try:
            with open(os.path.join(meta_dir, f)) as mf:
                j = json.load(mf)
                meta[j["name"]] = j
        except:
            continue

# Load lineage
with open(lineage_file) as f:
    lineage = json.load(f)

# Build tree (by parent)
tree = defaultdict(list)
for name, info in meta.items():
    parent = info.get("parent", "root")
    tree[parent].append(name)

# Color map
colors = {
    "Mimic": "cyan",
    "Parasite": "red",
    "Leech": "yellow",
    "Scout": "green",
    "Hunter": "magenta"
}

def print_tree(node="root", prefix=""):
    for child in sorted(tree.get(node, [])):
        p_type = meta.get(child, {}).get("personality", "Unknown")
        color = colors.get(p_type, "white")
        label = colored(f"{child} ({p_type})", color)
        print(f"{prefix}└─ {label}")
        print_tree(child, prefix + "   ")

print("\n🌲 LANIMORPH :: Personality Mutation Tree")
print("=".ljust(50, "="))
print_tree()
print("=".ljust(50, "="))
