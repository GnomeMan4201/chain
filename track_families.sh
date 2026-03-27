#!/data/data/com.termux/files/usr/bin/bash
log="$HOME/LANIMORPH/logs/inject_silent.log"
declare -A counts
max=1
ascii=0
csv=0
dash=0

# Flags: --ascii, --csv, --dash
for arg in "$@"; do
  case "$arg" in
    --ascii) ascii=1 ;;
    --csv) csv=1 ;;
    --dash) dash=1 ;;
  esac
done

echo -e "\n🧬 LANIMORPH :: Payload Family Tracker\n"

# Extract and classify payloads
while read -r line; do
    [[ "$line" == *"using"* ]] || continue
    name=$(echo "$line" | sed -n 's/.*using \(.*\)$/\1/p')
    name="$(basename "$name")"
    case "$name" in
        *exfil*|*dump*|*token*|*cookie*) fam="exfil" ;;
        *map*|*scan*|*finger*|*bluetooth*) fam="scanner" ;;
        *prank*|*fake*|*flash*|*scream*) fam="prank" ;;
        *worm*|*crawl*|*chain*) fam="lateral" ;;
        *mirror*|*mimic*|*polymorph*|*skin*) fam="polymorph" ;;
        *) fam="other" ;;
    esac
    ((counts["$fam"]++))
done < "$log"

# Find highest value
for f in "${!counts[@]}"; do
    [[ ${counts[$f]} -gt $max ]] && max=${counts[$f]}
done

# CSV output
if [[ $csv -eq 1 ]]; then
    out="$HOME/LANIMORPH/chain/payload_families.csv"
    echo "family,count" > "$out"
    for f in "${!counts[@]}"; do
        echo "$f,${counts[$f]}" >> "$out"
    done
    echo -e "[✓] CSV exported to: \033[1;32m$out\033[0m"
    exit 0
fi

# Bar chart mode
echo -e "\033[1;36m📊 Payload Family Distribution\033[0m"

output=""
for f in $(printf "%s\n" "${!counts[@]}" | while read -r k; do echo "$k ${counts[$k]}"; done | sort -k2 -nr | cut -d' ' -f1); do
    val=${counts[$f]}
    bar_len=$(( (val * 30) / max ))
    if [[ $ascii -eq 1 ]]; then
        bar=$(printf "%-${bar_len}s" | tr ' ' '#')
    else
        bar=$(printf "%-${bar_len}s" | tr ' ' '█')
    fi
    line=$(printf "\033[1;33m%-12s\033[0m | %-30s %3d" "$f" "$bar" "$val")
    echo "$line"
    output+="$(echo "$line" | sed 's/\x1B\[[0-9;]*[JKmsu]//g')"$'\n'
done

echo -e "\n[✓] Family classification complete.\n"

# Optional: log bar output to timeline
if [[ $dash -eq 1 ]]; then
    echo -e "[BAR GRAPH] [$(date +'%b %d %H:%M')] :: Payload family stats:\n$output" >> "$HOME/LANIMORPH/logs/inject_silent.log"
fi
