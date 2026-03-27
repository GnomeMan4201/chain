#!/usr/bin/env python3
import os, base64, subprocess
from datetime import datetime

payload_file = os.path.expanduser("~/LANIMORPH/chain/mutated_payload.py")
test_log = os.path.expanduser("~/LANIMORPH/logs/silent/selftest.log")

print("🧪 SELF-TEST: Checking payload...")

# 1. Basic syntax
try:
    compile(open(payload_file).read(), "<string>", "exec")
    print("[✓] Syntax: OK")
except Exception as e:
    print(f"[!] Syntax error: {e}")

# 2. Stealth tag check
with open(payload_file) as f:
    content = f.read()
    tags = ["curl", "base64", "bash", "wget", "http"]
    found = [t for t in tags if t in content]
    print(f"[•] Found {len(found)} stealth tags: {', '.join(found)}")

# 3. llama-cli opinion
if os.path.exists(payload_file):
    prompt = f"Evaluate the stealth of this payload:\n{content[:600]}"
    scored = subprocess.getoutput(f"llama-cli -p {prompt!r}").strip()
    with open(test_log, "a") as f:
        f.write(f"[{datetime.now()}] {scored}\n")
    print("[✓] LLM Stealth Score:")
    print(scored)
