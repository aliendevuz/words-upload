import json

json_path = "./en/beginner/words.json"
txt_path = "./en/beginner/tp.txt"

# txt fayldan tp qiymatlarni o‘qish
with open(txt_path, "r", encoding="utf-8") as f:
    tp_list = [line.strip() for line in f if line.strip()]

# JSONni o‘qish
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

if len(data) != len(tp_list):
    raise ValueError(f"❌ Elementlar soni mos emas: JSON={len(data)}, TXT={len(tp_list)}")

# tp ustunini to‘ldirish
for i, tp_value in enumerate(tp_list):
    old = data[i].get("tp", "")
    data[i]["tp"] = tp_value
    if old != tp_value:
        print(f"🔁 {i}: '{old}' -> '{tp_value}'")

# JSONni saqlash
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 'tp' maydoni ENGLISH words.json uchun ham muvaffaqiyatli to‘ldirildi.")
