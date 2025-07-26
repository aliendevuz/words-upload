import json
import os

def print_stat(data, lang_label, file_name):
    total = len(data)
    keys = ['w', 't', 'tp', 'd', 's', 'atp']
    print(f"\n📘 Hisobot: {lang_label.upper()} {file_name}")
    print(f"Umumiy so‘zlar soni: {total}")
    print("-" * 40)
    for key in keys:
        filled = sum(1 for item in data if item.get(key) and not str(item[key]).startswith(f"null_of_"))
        nulls = total - filled
        print(f"{key.upper():<3} | To‘ldirilgan: {filled:<4} | Bo‘sh/Null: {nulls}")
    print("-" * 40)

def main():
    files = [
        ("./en/beginner/words.json", "english"),
        ("./en/beginner/uz/words.json", "uzbek"),
    ]
    
    for path, lang in files:
        if not os.path.exists(path):
            print(f"❌ Fayl topilmadi: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                print_stat(data, lang, os.path.basename(path))
            except Exception as e:
                print(f"❌ Xatolik faylni o‘qishda ({path}): {e}")

if __name__ == "__main__":
    main()
