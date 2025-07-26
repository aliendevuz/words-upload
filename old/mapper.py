from pathlib import Path
import json
import re

# Fayl joylashuvi
words_path = Path("./en/beginner/words.json")

# JSONni yuklab olish
with open(words_path, "r", encoding="utf-8") as f:
    words = json.load(f)

# Oddiy mapping: asosiy tur mappingi (uz → en)
# Bu mapping faqat birlamchi dominant tur uchun (tp field)
mapping = {
    "fe’l": "verb",
    "fe’l (o‘tgan zamon)": "verb",
    "fe’l / ot": "verb",
    "fe’l / sifat": "verb",
    "fe’l / sifat / ravish": "verb",
    "fe’l/ ot": "verb",
    "fe’l/oldidan keluvchi so‘z": "verb",
    "fe’l/ot": "verb",
    "fe’lning o‘rindoshi": "verb",
    "yordamchi fe’l": "auxiliary verb",

    "ot": "noun",
    "ot (ko‘plik)": "noun",
    "ot (kun nomi)": "noun",
    "ot (oy nomi)": "noun",
    "ot (unvon)": "noun",
    "ot / fe’l": "noun",
    "ot / fe’lning ot shakli": "noun",
    "ot / ravish": "noun",
    "ot / ravish / predlog": "noun",
    "ot / sifat": "noun",
    "ot / sifat / fe’l": "noun",
    "ot / sifat / predlog": "noun",
    "ot / sifat / ravish": "noun",
    "ot / son": "noun",
    "ot / so‘z": "noun",
    "ot / unvon": "noun",
    "ot/fe’l": "noun",
    "ot/fe’lning o‘rindoshi": "noun",
    "ot/old so‘zi": "noun",
    "ot/sifat": "noun",
    "ot/sifat/fe’l": "noun",
    "ot/sifat/ravish": "noun",
    "ot/so‘zlama": "noun",

    "sifat": "adjective",
    "sifat (o‘tgan zamon)": "adjective",
    "sifat / fe’l": "adjective",
    "sifat / olmosh": "adjective",
    "sifat / ot": "adjective",
    "sifat / ot / ravish": "adjective",
    "sifat / ravish": "adjective",
    "sifat / so‘zlashuv": "adjective",
    "sifat/fe’l": "adjective",
    "sifat/grammatika termi": "adjective",
    "sifat/noun": "adjective",
    "sifat/olmosh": "adjective",
    "sifat/ot": "adjective",
    "sifat/ot/fe’l": "adjective",
    "sifat/ravish": "adjective",
    "sifat/son": "adjective",
    "sifat/so‘zlama": "adjective",

    "ravish": "adverb",
    "ravish / predlog": "adverb",
    "ravish / sifat": "adverb",
    "ravish/sifat": "adverb",

    "predlog": "preposition",
    "predlog / bog‘lovchi": "preposition",
    "predlog / bog‘lovchi / ravish": "preposition",
    "predlog / ravish": "preposition",
    "predlog/ ravish": "preposition",
    "predlog/ot": "preposition",
    "predlog/ravish": "preposition",

    "bog‘lovchi": "conjunction",
    "bog‘lovchi / ot": "conjunction",
    "bog‘lovchi / predlog": "conjunction",
    "bog‘lovchi/predlog": "conjunction",
    "bog‘lovchi/ravish": "conjunction",
    "bog‘lovchi/sifat": "conjunction",

    "aniqlovchi": "determiner",
    "aniqlovchi/ot": "determiner",
    "aniqlovchi/ravish": "determiner",
    "determinativ": "determiner",

    "artikl": "article",
    "olmosh": "pronoun",
    "olmosh (pronom)": "pronoun",
    "olmosh / bog‘lovchi": "pronoun",
    "olmosh / ot": "pronoun",
    "olmosh / ravish": "pronoun",
    "olmosh / savol so‘zi": "pronoun",
    "olmosh / sifat": "pronoun",
    "olmosh / son": "pronoun",
    "olmosh/sifat": "pronoun",

    "so‘roq olmoshi": "pronoun",
    "egalik olmoshi": "pronoun",
    "raqam olmoshi": "pronoun",

    "son": "numeral",
    "son / olmosh": "numeral",
    "son / ot": "numeral",
    "son / sifat": "numeral",
    "son/sifat": "numeral",

    "so‘zlama": "expression",
    "so‘z / ibora": "expression",
    "so‘zlashuv": "expression",
    "so‘zlashuv so‘zi": "expression",
    "nom": "expression",
    "ifoda": "expression",

    "inkor so‘zi": "particle",
    "javob so‘zi": "particle",

    "qisqartma": "abbreviation",
    "unvon / so‘z": "title",
    "qaram so‘z": "particle",
    "oldi so‘z": "prefix",
    "oldi so‘zi": "prefix",
    "old qo‘shimcha / olmosh": "prefix",
}

# So‘zlar ro‘yxatini yangilash
for item in words:
    val = item.get("tp")
    if not val:
        continue
    cleaned = val.strip()
    mapped = mapping.get(cleaned)
    item["atp"] = cleaned if not mapped else None
    item["tp"] = mapped if mapped else None

# JSONni qayta saqlash
with open(words_path, "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

"✅ 'tp' ustuni mapping asosida tozalandi va 'atp' ustuni qo‘shildi (agar kerak bo‘lsa)."
