#!/usr/bin/env python3
"""
Compile Tayport history articles into a single PDF via Pandoc.

Usage:
    cd /home/ubuntu/tayport-community-website
    python3 _book/compile.py

Output: _book/tayport-history.pdf  (and .md for inspection)
"""

import os
import re
import subprocess
import sys

HISTORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'history')
OUT_DIR = os.path.dirname(__file__)
OUT_MD = os.path.join(OUT_DIR, 'tayport-history.md')
OUT_PDF = os.path.join(OUT_DIR, 'tayport-history.pdf')

CATEGORY_ORDER = ['Local History', 'Memories', 'Poetry']
CATEGORY_KEYWORD = {
    'Local History': 'local-history',
    'Memories':      'local-memories',
    'Poetry':        'local-poetry',
}

FRONT_MATTER_RE = re.compile(r'^---\s*\n.*?---\s*\n', re.DOTALL)
JEKYLL_LINK_RE  = re.compile(r'\[([^\]]+)\]\(/history\)')
BACK_LINK_RE    = re.compile(r'\n---\n\n\[Back to History\]\(/history\)\s*$')


def strip_front_matter(text):
    return FRONT_MATTER_RE.sub('', text, count=1)


def clean_body(text):
    text = JEKYLL_LINK_RE.sub(r'\1', text)
    text = BACK_LINK_RE.sub('', text)
    # Remove layout-specific category line (e.g. "*Local History*")
    text = re.sub(r'^\*(Local History|Memories|Poetry)\*\s*\n', '', text, flags=re.MULTILINE)
    return text.strip()


def category_for_file(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read(500)
    # Keywords field uses: "tayport, memories, history" or "tayport, local poetry, history"
    if 'memories' in raw.lower() and 'local history' not in raw.lower():
        return 'Memories'
    if 'poetry' in raw.lower():
        return 'Poetry'
    return 'Local History'


def title_for_file(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^title:\s*(.+)', line)
            if m:
                # Strip " - Tayport Community" suffix
                return re.sub(r'\s*-\s*Tayport Community\s*$', '', m.group(1).strip())
    return os.path.basename(path).replace('.md', '').replace('-', ' ').title()


def collect_articles():
    articles = {cat: [] for cat in CATEGORY_ORDER}
    for fname in sorted(os.listdir(HISTORY_DIR)):
        if not fname.endswith('.md') or fname == 'index.md':
            continue
        path = os.path.join(HISTORY_DIR, fname)
        cat = category_for_file(path)
        title = title_for_file(path)
        articles[cat].append((title, path))
    for cat in articles:
        articles[cat].sort(key=lambda t: t[0])
    return articles


def build_markdown(articles):
    lines = []
    lines.append('% Tayport: A Community History')
    lines.append('% Compiled from tayport.org.uk')
    lines.append('% 2003 – 2025')
    lines.append('')

    for cat in CATEGORY_ORDER:
        if not articles[cat]:
            continue
        lines.append(f'# {cat}')
        lines.append('')
        for title, path in articles[cat]:
            with open(path, encoding='utf-8') as f:
                raw = f.read()
            body = clean_body(strip_front_matter(raw))
            lines.append(f'## {title}')
            lines.append('')
            lines.append(body)
            lines.append('')
            lines.append('---')
            lines.append('')

    return '\n'.join(lines)


def main():
    print('Collecting articles…')
    articles = collect_articles()
    for cat, items in articles.items():
        print(f'  {cat}: {len(items)} articles')

    print('Building combined Markdown…')
    md = build_markdown(articles)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f'  Written: {OUT_MD}')

    print('Running Pandoc…')
    cmd = [
        'pandoc', OUT_MD,
        '-o', OUT_PDF,
        '--pdf-engine=wkhtmltopdf',
        '--metadata', 'lang=en-GB',
        '--toc',
        '--toc-depth=2',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print('PDF generation failed. The combined Markdown is still at:')
        print(f'  {OUT_MD}')
        print('Error:', result.stderr[:500])
        sys.exit(1)

    print(f'  Written: {OUT_PDF}')
    print('Done.')


if __name__ == '__main__':
    main()
