#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint.

Writes one two-part micro-confession to /output/entry.txt:
a To: line naming who it was meant for, and the unsent message
itself, one line, exactly as typed, with no explanation after it.
Standard library only. The kit harness exports MAKEFUN_OUTPUT_DIR
and reads ``$MAKEFUN_OUTPUT_DIR/entry.txt`` afterwards; that
directory is honoured right after an explicit ENTRY_OUT.
"""

import os
from pathlib import Path

TO_LINE = "To: Maya, my sister's best friend"

MESSAGE = (
    "I still check if you're online before I text anyone else, "
    "and I've deleted this three times because you only ever see "
    "me as her little brother."
)

ENTRY = TO_LINE + "\n" + MESSAGE


def resolve_output_path() -> Path:
    """Return the entry.txt path to write.

    Honours ENTRY_OUT / MAKEFUN_OUTPUT_DIR / ENTRY_OUT_DIR / OUTPUT when
    set, whether they name a file or a directory, and otherwise defaults
    to the competition's /output/entry.txt. MAKEFUN_OUTPUT_DIR is the
    directory the kit harness exports and always names a directory,
    even before it exists.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        path = Path(entry_out)
        if path.suffix == ".txt" or path.is_file():
            return path
        return path / "entry.txt"
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        return Path(makefun_dir) / "entry.txt"
    for var in ("ENTRY_OUT_DIR", "OUTPUT"):
        value = os.environ.get(var)
        if value:
            path = Path(value)
            if path.suffix == ".txt" or path.is_file():
                return path
            return path / "entry.txt"
    return Path("/output/entry.txt")


def main() -> None:
    lines = ENTRY.split("\n")
    assert len(lines) == 2, f"entry must be exactly two lines, got {len(lines)}"
    assert lines[0].startswith("To: "), "first line must be the To: line"
    assert len(lines[1]) <= 200, f"message too long: {len(lines[1])}"
    assert len(ENTRY) <= 260, f"entry too long: {len(ENTRY)}"
    assert ENTRY.strip(), "entry must not be blank"
    assert not ENTRY.endswith("\n"), "no trailing newline after the message"
    out = resolve_output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {len(ENTRY)} characters to {out}")


if __name__ == "__main__":
    main()
