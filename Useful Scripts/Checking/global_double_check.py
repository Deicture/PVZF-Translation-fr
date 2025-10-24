import os
import subprocess

def run_global_check():
    """Run duplicate checks for all languages found in the Localization directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    localization_base = os.path.abspath(os.path.join(script_dir, "..", "..", "PvZ_Fusion_Translator", "Localization"))
    double_check_path = os.path.join(script_dir, "double_check.py")

    if not os.path.exists(localization_base):
        print("✗ Localization directory not found.")
        return

    languages = [d for d in os.listdir(localization_base) if os.path.isdir(os.path.join(localization_base, d))]

    if not languages:
        print("✗ No language folders found.")
        return

    print("=== PvZ Fusion Global Duplicate Checker ===\n")
    print(f"Found {len(languages)} languages: {', '.join(languages)}\n")

    for lang in languages:
        print(f"▶ Checking {lang}...")
        subprocess.run(["python", double_check_path], input=f"{lang}\n", text=True)
        print("-" * 40)

    print("\n✅ Global check complete. Reports generated in /reports/")

if __name__ == "__main__":
    run_global_check()
