#!/usr/bin/env python3
"""Read-only integrity and declared cumulative source-budget checks."""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
BLOCK = re.compile(r'<!-- charge ([A-Z0-9 ]+) start -->\n(.*?)\n<!-- charge \1 end -->', re.S)
WORD = re.compile(r"\b[\w]+(?:[’'-][\w]+)*\b")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def word_count(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return len(WORD.findall(text))

def source_blocks():
    rows = []
    for path in sorted(ROOT.rglob('*.md')):
        text = path.read_text()
        matches = list(BLOCK.finditer(text))
        assert len(re.findall(r'<!-- charge .*? start -->', text)) == len(matches), path
        assert len(re.findall(r'<!-- charge .*? end -->', text)) == len(matches), path
        for index, match in enumerate(matches, 1):
            rows.append({
                'file': str(path.relative_to(ROOT)),
                'block': index,
                'sources': match[1].split(),
                'words': word_count(match[2]),
                'text_sha256': digest(match[2].encode()),
            })
    return rows

def verify():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    expected = {row['path'] for row in manifest['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == expected | {'MANIFEST.json'}, (actual-expected, expected-actual)
    for row in manifest['files']:
        data = (ROOT/row['path']).read_bytes()
        assert len(data) == row['bytes'], row['path']
        assert digest(data) == row['sha256'], row['path']
        assert (ROOT/row['path']).suffix.lower() not in {'.zip','.pdf'}, row['path']
    budget = json.loads((ROOT/'SOURCE_BUDGET.json').read_text())
    blocks = source_blocks()
    assert blocks == budget['charged_blocks'], 'Charged text changed'
    totals = {key: 0 for key in budget['sources']}
    for row in blocks:
        for key in row['sources']:
            totals[key] += row['words']
    for key, total in totals.items():
        record = budget['sources'][key]
        assert total == record['derived_words'], (key,total,record)
        assert total <= 200, (key,total)
        assert record['article_body_verbatim_words'] == 0, key
        assert record['bibliographic_verbatim_words_upper_bound'] <= 25, key
    print(json.dumps({'integrity':'PASS','payload_files':len(expected),
                      'source_budget_arithmetic':'PASS','derived_words':totals,
                      'scope':'Checks declared accounting, not attribution completeness or philosophical truth'},indent=2))

if __name__ == '__main__':
    verify()
