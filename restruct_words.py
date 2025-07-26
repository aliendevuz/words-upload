import json
from pathlib import Path

# Manba va maqsad fayllar
src_path = Path("../assets/en/beginner/words.json")
target_path = Path("../assets/en/beginner/words_nested.json")

PARTS = 4
UNITS = 20
WORDS_PER_UNIT = 20

# Yuklash
with open(src_path, "r", encoding="utf-8") as f:
    words = json.load(f)

if len(words) != PARTS * UNITS * WORDS_PER_UNIT:
    raise ValueError(f"❌ words.json faylidagi elementlar soni 3600 emas: {len(words)}")

# Yangi struktura
nested = {}
index = 0

for part in range(PARTS):
    nested[str(part)] = {}
    for unit in range(UNITS):
        nested[str(part)][str(unit)] = words[index:index + WORDS_PER_UNIT]
        index += WORDS_PER_UNIT

# Saqlash
with open(target_path, "w", encoding="utf-8") as f:
    json.dump(nested, f, ensure_ascii=False, indent=2)

print(f"✅ Nested wordlar yaratildi: {target_path}")
