import json
import os

# Set working directory to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def merge_entries(primary_list, fallback_list, key):
    """
    Merge two lists of dictionaries based on a shared key.
    Prioritizes entries in primary_list when the key is present in both.
    """
    primary_dict = {item[key]: item for item in primary_list}
    fallback_dict = {item[key]: item for item in fallback_list}

    result = []

    # Use primary when present in both
    for k in sorted(primary_dict):
        if k in fallback_dict:
            result.append(primary_dict[k])

    # Add fallback-only entries
    for k in sorted(fallback_dict):
        if k not in primary_dict:
            result.append(fallback_dict[k])

    return result

# ---- MAIN ENTRY ----
if __name__ == '__main__':
    # Define language codes
    lang_primary = 'French'
    lang_fallback = 'English'

    # Define Almanac directory path
    almanac_base = os.path.abspath(os.path.join(script_dir, '..', 'PvZ_Fusion_Translator', 'Localization'))

    # Build full input paths
    lawn_primary_file = os.path.join(almanac_base, lang_primary, 'Almanac', 'LawnStringsTranslate.json')
    lawn_fallback_file = os.path.join(almanac_base, lang_fallback, 'Almanac', 'LawnStringsTranslate.json')

    zombie_primary_file = os.path.join(almanac_base, lang_primary, 'Almanac', 'ZombieStringsTranslate.json')
    zombie_fallback_file = os.path.join(almanac_base, lang_fallback, 'Almanac', 'ZombieStringsTranslate.json')

    # Load JSON data
    with open(lawn_primary_file, 'r', encoding='utf-8') as f:
        lawn_primary_data = json.load(f)
    with open(lawn_fallback_file, 'r', encoding='utf-8') as f:
        lawn_fallback_data = json.load(f)

    with open(zombie_primary_file, 'r', encoding='utf-8') as f:
        zombie_primary_data = json.load(f)
    with open(zombie_fallback_file, 'r', encoding='utf-8') as f:
        zombie_fallback_data = json.load(f)

    # Merge plant entries
    merged_plants = merge_entries(
        lawn_primary_data.get('plants', []),
        lawn_fallback_data.get('plants', []),
        key='seedType'
    )
    with open('LawnStringsTranslate.json', 'w', encoding='utf-8') as f:
        json.dump({'plants': merged_plants}, f, indent=4, ensure_ascii=False)

    # Merge zombie entries
    merged_zombies = merge_entries(
        zombie_primary_data.get('zombies', []),
        zombie_fallback_data.get('zombies', []),
        key='theZombieType'
    )
    with open('ZombieStringsTranslate.json', 'w', encoding='utf-8') as f:
        json.dump({'zombies': merged_zombies}, f, indent=4, ensure_ascii=False)

    print("✓ Merged output saved to:")
    print("  - LawnStringsTranslate.json")
    print("  - ZombieStringsTranslate.json")
