#!/usr/bin/env bash
# LANIMORPH :: XP by Personality

XP_FILE="$HOME/LANIMORPH/logs/unlocked_payloads.txt"

declare -A group_map=(
  ["Scout"]="Explorer"
  ["Recon"]="Explorer"
  ["Exfil"]="Parasite"
  ["Persist"]="Parasite"
)

echo "======================================"
echo "🧠  LANIMORPH :: XP by Personality"
echo "======================================"

awk -F'→' '
{
  role = $2; gsub(/^[ \t]+|[ \t]+$/, "", role)
  count[role]++
}
END {
  for (r in count) {
    printf "%s\n", r
    printf "  └── XP: %d\n", count[r]
  }
}
' "$XP_FILE" | awk '
  BEGIN {
    print "Personality :: XP Summary"
    print "--------------------------"
  }
  /^Scout/     { p["Explorer"] += $2 }
  /^Recon/     { p["Explorer"] += $2 }
  /^Exfil/     { p["Parasite"] += $2 }
  /^Persist/   { p["Parasite"] += $2 }
  END {
    for (type in p) {
      printf "%-12s | %s %d\n", type, gensub(/./, "█", "g", sprintf("%*s", p[type], "")), p[type]
    }
    print "--------------------------"
  }
'
