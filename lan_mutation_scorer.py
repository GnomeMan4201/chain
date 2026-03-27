#!/usr/bin/env python3
import os, glob, subprocess
from pathlib import Path
BUNDLES = Path("~/LANIMORPH/bundles/silent").expanduser().glob("*.zip")
for zipf in BUNDLES:
    if (zipf.with_suffix(".score.txt")).exists(): continue
    prompt = f"Rate the stealth and detectability of this payload mutation:\n\n{zipf.name}"
    result = subprocess.getoutput(f"llama-cli -p {prompt!r}").strip()
    with open(zipf.with_suffix(".score.txt"), "w") as out:
        out.write(result + "\n")
