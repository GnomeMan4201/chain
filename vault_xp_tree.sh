#!/usr/bin/env bash
# LANIMORPH :: XP Evolution Tree

XP_FILE="$HOME/LANIMORPH/logs/unlocked_payloads.txt"

echo "======================================"
echo "🌳  LANIMORPH :: XP Evolution Tree"
echo "======================================"

awk -F'→' '
{
  role = $2; gsub(/^[ \t]+|[ \t]+$/, "", role)
  count[role]++
}
END {
  for (r in count) {
    printf "%s\n", r
    printf "├── XP: %d\n", count[r]
    for (i = 0; i < count[r]; i++) {
      printf "│   └── █\n"
    }
    print ""
  }
}
' "$XP_FILE"

echo "======================================"
