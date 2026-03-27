#!/usr/bin/env bash
# LANIMORPH :: Vault + XP Exporter

DATE=$(date +%Y%m%d_%H%M%S)
BUNDLE="$HOME/LANIMORPH/vault_bundles/vault_xp_bundle_$DATE.zip"

mkdir -p "$HOME/LANIMORPH/vault_bundles"

zip -r "$BUNDLE" "$HOME/LANIMORPH/vault" "$HOME/LANIMORPH/logs/unlocked_payloads.txt" >/dev/null

echo "🗃  Vault XP bundle saved to:"
echo "$BUNDLE"
