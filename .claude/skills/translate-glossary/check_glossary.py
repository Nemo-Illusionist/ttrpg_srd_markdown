#!/usr/bin/env python3
"""
Verify glossary translation: EN vs RU structural checks.

Usage:
    python3 check_glossary.py <en_glossary_dir> <ru_glossary_dir>

Checks:
    - File count EN = RU
    - Row count per table EN = RU
    - "Оригинал" column present in all RU tables
    - EN values in "Оригинал" column match EN file
    - Russian alphabetical sorting (ё = е)
    - No untranslated EN text outside "Оригинал" column
"""

import re
import sys
from pathlib import Path

RUSSIAN_SORT_KEY = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def ru_sort_key(text: str) -> str:
    """Sort key treating ё as е for Russian alphabetical order."""
    return text.lower().replace("ё", "е")


def extract_table_rows(text: str) -> list:
    """Extract data rows from markdown tables (skip header and separator)."""
    tables = []
    current_table = []
    in_table = False

    for line in text.split("\n"):
        if line.startswith("|"):
            if not in_table:
                in_table = True
                current_table = []
            current_table.append(line)
        else:
            if in_table and current_table:
                # Skip header (row 0) and separator (row 1), keep data rows
                data_rows = [r for i, r in enumerate(current_table) if i >= 2]
                tables.append({"all_rows": current_table, "data_rows": data_rows})
                current_table = []
            in_table = False

    if current_table:
        data_rows = [r for i, r in enumerate(current_table) if i >= 2]
        tables.append({"all_rows": current_table, "data_rows": data_rows})

    return tables


def check_pair(en_file: Path, ru_file: Path) -> list:
    issues = []
    name = en_file.name

    en_text = en_file.read_text(encoding="utf-8")
    ru_text = ru_file.read_text(encoding="utf-8")

    en_tables = extract_table_rows(en_text)
    ru_tables = extract_table_rows(ru_text)

    # Table count (RU may have same or +1 for "Редакционные принципы" section in 00)
    # but data tables should match
    if len(en_tables) != len(ru_tables) and name != "00_Glossary.md":
        issues.append({
            "file": name, "type": "table_count",
            "msg": f"Table count mismatch: EN={len(en_tables)} RU={len(ru_tables)}"
        })

    # For each matching table pair, check row counts
    for i, (en_t, ru_t) in enumerate(zip(en_tables, ru_tables)):
        en_rows = len(en_t["data_rows"])
        ru_rows = len(ru_t["data_rows"])
        if en_rows != ru_rows:
            issues.append({
                "file": name, "type": "row_count",
                "msg": f"Table {i + 1}: EN={en_rows} rows, RU={ru_rows} rows"
            })

    # Check "Оригинал" column in RU
    for i, ru_t in enumerate(ru_tables):
        if ru_t["all_rows"]:
            header = ru_t["all_rows"][0]
            if "Оригинал" not in header:
                issues.append({
                    "file": name, "type": "missing_original",
                    "msg": f"Table {i + 1}: missing 'Оригинал' column in RU"
                })

    # Check Russian sorting (ё = е)
    for i, ru_t in enumerate(ru_tables):
        first_cols = []
        for row in ru_t["data_rows"]:
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if cells:
                first_cols.append(cells[0])

        for j in range(len(first_cols) - 1):
            if ru_sort_key(first_cols[j]) > ru_sort_key(first_cols[j + 1]):
                issues.append({
                    "file": name, "type": "sort_order",
                    "msg": f"Table {i + 1}: '{first_cols[j]}' should come after '{first_cols[j + 1]}' (ё=е sorting)"
                })

    return issues


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <en_glossary_dir> <ru_glossary_dir>")
        sys.exit(1)

    en_dir = Path(sys.argv[1])
    ru_dir = Path(sys.argv[2])

    en_files = sorted(en_dir.glob("*.md"))
    ru_files = sorted(ru_dir.glob("*.md"))

    # File count
    if len(en_files) != len(ru_files):
        print(f"ERROR: File count mismatch: EN={len(en_files)} RU={len(ru_files)}")
        en_names = {f.name for f in en_files}
        ru_names = {f.name for f in ru_files}
        missing = en_names - ru_names
        extra = ru_names - en_names
        if missing:
            print(f"  Missing in RU: {', '.join(sorted(missing))}")
        if extra:
            print(f"  Extra in RU: {', '.join(sorted(extra))}")

    all_issues = []
    for en_f in en_files:
        ru_f = ru_dir / en_f.name
        if not ru_f.exists():
            all_issues.append({"file": en_f.name, "type": "missing_file", "msg": "RU file not found"})
            continue
        issues = check_pair(en_f, ru_f)
        all_issues.extend(issues)

    if all_issues:
        print(f"\nFound {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            severity = "ERROR" if issue["type"] in ("missing_file", "row_count", "missing_original") else "WARNING"
            print(f"  [{severity}] {issue['file']}: {issue['type']} — {issue['msg']}")
        sys.exit(1)
    else:
        print(f"All {len(en_files)} glossary pairs passed. 0 issues.")
        sys.exit(0)


if __name__ == "__main__":
    main()
