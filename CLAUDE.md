# TTRPG SRD — импорт и перевод

Проект для импорта, перевода и публикации SRD (System Reference Document) настольных ролевых игр.

## Структура проекта

```
src/{game}/{version}/en/       — EN оригинал (markdown)
src/{game}/{version}/ru/       — RU перевод
src/{game}/{version}/ru/*_Glossary/  — глоссарий (словарь терминов)
src/site/                      — исходники сайта (index, assets, mkdocs.yml, overrides)
.github/scripts/               — скрипты сборки и генерации
.github/workflows/             — CI/CD workflows
```

При сборке (`prepare_docs.sh` или CI) `mkdocs.yml` и `overrides/` копируются из `src/site/` в корень.

Игры: `dnd` (D&D 5.1, 5.2), `daggerheart` (SRD 1.0), `brp` (BRP SRD 1.0).

## Скиллы (slash-команды)

### Импорт PDF → markdown

| Команда | Описание |
|---|---|
| `/import-srd` | Оркестратор полного пайплайна: convert → cleanup → verify → integrate |
| `/convert-pdf` | Конвертация PDF тремя инструментами (marker + pymupdf4llm + docling) |
| `/cleanup-artifacts` | Сведение результатов конвертеров + разбивка на файлы + чистка артефактов |
| `/verify-import` | Верификация полноты импорта — циклическая сверка markdown с PDF |

### Перевод EN → RU

| Команда | Описание |
|---|---|
| `/translate-srd` | Оркестратор полного пайплайна: глоссарий → перевод → верификация → интеграция |
| `/build-glossary` | Создание EN глоссария из исходников SRD |
| `/translate-glossary` | Перевод EN глоссария в RU (с сохранением оригинальных EN имён) |
| `/translate-verify` | Верификация RU глоссария командой из 3 агентов (минимум 3 раунда) |
| `/translate-content` | Перевод контентных файлов строго по глоссарию |
| `/verify-content` | Верификация перевода: весь перевод (3 агента) или одна страница (1 агент) |

### Интеграция в сайт

| Команда | Описание |
|---|---|
| `/integrate-srd` | Интеграция: prepare_docs.sh, pages.yml, mkdocs.yml nav, release workflow + tag |

## Правила (rules)

Автоматически подключаются по `paths:` при работе с соответствующими файлами.

### Импорт

| Правило | Описание | Подключается к |
|---|---|---|
| `file-naming-conventions.md` | Соглашения об именовании файлов и директорий | `src/**`, cleanup/build/integrate скиллы |
| `glossary-format.md` | Формат таблиц глоссария | `src/**/*_Glossary/**`, build/translate-glossary |
| `layout-recovery.md` | Восстановление структуры документа из PDF | cleanup-artifacts |
| `merge-extraction.md` | Сведение результатов PDF-конвертеров | cleanup-artifacts |
| `pdf-cleanup.md` | Нормализация markdown после конвертации | cleanup-artifacts, `src/**/en/**` |
| `verify-import.md` | Правила верификации импорта | verify-import, `src/**/en/**` |

### Перевод

| Правило | Описание | Подключается к |
|---|---|---|
| `translation-style.md` | Стиль перевода TTRPG-правил (как переводить) | `src/**/ru/**`, translate-content/glossary |
| `translation-validation.md` | Чеклист валидации перевода (структура, термины, оформление) | `src/**/ru/**`, translate-*/verify-content |
| `translation-quality-review.md` | Системный промт агента качества (жёсткая редакторская проверка) | `src/**/ru/**`, translate-verify/verify-content |

## Пайплайн импорта

```
PDF → /convert-pdf → /cleanup-artifacts → /verify-import → /integrate-srd
```

## Пайплайн перевода

```
/build-glossary → /translate-glossary → /translate-verify → /translate-content → /verify-content → /integrate-srd
```

Или одной командой: `/translate-srd` (фазы 0-8).

## Технические детали

- Все агенты используют **model: "opus"**
- Большие файлы (>3000 строк) — чанками через offset/limit
- Коммиты после каждого файла, сообщения на русском
- Сайт: MkDocs Material + mkdocs-static-i18n + mkdocs-minify-plugin
- Теги: `{short}-srd-v*` (dnd→`dnd-srd-v*`, daggerheart→`dh-srd-v*`, brp→`brp-srd-v*`)
