#!/data/data/com.termux/files/usr/bin/bash
log=~/LANIMORPH/logs/inject_silent.log

echo -e "\n🌐 LANIMORPH :: Payload Heatmap\n"
grep 'silent: Host' "$log" | grep '@' | awk -F'@' '
{
    payload = $2;
    gsub(/^ /, "", payload);
    hits[payload]++;
}
END {
    printf "%-25s %-10s\n", "Payload", "Hits";
    for (p in hits) {
        printf "%-25s %-10d\n", p, hits[p];
    }
}
'
echo -e "\n[✓] Heatmap complete.\n"
