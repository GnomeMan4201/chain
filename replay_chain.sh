#!/data/data/com.termux/files/usr/bin/bash
log=~/LANIMORPH/logs/inject_silent.log

echo -e "\n🔗 LANIMORPH :: Mutation Chain Replay\n"
grep 'silent: Host' "$log" | grep '@' | tail -n 40 | awk -F'@' '
{
    ip_part = $1
    payload = $2
    gsub(/^ /, "", payload)
    split(ip_part, arr, " ")
    ip = arr[length(arr)]
    printf "%s ──> %s\n", ip, payload;
}' | nl -w2 -s'. '
echo -e "\n[✓] Chain replay complete.\n"
