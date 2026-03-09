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

Конвертеры устанавливаются в **отдельные venv** (конфликт зависимостей между marker и docling):

```bash
# Проверка существующих venv
for tool in marker pymupdf docling; do
  venv="/tmp/venv-${tool}"
  if [ -d "$venv" ]; then echo "${tool}: OK (${venv})"; else echo "${tool}: NOT FOUND"; fi
done
```

Если отсутствуют — создать venv и установить (можно параллельно):

```bash
# Каждый в свой venv — обязательно, pip install без venv не работает (PEP 668)
python3 -m venv /tmp/venv-marker && /tmp/venv-marker/bin/pip install marker-pdf
python3 -m venv /tmp/venv-pymupdf && /tmp/venv-pymupdf/bin/pip install pymupdf4llm
python3 -m venv /tmp/venv-docling && /tmp/venv-docling/bin/pip install docling
```

Также проверь что PDF существует: `ls {pdf_path}`

### Шаг 2: Конвертация marker (структура, заголовки)

marker даёт лучшую структуру заголовков и списков. Поддерживает GPU/MPS.

**Важно:** На macOS MPS marker может падать с `torch.AcceleratorError` при layout detection.
Решение — переменная окружения для управления памятью MPS + отключение OCR (для цифровых PDF не нужен):

```bash
mkdir -p /tmp/{game}_marker && \
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 \
/tmp/venv-marker/bin/marker_single "{pdf_path}" \
  --output_dir /tmp/{game}_marker/ \
  --disable_ocr \
  --disable_image_extraction
```

Если всё равно падает — попробовать на CPU:

```bash
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 PYTORCH_ENABLE_MPS_FALLBACK=1 \
/tmp/venv-marker/bin/marker_single "{pdf_path}" \
  --output_dir /tmp/{game}_marker/ \
  --disable_ocr \
  --disable_image_extraction \
  --lowres_image_dpi 72
```

Найди результирующий `.md` файл в `/tmp/{game}_marker/` и скопируй:

```bash
cp /tmp/{game}_marker/*/*.md /tmp/{game}_marker.md
```

### Шаг 3: Конвертация pymupdf4llm (быстрый, хороший текст)

pymupdf4llm — самый быстрый конвертер, даёт чистый текст.

```bash
/tmp/venv-pymupdf/bin/python3 -c "
import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown('${pdf_path}')
pathlib.Path('/tmp/${game}_pymupdf.md').write_text(md_text)
print(f'OK: {len(md_text)} chars, {md_text.count(chr(10))} lines')
"
```

Результат: `/tmp/{game}_pymupdf.md`

### Шаг 4: Конвертация docling (лучшие таблицы)

docling лучше всех обрабатывает таблицы и сложный layout.

```bash
/tmp/venv-docling/bin/docling "{pdf_path}" --to md --output /tmp/{game}_docling/
cp /tmp/{game}_docling/*.md /tmp/{game}_docling.md
```

Альтернативный способ — через Python API (CLI может быть не в PATH):

```bash
/tmp/venv-docling/bin/python3 -c "
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert('${pdf_path}')
md_text = result.document.export_to_markdown()
with open('/tmp/${game}_docling.md', 'w') as f:
    f.write(md_text)
print(f'OK: {len(md_text)} chars, {md_text.count(chr(10))} lines')
"
```

**Примечание:** docling — самый медленный конвертер (30-60 мин на 400 стр.), но лучший для таблиц.

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
