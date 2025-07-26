import json
from pathlib import Path

# Maqsad fayl (beginner uz hikoyalar uchun)
uz_path = Path("../assets/en/beginner/stories_nested.json")

# Parametrlar
PARTS = 4         # 0..3
UNITS = 20        # 0..19
STORIES = 3       # 0..2

# Yangi tuzilgan data
uz_data = {}

for part in range(PARTS):
    uz_data[str(part)] = {}
    for unit in range(UNITS):
        uz_data[str(part)][str(unit)] = {}
        for story_number in range(STORIES):
            uz_data[str(part)][str(unit)][str(story_number)] = {
                "h": f"null_of_{part}_{unit}_{story_number}_h",
                "b": f"null_of_{part}_{unit}_{story_number}_b"
            }

# JSON faylga yozish
with open(uz_path, "w", encoding="utf-8") as f:
    json.dump(uz_data, f, ensure_ascii=False, indent=2)

print(f"✅ Beginner uchun placeholder hikoyalar yozildi: {uz_path}")
