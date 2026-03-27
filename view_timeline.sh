#!/data/data/com.termux/files/usr/bin/bash
log=~/LANIMORPH/logs/inject_silent.log
echo -e "\n📈 LANIMORPH :: Mutation Timeline View\n"
awk -F'[][]' '/silent: Host/ {
    split($4, parts, " ");
    printf "%s ── %s\n", $2, parts[length(parts)]
}' "$log" | nl -w2 -s'. '
echo -e "\n[✓] Timeline complete.\n"
