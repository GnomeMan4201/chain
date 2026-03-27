#!/usr/bin/env bash
# LANIMORPH :: Payload Injector (Shell Wrapper)

PAYLOAD="$1"
TARGET="$2"

if [ -z "$PAYLOAD" ] || [ -z "$TARGET" ]; then
  echo "Usage: inject_payload.sh <payload> <target_ip>"
  exit 1
fi

python3 ~/LANIMORPH/chain/inject_manual.py "$PAYLOAD" "$TARGET"
