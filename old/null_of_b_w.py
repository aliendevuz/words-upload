import json
import os

EN_FILE = "./en/beginner/words.json"
UZ_FILE = "./en/beginner/uz/words.json"

def update_en_words(data):
    for i, word in enumerate(data):
        word["t"] = f"null_of_en({i})_t"
        word["tp"] = f"null_of_en({i})_tp"
        word["d"] = f"null_of_en({i})_d"
        word["s"] = f"null_of_en({i})_s"
    return data

def make_uz_words(data):
    uz_data = []
    for i in range(len(data)):
        uz_data.append({
            "w":  f"null_of_uz({i})_w",
            "t":  f"null_of_uz({i})_t",
            "tp": f"null_of_uz({i})_tp",
            "d":  f"null_of_uz({i})_d",
            "s":  f"null_of_uz({i})_s"
        })
    return uz_data

def main():
    if not os.path.exists(EN_FILE):
        print(f"❌ EN fayl topilmadi: {EN_FILE}")
        return

    with open(EN_FILE, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    en_data = update_en_words(en_data)
    with open(EN_FILE, "w", encoding="utf-8") as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Yangilandi: {EN_FILE}")

    uz_data = make_uz_words(en_data)
    os.makedirs(os.path.dirname(UZ_FILE), exist_ok=True)
    with open(UZ_FILE, "w", encoding="utf-8") as f:
        json.dump(uz_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Yaratildi: {UZ_FILE}")

if __name__ == "__main__":
    main()
