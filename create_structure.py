import os

# Config
languages = ['en']
collections = ['beginner', 'essential']
native_lang = 'uz'
parts = range(6)
units = range(30)
word_indices = range(20)
story_numbers = range(3)
story_chunks = range(5)
audio_fields = ['w', 'd', 's']

# Helper
def ensure_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            pass

# Base path
base = os.path.abspath('../assets')

# Root meta
ensure_file(os.path.join(base, 'meta.json'))

for lang in languages:
    lang_path = os.path.join(base, lang)
    ensure_file(os.path.join(lang_path, 'meta.json'))
    ensure_file(os.path.join(lang_path, 'image.jpg'))

    for col in collections:
        col_path = os.path.join(lang_path, col)
        ensure_file(os.path.join(col_path, 'meta.json'))
        ensure_file(os.path.join(col_path, 'image.jpg'))

        # Words and stories
        ensure_file(os.path.join(col_path, 'words.json'))
        ensure_file(os.path.join(col_path, 'stories.json'))

        # Native translation
        native_path = os.path.join(col_path, native_lang)
        ensure_file(os.path.join(native_path, 'words.json'))
        ensure_file(os.path.join(native_path, 'stories.json'))

        # Picture structure
        for p in parts:
            part_path = os.path.join(col_path, 'picture', str(p))
            ensure_file(os.path.join(part_path, 'image.jpg'))
            for u in units:
                unit_path = os.path.join(part_path, str(u))
                # Story pictures
                for s in story_numbers:
                    story_path = os.path.join(unit_path, str(s))
                    ensure_file(os.path.join(story_path, 'head.jpg'))
                    for i in story_chunks:
                        ensure_file(os.path.join(story_path, f'{i}.jpg'))
                # Word pictures
                for i in word_indices:
                    ensure_file(os.path.join(unit_path, f'{i}.jpg'))

        # Audio structure
        for p in parts:
            for u in units:
                for w in word_indices:
                    word_path = os.path.join(col_path, 'audio', str(p), str(u), str(w))
                    # Word audio fields
                    for f in audio_fields:
                        ensure_file(os.path.join(word_path, f'{f}.mp3'))
                    # Story audio
                    for s in story_numbers:
                        story_audio = os.path.join(word_path, str(s))
                        ensure_file(os.path.join(story_audio, 'head.mp3'))
                        for i in story_chunks:
                            ensure_file(os.path.join(story_audio, f'{i}.mp3'))
