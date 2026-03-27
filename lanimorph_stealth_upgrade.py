#!/usr/bin/env python3
import sys, uuid
from pathlib import Path
from subprocess import run

def main(payload_file):
    payload = Path(payload_file).expanduser().resolve()
    if not payload.exists():
        print(f"[!] File not found: {payload}")
        return

    prompt = f"""You are a stealth-focused red team assistant. Your job is to mutate this shell payload to reduce detection and improve stealth. Keep its core behavior intact.\n\n### PAYLOAD:\n{payload.read_text()}"""
    stealth_out = payload.with_suffix(".stealth.ai.txt")

    print("[~] Running offline LLaMA for stealth suggestions...")
    result = run([
        "llama-cli",
        "--model", str(Path.home() / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"),
        "--prompt", prompt
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("[!] Error running llama-cli")
        print(result.stderr)
        return

    stealth_out.write_text(result.stdout)
    print(f"[+] Suggestions saved → {stealth_out.name}")

    # Optional: auto-write stealth variant
    lines = result.stdout.splitlines()
    stealth_code = "\n".join([
        l for l in lines if l.strip().startswith(("echo", "#", "rm", "touch"))
    ])
    if stealth_code:
        uid = uuid.uuid4().hex[:8]
        new_file = payload.parent / f"mutated_stealth_{uid}.sh"
        new_file.write_text(stealth_code)
        print(f"[✓] New stealth variant → {new_file.name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lanimorph_stealth_upgrade.py <mutated_payload.sh>")
    else:
        main(sys.argv[1])
