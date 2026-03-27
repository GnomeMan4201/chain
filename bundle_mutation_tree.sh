#!/bin/bash
# LANIMORPH :: Advanced Mutation Tree ZIP Bundler

BUNDLE_DIR="$HOME/LANIMORPH/export"
mkdir -p "$BUNDLE_DIR"

DATE=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="mutation_bundle_${DATE}.zip"
ZIP_PATH="$BUNDLE_DIR/$ZIP_NAME"

echo "[*] Regenerating lineage + SVG..."
python3 ~/LANIMORPH/chain/tag_lineage.py
python3 ~/LANIMORPH/chain/mutation_tree_svg.py
python3 ~/LANIMORPH/chain/tree_viewer_html.py

echo "[*] Generating stats..."
# Stats file
STATS_FILE="$HOME/LANIMORPH/chain/mutation_stats.txt"
python3 - << EOF2 > "$STATS_FILE"
import json, os
meta_dir = os.path.expanduser("~/LANIMORPH/vault/metadata")
counts = {}
for f in os.listdir(meta_dir):
  if f.endswith(".meta"):
    with open(os.path.join(meta_dir, f)) as m:
      p = json.load(m).get("personality", "Unknown")
      counts[p] = counts.get(p, 0) + 1
print("LANIMORPH Personality Stats\n" + "="*30)
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
  print(f"{k:<10} : {v}")
EOF2

echo "[*] Calculating deepest lineage path..."
DEEP_FILE="$HOME/LANIMORPH/chain/deepest_lineage.txt"
python3 - << EOF3 > "$DEEP_FILE"
import json
with open(os.path.expanduser("~/LANIMORPH/logs/mutation_lineage.json")) as f:
  lineage = json.load(f)
depths = {}
def trace(name):
  parent = lineage.get(name, {}).get("parent")
  return 1 + trace(parent) if parent else 1
for name in lineage:
  depths[name] = trace(name)
deepest = max(depths.items(), key=lambda x: x[1])
print(f"Deepest Mutation Chain:\n{deepest[0]} → depth {deepest[1]}")
EOF3

echo "[*] Creating ZIP bundle..."
zip -j "$ZIP_PATH" \
  "$HOME/LANIMORPH/chain/mutation_tree.svg" \
  "$HOME/LANIMORPH/chain/mutation_tree.html" \
  "$HOME/LANIMORPH/logs/mutation_lineage.json" \
  "$HOME/LANIMORPH/logs/inject_silent.log" \
  "$HOME/LANIMORPH/chain/mutation_stats.txt" \
  "$HOME/LANIMORPH/chain/deepest_lineage.txt"

# Optionally add .meta files
META_FILES=$(find "$HOME/LANIMORPH/vault/metadata/" -type f -name "*.meta")
zip -j "$ZIP_PATH" $META_FILES

# Optionally add QR flyers
QR_DIR="$HOME/LANIMORPH/vault/qr"
if [ -d "$QR_DIR" ]; then
  find "$QR_DIR" -type f -name "*.html" -o -name "*.png" | zip -j "$ZIP_PATH" -@
fi

echo "[✓] Advanced bundle created: $ZIP_PATH"
