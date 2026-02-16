#!/usr/bin/env python3
"""
Группировка монстров в 12_MonstersA-Z.md по тематическим и буквенным секциям.

Аналогично group_animals.py:
1. Читает файл, парсит H1 + H2-блоки (монстры)
2. Понижает заголовки: ## → ###, ### → ####
3. Распределяет монстров в тематические группы или буквенные секции
4. Сортирует внутри каждого H2 по алфавиту
5. Сортирует H2: алфавитно, буквенная перед тематической при равенстве
6. Записывает результат
"""

import re
import sys
from pathlib import Path

# === Тематические группы: EN ===
EN_GROUPS = {
    "Angels": [
        "Deva", "Planetar", "Solar",
    ],
    "Animated Objects": [
        "Animated Armor", "Animated Flying Sword", "Animated Rug of Smothering",
    ],
    "Awakened Plants": [
        "Awakened Shrub", "Awakened Tree",
    ],
    "Bandits": [
        "Bandit", "Bandit Captain",
    ],
    "Bugbears": [
        "Bugbear Stalker", "Bugbear Warrior",
    ],
    "Cultists": [
        "Cultist", "Cultist Fanatic",
    ],
    "Demons": [
        "Balor", "Dretch", "Glabrezu", "Hezrou", "Marilith", "Nalfeshnee", "Quasit", "Vrock",
    ],
    "Devils": [
        "Barbed Devil", "Bearded Devil", "Bone Devil", "Chain Devil", "Erinyes",
        "Horned Devil", "Ice Devil", "Imp", "Lemure", "Pit Fiend",
    ],
    "Dragons": [
        "Adult Black Dragon", "Adult Blue Dragon", "Adult Brass Dragon", "Adult Bronze Dragon",
        "Adult Copper Dragon", "Adult Gold Dragon", "Adult Green Dragon", "Adult Red Dragon",
        "Adult Silver Dragon", "Adult White Dragon",
        "Ancient Black Dragon", "Ancient Blue Dragon", "Ancient Brass Dragon", "Ancient Bronze Dragon",
        "Ancient Copper Dragon", "Ancient Gold Dragon", "Ancient Green Dragon", "Ancient Red Dragon",
        "Ancient Silver Dragon", "Ancient White Dragon",
        "Young Black Dragon", "Young Blue Dragon", "Young Brass Dragon", "Young Bronze Dragon",
        "Young Copper Dragon", "Young Gold Dragon", "Young Green Dragon", "Young Red Dragon",
        "Young Silver Dragon", "Young White Dragon",
        "Black Dragon Wyrmling", "Blue Dragon Wyrmling", "Brass Dragon Wyrmling",
        "Bronze Dragon Wyrmling", "Copper Dragon Wyrmling", "Gold Dragon Wyrmling",
        "Green Dragon Wyrmling", "Red Dragon Wyrmling", "Silver Dragon Wyrmling",
        "White Dragon Wyrmling",
    ],
    "Elementals": [
        "Air Elemental", "Earth Elemental", "Fire Elemental", "Water Elemental",
    ],
    "Fungi": [
        "Shrieker Fungus", "Violet Fungus",
    ],
    "Giants": [
        "Cloud Giant", "Fire Giant", "Frost Giant", "Hill Giant", "Stone Giant", "Storm Giant",
    ],
    "Goblins": [
        "Goblin Boss", "Goblin Minion", "Goblin Warrior",
    ],
    "Golems": [
        "Clay Golem", "Flesh Golem", "Iron Golem", "Stone Golem",
    ],
    "Guards": [
        "Guard", "Guard Captain",
    ],
    "Hags": [
        "Green Hag", "Night Hag", "Sea Hag",
    ],
    "Hobgoblins": [
        "Hobgoblin Captain", "Hobgoblin Warrior",
    ],
    "Lycanthropes": [
        "Werebear", "Wereboar", "Wererat", "Weretiger", "Werewolf",
    ],
    "Mages": [
        "Archmage", "Druid", "Mage",
    ],
    "Mephits": [
        "Dust Mephit", "Ice Mephit", "Magma Mephit", "Steam Mephit",
    ],
    "Mummies": [
        "Mummy", "Mummy Lord",
    ],
    "Nagas": [
        "Guardian Naga", "Spirit Naga",
    ],
    "Oozes": [
        "Black Pudding", "Gelatinous Cube", "Gray Ooze", "Ochre Jelly",
    ],
    "Pirates": [
        "Pirate", "Pirate Captain",
    ],
    "Priests": [
        "Priest", "Priest Acolyte",
    ],
    "Skeletons": [
        "Minotaur Skeleton", "Skeleton", "Warhorse Skeleton",
    ],
    "Sphinxes": [
        "Sphinx of Lore", "Sphinx of Valor", "Sphinx of Wonder",
    ],
    "Thugs": [
        "Tough", "Tough Boss",
    ],
    "Trolls": [
        "Troll", "Troll Limb",
    ],
    "Vampires": [
        "Vampire", "Vampire Familiar", "Vampire Spawn",
    ],
    "Warriors": [
        "Berserker", "Gladiator", "Knight", "Warrior Infantry", "Warrior Veteran",
    ],
    "Zombies": [
        "Ogre Zombie", "Zombie",
    ],
}

# === Тематические группы: RU ===
RU_GROUPS = {
    "Ангелы": [
        "Дэва", "Планетар", "Солар",
    ],
    "Оживлённые предметы": [
        "Оживлённый доспех", "Оживлённый ковёр-душитель", "Оживлённый летающий меч",
    ],
    "Пробуждённые растения": [
        "Пробуждённое дерево", "Пробуждённый куст",
    ],
    "Бандиты": [
        "Бандит", "Капитан бандитов",
    ],
    "Багбиры": [
        "Багбир-охотник", "Багбир-воин",
    ],
    "Культисты": [
        "Культист", "Фанатик-культист",
    ],
    "Демоны": [
        "Балор", "Врок", "Глабрезу", "Дретч", "Квазит", "Марилит", "Налфешни", "Хезроу",
    ],
    "Дьяволы": [
        "Бородатый дьявол", "Имп", "Костяной дьявол", "Ледяной дьявол", "Лемур",
        "Рогатый дьявол", "Цепной дьявол", "Шипастый дьявол", "Эриния", "Ямный дьявол",
    ],
    "Драконы": [
        "Взрослый чёрный дракон", "Взрослый синий дракон", "Взрослый латунный дракон",
        "Взрослый бронзовый дракон", "Взрослый медный дракон", "Взрослый золотой дракон",
        "Взрослый зелёный дракон", "Взрослый красный дракон", "Взрослый серебряный дракон",
        "Взрослый белый дракон",
        "Древний чёрный дракон", "Древний синий дракон", "Древний латунный дракон",
        "Древний бронзовый дракон", "Древний медный дракон", "Древний золотой дракон",
        "Древний зелёный дракон", "Древний красный дракон", "Древний серебряный дракон",
        "Древний белый дракон",
        "Молодой чёрный дракон", "Молодой синий дракон", "Молодой латунный дракон",
        "Молодой бронзовый дракон", "Молодой медный дракон", "Молодой золотой дракон",
        "Молодой зелёный дракон", "Молодой красный дракон", "Молодой серебряный дракон",
        "Молодой белый дракон",
        "Детёныш чёрного дракона", "Детёныш синего дракона", "Детёныш латунного дракона",
        "Детёныш бронзового дракона", "Детёныш медного дракона", "Детёныш золотого дракона",
        "Детёныш зелёного дракона", "Детёныш красного дракона", "Детёныш серебряного дракона",
        "Детёныш белого дракона",
    ],
    "Элементали": [
        "Водяной элементаль", "Воздушный элементаль", "Земляной элементаль", "Огненный элементаль",
    ],
    "Грибы": [
        "Визгун", "Фиолетовый гриб",
    ],
    "Великаны": [
        "Каменный великан", "Ледяной великан", "Облачный великан",
        "Огненный великан", "Холмовой великан", "Штормовой великан",
    ],
    "Гоблины": [
        "Гоблин-босс", "Гоблин-воин", "Гоблин-миньон",
    ],
    "Големы": [
        "Глиняный голем", "Голем из плоти", "Железный голем", "Каменный голем",
    ],
    "Стражники": [
        "Капитан стражи", "Стражник",
    ],
    "Карги": [
        "Зелёная карга", "Морская карга", "Ночная карга",
    ],
    "Хобгоблины": [
        "Хобгоблин-капитан", "Хобгоблин-воин",
    ],
    "Оборотни": [
        "Вервепрь", "Вервольф", "Веркрыса", "Вермедведь", "Вертигр",
    ],
    "Маги": [
        "Архимаг", "Друид", "Маг",
    ],
    "Мефиты": [
        "Ледяной мефит", "Магмовый мефит", "Паровой мефит", "Пылевой мефит",
    ],
    "Мумии": [
        "Мумия", "Повелитель мумий",
    ],
    "Наги": [
        "Духовная нага", "Нага-страж",
    ],
    "Слизи": [
        "Желатиновый куб", "Охровый студень", "Серая слизь", "Чёрная слизь",
    ],
    "Пираты": [
        "Капитан пиратов", "Пират",
    ],
    "Жрецы": [
        "Жрец", "Жрец-послушник",
    ],
    "Скелеты": [
        "Скелет", "Скелет боевого коня", "Скелет минотавра",
    ],
    "Сфинксы": [
        "Сфинкс доблести", "Сфинкс знаний", "Сфинкс чудес",
    ],
    "Головорезы": [
        "Главарь головорезов", "Головорез",
    ],
    "Тролли": [
        "Конечность тролля", "Тролль",
    ],
    "Вампиры": [
        "Вампир", "Порождение вампира", "Фамильяр вампира",
    ],
    "Воины": [
        "Берсерк", "Ветеран-воин", "Гладиатор", "Пехотинец-воин", "Рыцарь",
    ],
    "Зомби": [
        "Зомби", "Огр-зомби",
    ],
}

# Построить обратный словарь: имя монстра → название группы
def build_reverse_map(groups):
    rev = {}
    for group_name, monsters in groups.items():
        for m in monsters:
            rev[m] = group_name
    return rev


def parse_monsters(text):
    """
    Парсит markdown-файл: возвращает (h1_line, list_of_monster_blocks).
    Каждый блок = (name, content) где content — всё от строки после ## до следующего ##.
    """
    lines = text.split('\n')
    h1_line = None
    monsters = []
    current_name = None
    current_lines = []

    for line in lines:
        if line.startswith('# ') and not line.startswith('## '):
            h1_line = line
            continue
        if line.startswith('## '):
            if current_name is not None:
                monsters.append((current_name, '\n'.join(current_lines)))
            current_name = line[3:].strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_name is not None:
        monsters.append((current_name, '\n'.join(current_lines)))

    return h1_line, monsters


def demote_headers(content):
    """
    Понижает заголовки H3→H4 внутри блока монстра.
    (H2→H3 делается при выводе имени монстра.)
    """
    result = []
    for line in content.split('\n'):
        if line.startswith('### '):
            result.append('#' + line)  # ### → ####
        else:
            result.append(line)
    return '\n'.join(result)


def get_sort_key(name, lang):
    """Ключ сортировки для имени монстра."""
    return name.lower()


def get_letter(name, lang):
    """Получить первую букву для буквенной секции."""
    first = name[0].upper()
    return first


def sort_h2_key(section_name, doc_title):
    """
    Ключ сортировки для H2-секций.
    Формат секции: "{doc_title}: {suffix}"
    Буквенная секция (одна буква) идёт перед тематической при равенстве.
    Сортировка алфавитная по суффиксу, буквенная перед тематической.
    """
    prefix = doc_title + ": "
    suffix = section_name[len(prefix):]
    # Буквенная = суффикс — одна буква
    is_letter = len(suffix) == 1
    # Сортируем по (suffix_lower, 0 если буква иначе 1)
    return (suffix.lower(), 0 if is_letter else 1)


def process_file(filepath, groups, doc_title):
    """Обрабатывает один файл."""
    text = Path(filepath).read_text(encoding='utf-8')
    h1_line, monsters = parse_monsters(text)

    if h1_line is None:
        print(f"ОШИБКА: H1 не найден в {filepath}", file=sys.stderr)
        sys.exit(1)

    reverse_map = build_reverse_map(groups)

    # Считаем группированных и одиночек
    grouped_count = 0
    loner_count = 0

    # Распределяем монстров по секциям
    # section_key → list of (name, demoted_content)
    sections = {}

    for name, content in monsters:
        demoted = demote_headers(content)

        if name in reverse_map:
            group_name = reverse_map[name]
            section_key = f"{doc_title}: {group_name}"
            grouped_count += 1
        else:
            letter = get_letter(name, doc_title)
            section_key = f"{doc_title}: {letter}"
            loner_count += 1

        if section_key not in sections:
            sections[section_key] = []
        sections[section_key].append((name, demoted))

    # Сортируем монстров внутри каждой секции
    for key in sections:
        sections[key].sort(key=lambda x: x[0].lower())

    # Сортируем секции
    sorted_keys = sorted(sections.keys(), key=lambda k: sort_h2_key(k, doc_title))

    # Собираем результат
    result_lines = [h1_line, '']

    for key in sorted_keys:
        result_lines.append(f'## {key}')
        result_lines.append('')

        for name, content in sections[key]:
            result_lines.append(f'### {name}')
            result_lines.append('')
            # content уже начинается с новой строки после имени
            # Убираем начальные/конечные пустые строки из content
            stripped = content.strip('\n')
            result_lines.append(stripped)
            result_lines.append('')

    # Финализация: убираем лишний trailing newline, добавляем один
    output = '\n'.join(result_lines)
    # Убираем множественные пустые строки в конце
    output = output.rstrip('\n') + '\n'

    Path(filepath).write_text(output, encoding='utf-8')

    print(f"Обработан: {filepath}")
    print(f"  Монстров в группах: {grouped_count}")
    print(f"  Одиночек: {loner_count}")
    print(f"  Всего: {grouped_count + loner_count}")
    print(f"  Секций H2: {len(sorted_keys)}")


def main():
    base = Path(__file__).resolve().parent.parent / 'src' / 'dnd' / 'srd-5.2'

    en_file = base / 'en-v2' / '12_MonstersA-Z.md'
    ru_file = base / 'ru-v2' / '12_MonstersA-Z.md'

    print("=== EN ===")
    process_file(en_file, EN_GROUPS, "Monsters A–Z")

    print()
    print("=== RU ===")
    process_file(ru_file, RU_GROUPS, "Монстры от А до Я")


if __name__ == '__main__':
    main()
