"""Read-only lexical candidate screen; it does not prove semantic independence."""
from pathlib import Path
import hashlib
import json
import re
import unicodedata

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
ROOTS = [
    WORKSPACE / 'recovery-t20/addendum',
    WORKSPACE / 'recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008',
    HERE / 'readbacks',
]
TERMS = ['shafii', 'shaafii', 'shafee', 'shafi', 'الشافعي', 'khumayyis',
         'خميس', 'ishari', 'ishaaree', 'العشاري', 'four imams', 'four imaams',
         '1OrvxcNHsfcivltwx2G2s0hNdnos7VPxn', 'known by deep thought',
         'reached by the intellect', 'takes the place of actually witnessing',
         'not reached by the intellect']

def normalize(text):
    text = unicodedata.normalize('NFKD', text).lower()
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9\u0600-\u06ff]+', '', text)

files, hits = [], []
for root in ROOTS:
    if not root.is_dir():
        raise FileNotFoundError(root)
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {
            '.md', '.json', '.jsonl', '.txt', '.py', '.lean', '.yaml', '.yml', '.csv'
        }:
            continue
        data = path.read_bytes()
        try:
            content = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        record_path = str(path.relative_to(WORKSPACE))
        files.append({'path': record_path, 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest()})
        for line_number, line in enumerate(content.splitlines(), 1):
            normalized = normalize(line)
            matched = [term for term in TERMS if normalize(term) in normalized]
            if matched:
                hits.append({'path': record_path, 'line': line_number,
                             'terms': matched, 'text': line})

result = {
    'scope': 'Lexical candidate screen of recovered addendum/checkpoint text and eight pinned daee readbacks. A negative match is not a formal proof of absent implicit dependence.',
    'normalization': 'NFKD, lowercase, remove combining marks and punctuation/spacing',
    'terms': TERMS, 'files_scanned': len(files),
    'total_bytes': sum(f['bytes'] for f in files), 'hits': hits, 'files': files,
}
(HERE / 'CITATION_SCREEN.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({'files_scanned': len(files), 'total_bytes': result['total_bytes'],
                  'candidate_hits': len(hits)}, indent=2))
