#!/usr/bin/env python3
import os, subprocess
from datetime import datetime

VAULT = os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")
LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
OUT = os.path.expanduser("~/LANIMORPH/chain/summary/summary.md")

def get_payload():
    if not os.path.exists(VAULT): return "No payload found."
    return open(VAULT).read()

def get_log():
    if not os.path.exists(LOG): return "No chain log."
    return "".join(open(LOG).readlines()[-10:])

def run_llama(input_text):
    try:
        out = subprocess.check_output(['llama-cli', '--model', 'mistral-7b-instruct-v0.2.Q4_K_M.gguf'], input=input_text.encode(), timeout=30)
        return out.decode()
    except Exception as e:
        return f"[AI ERROR] {e}"

def main():
    payload = get_payload()
    log = get_log()
    context = f"### PAYLOAD:\n{payload}\n\n### CHAIN LOG:\n{log}\n\nSummarize threat level, stealth traits, intent, mutation risk."
    summary = run_llama(context)

    with open(OUT, "w") as f:
        f.write("# LANIMORPH :: AI Payload Summary\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")
        f.write(summary)

    print(f"[✓] Summary written to: {OUT}")

if __name__ == "__main__":
    main()
