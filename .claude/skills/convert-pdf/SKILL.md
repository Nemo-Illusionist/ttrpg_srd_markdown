---
description: "Конвертация PDF в сырой markdown тремя инструментами (marker + pymupdf4llm + docling). Используй при импорте нового SRD из PDF."
user-invocable: true
---

# /convert-pdf — Конвертация PDF в markdown

## Использование

```
/convert-pdf <pdf_path> <game> <version>
```

Пример: `/convert-pdf /tmp/brp-srd.pdf brp srd-1.0`

## Алгоритм

### Основной способ — скрипт

Скрипт `.claude/skills/convert-pdf/convert_pdf.py` автоматически:
- Проверяет/создаёт venv для каждого конвертера
- Запускает все три конвертера последовательно с правильными параметрами
- Обрабатывает ошибки (marker fallback MPS→CPU, таймауты)
- Выводит статистику и сохраняет сводку в JSON

```bash
python3 .claude/skills/convert-pdf/convert_pdf.py "{pdf_path}" "{game}"
```

Результат:
- `/tmp/{game}_marker.md` — marker (лучшие заголовки и структура)
- `/tmp/{game}_pymupdf.md` — pymupdf4llm (быстрый, чистый текст)
- `/tmp/{game}_docling.md` — docling (лучшие таблицы)
- `/tmp/{game}_convert_summary.json` — машиночитаемая сводка

### Ручной запуск отдельных конвертеров

Если скрипт не подходит (например, нужен только один конвертер или кастомные параметры):

#### marker (структура, заголовки)

```bash
mkdir -p /tmp/{game}_marker && \
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 \
/tmp/venv-marker/bin/marker_single "{pdf_path}" \
  --output_dir /tmp/{game}_marker/ \
  --disable_ocr \
  --disable_image_extraction
cp /tmp/{game}_marker/*/*.md /tmp/{game}_marker.md
```

Fallback на CPU (если MPS падает с `torch.AcceleratorError`):

```bash
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 PYTORCH_ENABLE_MPS_FALLBACK=1 \
/tmp/venv-marker/bin/marker_single "{pdf_path}" \
  --output_dir /tmp/{game}_marker/ \
  --disable_ocr --disable_image_extraction --lowres_image_dpi 72
```

#### pymupdf4llm (быстрый текст)

```bash
/tmp/venv-pymupdf/bin/python3 -c "
import pymupdf4llm, pathlib
md = pymupdf4llm.to_markdown('${pdf_path}')
pathlib.Path('/tmp/${game}_pymupdf.md').write_text(md)
print(f'OK: {len(md)} chars, {md.count(chr(10))} lines')
"
```

#### docling (таблицы, 30-60 мин на 400 стр.)

```bash
/tmp/venv-docling/bin/python3 -c "
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('${pdf_path}')
md = result.document.export_to_markdown()
open('/tmp/${game}_docling.md', 'w').write(md)
print(f'OK: {len(md)} chars, {md.count(chr(10))} lines')
"
```

### Установка venv (если не установлены)

Каждый конвертер в свой venv — обязательно (PEP 668 + конфликт зависимостей marker↔docling):

```bash
python3 -m venv /tmp/venv-marker && /tmp/venv-marker/bin/pip install marker-pdf
python3 -m venv /tmp/venv-pymupdf && /tmp/venv-pymupdf/bin/pip install pymupdf4llm
python3 -m venv /tmp/venv-docling && /tmp/venv-docling/bin/pip install docling
```

Можно запускать параллельно — они независимы.

## Сильные и слабые стороны конвертеров

| Конвертер | Хорош для | Слаб в | Скорость |
|-----------|-----------|--------|----------|
| marker | Заголовки (уровни `#`), общая структура, таблицы | Может падать на MPS | ~50 мин / 400 стр. |
| pymupdf4llm | Чистый текст абзацев, скорость | Таблицы (0 форматированных), разрывы строк | ~1 мин / 400 стр. |
| docling | Таблицы (структура `\|`), сложный layout | Заголовки (плоская иерархия), скорость | ~40 мин / 400 стр. |

## Обработка ошибок

- Конвертер не установлен и пользователь отказался → пропустить, предупредить
- Конвертер падает → сохранить stderr, показать пользователю, продолжить с остальными
- **Минимум 2 из 3** конвертеров должны отработать для продолжения
- Пустой выходной файл → считать как ошибку

## Технические требования

- Все результаты в `/tmp/` — коммитов нет
- PDF может быть большим (100+ страниц)
- Таймауты: marker 10 мин (+ 10 мин CPU fallback), pymupdf 5 мин, docling 60 мин
