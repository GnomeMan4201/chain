#!/data/data/com.termux/files/usr/bin/bash
mapfile -t lines < ~/LANIMORPH/profiles/assigned.txt

declare -A symbols=(
    [Scout]="🔍"
    [Leech]="🕷️"
    [Mimic]="🌀"
    [Prankster]="🎭"
    [Hunter]="🎯"
    [Unknown]="❓"
)

echo -e "\n🌐 LANIMORPH :: Personality Map of Subnet\n"

cols=6
count=0

for entry in "${lines[@]}"; do
    ip="${entry%%:*}"
    profile="${entry##*:}"
    sym="${symbols[$profile]:-${symbols[Unknown]}}"
    printf "%-17s %-10s %s\t" "$ip" "$profile" "$sym"
    ((count++))
    if (( count % cols == 0 )); then echo ""; fi
done

echo -e "\n[✓] Visual map generated.\n"
