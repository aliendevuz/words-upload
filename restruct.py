import json
from pathlib import Path

src_paths = [
    Path("../assets/en/essential/stories.json"),
    Path("../assets/en/essential/uz/stories.json")
]

target_paths = [
    Path("../assets/en/essential/stories_nested.json"),
    Path("../assets/en/essential/uz/stories_nested.json")
]

for src_path, target_path in zip(src_paths, target_paths):
    if not src_path.exists():
        print(f"⚠️ Source file not found: {src_path}")
        continue

    with open(src_path, "r", encoding="utf-8") as f:
        stories = json.load(f)

    if len(stories) != 540:
        print(f"⚠️ Unexpected number of stories in {src_path}: {len(stories)} (expected 540)")
        continue

    result = {}

    for idx, story in enumerate(stories):
        story_number = idx // 180               # 0..2
        relative_index = idx % 180              # 0..179
        part = relative_index // 30             # 0..5
        unit = relative_index % 30              # 0..29

        # Yangi kalitlar mavjud bo'lmasa, ularni yaratamiz
        result.setdefault(str(part), {})
        result[str(part)].setdefault(str(unit), {})
        result[str(part)][str(unit)][str(story_number)] = story

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(stories)} stories -> {target_path}")
