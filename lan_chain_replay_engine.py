import os
from datetime import datetime
from pathlib import Path

LOG_FILE = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")

def extract_events():
    events = []
    if not os.path.exists(LOG_FILE):
        return events
    with open(LOG_FILE) as f:
        lines = f.readlines()
    for line in lines:
        if "::" in line:
            try:
                parts = line.strip().split("::")
                if len(parts) == 3:
                    ip = parts[0].split(":")[1]
                    mutation = parts[1].split("=")[1]
                    ts = parts[2].split("=")[1]
                    events.append((ip, mutation, ts))
            except:
                continue
    return events

def replay_event(target_ip, mutation_id, timestamp):
    try:
        replay_dir = Path(os.path.expanduser(f"~/LANIMORPH/chain/replays/{target_ip}"))
        replay_dir.mkdir(parents=True, exist_ok=True)

        payload = f"echo Replaying mutation: {mutation_id} on {target_ip} at {timestamp}"
        pfile = replay_dir / f"replay_{timestamp}.sh"
        with open(pfile, "w") as f:
            f.write(payload)

        flyer = replay_dir / "flyer.html"
        with open(flyer, "w") as f:
            f.write(f"<h2>Replay Payload for {target_ip}</h2><p>Mutation: {mutation_id}</p>")

        qrfile = replay_dir / "qr.png"
        qr_cmd = f"echo file://{pfile} | qrencode -o {qrfile}"
        os.system(qr_cmd)

        zipname = replay_dir / f"replay_{mutation_id}_{timestamp}.zip"
        os.system(f"zip -j {zipname} {pfile} {flyer} {qrfile}")

        print(f"[✓] Replayed + bundled: {target_ip} -> {zipname}")
    except Exception as e:
        print(f"[!] Failed to replay {target_ip}: {e}")

def main():
    events = extract_events()
    if not events:
        print("[!] No replayable events found.")
        return
    print(f"[~] Replaying {len(events)} past injections...")
    for tgt, mid, ts in events:
        replay_event(tgt, mid, ts)

if __name__ == "__main__":
    main()
