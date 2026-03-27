#!/usr/bin/env bash
# LANIMORPH :: Real Personality Overview (No Dummy Mode)

TAG_LOG="$HOME/LANIMORPH/logs/personality_tags.log"
MEM_LOG="$HOME/LANIMORPH/logs/mutation_memory.log"

# Verify logs exist
[[ ! -f "$TAG_LOG" ]] && { echo "[!] Missing: $TAG_LOG"; exit 1; }
[[ ! -f "$MEM_LOG" ]] && { echo "[!] Missing: $MEM_LOG"; exit 1; }

declare -A seen
declare -A count
declare -A first_time
declare -A tag

# Parse personality tags
while read -r line; do
  ip=$(echo "$line" | awk '{print $1}')
  personality=$(echo "$line" | awk '{print $3}')
  [[ -n "$ip" && -n "$personality" ]] && tag["$ip"]="$personality"
done < "$TAG_LOG"

# Parse infection memory
while read -r line; do
  ip=$(echo "$line" | grep -oP '\d+\.\d+\.\d+\.\d+')
  time=$(echo "$line" | cut -d' ' -f2-3)
  [[ -z "$ip" ]] && continue
  count["$ip"]=$((count["$ip"] + 1))
  [[ -z "${first_time["$ip"]}" ]] && first_time["$ip"]="$time"
done < "$MEM_LOG"

# Output real data only
echo
echo "🧬 LANIMORPH :: Personality Overview (Live Only)"
echo
printf "%-15s %-12s %-20s %s\n" "IP" "Personality" "First Seen" "Hits"
printf -- "------------------------------------------------------------\n"
for ip in "${!tag[@]}"; do
  printf "%-15s %-12s %-20s %s\n" \
    "$ip" \
    "${tag[$ip]}" \
    "${first_time[$ip]:-—}" \
    "${count[$ip]:-0}"
done
