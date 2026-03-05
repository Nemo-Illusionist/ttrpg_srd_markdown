# Basic Roleplaying Character Sheet

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

<h2>Basic Roleplaying Character Sheet</h2>

<!-- TOP ROW: Identity | Characteristics | Derived -->
<div class="brp-top">

<!-- Identity -->
<div>
<div class="section-title">Identity</div>
<div class="brp-field"><label>Name</label><input type="text"><label>Profession</label><input type="text"></div>
<div class="brp-field"><label>Race</label><input type="text" style="width:50px"><label>Age</label><input type="text" style="width:30px"><label>Gender</label><input type="text"></div>
<div class="brp-field"><label>Handedness</label><input type="text" style="width:50px"><label>Height & Weight</label><input type="text"></div>
<div class="brp-field"><label>Description</label><input type="text"></div>
<div class="brp-field"><label>Distinctive Feature(s)</label><input type="text"></div>
</div>

<!-- Characteristics -->
<div>
<div class="section-title">Characteristics</div>
<div class="brp-char-grid">
<label>STR</label><input type="text"><label>Effort Roll</label><input type="text">
<label>CON</label><input type="text"><label>Stamina Roll</label><input type="text">
<label>SIZ</label><input type="text"><label></label><input type="text" style="visibility:hidden">
<label>INT</label><input type="text"><label>Idea Roll</label><input type="text">
<label>POW</label><input type="text"><label>Luck Roll</label><input type="text">
<label>DEX</label><input type="text"><label>Agility Roll</label><input type="text">
<label>APP</label><input type="text"><label>Charisma Roll</label><input type="text">
</div>
</div>

<!-- Derived Characteristics -->
<div>
<div class="section-title">Derived Characteristics</div>
<div class="brp-field"><label>MOV</label><input type="text" style="width:30px"><label>Damage Bonus</label><input type="text"></div>
<div style="margin-top:4px">
<div><span class="brp-boxes-label">Hit Points</span></div>
<div class="brp-boxes"><span class="brp-boxes-label" style="font-size:8px">DEAD</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span></div>
<div class="brp-boxes"><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span><span>16</span></div>
<div class="brp-boxes"><span>17</span><span>18</span><span>19</span><span>20</span><span>21</span><span>22</span><span>23</span><span>24</span><span>25</span></div>
</div>
<div style="margin-top:4px">
<div><span class="brp-boxes-label">Power Points</span></div>
<div class="brp-boxes"><span class="brp-boxes-label" style="font-size:8px">UNC</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span></div>
<div class="brp-boxes"><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span><span>16</span></div>
<div class="brp-boxes"><span>17</span><span>18</span><span>19</span><span>20</span><span>21</span><span>22</span><span>23</span><span>24</span><span>25</span></div>
</div>
</div>

</div><!-- /brp-top -->

<!-- SKILLS — 3 columns -->
<div class="brp-skills">
<div class="section-title">Skills</div>

<!-- Column 1 -->
<div>
<div class="brp-skill"><span class="sname">Appraise (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Art (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Artillery (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Bargain (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Brawl (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Climb (40)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Command (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Craft (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Demolition (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Disguise (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Dodge (DEX&times;2)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Drive (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Energy Weapon (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Etiquette (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Fast Talk (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Fine Manipulation (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Firearm (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">First Aid (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Fly (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Gaming (INT+POW)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

<!-- Column 2 -->
<div>
<div class="brp-skill"><span class="sname">Grapple (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Heavy Machine (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Heavy Weapon (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Hide (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Insight (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Jump (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Knowledge (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Language, Own (INT&times;5)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Language, Other (______) (00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Listen (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Literacy (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Martial Arts (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Medicine (05% or 00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Melee Weapon (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Missile Weapon (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Navigate (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Perform (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

<!-- Column 3 -->
<div>
<div class="brp-skill"><span class="sname">Persuade (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Pilot (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Projection (DEX&times;2)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Psychotherapy (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Repair (______) (15)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Research (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Ride (______) (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Science (______) (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Sense (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Shield (______) (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Sleight of Hand (05)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Spot (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Status (var)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Stealth (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Strategy (01)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Swim (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Teach (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Technical Skill (______) (00)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Throw (25)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
<div class="brp-skill"><span class="sname">Track (10)</span><input type="text"> <span class="pct">%</span> <span class="xp"></span></div>
</div>

</div><!-- /brp-skills -->

<!-- BOTTOM ROW: Equipment | Weapons & Shields + Armor -->
<div class="brp-bottom">

<!-- Equipment -->
<div>
<div class="section-title">Equipment</div>
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
<div class="section-title">Weapons & Shields</div>
<table>
<tr><th>Weapon</th><th>%</th><th>Damage</th><th>Hands</th><th>HP</th><th>Range</th></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><em>Brawl</em></td><td><input type="text"></td><td><em>1D3+</em></td><td><em>1</em></td><td><em>—</em></td><td><em>—</em></td></tr>
</table>

<div class="section-title">Armor</div>
<table>
<tr><th>Type</th><th>Points</th><th>Modifier</th></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
</table>
</div>

</div><!-- /brp-bottom -->

</div><!-- /brp-sheet -->
