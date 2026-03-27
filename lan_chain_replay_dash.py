import os
from datetime import datetime
from pathlib import Path

base = Path.home() / "LANIMORPH" / "chain" / "replays"
log_file = Path.home() / "LANIMORPH" / "logs" / "silent" / "inject_silent.log"

replay_manifest = []
for target_dir in base.glob("*"):
    if not target_dir.is_dir():
        continue
    for zipfile in target_dir.glob("*.zip"):
        parts = zipfile.name.split("_")
        if len(parts) >= 4:
            replay_manifest.append({
                "host": target_dir.name,
                "mutation": parts[1],
                "timestamp": parts[2],
                "zip": zipfile.name
            })

replay_manifest.sort(key=lambda x: x["timestamp"], reverse=True)

lines = ["="*66, " LANIMORPH :: CHAIN REPLAY DASHBOARD", "="*66]
for entry in replay_manifest:
    try:
        ts = datetime.utcfromtimestamp(int(entry["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
    except:
        ts = entry["timestamp"]
    lines.append(f"[{ts}] {entry['host']} :: mutation={entry['mutation']} :: {entry['zip']}")

dashboard_path = base / "lan_chain_replay_dashboard.txt"
dashboard_path.write_text("\n".join(lines))
print(f"[✓] Dashboard saved to: {dashboard_path}")
