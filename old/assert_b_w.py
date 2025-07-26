import json

WORDS_JSON_PATH = "./en/beginner/words.json"
W_TXT_PATH = "./en/beginner/w.txt"

def load_words_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [entry.get("w", "").strip() for entry in data]

def load_txt_words(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def compare_words(json_words, txt_words):
    if len(json_words) != len(txt_words):
        print(f"❌ UZUNLIK MOS EMAS: JSON={len(json_words)}, TXT={len(txt_words)}")
        return False

    all_match = True
    for i, (j_word, t_word) in enumerate(zip(json_words, txt_words)):
        if j_word != t_word:
            print(f"❌ Mos emas: index {i} -> JSON='{j_word}' vs TXT='{t_word}'")
            all_match = False

    if all_match:
        print("✅ Barcha so‘zlar to‘liq mos!")
    return all_match

def main():
    json_words = load_words_json(WORDS_JSON_PATH)
    txt_words = load_txt_words(W_TXT_PATH)
    compare_words(json_words, txt_words)

if __name__ == "__main__":
    main()
