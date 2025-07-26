import json

json_path = "./en/beginner/words.json"

# JSONni o‘qish
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Unique tp qiymatlarni yig‘ish
tp_values = set()
for item in data:
    tp = item.get("tp", "").strip()
    if tp:
        tp_values.add(tp)

# Natijani chiqarish
print("📘 'tp' ustunidagi noyob qiymatlar:")
for val in sorted(tp_values):
    print("-", val)

print(f"\n🔎 Jami noyob qiymatlar soni: {len(tp_values)}")
