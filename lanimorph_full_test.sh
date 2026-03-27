
# Fix: fallback path if $DECODED is empty
if [ -z "$DECODED" ] || [ ! -f "$DECODED" ]; then
  DECODED="$HOME/LANIMORPH/vault/vault_payload_decoded.sh"
  [ -f "$DECODED" ] || echo "[!] Missing decoded payload at \$DECODED"
fi

