# Лист персонажа Basic Roleplaying

<style>
/* BRP Character Sheet — screen + print */
.brp-sheet { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; min-width: 800px; max-width: 800px; margin: 0 auto; color: #222; overflow-x: auto; }
.brp-sheet * { box-sizing: border-box; }
.brp-sheet h2 { font-size: 18px; text-align: center; margin: 0 0 8px; color: #b71c1c; text-transform: uppercase; letter-spacing: 2px; }
.brp-sheet .section-title { font-size: 12px; font-weight: bold; color: #b71c1c; text-transform: uppercase; margin: 8px 0 4px; border-bottom: 2px solid #b71c1c; padding-bottom: 2px; }

/* Top row: Identity | Characteristics | Derived */
.brp-top { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 8px; }
.brp-top > div { border: 1px solid #ccc; padding: 6px; border-radius: 4px; }

/* Field rows */
.brp-field { display: flex; align-items: baseline; margin-bottom: 3px; gap: 4px; }
.brp-field label { font-size: 10px; white-space: nowrap; }
.brp-field input[type="text"] { flex: 1; border: none; border-bottom: 1px solid #999; font-size: 11px; padding: 1px 2px; background: transparent; min-width: 0; }
.brp-field-half { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }

/* Characteristics grid */
.brp-char-grid { display: grid; grid-template-columns: auto 1fr auto 1fr; gap: 2px 6px; align-items: baseline; }
.brp-char-grid label { font-weight: bold; font-size: 11px; }
.brp-char-grid input { border: none; border-bottom: 1px solid #999; width: 100%; font-size: 11px; padding: 1px; background: transparent; }

/* HP/PP boxes */
.brp-boxes { display: flex; flex-wrap: wrap; gap: 1px; margin: 2px 0; }
.brp-boxes span { width: 18px; height: 16px; border: 1px solid #666; display: inline-flex; align-items: center; justify-content: center; font-size: 8px; background: #fff; }
.brp-boxes-label { font-size: 9px; font-weight: bold; margin-right: 4px; }

/* Skills — 3 columns */
.brp-skills { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px 10px; margin-bottom: 8px; border: 1px solid #ccc; padding: 6px; border-radius: 4px; }
.brp-skills .section-title { grid-column: 1 / -1; }
.brp-skill { display: flex; align-items: baseline; font-size: 10px; gap: 2px; }
.brp-skill .sname { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.brp-skill input[type="text"] { width: 28px; border: none; border-bottom: 1px solid #999; font-size: 10px; text-align: right; padding: 0 1px; background: transparent; }
.brp-skill .pct { font-size: 9px; color: #666; }
.brp-skill .xp { width: 10px; height: 10px; border: 1px solid #666; display: inline-block; vertical-align: middle; }

/* Bottom row: Equipment | Weapons & Shields + Armor */
.brp-bottom { display: grid; grid-template-columns: 1fr 2fr; gap: 10px; }
.brp-bottom > div { border: 1px solid #ccc; padding: 6px; border-radius: 4px; }

/* Tables */
.brp-sheet table { width: 100%; border-collapse: collapse; font-size: 10px; margin: 4px 0; }
.brp-sheet th { text-align: left; font-weight: bold; border-bottom: 1px solid #999; padding: 2px 4px; font-size: 10px; }
.brp-sheet td { border-bottom: 1px solid #ddd; padding: 2px 4px; }
.brp-sheet td input { border: none; width: 100%; font-size: 10px; background: transparent; }

/* Dark theme (MkDocs Material slate) */
[data-md-color-scheme="slate"] .brp-sheet { color: #e0e0e0; }
[data-md-color-scheme="slate"] .brp-top > div,
[data-md-color-scheme="slate"] .brp-skills,
[data-md-color-scheme="slate"] .brp-bottom > div { border-color: #555; }
[data-md-color-scheme="slate"] .brp-field input[type="text"],
[data-md-color-scheme="slate"] .brp-char-grid input,
[data-md-color-scheme="slate"] .brp-skill input[type="text"],
[data-md-color-scheme="slate"] .brp-sheet td input { border-bottom-color: #666; color: #e0e0e0; }
[data-md-color-scheme="slate"] .brp-boxes span { border-color: #888; background: #2e2e2e; color: #ccc; }
[data-md-color-scheme="slate"] .brp-sheet th { border-bottom-color: #666; color: #ccc; }
[data-md-color-scheme="slate"] .brp-sheet td { border-bottom-color: #444; }
[data-md-color-scheme="slate"] .brp-skill .pct { color: #999; }
[data-md-color-scheme="slate"] .brp-skill .xp { border-color: #888; }

/* Print */
@media print {
  .brp-sheet { max-width: 100%; page-break-inside: avoid; }
  .md-header, .md-footer, .md-sidebar, .md-tabs, nav, .md-content > .md-content__inner > h1 { display: none !important; }
  .brp-field input, .brp-char-grid input, .brp-skill input, .brp-sheet td input { border-bottom: 1px solid #999 !important; }
  .brp-sheet { font-size: 10px; }
}
</style>

<div class="brp-sheet">

<h2>Лист персонажа Basic Roleplaying</h2>

<!-- TOP ROW: Identity | Characteristics | Derived -->
<div class="brp-top">

<!-- Identity -->
<div>
<div class="section-title">Личность</div>
<div class="brp-field"><label>Имя</label><input type="text"><label>Профессия</label><input type="text"></div>
<div class="brp-field"><label>Раса</label><input type="text" style="width:50px"><label>Возраст</label><input type="text" style="width:30px"><label>Пол</label><input type="text"></div>
<div class="brp-field"><label>Рабочая рука</label><input type="text" style="width:50px"><label>Рост и Вес</label><input type="text"></div>
<div class="brp-field"><label>Описание</label><input type="text"></div>
<div class="brp-field"><label>Особые приметы</label><input type="text"></div>
</div>

<!-- Characteristics -->
<div>
<div class="section-title">Характеристики</div>
<div class="brp-char-grid">
<label>СИЛ</label><input type="text"><label>Бросок Силы</label><input type="text">
<label>ВЫН</label><input type="text"><label>Бросок Выносливости</label><input type="text">
<label>РАЗ</label><input type="text"><label></label><input type="text" style="visibility:hidden">
<label>ИНТ</label><input type="text"><label>Бросок Интеллекта</label><input type="text">
<label>ВОЛ</label><input type="text"><label>Бросок Воли</label><input type="text">
<label>ЛОВ</label><input type="text"><label>Бросок Ловкости</label><input type="text">
<label>ВНШ</label><input type="text"><label>Бросок Внешности</label><input type="text">
</div>
</div>

<!-- Derived Characteristics -->
<div>
<div class="section-title">Производные характеристики</div>
<div class="brp-field"><label>ПЕР</label><input type="text" style="width:30px"><label>Бонус урона</label><input type="text"></div>
<div style="margin-top:4px">
<div><span class="brp-boxes-label">Хиты</span></div>
<div class="brp-boxes"><span class="brp-boxes-label" style="font-size:8px">МЁРТВ</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span></div>
<div class="brp-boxes"><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span><span>16</span></div>
<div class="brp-boxes"><span>17</span><span>18</span><span>19</span><span>20</span><span>21</span><span>22</span><span>23</span><span>24</span><span>25</span></div>
</div>
<div style="margin-top:4px">
<div><span class="brp-boxes-label">Очки Воли</span></div>
<div class="brp-boxes"><span class="brp-boxes-label" style="font-size:8px">БЕЗ СОЗ.</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span></div>
<div class="brp-boxes"><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span><span>16</span></div>
<div class="brp-boxes"><span>17</span><span>18</span><span>19</span><span>20</span><span>21</span><span>22</span><span>23</span><span>24</span><span>25</span></div>
</div>
</div>

</div><!-- /brp-top -->

<!-- SKILLS — 3 columns -->
<div class="brp-skills">
<div class="section-title">Навыки</div>

<!-- Column 1 -->
<div>
<div class="brp-skill"><span class="sname">Оценка (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Искусство (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Артиллерия (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Торговля (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Драка (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Лазание (40)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Командование (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Ремесло (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Подрывное дело (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Маскировка (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Уклонение (ЛОВ&times;2)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Вождение (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Энерг. оружие (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Этикет (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Убалтывание (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Точная работа (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Огнестрел. (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Первая помощь (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Полёт (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Азартные игры (ИНТ+ВОЛ)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

<!-- Column 2 -->
<div>
<div class="brp-skill"><span class="sname">Захват (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Тяж. техника (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Тяж. оружие (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Прятки (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Проницательность (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Прыжок (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Знание (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Язык, родной (ИНТ&times;5)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Язык, другой (______) (00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Слух (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Грамотность (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Боевые искусства (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Медицина (05% или 00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Ближн. оружие (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Дист. оружие (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Навигация (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Выступление (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

<!-- Column 3 -->
<div>
<div class="brp-skill"><span class="sname">Убеждение (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Пилотирование (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Проецирование (ЛОВ&times;2)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Психотерапия (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Ремонт (______) (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Исследование (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Верховая езда (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Наука (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Чутьё (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Щит (______) (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Ловкость рук (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Внимательность (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Статус (разн.)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Скрытность (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Стратегия (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Плавание (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Обучение (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Техника (______) (00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Метание (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Выслеживание (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

</div><!-- /brp-skills -->

<!-- BOTTOM ROW: Equipment | Weapons & Shields + Armor -->
<div class="brp-bottom">

<!-- Equipment -->
<div>
<div class="section-title">Снаряжение</div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
<div class="brp-field"><input type="text"></div>
</div>

<!-- Weapons & Shields + Armor -->
<div>
<div class="section-title">Оружие и щиты</div>
<table>
<tr><th>Оружие</th><th>%</th><th>Урон</th><th>Руки</th><th>ХП</th><th>Дальность</th></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><em>Драка</em></td><td><input type="text"></td><td><em>1D3+</em></td><td><em>1</em></td><td><em>—</em></td><td><em>—</em></td></tr>
</table>

<div class="section-title">Броня</div>
<table>
<tr><th>Тип</th><th>Очки</th><th>Модификатор</th></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
</table>
</div>

</div><!-- /brp-bottom -->

</div><!-- /brp-sheet -->
