import os
import json
import re

# 📁 Fayl yo'llari
BASE_DIR = './en/essential'
TXT_FILES = [f'story{i}.txt' for i in range(1, 7)]
STORY2_JSON = os.path.join(BASE_DIR, 'story2.json')
STORY3_JSON = os.path.join(BASE_DIR, 'story3.json')

# 📘 JSON fayllarni yuklab olish
with open(STORY2_JSON, 'r', encoding='utf-8') as f:
    story2_data = json.load(f)

with open(STORY3_JSON, 'r', encoding='utf-8') as f:
    story3_data = json.load(f)

assert len(story2_data) == 180, "❌ story2.json da elementlar soni 180 emas!"
assert len(story3_data) == 180, "❌ story3.json da elementlar soni 180 emas!"

# ✒️ Hikoyalarni yig‘ish
story1_list = []  # For story2.json
story2_list = []  # For story3.json

def get_next_nonempty_line(lines, start_index):
    """Bo'sh qatorlarni o'tkazib, keyingi mazmunli qatorni va indexni qaytaradi"""
    i = start_index
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i >= len(lines):
        return None, i
    return lines[i], i


def parse_unit_block(lines, file_name):
    units = []
    i = 0
    while i < len(lines):
        if re.match(r'^\s*Unit\s+\d+\s*$', lines[i]):
            unit_title = lines[i].strip()
            i += 1

            # Story 1 title
            line, i = get_next_nonempty_line(lines, i)
            if not line or not re.match(r'^Story 1:\s*(.+)', line):
                raise ValueError(f"❌ {file_name}, {unit_title} - Story 1 sarlavhasi topilmadi: '{line}'")
            h1 = line.replace("Story 1:", "").strip()
            i += 1

            # Story 1 body
            b1_lines = []
            while i < len(lines) and not re.match(r'^Story 2:\s*(.+)', lines[i]):
                b1_lines.append(lines[i])
                i += 1
            b1 = '\n'.join([line.strip() for line in b1_lines]).strip()

           # Story 2 title
            line, i = get_next_nonempty_line(lines, i)
            if not line or not re.match(r'^Story 2:\s*(.+)', line):
                raise ValueError(f"❌ {file_name}, {unit_title} - Story 2 sarlavhasi topilmadi: '{line}'")
            h2 = line.replace("Story 2:", "").strip()
            i += 1

            # Story 2 body
            b2_lines = []
            while i < len(lines) and not re.match(r'^Unit\s+\d+\s*$', lines[i]):
                b2_lines.append(lines[i])
                i += 1
            b2 = '\n'.join([line.strip() for line in b2_lines]).strip()

            units.append(((h1, b1), (h2, b2)))
        else:
            i += 1
    return units

# 🔁 Har bir faylni o‘qib, hikoyalarni yig‘amiz
for fname in TXT_FILES:
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
        try:
            units = parse_unit_block(lines, fname)
            for (h1, b1), (h2, b2) in units:
                story1_list.append({'h': h1, 'b': b1})
                story2_list.append({'h': h2, 'b': b2})
        except ValueError as e:
            print(str(e))
            exit(1)

# 🔍 Tekshiruv
assert len(story1_list) == 180, f"❌ Story 1 hikoyalar soni noto‘g‘ri: {len(story1_list)}"
assert len(story2_list) == 180, f"❌ Story 2 hikoyalar soni noto‘g‘ri: {len(story2_list)}"

# 📝 Ma'lumotlarni .json fayllarga joylash
for i in range(180):
    story2_data[i]['h'] = story1_list[i]['h']
    story2_data[i]['b'] = story1_list[i]['b']
    story3_data[i]['h'] = story2_list[i]['h']
    story3_data[i]['b'] = story2_list[i]['b']

# 💾 Yozish
with open(STORY2_JSON, 'w', encoding='utf-8') as f:
    json.dump(story2_data, f, ensure_ascii=False, indent=2)

with open(STORY3_JSON, 'w', encoding='utf-8') as f:
    json.dump(story3_data, f, ensure_ascii=False, indent=2)

print("✅ Hikoyalar muvaffaqiyatli joylandi: story2.json (Story 1), story3.json (Story 2)")
