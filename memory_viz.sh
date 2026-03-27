#!/data/data/com.termux/files/usr/bin/bash
mem="$HOME/LANIMORPH/chain/mutation_memory.db"

echo -e "\n🧠 LANIMORPH :: Mutation Memory Map\n"

while IFS=: read -r host data; do
    fams=$(echo "$data" | tr ',' ' ')
    printf "\033[1;32m%-15s\033[0m | " "$host"
    for f in $fams; do
        case "$f" in
            exfil) icon="📤" ;;
            scanner) icon="🔎" ;;
            prank) icon="🎭" ;;
            lateral) icon="🕷" ;;
            polymorph) icon="🧬" ;;
            other) icon="📦" ;;
            *) icon="❓" ;;
        esac
        echo -n "$icon "
    done
    echo
done < "$mem"

echo -e "\n[✓] Timeline map complete.\n"
