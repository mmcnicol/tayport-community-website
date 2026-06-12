#!/usr/bin/env python3
"""
Read dimensions from local JPEG files and update photo .md files to use
HTML <img> tags with explicit width/height, preventing layout shift.

Usage:
    cd /home/ubuntu/tayport-community-website
    python3 _mysql-backups/add_photo_dimensions.py
"""

import os, re
from PIL import Image

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(ROOT, 'media')
PHOTO_DIR = os.path.join(ROOT, 'photo')

# Markdown image: !["alt"](url)  →  <img src="url" alt="alt" width="W" height="H">
MD_IMG_RE = re.compile(r'!\["([^"]*?)"\]\((https://tayport\.org\.uk/media/\S+?)\)')


def img_dims(photo_num):
    path = os.path.join(MEDIA_DIR, f'{photo_num:03d}.jpg')
    if not os.path.exists(path):
        return None
    try:
        with Image.open(path) as img:
            return img.size  # (width, height)
    except Exception as e:
        print(f'  WARN photo {photo_num}: {e}')
        return None


def update_md(photo_num, width, height):
    path = os.path.join(PHOTO_DIR, f'{photo_num}.md')
    if not os.path.exists(path):
        return False

    with open(path, encoding='utf-8') as f:
        text = f.read()

    def replace(m):
        alt, url = m.group(1), m.group(2)
        return f'<img src="{url}" alt="{alt}" width="{width}" height="{height}">'

    new_text = MD_IMG_RE.sub(replace, text)
    if new_text == text:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return True


def main():
    updated = 0
    missing = 0
    for n in range(1, 405):
        dims = img_dims(n)
        if dims is None:
            missing += 1
            continue
        w, h = dims
        if update_md(n, w, h):
            updated += 1

    print(f'Updated: {updated}  |  No local image: {missing}  |  Total: 404')


if __name__ == '__main__':
    main()
