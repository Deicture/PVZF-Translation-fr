import json
import os
import re

def find_duplicates_in_almanac(filepath, key_field, report_lines):
    """
    Detect duplicates in Almanac-type JSONs (plants or zombies),
    showing all real line numbers from the JSON file.
    """
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        raw_lines = file.readlines()
        file.seek(0)
        data = json.load(file)

    entries = data.get('plants') or data.get('zombies')
    if not entries:
        print(f"✗ Unsupported structure in {os.path.basename(filepath)}")
        return False

    # Regex pattern to locate each key_field's numeric value
    pattern = re.compile(rf'\"{key_field}\"\s*:\s*(\d+)', re.IGNORECASE)
    line_map = {}
    for idx, line in enumerate(raw_lines, start=1):
        match = pattern.search(line)
        if match:
            value = int(match.group(1))
            line_map.setdefault(value, []).append(idx)  # store all occurrences

    seen = {}
    duplicates = {}

    # Detect duplicates logically from JSON structure
    for entry in entries:
        key_value = entry.get(key_field)
        if key_value is None:
            continue
        seen.setdefault(key_value, 0)
        seen[key_value] += 1

    # Identify all keys that appear more than once
    for key, count in seen.items():
        if count > 1:
            duplicates[key] = line_map.get(key, [])

    if duplicates:
        print(f"\n⚠️ Duplicates found in {os.path.basename(filepath)}:\n")
        report_lines.append(f"### ⚠️ {os.path.basename(filepath)}\n")
        for key, lines in duplicates.items():
            line_list = ', '.join(str(l) for l in lines)
            line = f"- `{key_field}` **{key}** → lines {line_list}"
            print(" ", line)
            report_lines.append(line)
        report_lines.append(f"\n_Total duplicates: {len(duplicates)}_\n")
        return True
    else:
        print(f"✅ No duplicates found in {os.path.basename(filepath)}")
        return False


def find_duplicates_in_achievements(filepath, report_lines):
    """Detect duplicate keys in Achievements JSON, showing all real line numbers."""
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        raw_lines = file.readlines()
        file.seek(0)
        data = json.load(file)

    pattern = re.compile(r'\"([^\"]+)\"\s*:\s*\{')
    line_map = {}
    for idx, line in enumerate(raw_lines, start=1):
        match = pattern.search(line)
        if match:
            key = match.group(1)
            line_map.setdefault(key, []).append(idx)

    seen = {}
    duplicates = {}

    for key in data.keys():
        seen.setdefault(key, 0)
        seen[key] += 1

    for key, count in seen.items():
        if count > 1:
            duplicates[key] = line_map.get(key, [])

    if duplicates:
        print(f"\n⚠️ Duplicates found in {os.path.basename(filepath)}:\n")
        report_lines.append(f"### ⚠️ {os.path.basename(filepath)}\n")
        for key, lines in duplicates.items():
            line_list = ', '.join(str(l) for l in lines)
            line = f"- Key `{key}` → lines {line_list}"
            print(" ", line)
            report_lines.append(line)
        report_lines.append(f"\n_Total duplicates: {len(duplicates)}_\n")
        return True
    else:
        print(f"✅ No duplicates found in {os.path.basename(filepath)}")
        return False


def run_duplicate_check(language):
    """
    Run duplicate checks for LawnStringsTranslate.json, ZombieStringsTranslate.json,
    and AchievementsTextTranslate.json in the specified localization folder.
    Generate a markdown report in /reports with all real line numbers.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    base_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "PvZ_Fusion_Translator", "Localization", language))
    lawn_path = os.path.join(base_dir, "Almanac", "LawnStringsTranslate.json")
    zombie_path = os.path.join(base_dir, "Almanac", "ZombieStringsTranslate.json")
    achievements_path = os.path.join(base_dir, "Almanac", "AchievementsTextTranslate.json")

    print(f"\n=== Checking duplicates for language: {language} ===")

    report_lines = [f"# 🧩 Duplicate Finder Report — {language}\n"]
    found = False

    if os.path.exists(lawn_path):
        if find_duplicates_in_almanac(lawn_path, "seedType", report_lines):
            found = True
    else:
        print("⚠️ LawnStringsTranslate.json not found.")

    if os.path.exists(zombie_path):
        if find_duplicates_in_almanac(zombie_path, "theZombieType", report_lines):
            found = True
    else:
        print("⚠️ ZombieStringsTranslate.json not found.")

    if os.path.exists(achievements_path):
        if find_duplicates_in_achievements(achievements_path, report_lines):
            found = True
    else:
        print("⚠️ AchievementsTextTranslate.json not found.")

    report_path = os.path.join(reports_dir, f"needFixDoubleFind_{language}.md")

    if found:
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write("\n".join(report_lines))
        print(f"\n📄 Report generated: {report_path}")
    else:
        if os.path.exists(report_path):
            os.remove(report_path)
            print("\n🧹 No duplicates found — old report deleted.")
        else:
            print("\n✅ No duplicates found. No report generated.")


if __name__ == "__main__":
    print("=== PvZ Fusion Duplicate Checker ===")
    lang = input("Enter the language folder name (e.g. 'French', 'Japanese', 'English'): ").strip()
    run_duplicate_check(lang)
