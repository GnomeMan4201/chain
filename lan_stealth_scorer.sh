#!/usr/bin/env bash
PAYLOAD="$1"
MODEL="~/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
PROMPT="Rate the stealth and evasiveness of the following payload in one sentence:"

if [ ! -f "$PAYLOAD" ]; then
  echo "[x] Payload not found: $PAYLOAD"; exit 1
fi

TEXT=$(cat "$PAYLOAD")
echo -e "$PROMPT\n\n$TEXT" | llama-cli --model "$MODEL"
