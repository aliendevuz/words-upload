import os
import json
import glob

FIELDS = ["h", "b"]

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ JSON o‘qishda xato: {path}\n{e}")
        return []

def is_empty(value):
    if value is None:
        return True
    val = str(value).strip().lower()
    return val == "null" or val == "" or val.startswith("null_of_")

def count_field_stats(data):
    stats = {field: {"filled": 0, "empty": 0} for field in FIELDS}
    for entry in data:
        for field in FIELDS:
            value = entry.get(field)
            if is_empty(value):
                stats[field]["empty"] += 1
            else:
                stats[field]["filled"] += 1
    return stats

def print_report(name, stats, total):
    print(f"\n📘 Hisobot: {name}")
    print(f"Umumiy hikoyalar soni: {total}")
    print("-" * 40)
    for field in FIELDS:
        filled = stats[field]["filled"]
        empty = stats[field]["empty"]
        print(f"{field.upper():<3} | To‘ldirilgan: {filled:<4} | Bo‘sh/Null: {empty:<4}")
    print("-" * 40)

def main():
    en_dir = "./en/essential"
    uz_dir = "./en/essential/uz"

    # story*.json fayllarni topamiz
    en_story_files = sorted(glob.glob(os.path.join(en_dir, "story*.json")))

    if not en_story_files:
        print("❗ Hech qanday story fayl topilmadi.")
        return

    for en_path in en_story_files:
        filename = os.path.basename(en_path)
        uz_path = os.path.join(uz_dir, filename)

        en_data = load_json(en_path)
        uz_data = load_json(uz_path) if os.path.exists(uz_path) else []

        # EN
        en_stats = count_field_stats(en_data)
        print_report(f"ENGLISH {filename}", en_stats, len(en_data))

        # UZ
        if uz_data:
            uz_stats = count_field_stats(uz_data)
            print_report(f"UZBEK {filename}", uz_stats, len(uz_data))
        else:
            print(f"\n⚠️ Ogohlantirish: UZBEK fayl topilmadi — {uz_path}")

        # Solishtirish
        if len(en_data) != len(uz_data):
            print(f"⚠️ Uzunlik farqi: EN: {len(en_data)}, UZ: {len(uz_data)}")

if __name__ == "__main__":
    main()
