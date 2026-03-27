#!/data/data/com.termux/files/usr/bin/bash
prof=~/LANIMORPH/profiles/assigned.txt

echo -e "\n🧠 LANIMORPH :: Personality Trait Overview\n"
awk -F':' '{traits[$2]++} END {
    printf "%-15s %-10s\n", "Profile", "Count";
    for (p in traits) printf "%-15s %-10d\n", p, traits[p];
}' "$prof"
echo -e "\n[✓] Trait analysis complete.\n"
