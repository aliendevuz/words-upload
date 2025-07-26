import os
import json

FIELDS = ["h", "b"]

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ JSON o‘qishda xato: {path}\n{e}")
        return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def patch_nulls(data, lang_tag, filename):
    for idx, entry in enumerate(data):
        for field in FIELDS:
            val = entry.get(field)
            # if val is None or str(val).strip().lower() == "null" or str(val).strip() == "":
            entry[field] = f"null_of_{lang_tag}_{idx}_{field}"
    return data

def main():
    files_to_patch = [
        ("./en/essential/story2.json", "en"),
        ("./en/essential/story3.json", "en"),
        ("./en/essential/uz/story1.json", "uz"),
        ("./en/essential/uz/story2.json", "uz"),
        ("./en/essential/uz/story3.json", "uz")
    ]

    for path, lang in files_to_patch:
        if not os.path.exists(path):
            print(f"⚠️ Fayl topilmadi: {path}")
            continue

        data = load_json(path)
        patched = patch_nulls(data, lang, os.path.basename(path))
        save_json(path, patched)
        print(f"✅ Patch bajarildi: {path}")

if __name__ == "__main__":
    main()
