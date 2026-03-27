#!/usr/bin/env python3
# LANIMORPH :: Mutation Tree HTML Viewer (Enhanced)

import os, json

lineage_path = os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")
meta_dir     = os.path.expanduser("~/LANIMORPH/vault/metadata/")
output_path  = os.path.expanduser("~/LANIMORPH/chain/mutation_tree.html")

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

# HTML colors for personalities
colors = {
    "Mimic": "cyan",
    "Parasite": "violet",
    "Hunter": "crimson",
    "Scout": "limegreen",
    "Leech": "orange",
    "Unknown": "gray"
}

# Recursively build HTML
def print_tree(node, depth=0):
    out = ""
    children = [k for k, v in lineage.items() if v.get("parent") == node]
    out += "<ul>\n"
    for child in children:
        meta = metadata.get(child, {})
        p = meta.get("personality", "Unknown")
        g = meta.get("generation", "?")
        color = colors.get(p, "black")
        tag = f"<b style='color:{color}'>{child}</b> <small>[{p} | Gen {g}]</small>"
        out += "  " * depth + f"<li>{tag}</li>\n"
        out += print_tree(child, depth + 1)
    out += "</ul>\n"
    return out

roots = [k for k in lineage if lineage[k].get("parent") not in lineage]

html = """<html><head><title>LANIMORPH Tree</title>
<style>
  body { font-family: monospace; background: #111; color: #eee; padding: 20px; }
  ul { list-style: none; margin-left: 20px; }
  li { margin: 4px 0; }
</style>
</head><body>
<h2>🧬 LANIMORPH :: Mutation Tree Viewer</h2>
"""

for r in roots:
    html += f"<b style='color:gold'>{r}</b> <small>[root]</small>\n"
    html += print_tree(r)

html += "<hr><p>Generated from inject_silent.log</p></body></html>"

with open(output_path, "w") as f:
    f.write(html)

print(f"[✓] Tree HTML saved to: {output_path}")
print("[~] Opening in Termux browser (if available)...")
os.system(f"termux-open {output_path}")
