#!/usr/bin/env bash
# Prepare docs/ from src/ for local mkdocs serve/build.
# Mirrors the CI copy logic from .github/workflows/pages.yml.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# MkDocs config and overrides
cp .github/mkdocs.yml mkdocs.yml
cp -r .github/overrides overrides

# Site-level files (index pages, assets, robots.txt)
mkdir -p docs/
cp -r src/site/* docs/

# D&D SRD 5.2
mkdir -p docs/ru/dnd/srd-5.2/03_Classes docs/ru/dnd/srd-5.2/14_Glossary
mkdir -p docs/en/dnd/srd-5.2/03_Classes docs/en/dnd/srd-5.2/14_Glossary
cp -r src/dnd/srd-5.2/ru/* docs/ru/dnd/srd-5.2/
cp -r src/dnd/srd-5.2/en/* docs/en/dnd/srd-5.2/

# D&D SRD 5.1
mkdir -p docs/en/dnd/srd-5.1/06_Classes docs/en/dnd/srd-5.1/16_Glossary
mkdir -p docs/ru/dnd/srd-5.1/06_Classes docs/ru/dnd/srd-5.1/16_Glossary
cp -r src/dnd/srd-5.1/en/* docs/en/dnd/srd-5.1/
cp -r src/dnd/srd-5.1/ru/* docs/ru/dnd/srd-5.1/

# D&D Converting guide
mkdir -p docs/en/dnd/converting-srd-5.2 docs/ru/dnd/converting-srd-5.2
cp src/dnd/converting-srd-5.2/en/* docs/en/dnd/converting-srd-5.2/
cp src/dnd/converting-srd-5.2/ru/* docs/ru/dnd/converting-srd-5.2/

# Daggerheart SRD 1.0
mkdir -p docs/en/daggerheart/srd-1.0/04_Classes docs/en/daggerheart/srd-1.0/17_Glossary
mkdir -p docs/ru/daggerheart/srd-1.0/04_Classes docs/ru/daggerheart/srd-1.0/17_Glossary
cp -r src/daggerheart/srd-1.0/en/* docs/en/daggerheart/srd-1.0/
cp -r src/daggerheart/srd-1.0/ru/* docs/ru/daggerheart/srd-1.0/

# BRP SRD 1.0
mkdir -p docs/en/brp/srd-1.0/09_Glossary docs/ru/brp/srd-1.0/09_Glossary
cp -r src/brp/srd-1.0/en/* docs/en/brp/srd-1.0/
cp -r src/brp/srd-1.0/ru/* docs/ru/brp/srd-1.0/

echo "docs/ prepared from src/"
