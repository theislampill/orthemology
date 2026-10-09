"""Reproduce local paragraph locators from the exact received HTML; no emendation."""
import html
import pathlib
import re
root = pathlib.Path(__file__).parent
for section in ('001', '003'):
    source = (root / f'safadiyya-{section}.html').read_text(encoding='utf8')
    body = source.split('</h1>', 1)[1].split('<h6>', 1)[0]
    body = re.sub('<[^>]+>', '\n', body)
    paragraphs = [html.unescape(x).strip() for x in body.splitlines() if html.unescape(x).strip()]
    output = ''.join(f'SF-S{section}-L{i:04d} {x}\n' for i, x in enumerate(paragraphs, 1))
    (root / f'safadiyya-{section}.txt').write_text(output, encoding='utf8')
