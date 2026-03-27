#!/usr/bin/env bash
# LANIMORPH :: Vault Unlock Overview (ASCII Bar Chart)

XP_FILE="$HOME/LANIMORPH/logs/unlocked_payloads.txt"

if [ ! -f "$XP_FILE" ]; then
  echo "[!] No unlock log found."
  exit 1
fi

echo "======================================"
echo "🧬  LANIMORPH :: UNLOCK OVERVIEW"
echo "======================================"

awk -F'→' -f - "$XP_FILE" << 'AWK_END'
{
  gsub(/^[ \t]+|[ \t]+$/, "", $2)
  count[$2]++
}
END {
  for (role in count) {
    roles[role] = count[role]
  }

  n = asorti(roles, sorted, "@val_num_desc")
  for (i = 1; i <= n; i++) {
    role = sorted[i]
    bar = ""
    for (j = 0; j < roles[role]; j++) {
      bar = bar "█"
    }
    printf "%-10s | %s %d\n", role, bar, roles[role]
  }
}
AWK_END

echo "======================================"
