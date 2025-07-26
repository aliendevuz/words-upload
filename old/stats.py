import json
import os

# Fayl yo'li
WORDS_PATH = os.path.join("..", "assets", "en", "beginner", "words.json")

# Tekshiriladigan ustunlar
FIELDS = ["w", "t", "tp", "d", "s", "atp"]

def is_filled(value):
    return value is not None and value != ""

def main():
    with open(WORDS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    print("📘 Hisobot: ENGLISH beginner/words.json")
    print(f"Umumiy so‘zlar soni: {total}")
    print("-" * 40)

    for field in FIELDS:
        filled = sum(1 for item in data if is_filled(item.get(field)))
        empty = total - filled
        print(f"{field.upper():<4}| To‘ldirilgan: {filled:<5} | Bo‘sh/Null: {empty}")
    
    print("-" * 40)

if __name__ == "__main__":
    main()
