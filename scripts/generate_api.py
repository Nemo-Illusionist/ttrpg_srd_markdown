#!/usr/bin/env python3
"""Generate static JSON API from D&D SRD Markdown sources.

Usage:
    python3 scripts/generate_api.py --src-root src/dnd --output-dir site/api
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts dir to path so parsers package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import SOURCES, SKIP_HEADINGS_SPELL, SKIP_HEADINGS_MONSTER
from parsers import parse_spells, parse_monsters, parse_magic_items

SYSTEM = "dnd"
SYSTEM_NAME = "Dungeons & Dragons"

VERSION_NAMES = {"srd52": "SRD 5.2.1", "srd51": "SRD 5.1"}


def resolve_cross_refs(all_data: dict) -> None:
    """Resolve spell name → slug cross-references for monsters and magic items."""
    spell_lookup: dict[tuple[str, str], dict[str, str]] = {}

    for key, entities in all_data.items():
        ver, lang, resource = key
        if resource != "spells":
            continue
        lookup = {}
        for spell in entities:
            lookup[spell["name"].lower()] = spell["slug"]
            if spell.get("name_en"):
                lookup[spell["name_en"].lower()] = spell["slug"]
        spell_lookup[(ver, lang)] = lookup

    for key, entities in all_data.items():
        ver, lang, resource = key
        if resource not in ("monsters", "animals", "magic-items"):
            continue
        lookup = spell_lookup.get((ver, lang), {})
        if not lookup:
            continue
        for entity in entities:
            if "spells" in entity and entity["spells"]:
                resolved = []
                for spell_name in entity["spells"]:
                    slug = lookup.get(spell_name.lower())
                    if slug:
                        resolved.append(slug)
                entity["spells"] = resolved


def write_json(path: Path, data) -> None:
    """Write data as JSON with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_index_html(path: Path, title: str, links: list[dict], breadcrumbs: list[dict] | None = None) -> None:
    """Write an index.html navigation page.

    links: list of {"href": "...", "label": "...", "badge": "..." (optional)}
    breadcrumbs: list of {"href": "...", "label": "..."} for navigation trail
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    bc_html = ""
    if breadcrumbs:
        parts = []
        for bc in breadcrumbs:
            if bc.get("href"):
                parts.append(f'<a href="{bc["href"]}">{bc["label"]}</a>')
            else:
                parts.append(f'<span>{bc["label"]}</span>')
        bc_html = f'<nav class="breadcrumbs">{"&nbsp;/&nbsp;".join(parts)}</nav>'

    items = []
    for link in links:
        badge = f' <span class="badge">{link["badge"]}</span>' if link.get("badge") else ""
        items.append(f'<li><a href="{link["href"]}">{link["label"]}</a>{badge}</li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; background: #fafafa; }}
  h1 {{ font-size: 1.5rem; margin-bottom: .5rem; }}
  .breadcrumbs {{ font-size: .85rem; color: #666; margin-bottom: 1.5rem; }}
  .breadcrumbs a {{ color: #4361ee; text-decoration: none; }}
  .breadcrumbs a:hover {{ text-decoration: underline; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: .4rem 0; }}
  li a {{ color: #4361ee; text-decoration: none; font-size: 1.05rem; }}
  li a:hover {{ text-decoration: underline; }}
  .badge {{ background: #e8eaf6; color: #3949ab; padding: .15rem .5rem; border-radius: .75rem; font-size: .8rem; margin-left: .5rem; }}
  footer {{ margin-top: 2rem; font-size: .75rem; color: #999; }}
</style>
</head>
<body>
{bc_html}
<h1>{title}</h1>
<ul>
{"".join(items)}
</ul>
<footer>TTRPG SRD Markdown &mdash; Static JSON API</footer>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description="Generate D&D SRD JSON API")
    parser.add_argument("--src-root", required=True, help="Root directory of SRD markdown sources")
    parser.add_argument("--output-dir", required=True, help="Output directory for JSON API (e.g. site/api)")
    parser.add_argument("--individual", action="store_true",
                        help="Generate individual {slug}.json files (default: only all.json per resource)")
    args = parser.parse_args()

    src_root = Path(args.src_root)
    output_dir = Path(args.output_dir)

    if not src_root.is_dir():
        print(f"Error: source root '{src_root}' not found", file=sys.stderr)
        sys.exit(1)

    system_dir = output_dir / SYSTEM

    # Parse all sources
    all_data: dict[tuple[str, str, str], list[dict]] = {}
    total_entities = 0

    for source in SOURCES:
        ver = source["ver"]
        lang = source["lang"]
        entity_type = source["type"]
        filepath = src_root / source["file"]
        heading_level = source["h"]
        after = source.get("after")
        out_resource = source.get("out")

        if not filepath.is_file():
            print(f"  Warning: {filepath} not found, skipping", file=sys.stderr)
            continue

        text = filepath.read_text(encoding="utf-8")

        if entity_type == "spell":
            entities = parse_spells(text, heading_level, lang, after, SKIP_HEADINGS_SPELL)
            resource = "spells"
        elif entity_type == "monster":
            entities = parse_monsters(text, heading_level, lang, after, SKIP_HEADINGS_MONSTER)
            resource = out_resource or "monsters"
        elif entity_type == "magic_item":
            entities = parse_magic_items(text, heading_level, lang, after)
            resource = "magic-items"
        else:
            print(f"  Warning: unknown type '{entity_type}', skipping", file=sys.stderr)
            continue

        key = (ver, lang, resource)
        if key in all_data:
            all_data[key].extend(entities)
        else:
            all_data[key] = entities

        count = len(entities)
        total_entities += count
        print(f"  {ver}/{lang}/{resource}: {count} entities from {source['file']}")

    # Resolve cross-references
    resolve_cross_refs(all_data)

    # Write files and collect hierarchy info
    file_count = 0

    # Collectors for hierarchical meta files
    # ver → lang → resource → slugs
    hierarchy: dict[str, dict[str, dict[str, list[str]]]] = {}

    for (ver, lang, resource), entities in sorted(all_data.items()):
        hierarchy.setdefault(ver, {}).setdefault(lang, {})[resource] = []

        slugs = []
        for entity in entities:
            slug = entity["slug"]
            slugs.append(slug)
            if args.individual:
                write_json(system_dir / ver / lang / resource / f"{slug}.json", entity)
                file_count += 1

        slugs.sort()
        hierarchy[ver][lang][resource] = slugs

        # all.json
        write_json(
            system_dir / ver / lang / resource / "all.json",
            sorted(entities, key=lambda e: e["slug"]),
        )
        file_count += 1

    # --- Hierarchical meta.json + index.html files ---

    base_url = "."  # relative links

    # Level 5: /dnd/{ver}/{lang}/{resource}/ — list of slugs
    for ver, langs in sorted(hierarchy.items()):
        for lang, resources in sorted(langs.items()):
            for resource, slugs in sorted(resources.items()):
                res_dir = system_dir / ver / lang / resource
                write_json(res_dir / "meta.json", {
                    "resource": resource,
                    "total": len(slugs),
                    "slugs": slugs,
                })
                file_count += 1

                links = [{"href": "all.json", "label": "all.json", "badge": f"{len(slugs)} items"}]
                if args.individual:
                    for slug in slugs:
                        links.append({"href": f"{slug}.json", "label": slug})
                bc = [
                    {"href": "../../../../", "label": "api"},
                    {"href": "../../../", "label": SYSTEM},
                    {"href": "../../", "label": VERSION_NAMES.get(ver, ver)},
                    {"href": "../", "label": lang},
                    {"href": None, "label": resource},
                ]
                write_index_html(res_dir / "index.html",
                                 f"{resource} — {lang} — {VERSION_NAMES.get(ver, ver)}",
                                 links, bc)
                file_count += 1

    # Level 4: /dnd/{ver}/{lang}/ — available resources
    for ver, langs in sorted(hierarchy.items()):
        for lang, resources in sorted(langs.items()):
            lang_dir = system_dir / ver / lang
            links = []
            for resource, slugs in sorted(resources.items()):
                links.append({"href": f"{resource}/", "label": resource, "badge": str(len(slugs))})

            bc = [
                {"href": "../../../", "label": "api"},
                {"href": "../../", "label": SYSTEM},
                {"href": "../", "label": VERSION_NAMES.get(ver, ver)},
                {"href": None, "label": lang},
            ]
            write_index_html(lang_dir / "index.html",
                             f"{lang} — {VERSION_NAMES.get(ver, ver)}",
                             links, bc)
            file_count += 1

    # Level 3: /dnd/{ver}/ — available languages
    for ver, langs in sorted(hierarchy.items()):
        ver_dir = system_dir / ver
        links = []
        for lang in sorted(langs):
            links.append({"href": f"{lang}/", "label": lang})

        bc = [
            {"href": "../../", "label": "api"},
            {"href": "../", "label": SYSTEM},
            {"href": None, "label": VERSION_NAMES.get(ver, ver)},
        ]
        write_index_html(ver_dir / "index.html",
                         VERSION_NAMES.get(ver, ver),
                         links, bc)
        file_count += 1

    # Level 2: /dnd/ — available versions
    links = []
    for ver in sorted(hierarchy):
        links.append({"href": f"{ver}/", "label": VERSION_NAMES.get(ver, ver)})

    bc = [
        {"href": "../", "label": "api"},
        {"href": None, "label": SYSTEM_NAME},
    ]
    write_index_html(system_dir / "index.html",
                     SYSTEM_NAME,
                     links, bc)
    file_count += 1

    # Level 1: /api/ — available systems
    write_index_html(output_dir / "index.html",
                     "TTRPG SRD API",
                     [{"href": f"{SYSTEM}/", "label": SYSTEM_NAME}])
    file_count += 1

    print(f"\nDone: {file_count} files written ({total_entities} entities)")


if __name__ == "__main__":
    main()
