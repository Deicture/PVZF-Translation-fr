# 🧩 PvZ Fusion Translation and Validation Toolkit

This toolkit contains all Python scripts used to **convert, validate, and synchronize translation files** for the *Plants vs Zombies: Fusion* localization project.
Each script automates a part of the translation workflow — from Excel export to JSON generation, comparison, CSV extraction, and duplicate verification.

---

## 📦 Included Scripts

| Script                         | Purpose                                                           | Typical Use Case                                                    |
| :----------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------ |
| **`jsonifier.py`**             | Converts Excel translation sheets to structured JSON files.       | Use when translators update the master spreadsheet.                 |
| **`csver.py`**                 | Converts JSON files to CSV format for readability.                | Use when you need to review or edit JSON in Excel or Google Sheets. |
| **`almanac_json_comparer.py`** | Merges *Almanac* JSONs (Plants & Zombies) between two languages.  | Combine Japanese and English JSONs to fill missing entries.         |
| **`strings_json_comparer.py`** | Compares and merges *Strings* and *Regexes* JSONs.                | Synchronize UI text dictionaries between two languages.             |
| **`double_check.py`**          | Detects duplicate IDs or keys inside JSONs for a single language. | Use before committing translations to detect conflicting IDs.       |
| **`global_double_check.py`**   | Runs `double_check.py` for all languages at once.                 | Use before release or merging PRs to ensure consistency globally.   |

---

## ⚙️ Requirements

All scripts require **Python 3.8+**. Some scripts also use the **pandas** library.

Install dependencies:

```bash
pip install pandas
```

All scripts auto-adjust to their own directory, so they can be run from anywhere.

---

## 🌿 `jsonifier.py` — Excel ➜ JSON

Converts Excel sheets into JSON files formatted for the game.

**Usage:**

```bash
python jsonifier.py
```

**Default input file:** `Fusion English Translation.xlsx`

**Output files:**

* `LawnStringsTranslate.json` → Plants
* `ZombieStringsTranslate.json` → Zombies
* `translation_strings.json` → General strings
* `translation_regexs.json` → Regex text patterns
* `AchievementsTextTranslate.json` → Achievement texts

---

## 🌻 `csver.py` — JSON ➜ CSV

Converts structured JSON files into flat CSVs for spreadsheet editing.

**Usage:**

```bash
python csver.py
```

**Output examples:**

* `poutput.csv` → from `LawnStringsTranslate.json`
* `zoutput.csv` → from `ZombieStringsTranslate.json`
* `soutput.csv` → from `translation_strings.json`
* `routput.csv` → from `translation_regexs.json`
* `aoutput.csv` → from `AchievementsTextTranslate.json`

---

## 🧠 `almanac_json_comparer.py` — Merge Almanac Files

Merges **Plants** and **Zombies** JSONs between two languages (e.g., Japanese and English).

**Default setup:**

```python
lang_primary = 'Japanese'
lang_fallback = 'English'
```

**Rules:**

1. If an entry exists in both → keep the primary version.
2. If missing in primary → copy from fallback.

**Usage:**

```bash
python almanac_json_comparer.py
```

Outputs:

* `LawnStringsTranslate.json`
* `ZombieStringsTranslate.json`

---

## 🧩 `strings_json_comparer.py` — Merge Strings & Regex Dictionaries

Compares two string dictionaries (A = higher priority, B = fallback) and merges them.

**Rules:**

* Keys in both → use A’s value.
* Keys only in A → skip (usually untranslated placeholders).
* Keys only in B → include B’s value.

**Usage:**

```bash
python strings_json_comparer.py
```

Outputs:

* `translation_strings.json`
* `translation_regexs.json`

---

## 🔍 `double_check.py` — Duplicate Finder (Single Language)

Scans JSON files in a single language to find duplicated entries and show their **real file line numbers**.

**Checks performed:**

| File                             | Field Checked   | Description             |
| :------------------------------- | :-------------- | :---------------------- |
| `LawnStringsTranslate.json`      | `seedType`      | Plants                  |
| `ZombieStringsTranslate.json`    | `theZombieType` | Zombies                 |
| `AchievementsTextTranslate.json` | key             | Achievement definitions |

**Usage:**

```bash
cd "Useful Scripts/Checking"
python double_check.py
```

Then enter the language name (e.g., `French`, `Japanese`, `English`).

**Example output:**

```markdown
# 🧩 Duplicate Finder Report — English

### ⚠️ LawnStringsTranslate.json

- `seedType` **1324** → lines 3175, 3178, 3181

_Total duplicates: 1_
```

**Reports saved to:**

```
Useful Scripts/Checking/reports/needFixDoubleFind_<LANG>.md
```

If no duplicates are found, old reports are automatically deleted.

---

## 🌍 `global_double_check.py` — Duplicate Finder (All Languages)

Automatically runs the duplicate check for every language folder found in:

```
PvZ_Fusion_Translator/Localization/
```

**Usage:**

```bash
cd "Useful Scripts/Checking"
python global_double_check.py
```

**Behavior:**

* Lists all languages (e.g., English, French, Japanese, Spanish...)
* Executes `double_check.py` for each
* Creates one report per language inside `/reports/`

**Example output:**

```
reports/
├── needFixDoubleFind_English.md
├── needFixDoubleFind_French.md
└── needFixDoubleFind_Japanese.md
```

---

## 🧰 Recommended Workflow

1. **After translator updates Excel:** Run `jsonifier.py` to generate fresh JSONs.
2. **Before code merge or review:** Run `double_check.py` or `global_double_check.py` to ensure there are no duplicate IDs.
3. **For debugging / manual inspection:** Use `csver.py` to export JSONs as spreadsheets.
4. **When merging translations:** Use `almanac_json_comparer.py` and `strings_json_comparer.py` to combine primary/fallback languages.

