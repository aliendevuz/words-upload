import os
import json
from pathlib import Path
from collections import defaultdict

# Sozlamalar
collections = {
    'beginner': {
        'parts': 4,
        'units': 20,
        'stories_per_unit': 3
    },
    'essential': {
        'parts': 6,
        'units': 30,
        'stories_per_unit': 3
    }
}

source_root = Path("../assets/v1/en")
target_root = Path("../assets/en")


def extract_story_index(story_filename):
    return int(story_filename.stem.replace("story", ""))


def calculate_position(collection, index):
    cfg = collections[collection]
    part = index // (cfg['units'] * cfg['stories_per_unit'])
    unit = (index // cfg['stories_per_unit']) % cfg['units']
    story_number = index % cfg['stories_per_unit']
    return str(part), str(unit), str(story_number)


def collect_and_group(collection, is_native=False):
    folder = "uz" if is_native else ""
    story_dir = source_root / collection / folder
    story_files = sorted(story_dir.glob("story*.json"))

    grouped = defaultdict(lambda: defaultdict(dict))

    for story_file in story_files:
        index = extract_story_index(story_file)
        part, unit, story_number = calculate_position(collection, index)
        with open(story_file, "r", encoding="utf-8") as f:
            content = json.load(f)
        # content is a list of dicts but we only take the first one
        grouped[part][unit][story_number] = content[0] if isinstance(content, list) else content

    return grouped


def save_grouped_json(grouped, out_path):
    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(grouped, f, ensure_ascii=False, indent=2)


def main():
    for collection in collections:
        print(f"📦 Processing: {collection}")

        # EN version
        grouped_en = collect_and_group(collection, is_native=False)
        en_path = target_root / collection / "stories.json"
        save_grouped_json(grouped_en, en_path)
        print(f"✅ EN -> {en_path}")

        # UZ version
        grouped_uz = collect_and_group(collection, is_native=True)
        uz_path = target_root / collection / "uz" / "stories.json"
        save_grouped_json(grouped_uz, uz_path)
        print(f"✅ UZ -> {uz_path}")


if __name__ == "__main__":
    main()
