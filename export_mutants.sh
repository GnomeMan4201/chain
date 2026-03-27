#!/data/data/com.termux/files/usr/bin/bash
ts=$(date +%Y%m%d_%H%M%S)
zip ~/storage/shared/LANIMORPH_MUTANTS_$ts.zip -r ~/LANIMORPH/mutated
echo "[✓] Exported LANIMORPH mutants to USB: LANIMORPH_MUTANTS_$ts.zip"
