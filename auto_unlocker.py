#!/usr/bin/env python3
# LANIMORPH :: Auto Unlocker (Always Unlock Mode)

families = {
    "Scout": "scout_payload.sh",
    "Exfil": "exfil_payload.sh",
    "Recon": "recon_payload.sh",
    "Persist": "persist_payload.sh"
}

print("🔓 All Payload Families Unlocked:")
for fam, file in families.items():
    print(f"[+] Unlocked → {fam}: {file}")
