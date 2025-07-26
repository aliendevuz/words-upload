import os
import shutil
from pathlib import Path

# Manba va manzil papkalar
source_base = Path("../assets/v1/en/essential/picture")
destination_base = Path("../assets/en/essential/picture")

# Har bir part va unit bo'yicha rasm fayllarini ko'chirish
for part in range(6):
    for unit in range(30):
        src_dir = source_base / str(part) / str(unit)
        dest_dir = destination_base / str(part) / str(unit)
        if src_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
            for img_file in src_dir.glob("*.jpg"):
                shutil.copy(img_file, dest_dir / img_file.name)
