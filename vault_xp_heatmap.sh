#!/usr/bin/env bash
# LANIMORPH :: XP Heatmap by IP

XP_FILE="$HOME/LANIMORPH/logs/unlocked_payloads.txt"

if [ ! -f "$XP_FILE" ]; then
  echo "[!] XP log missing"
  exit 1
fi

echo "======================================"
echo "🌐  LANIMORPH :: XP Heatmap by Host"
echo "======================================"

awk -F'→' '
{
  gsub(/^[ \t]+|[ \t]+$/, "", $1)
  host = $1
  count[host]++
}
END {
  for (host in count) {
    bar = ""
    for (i = 0; i < count[host]; i++) {
      bar = bar "█"
    }
    printf "%-15s | %s %d\n", host, bar, count[host]
  }
}
' "$XP_FILE"

echo "======================================"
