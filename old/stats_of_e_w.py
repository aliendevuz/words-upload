import json

FIELDS = ["w", "t", "tp", "d", "s"]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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
    print(f"Umumiy yozuvlar soni: {total}")
    print("-" * 40)
    for field in FIELDS:
        filled = stats[field]["filled"]
        empty = stats[field]["empty"]
        print(f"{field.upper():<3} | To‘ldirilgan: {filled:<4} | Bo‘sh/Null: {empty:<4}")
    print("-" * 40)

def main():
    en_path = "./en/essential/words.json"
    uz_path = "./en/essential/uz/words.json"

    en_data = load_json(en_path)
    uz_data = load_json(uz_path)

    en_stats = count_field_stats(en_data)
    uz_stats = count_field_stats(uz_data)

    print_report("ENGLISH words.json", en_stats, len(en_data))
    print_report("UZBEK uz/words.json", uz_stats, len(uz_data))

    if len(en_data) != len(uz_data):
        print(f"\n⚠️ Ogohlantirish: Fayllar uzunligi bir xil emas! EN: {len(en_data)}, UZ: {len(uz_data)}")

if __name__ == "__main__":
    main()
