import json
import os

# Set working directory to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def compare_json_files(a_path, b_path, output_filename):
    """
    Compares two JSON files and writes the merged result to a new file in this script's directory.

    Rules:
    a. If a key is present in both A and B, use A's value in C.
    b. If a key is only in A, don't include it in C.
    c. If a key is only in B, include it in C with B's value.
    """
    try:
        with open(a_path, 'r', encoding='utf-8') as file:
            a_data = json.load(file)
        with open(b_path, 'r', encoding='utf-8') as file:
            b_data = json.load(file)

        if not isinstance(a_data, dict) or not isinstance(b_data, dict):
            raise ValueError("Both JSON files must be dictionaries.")

        c_data = {}

        # (a) Keys in both → A's value
        for key in a_data:
            if key in b_data:
                c_data[key] = a_data[key]

        # (c) Keys only in B → B's value
        for key in b_data:
            if key not in a_data:
                c_data[key] = b_data[key]

        output_path = os.path.join(script_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(c_data, file, indent=4, ensure_ascii=False)

        print(f"✓ {output_filename} generated successfully.")

    except Exception as e:
        print(f"✗ Error while processing {output_filename}: {e}")


# ---- MAIN ENTRY ----
if __name__ == '__main__':
    # Set the base directory for localization
    localization_base = os.path.abspath(os.path.join(script_dir, '..', 'PvZ_Fusion_Translator', 'Localization'))

    # Input language codes
    lang_a = 'Japanese'  # Higher priority
    lang_b = 'English'  # Fallback

    # Construct full paths to the JSON files
    a_regex_path = os.path.join(localization_base, lang_a, 'Strings', 'translation_regexs.json')
    b_regex_path = os.path.join(localization_base, lang_b, 'Strings', 'translation_regexs.json')

    a_strings_path = os.path.join(localization_base, lang_a, 'Strings', 'translation_strings.json')
    b_strings_path = os.path.join(localization_base, lang_b, 'Strings', 'translation_strings.json')

    # Run comparison and write to output
    compare_json_files(a_regex_path, b_regex_path, 'translation_regexs.json')
    compare_json_files(a_strings_path, b_strings_path, 'translation_strings.json')
