#!/data/data/com.termux/files/usr/bin/bash
# LANIMORPH :: Tree HTML + Lineage ZIP Export

out="$HOME/LANIMORPH/export/tree_bundle_$(date +%Y%m%d_%H%M%S).zip"
mkdir -p "$HOME/LANIMORPH/export"

zip -j "$out" \
  "$HOME/LANIMORPH/chain/mutation_tree.html" \
  "$HOME/LANIMORPH/logs/mutation_lineage.json"

echo -e "\n[✓] Tree bundle created: $out"
