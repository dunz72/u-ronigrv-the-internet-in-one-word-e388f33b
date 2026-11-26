"""The Internet in One Word — entry writer (stdlib only).

Writes the single entry word directly to $MAKEFUN_OUTPUT_DIR/entry.txt.
The word is embedded in this file on purpose: main.py never reads
entry.txt from the repo, so the entry survives even if a repo created
through a web UI drops entry.txt.
"""

import hashlib
import os
import sys
from pathlib import Path

WORD = "tabsoup"


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    # Validate: the entry must be exactly one word — no spaces, no newlines.
    if not WORD or any(ch.isspace() for ch in WORD):
        print("error: WORD must be a single word with no whitespace", file=sys.stderr)
        return 1

    data = WORD.encode("utf-8")

    out_dir = Path(output_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.txt"
        out_path.write_bytes(data)
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out_path} ({len(data)} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
