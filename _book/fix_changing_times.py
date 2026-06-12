#!/usr/bin/env python3
"""
Parse the mangled HTML-table remnants in history/changing-times.md and
rewrite it as a clean Markdown list, preserving all data.

Usage:
    cd /home/ubuntu/tayport-community-website
    python3 _book/fix_changing_times.py
"""

import re, os, sys

SRC = os.path.join(os.path.dirname(__file__), '..', 'history', 'changing-times.md')
LINK_RE  = re.compile(r'\[([^\]]+)\]\([^)]+\)')
ADDR_RE  = re.compile(r'^\s{1,8}(\d+\s+(?:Castle|Broad)\s+Street)\s*$', re.I)
HAS_LINK = re.compile(r'\[')
YEARS    = ['1951', '1951–62', '1981', '1985', '2003']


def parse_cells(lines):
    """
    Convert the raw lines between two address entries into a list of
    (name, type_text) tuples or None (empty cell), one per year column.
    """
    cells = []
    name  = None
    typ   = ''

    def commit(n, t):
        cells.append((n.strip(), t.strip()))

    for line in lines:
        # Compute indent from the ORIGINAL line (before rstrip) so that
        # whitespace-only lines like '     ' have indent=5, not 0.
        indent        = len(line) - len(line.lstrip())
        text          = LINK_RE.sub(r'\1', line).strip()
        is_whitespace = (text == '')

        if is_whitespace:
            if indent <= 1:
                # Blank line or single-space noise — skip
                continue
            if indent >= 4:
                # Whitespace-only at 4+ spaces = empty table cell
                if name:
                    commit(name, typ)
                    name = None
                    typ  = ''
                cells.append(None)
            # 2-3 space whitespace = row separator noise — skip
            continue

        # Has content
        if indent >= 6:
            if HAS_LINK.search(line):
                # A link at 6-space indent is actually an occupant name
                # (happens when the HTML <a> was inside <td> at the same
                # depth as <em> tags)
                if name:
                    commit(name, typ)
                    typ = ''
                name = text
            else:
                # Business type (sub-line of current occupant)
                if name:
                    typ = (typ + ' ' + text).strip() if typ else text
        elif indent >= 2:
            # New occupant name at 2–5 space indent
            if name:
                commit(name, typ)
                typ = ''
            name = text

    if name:
        commit(name, typ)

    return cells


def cells_to_markdown(address, cells):
    """Format an address + its cell list as Markdown."""
    entries = []
    for i, cell in enumerate(cells):
        if i >= len(YEARS):
            break
        if cell is None:
            continue
        n, t = cell
        if not n:
            continue
        entry = f'- **{YEARS[i]}**: {n}'
        if t:
            entry += f' — {t}'
        entries.append(entry)
    if not entries:
        return ''
    return f'**{address}**\n' + '\n'.join(entries)


def main():
    with open(SRC, encoding='utf-8') as f:
        raw = f.read()

    # Split off front-matter
    fm_end = raw.index('---', 3) + 3          # end of closing ---
    front  = raw[:fm_end]
    body   = raw[fm_end:]

    lines = body.split('\n')

    # Collect intro (before first address) and footer (after last data)
    intro_lines   = []
    table_groups  = []   # [(address, [lines])]
    footer_lines  = []

    cur_addr  = None
    cur_lines = []
    in_footer = False

    for line in lines:
        if in_footer:
            footer_lines.append(line)
            continue

        addr_m = ADDR_RE.match(line)
        if addr_m:
            if cur_addr:
                table_groups.append((cur_addr, cur_lines))
            elif cur_lines:
                # Lines before first address = still intro
                intro_lines.extend(cur_lines)
            cur_addr  = addr_m.group(1).strip()
            cur_lines = []
            continue

        if cur_addr is None:
            intro_lines.append(line)
        else:
            # Check for footer sentinel
            stripped = line.strip()
            if stripped.startswith('Please help') or (stripped == '---' and not any(
                    ADDR_RE.match(l) for l in cur_lines)):
                table_groups.append((cur_addr, cur_lines))
                cur_addr  = None
                cur_lines = []
                in_footer = True
                footer_lines.append(line)
            else:
                cur_lines.append(line)

    if cur_addr:
        table_groups.append((cur_addr, cur_lines))

    # Build output
    out = [front, '']
    out.append('## Changing Times')
    out.append('')
    out.append('*Local History*')
    out.append('')

    intro_text = '\n'.join(intro_lines)
    # Extract the single intro paragraph
    m = re.search(r'(If you had taken.+?shed light on just that:)', intro_text, re.DOTALL)
    if m:
        out.append(m.group(1).strip())
        out.append('')

    # Separator to show year columns
    out.append('*Year columns: 1951 · 1951–62 · 1981 · 1985 · 2003*')
    out.append('')

    # Street-section headings
    prev_street = None
    for address, cell_lines in table_groups:
        street = 'Broad Street' if 'Broad' in address else 'Castle Street'
        if street != prev_street:
            out.append(f'### {street}')
            out.append('')
            prev_street = street

        cells  = parse_cells(cell_lines)
        md_row = cells_to_markdown(address, cells)
        if md_row:
            out.append(md_row)
            out.append('')

    # Footer
    footer_text = '\n'.join(footer_lines).strip()
    if footer_text:
        out.append(footer_text)
        out.append('')
    out.append('[Back to History](/history)')

    result = '\n'.join(out)

    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Wrote {len(table_groups)} address entries to {SRC}')

    # Quick sanity: print first 60 lines
    print()
    print('--- preview (first 60 lines) ---')
    for ln in result.split('\n')[:60]:
        print(ln)


if __name__ == '__main__':
    main()
