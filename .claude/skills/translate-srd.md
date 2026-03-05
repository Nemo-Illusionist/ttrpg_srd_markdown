---
description: "Оркестратор полного пайплайна перевода SRD — от глоссария до интеграции в сайт"
user_invocable: true
---

# /translate-srd — Полный пайплайн перевода SRD

## Использование

```
/translate-srd <game> <version>
```

Пример: `/translate-srd daggerheart srd-1.0`

## Пайплайн

Выполняй фазы строго последовательно. Каждая фаза — отдельный skill.

### Phase 1: Создание EN глоссария

```
→ /build-glossary {game} {version}
```

Вызови skill `build-glossary` с аргументами `{game} {version}`.

После завершения выведи:
```
✓ Phase 1 завершена: EN глоссарий создан
```

### Phase 2: Перевод глоссария

```
→ /translate-glossary {game} {version}
```

Вызови skill `translate-glossary` с аргументами `{game} {version}`.

После завершения:
```
✓ Phase 2 завершена: RU глоссарий создан
```

### Phase 3: Автоверификация глоссария

```
→ /translate-verify {game} {version}
```

Вызови skill `translate-verify` с аргументами `{game} {version}`.

Это включает:
- 3 агента параллельно, минимум 3 раунда
- Автоматические исправления с коммитами

После завершения:
```
✓ Phase 3 завершена: автоверификация пройдена (N раундов, M исправлений)
```

### Phase 4: Ручная проверка (цикл)

`/translate-verify` уже включает AskUserQuestion с циклом ручной проверки.
Этот этап завершается когда пользователь говорит "ОК".

```
✓ Phase 4 завершена: ручная проверка пройдена
```

### Phase 5: Перевод контента

```
→ /translate-content {game} {version}
```

Вызови skill `translate-content` с аргументами `{game} {version}`.

После завершения:
```
✓ Phase 5 завершена: контент переведён (K файлов)
```

### Phase 6: Верификация контента

```
→ /verify-content {game} {version}
```

Вызови skill `verify-content` с аргументами `{game} {version}`.

После завершения:
```
✓ Phase 6 завершена: верификация контента пройдена (N раундов)
```

### Phase 7: Интеграция в сайт

Выполни вручную (без отдельного skill):

#### 7.1 Скрипт prepare_docs.sh

1. Прочитай `scripts/prepare_docs.sh`
2. Добавь cp-команды для нового SRD по образцу существующих:

```bash
# {Game} {Version}
cp -r src/{game}/{version}/en/* docs/en/{game}/{version}/
cp -r src/{game}/{version}/ru/* docs/ru/{game}/{version}/
```

3. Коммит: `Интеграция {game} {version}: prepare_docs.sh`

#### 7.2 GitHub Actions workflow

1. Прочитай `.github/workflows/pages.yml`
2. Добавь в секцию "Copy source files" (по образцу):

```yaml
- name: Copy {game} {version} sources
  run: |
    cp -r src/{game}/{version}/en/* docs/en/{game}/{version}/
    cp -r src/{game}/{version}/ru/* docs/ru/{game}/{version}/
```

3. Коммит: `Интеграция {game} {version}: pages.yml`

#### 7.3 Навигация в mkdocs.yml

1. Прочитай `mkdocs.yml`
2. Добавь навигацию для нового SRD в секцию `nav:`:
   - Определи структуру по файлам в `src/{game}/{version}/ru/`
   - Следуй существующему паттерну навигации
3. Коммит: `Интеграция {game} {version}: навигация mkdocs.yml`

#### 7.4 Финальный отчёт

```
✓ Phase 7 завершена: интеграция в сайт

Полный пайплайн завершён для {game} {version}:
- Phase 1: EN глоссарий ✓
- Phase 2: RU глоссарий ✓
- Phase 3: Автоверификация (N раундов) ✓
- Phase 4: Ручная проверка ✓
- Phase 5: Перевод контента (K файлов) ✓
- Phase 6: Верификация контента ✓
- Phase 7: Интеграция в сайт ✓

Всего коммитов: ~X
```

## Восстановление после сбоя

Если пайплайн прерван, можно перезапустить с любой фазы, вызвав соответствующий skill напрямую:

- Глоссарий уже есть → начни с `/translate-glossary`
- RU глоссарий есть → начни с `/translate-verify`
- Контент не переведён → начни с `/translate-content`
- Контент есть → начни с `/verify-content`

## Технические требования

- Все агенты во всех фазах — **model: "opus"**
- Каждая фаза создаёт свои коммиты
- Пайплайн останавливается на Phase 4 для ручной проверки
- При ошибке в любой фазе — остановка и отчёт пользователю
- Сообщения коммитов на русском
