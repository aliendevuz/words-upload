import json
import os

def make_null_story(lang, index):
    return {
        "h": f"null_of_{lang}_{index}_h",
        "b": f"null_of_{lang}_{index}_b"
    }

def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    story_count = 80
    base_dir = "./en/beginner"

    for story_num in range(1, 4):
        en_file = os.path.join(base_dir, f"story{story_num}.json")
        uz_file = os.path.join(base_dir, "uz", f"story{story_num}.json")

        en_data = [make_null_story("en", i) for i in range(story_count)]
        uz_data = [make_null_story("uz", i) for i in range(story_count)]

        write_file(en_file, en_data)
        write_file(uz_file, uz_data)

    print(f"✅ Beginner hikoya fayllari yaratildi: har birida {story_count} ta item (en/uz)")

if __name__ == "__main__":
    main()
