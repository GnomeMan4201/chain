#!/data/data/com.termux/files/usr/bin/bash
log="$HOME/LANIMORPH/logs/inject_silent.log"

echo -e "\n🛰️  LANIMORPH :: Real-Time Mutation Radar\n"
echo -e "Timestamp            | IP             | Profile     | Payload\n"
echo -e "---------------------+----------------+-------------+--------------------------"

grep 'silent: Host' "$log" | grep '@' | tail -n 50 | while read -r line; do
    ts=$(echo "$line" | cut -d']' -f1 | cut -d'[' -f2)
    ip=$(echo "$line" | awk '{print $NF}')
    profile=$(echo "$line" | grep -oP '\[\K[^]]+(?=\])')
    payload=$(echo "$line" | cut -d'@' -f2 | xargs basename)
    printf "%-21s | %-14s | %-11s | %s\n" "$ts" "$ip" "$profile" "$payload"
done

echo -e "\n[✓] Radar sync complete.\n"
