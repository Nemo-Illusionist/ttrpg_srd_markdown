#!/usr/bin/env python3
"""
Markdown normalization after PDF extraction.
Mechanical cleanup: ligatures, soft hyphens, spaces, dashes, empty lines.

Usage:
    python3 normalize_markdown.py <file.md>           — normalize in place
    python3 normalize_markdown.py <input.md> <output.md>  — normalize to new file
    python3 normalize_markdown.py <directory>          — normalize all .md in directory

Rules based on .claude/rules/pdf-cleanup.md
"""

import re
import sys
from pathlib import Path
from collections import Counter

stats = Counter()


def normalize(text: str) -> str:
    original = text

    # Ligatures: ﬁ→fi, ﬂ→fl, ﬀ→ff, ﬃ→ffi, ﬄ→ffl
    ligatures = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}
    for lig, repl in ligatures.items():
        count = text.count(lig)
        if count:
            stats["ligatures"] += count
            text = text.replace(lig, repl)

    # Soft hyphens
    count = text.count("\u00AD")
    if count:
        stats["soft_hyphens"] += count
        text = text.replace("\u00AD", "")

    # Double/multiple spaces → single (not in code blocks)
    new_text = re.sub(r"(?<!^)  +(?!$)", " ", text, flags=re.MULTILINE)
    stats["double_spaces"] += len(text) - len(new_text)
    text = new_text

    # Trailing whitespace
    new_text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    stats["trailing_whitespace"] += len(text) - len(new_text)
    text = new_text

    # -- → — (em dash), but not in code blocks or table separators |---|
    def replace_dashes(line):
        if line.strip().startswith("|") and "---" in line:
            return line  # table separator
        if line.strip().startswith("```"):
            return line  # code block marker
        new_line = re.sub(r"(?<!\|)--(?!\||-)", "—", line)
        if new_line != line:
            stats["em_dashes"] += 1
        return new_line

    text = "\n".join(replace_dashes(line) for line in text.split("\n"))

    # " - " in middle of sentence → " — " (but not list markers)
    def replace_space_dash(line):
        if re.match(r"^\s*-\s", line):
            return line  # list item
        if line.strip().startswith("|"):
            return line  # table
        new_line = re.sub(r"(\S) - (\S)", r"\1 — \2", line)
        if new_line != line:
            stats["space_dashes"] += 1
        return new_line

    text = "\n".join(replace_space_dash(line) for line in text.split("\n"))

    # 3+ consecutive empty lines → 2
    new_text = re.sub(r"\n{4,}", "\n\n\n", text)
    if new_text != text:
        stats["excess_empty_lines"] += 1
    text = new_text

    return text


def process_file(filepath: Path, output: Path = None):
    text = filepath.read_text(encoding="utf-8")
    result = normalize(text)

    if output:
        output.write_text(result, encoding="utf-8")
    else:
        filepath.write_text(result, encoding="utf-8")

    changed = text != result
    return changed


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.md|directory> [output.md]")
        sys.exit(1)

    target = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if target.is_dir():
        files = sorted(target.rglob("*.md"))
        changed = 0
        for f in files:
            if process_file(f):
                changed += 1
                print(f"  normalized: {f.name}")
        print(f"\nProcessed {len(files)} files, {changed} changed")
    elif target.is_file():
        process_file(target, output)
        print(f"Normalized: {target}" + (f" → {output}" if output else " (in place)"))
    else:
        print(f"Error: {target} not found")
        sys.exit(1)

    if stats:
        print("Fixes:")
        for key, count in sorted(stats.items()):
            print(f"  {key}: {count}")


if __name__ == "__main__":
    main()
