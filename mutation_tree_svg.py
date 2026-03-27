#!/usr/bin/env python3
# LANIMORPH :: Mutation Tree SVG Renderer

import os, json
from graphviz import Digraph

lineage_path = os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")
meta_dir     = os.path.expanduser("~/LANIMORPH/vault/metadata/")
svg_out_path = os.path.expanduser("~/LANIMORPH/chain/mutation_tree.svg")

if not os.path.exists(lineage_path):
    print("[!] No lineage data found.")
    exit(1)

with open(lineage_path, "r") as f:
    lineage = json.load(f)

# Load metadata
metadata = {}
for fname in os.listdir(meta_dir):
    if fname.endswith(".meta"):
        try:
            with open(os.path.join(meta_dir, fname)) as f:
                meta = json.load(f)
                name = meta.get("name", fname.replace(".meta", ""))
                metadata[name] = meta
        except:
            continue

# Setup graph
dot = Digraph("LANIMORPH_Tree", format="svg")
dot.attr(bgcolor="#111111", fontname="Courier", fontsize="12")

# Add nodes
for name, meta in metadata.items():
    p = meta.get("personality", "Unknown")
    g = meta.get("generation", "?")
    color = {
        "Mimic": "cyan",
        "Parasite": "violet",
        "Hunter": "crimson",
        "Scout": "limegreen",
        "Leech": "orange"
    }.get(p, "gray")

    dot.node(name,
        f"{name}\n[{p} | Gen {g}]",
        color=color,
        fontcolor=color,
        style="filled",
        fillcolor="#222222"
    )

# Add edges
for name, info in lineage.items():
    parent = info.get("parent")
    if parent and parent in metadata:
        dot.edge(parent, name, color="#666666")

# Output
dot.render(svg_out_path, view=False)
print(f"[✓] SVG mutation tree saved to: {svg_out_path}")
