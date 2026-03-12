---
description: "Оркестратор полного пайплайна импорта PDF в markdown. Вызывает convert-pdf, cleanup-artifacts, verify-import, integrate-srd."
user-invocable: true
---

# /import-srd — Полный пайплайн импорта SRD

## Использование

```
/import-srd <pdf_path> <game> <version>
```

Пример: `/import-srd /tmp/brp-srd.pdf brp srd-1.0`

## Пайплайн

Выполняй фазы строго последовательно. Каждая фаза — отдельный skill.

### Phase 0: Создание ветки

1. **Создай ветку импорта:**
   ```bash
   git checkout -b import/{game}-{version}
   ```
   - Если ветка уже существует (продолжение прерванного пайплайна) → переключись на неё: `git checkout import/{game}-{version}`
2. Все коммиты фаз 1-3 идут в эту ветку

```
✓ Phase 0 завершена: ветка import/{game}-{version} создана
```

### Phase 1: Конвертация PDF

```
→ /convert-pdf {pdf_path} {game} {version}
```

Вызови skill `convert-pdf` с аргументами `{pdf_path} {game} {version}`.

Результат: три файла в `/tmp/` — сырой markdown от трёх конвертеров.

После завершения:
```
✓ Phase 1 завершена: PDF конвертирован (marker + pymupdf4llm + docling)
```

### Phase 2: Сведение + разбивка + чистка

```
→ /cleanup-artifacts {game} {version}
```

Вызови skill `cleanup-artifacts` с аргументами `{game} {version}`.

Это включает:
- Сведение лучших частей из трёх конвертеров
- Отчёт о полезности каждого конвертера
- Разбивка на файлы `src/{game}/{version}/en/NN_Name.md`
- Чистка артефактов PDF

После завершения:
```
✓ Phase 2 завершена: файлы созданы и очищены (K файлов)
```

### Phase 3: Верификация полноты

```
→ /verify-import {game} {version}
```

Вызови skill `verify-import` с аргументами `{game} {version}`.

Это включает:
- Автоматическая проверка полноты, структуры, таблиц, форматирования
- Циклические исправления до полной чистоты
- Пауза для ручной проверки пользователем

После завершения:
```
✓ Phase 3 завершена: верификация пройдена (N раундов, M исправлений)
```

### Phase 3.5: Squash merge в main

1. Переключись на main:
   ```bash
   git checkout main
   ```
2. Squash merge ветки импорта:
   ```bash
   git merge --squash import/{game}-{version}
   ```
3. Создай коммит:
   ```
   Импорт {game} {version}: EN markdown из PDF (N файлов)
   ```
4. Удали ветку:
   ```bash
   git branch -d import/{game}-{version}
   ```

```
✓ Phase 3.5 завершена: squash merge в main
```

### Phase 4: Интеграция в сайт

```
→ /integrate-srd {game} {version}
```

Вызови skill `integrate-srd` с аргументами `{game} {version}`.

Это включает:
- `.github/scripts/prepare_docs.sh` — команды копирования
- `.github/workflows/pages.yml` — CI деплой
- `src/site/mkdocs.yml` — навигация + nav_translations
- `.github/workflows/release-{game}.yml` — release workflow
- Релизный тег + push (с подтверждением пользователя)

После завершения:
```
✓ Phase 4 завершена: интеграция в сайт + релиз

Полный пайплайн импорта завершён для {game} {version}:
- Phase 0: Ветка import/{game}-{version} ✓
- Phase 1: Конвертация PDF ✓
- Phase 2: Сведение + разбивка + чистка (K файлов) ✓
- Phase 3: Верификация (N раундов, M исправлений) ✓
- Phase 3.5: Squash merge в main ✓
- Phase 4: Интеграция + релиз ✓
```

## Восстановление после сбоя

Если пайплайн прерван, можно перезапустить с любой фазы, вызвав соответствующий skill напрямую.

**Ветка:** при возобновлении проверь, существует ли ветка `import/{game}-{version}`. Если да — переключись на неё перед продолжением. Если нет (фазы 1-3 не начинались или уже смержены) — создай новую.

- PDF ещё не конвертирован → начни с `/convert-pdf` (Phase 1)
- PDF уже конвертирован (файлы в `/tmp/`) → начни с `/cleanup-artifacts` (Phase 2)
- Файлы созданы, но не проверены → начни с `/verify-import` (Phase 3)
- Всё чисто и проверено → начни с `/integrate-srd` (Phase 4, уже в main)

## Технические требования

- Все агенты во всех фазах — **model: "opus"**
- Фазы 1-3 работают в ветке `import/{game}-{version}`, коммиты по файлам
- Phase 3.5: squash merge в main (один коммит в истории main)
- Phase 4 (интеграция) — уже в main
- Пайплайн останавливается на Phase 3 для ручной проверки
- При ошибке в любой фазе — остановка и отчёт пользователю
- Сообщения коммитов на русском
