#!/usr/bin/env bash
FLYER="$HOME/LANIMORPH/flyers/latest_flyer.html"
if [ -f "$FLYER" ]; then
    cp "$FLYER" ~/storage/downloads/
    termux-open ~/storage/downloads/latest_flyer.html
    echo "[✓] Flyer opened"
else
    echo "[x] No flyer found at $FLYER"
fi
