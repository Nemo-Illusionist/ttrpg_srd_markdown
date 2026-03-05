---
description: "Конвертация PDF в сырой markdown тремя инструментами (marker + pymupdf4llm + docling)"
user-invocable: true
---

# /convert-pdf — Конвертация PDF в markdown

## Использование

```
/convert-pdf <pdf_path> <game> <version>
```

Пример: `/convert-pdf /tmp/brp-srd.pdf brp srd-1.0`

## Алгоритм

### Шаг 1: Проверка зависимостей

Проверь наличие каждого инструмента:

```bash
python3 -c "import marker" 2>/dev/null && echo "marker: OK" || echo "marker: NOT FOUND"
python3 -c "import pymupdf4llm" 2>/dev/null && echo "pymupdf4llm: OK" || echo "pymupdf4llm: NOT FOUND"
python3 -c "import docling" 2>/dev/null && echo "docling: OK" || echo "docling: NOT FOUND"
```

Если что-то отсутствует — предложи установку через AskUserQuestion:

```
Не найдены зависимости: {список}
Установить? pip install marker-pdf pymupdf4llm docling
```

Также проверь что PDF существует: `ls {pdf_path}`

### Шаг 2: Конвертация marker (структура, заголовки)

marker даёт лучшую структуру заголовков и списков. Поддерживает GPU/MPS.

```bash
marker_single "{pdf_path}" --output_dir /tmp/{game}_marker/
```

Найди результирующий `.md` файл в `/tmp/{game}_marker/` и скопируй:

```bash
cp /tmp/{game}_marker/*/*.md /tmp/{game}_marker.md
```

Если `marker_single` не найден как команда, используй:

```bash
python3 -m marker.scripts.single "{pdf_path}" --output_dir /tmp/{game}_marker/
```

### Шаг 3: Конвертация pymupdf4llm (быстрый, хороший текст)

pymupdf4llm — самый быстрый конвертер, даёт чистый текст.

Создай и запусти Python-скрипт:

```python
import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("{pdf_path}")
pathlib.Path("/tmp/{game}_pymupdf.md").write_text(md_text)
print(f"OK: {len(md_text)} chars, {md_text.count(chr(10))} lines")
```

Результат: `/tmp/{game}_pymupdf.md`

### Шаг 4: Конвертация docling (лучшие таблицы)

docling лучше всех обрабатывает таблицы и сложный layout.

```bash
docling "{pdf_path}" --to md --output /tmp/{game}_docling/
```

Найди результирующий `.md` и скопируй:

```bash
cp /tmp/{game}_docling/*.md /tmp/{game}_docling.md
```

Если `docling` CLI не найден, используй Python:

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("{pdf_path}")
md_text = result.document.export_to_markdown()
with open("/tmp/{game}_docling.md", "w") as f:
    f.write(md_text)
print(f"OK: {len(md_text)} chars")
```

### Шаг 5: Статистика

Выведи сводку по всем трём результатам:

```
Конвертация завершена:

| Конвертер   | Строк | Заголовков | Таблиц | Размер  |
|-------------|-------|------------|--------|---------|
| marker      | ...   | ...        | ...    | ... KB  |
| pymupdf4llm | ...   | ...        | ...    | ... KB  |
| docling     | ...   | ...        | ...    | ... KB  |

Файлы:
- /tmp/{game}_marker.md
- /tmp/{game}_pymupdf.md
- /tmp/{game}_docling.md

Следующий шаг: /cleanup-artifacts {game} {version}
```

Подсчёт:
- Строк: `wc -l`
- Заголовков: `grep -c '^#' {file}`
- Таблиц: `grep -c '^\|' {file}` (строки начинающиеся с `|`)

## Обработка ошибок

- Если один из конвертеров не установлен и пользователь отказался — пропусти его, но предупреди что сведение будет менее точным
- Если конвертер падает — сохрани stderr, покажи пользователю, продолжи с остальными
- Минимум 2 из 3 конвертеров должны отработать для продолжения

## Технические требования

- Все результаты в `/tmp/` — коммитов нет
- Все агенты — **model: "opus"**
- PDF может быть большим (100+ страниц) — таймаут 10 минут на каждый конвертер
