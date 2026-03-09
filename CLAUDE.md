# TTRPG SRD — импорт и перевод

Проект для импорта, перевода и публикации SRD (System Reference Document) настольных ролевых игр.

## Структура проекта

```
src/{game}/{version}/en/       — EN оригинал (markdown)
src/{game}/{version}/ru/       — RU перевод
src/{game}/{version}/ru/*_Glossary/  — глоссарий (словарь терминов)
src/{game}/translate/          — словари и логи (logs/, 01_dictionary_base, ...)
src/translate/                 — общие переводческие артефакты (все системы)
src/site/                      — исходники сайта (index, assets, mkdocs.yml, overrides)
.github/scripts/               — скрипты сборки и генерации
.github/workflows/             — CI/CD workflows

{version} — идентификатор документа, не обязательно версия: srd-5.2, srd-1.0, kobold-toe и т.д.
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

### Утилиты

| Команда | Описание |
|---|---|
| `/validate-markdown` | Валидация структуры markdown: таблицы, заголовки, списки, форматирование, парная проверка EN↔RU |

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
| `translation-style.md` | Стиль перевода TTRPG-правил + конкретные антипаттерны с примерами | `src/**/ru/**`, translate-content/glossary |
| `translation-validation.md` | Чеклист валидации перевода (структура, термины, оформление) | `src/**/ru/**`, translate-*/verify-content |
| `translation-quality-review.md` | Системный промт агента качества (жёсткая редакторская проверка) | `src/**/ru/**`, translate-verify/verify-content |
| `translate-dictionaries.md` | Структура и формат словарей `translate/`, приоритет источников | `src/*/translate/**`, translate-*/verify-content |
| `terminology-propagation.md` | Пропагация терминологических изменений, conflict resolution, verify loop | `src/**/ru/**`, `src/*/translate/**`, translate-*/verify-content |

### Общие

| Правило | Описание | Подключается к |
|---|---|---|
| `quality-gates.md` | Блокирующие условия по этапам (error/warning/note) | Все pipeline-скиллы, validate-markdown |

## Пайплайн импорта

Оркестратор: `/import-srd` — все фазы последовательно.

```
Phase 0:   Создание ветки import/{game}-{version}
Phase 1:   /convert-pdf        — PDF → 3 markdown в /tmp/
Phase 2:   /cleanup-artifacts  — сведение + разбивка + чистка → src/{game}/{version}/en/
Phase 3:   /verify-import      — циклическая верификация + ручная проверка
Phase 3.5: Squash merge в main
Phase 4:   /integrate-srd      — интеграция в сайт (уже в main)
```

## Пайплайн перевода

Оркестратор: `/translate-srd` — все фазы последовательно.

```
Phase 0:   Проверка EN + создание ветки translate/{game}-{version}
Phase 0.5: Загрузка reference-глоссариев (кросс-версионная согласованность)
Phase 1:   /build-glossary     — EN глоссарий из исходников
Phase 2:   /translate-glossary — RU глоссарий + словари translate/
Phase 3:   /translate-verify   — верификация глоссария (3 агента, 3+ раундов)
Phase 4:   Ручная проверка глоссария
Phase 5:   /translate-content  — перевод контента по словарю
Phase 6:   /verify-content     — верификация контента (3 агента, 3+ раундов)
Phase 7:   Ручная проверка контента
Phase 7.5: Squash merge в main
Phase 8:   /integrate-srd      — интеграция в сайт (уже в main)
```

## Сборка сайта

Сайт собирается копированием — исходники из `src/` копируются в `docs/` и корень:

```bash
bash .github/scripts/prepare_docs.sh   # подготовка
mkdocs serve                            # локальный сервер
mkdocs build                            # билд в site/
bash .github/scripts/prepare_docs.sh --clean  # очистка
```

Скрипт: `src/site/mkdocs.yml` и `overrides/` → корень, `src/` → `docs/{en,ru}/`.
CI (`pages.yml`) вызывает тот же скрипт.

## Терминологические решения

Спорные переводческие решения и их обоснования:
- `src/{game}/translate/logs/{date}_log.md` — решения для конкретной системы
- `src/translate/logs/{date}_log.md` — общие решения (все системы)

Словари фиксируют **что** переводить как, логи — **когда и почему**.
При изменении термина — `.claude/rules/terminology-propagation.md`.

## Технические детали

- Все агенты используют **model: "opus"**
- Большие файлы (>3000 строк) — чанками через offset/limit
- Коммиты после каждого файла, сообщения на русском
- Сайт: MkDocs Material + mkdocs-static-i18n + mkdocs-minify-plugin
- Теги: `{short}-srd-v*` (dnd→`dnd-srd-v*`, daggerheart→`dh-srd-v*`, brp→`brp-srd-v*`)
