#!/usr/bin/env python3
# LANIMORPH :: Deepest Lineage Finder

import os, json

lineage_path = os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")
meta_dir     = os.path.expanduser("~/LANIMORPH/vault/metadata/")

if not os.path.exists(lineage_path):
    print("[!] No lineage data found.")
    exit(1)

with open(lineage_path, "r") as f:
    data = json.load(f)

deepest = max(data.items(), key=lambda x: x[1].get("depth", 0), default=None)

if not deepest:
    print("[!] No lineage data to analyze.")
    exit(1)

payload, info = deepest
lineage = info.get("lineage", [])
depth   = info.get("depth", 0)

# Try to load personality tag
personality = "Unknown"
meta_path = os.path.join(meta_dir, f"{payload}.meta")
if os.path.exists(meta_path):
    try:
        with open(meta_path, "r") as m:
            meta = json.load(m)
            personality = meta.get("personality", "Unknown")
    except:
        pass

# Display
print("\n🧬 LANIMORPH :: Deepest Mutation Lineage")
print("=" * 50)
print(f"Payload      : {payload}")
print(f"Personality  : {personality}")
print(f"Depth        : {depth}")
print(f"Lineage      :")
for i, p in enumerate(lineage):
    print(f"  {'└──' if i == len(lineage)-1 else '├──'} {p}")
print("=" * 50 + "\n")
