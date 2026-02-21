"""Configuration for D&D SRD API generation."""

SOURCES = [
    # SRD 5.2 RU
    {"ver": "srd52", "lang": "ru", "type": "spell",      "file": "srd-5.2/ru/07_Spells.md",       "h": 3},
    {"ver": "srd52", "lang": "ru", "type": "monster",     "file": "srd-5.2/ru/12_MonstersA-Z.md",  "h": 3},
    {"ver": "srd52", "lang": "ru", "type": "magic_item",  "file": "srd-5.2/ru/10_MagicItems.md",   "h": 4, "after": "## Магические предметы от А до Я"},
    {"ver": "srd52", "lang": "ru", "type": "monster",     "file": "srd-5.2/ru/13_Animals.md",      "h": 3, "out": "animals"},
    # SRD 5.2 EN
    {"ver": "srd52", "lang": "en", "type": "spell",      "file": "srd-5.2/en/07_Spells.md",       "h": 3},
    {"ver": "srd52", "lang": "en", "type": "monster",     "file": "srd-5.2/en/12_MonstersA-Z.md",  "h": 3},
    {"ver": "srd52", "lang": "en", "type": "magic_item",  "file": "srd-5.2/en/10_MagicItems.md",   "h": 4, "after": "## Magic Items A\u2013Z"},
    {"ver": "srd52", "lang": "en", "type": "monster",     "file": "srd-5.2/en/13_Animals.md",      "h": 3, "out": "animals"},
    # SRD 5.1 RU
    {"ver": "srd51", "lang": "ru", "type": "spell",      "file": "srd-5.1/ru/10_Spells.md",       "h": 3},
    {"ver": "srd51", "lang": "ru", "type": "monster",     "file": "srd-5.1/ru/15_MonstersA-Z.md",  "h": 3},
    {"ver": "srd51", "lang": "ru", "type": "magic_item",  "file": "srd-5.1/ru/13_MagicItems.md",   "h": 4},
    # SRD 5.1 EN
    {"ver": "srd51", "lang": "en", "type": "spell",      "file": "srd-5.1/en/10_Spells.md",       "h": 3},
    {"ver": "srd51", "lang": "en", "type": "monster",     "file": "srd-5.1/en/15_MonstersA-Z.md",  "h": 3},
    {"ver": "srd51", "lang": "en", "type": "magic_item",  "file": "srd-5.1/en/13_MagicItems.md",   "h": 4},
]

# Heading patterns that are NOT entity entries (section headers, rules text, etc.)
# Used to filter out non-entity headings from spell/monster/magic_item files.
SKIP_HEADINGS_SPELL = {
    # EN SRD 5.2
    "Preparing Spells", "Always-Prepared Spells", "Spell Level",
    "School of Magic", "Class Spell Lists", "Casting Time", "Range",
    "Components", "Duration", "Effects", "Gaining Spells",
    # EN SRD 5.1
    "Spell Level", "Known and Prepared Spells", "Spell Slots",
    "Casting Time", "Spell Range", "Components", "Duration",
    "Targets", "Areas of Effect", "Spell Saving Throws",
    "Spell Attack Rolls", "Combining Magical Effects",
    # RU SRD 5.2
    "Подготовка заклинаний", "Всегда подготовленные заклинания",
    "Уровень заклинания", "Школа магии", "Списки заклинаний классов",
    "Время сотворения", "Дистанция", "Компоненты", "Длительность",
    "Эффекты", "Получение заклинаний",
    # RU SRD 5.1
    "Уровень заклинания", "Известные и подготовленные заклинания",
    "Ячейки заклинаний", "Время накладывания", "Дистанция заклинания",
    "Компоненты", "Длительность", "Цели", "Области воздействия",
    "Спасброски от заклинаний", "Броски атаки заклинаниями",
    "Комбинирование магических эффектов",
}

SKIP_HEADINGS_MONSTER = {
    "Customizing NPCs", "Настройка НИП",
}

# Resource type to output directory name mapping
RESOURCE_DIR = {
    "spell": "spells",
    "monster": "monsters",
    "magic_item": "magic-items",
}
