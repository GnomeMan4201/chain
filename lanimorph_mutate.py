#!/usr/bin/env python3
import uuid, random, json
from pathlib import Path
from lanimorph_ai_scorer import score_payload

SRC_DIR = Path.home() / "LANIMORPH" / "payloads"
LOG_FILE = Path.home() / "LANIMORPH" / "logs" / "lineage.json"
EXPORTS_DIR = Path.home() / "LANIMORPH" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def mutate_content(code):
    lines = code.strip().splitlines()
    if len(lines) < 2:
        return code + "\n# mutation: minimal"
    random.shuffle(lines)
    junk = f"echo $((RANDOM % 9 + 1)) > /dev/null"
    lines.insert(random.randint(0, len(lines)-1), junk)
    return "\n".join(lines)

def mutate_file(payload_path):
    orig = Path(payload_path)
    content = orig.read_text()
    mutated = mutate_content(content)

    uid = uuid.uuid4().hex[:8]
    out_file = SRC_DIR / f"mutated_{uid}.sh"
    out_file.write_text(mutated)
    print(f"[✓] Mutated payload: {out_file.name}")

    score_payload(out_file)

    lineage = {
        "uid": uid,
        "parent": orig.name,
        "child": out_file.name,
        "path": str(out_file),
    }
    try:
        log = json.loads(LOG_FILE.read_text())
    except:
        log = []
    log.append(lineage)
    LOG_FILE.write_text(json.dumps(log, indent=2))

    # Auto-export ZIP
    zip_name = EXPORTS_DIR / f"{out_file.stem}_export.zip"
    from zipfile import ZipFile
    with ZipFile(zip_name, 'w') as zipf:
        zipf.write(out_file, out_file.name)
        summary = out_file.with_suffix('.sh.summary.ai.txt')
        if summary.exists():
            zipf.write(summary, summary.name)
    print(f"[+] Exported to ZIP → {zip_name.name}")

    # Auto-refresh dashboard
    print("[~] Launching scoreboard...")
    import subprocess
    subprocess.run(["python", str(Path.home() / "LANIMORPH" / "ui" / "lanimorph_dash.py")])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python lanimorph_mutate.py <base_payload.sh>")
    else:
        mutate_file(sys.argv[1])
