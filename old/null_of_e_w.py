import json

FIELDS = ["t", "tp", "d", "s"]  # w maydoniga tegmaymiz

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def patch_nulls(data, lang_tag="uz"):
    for idx, entry in enumerate(data):
        for field in FIELDS:
            value = entry.get(field)
            if value is None or str(value).strip().lower() == "null" or str(value).strip() == "":
                entry[field] = f"null_of_{lang_tag}_{idx}_{field}"
    return data

def main():
    path = "./en/essential/uz/words.json"
    uz_data = load_json(path)

    patched_data = patch_nulls(uz_data)
    save_json(path, patched_data)

    print(f"✅ Bo‘sh qiymatlar 'null_of_uz_<index>_<field>' formatida to‘ldirildi: {path}")

if __name__ == "__main__":
    main()
