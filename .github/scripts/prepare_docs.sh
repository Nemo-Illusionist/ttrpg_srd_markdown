#!/usr/bin/env bash
# Единый скрипт подготовки окружения для MkDocs.
# Используется локально и в CI (pages.yml).
#
# Что делает:
#   1. Копирует mkdocs.yml и overrides/ из src/site/ в корень
#   2. Собирает docs/ из src/site/ + src/{game}/{version}/{en,ru}
#
# Использование:
#   bash .github/scripts/prepare_docs.sh          — подготовка
#   bash .github/scripts/prepare_docs.sh --clean   — очистка сгенерированных файлов
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [[ "${1:-}" == "--clean" ]]; then
  rm -rf docs/ site/ mkdocs.yml overrides/
  echo "Cleaned: docs/ site/ mkdocs.yml overrides/"
  exit 0
fi

# 1. MkDocs config и overrides → корень
cp src/site/mkdocs.yml mkdocs.yml
cp -r src/site/overrides overrides

# 2. Site-level файлы (index, assets, robots.txt)
mkdir -p docs/
cp -r src/site/* docs/

# 3. SRD контент → docs/{en,ru}/
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

echo "Ready: mkdocs.yml, overrides/, docs/ prepared from src/"
