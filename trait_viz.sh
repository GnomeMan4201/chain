#!/data/data/com.termux/files/usr/bin/bash
input=~/LANIMORPH/profiles/assigned.txt

declare -A colors=(
  [Scout]="\033[1;34m"       # Blue
  [Leech]="\033[1;31m"       # Red
  [Mimic]="\033[1;33m"       # Yellow
  [Hunter]="\033[1;35m"      # Magenta
  [Prankster]="\033[1;32m"   # Green
)

reset="\033[0m"

echo -e "\n🧠  LANIMORPH :: TRAIT MAP\n"

awk -F':' '{print $1, $2}' "$input" | sort -k2 | while read -r ip trait; do
  color="${colors[$trait]}"
  [[ -z "$color" ]] && color="\033[1;37m" # Default white
  printf "  ${color}%-15s → %-10s${reset}\n" "$ip" "$trait"
done

echo -e "\n[✓] Trait map rendered.\n"
