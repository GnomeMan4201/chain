#!/usr/bin/env bash
# LANIMORPH :: XP Heatmap View (Color-coded Payload XP)

DB="$HOME/LANIMORPH/chain/xp_log.db"
declare -A THRESHOLDS=( ["Scout"]=5 ["Exfil"]=3 ["Recon"]=5 ["Persist"]=4 )

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[1;30m'
NC='\033[0m'

sqlite3 "$DB" "SELECT 1 FROM xp LIMIT 1;" 2>/dev/null || {
  echo "[!] XP table missing. Run: patch_xp_table.py"
  exit 1
}

echo -e "\n🧪 XP HEATMAP :: Payload Family Intensity\n"

for fam in Scout Exfil Recon Persist; do
  count=$(sqlite3 "$DB" "SELECT COALESCE(SUM(points), 0) FROM xp WHERE LOWER(payload_family)=LOWER('$fam';")
  target=${THRESHOLDS[$fam]}
  percent=$(( (100 * count) / target ))

  # Set color
  if [ "$percent" -ge 100 ]; then
    COLOR="$GREEN"
  elif [ "$percent" -ge 50 ]; then
    COLOR="$YELLOW"
  elif [ "$percent" -gt 0 ]; then
    COLOR="$RED"
  else
    COLOR="$GRAY"
  fi

  # Bar logic
  bar_width=20
  filled=$(( (percent * bar_width) / 100 ))
  empty=$(( bar_width - filled ))
  bar=$(printf "%0.s█" $(seq 1 $filled))
  bar+=$(printf "%0.s " $(seq 1 $empty))

  printf "%-8s ${COLOR}[%s]${NC} %2s / %s XP (%s%%)\n" "$fam" "$bar" "$count" "$target" "$percent"
done
