"""Independent direct-signature oracle and deliberately false-model controls."""
from pathlib import Path
import hashlib
import json
from collections import defaultdict

BASE = Path(__file__).resolve().parent
code_path = BASE / 'contract_check.py'
raw = json.loads((BASE.parent / 'sources/source_rows.json').read_text())
records = raw['records']
expected = {}
for name, columns in [
    ('content_only', ()),
    ('content_and_voice', ('voice',)),
    ('content_voice_and_work_exclusion', ('voice', 'work')),
]:
    groups = defaultdict(set)
    for r in records:
        value = {'voice': r['role'].startswith('direct_exposition'), 'work': r['work_id']}
        groups[tuple(r['antecedents'])].add(tuple(value[k] for k in columns))
    expected[name] = max(len(g) for g in groups.values())
if expected != {'content_only': 1, 'content_and_voice': 2, 'content_voice_and_work_exclusion': 3}:
    raise AssertionError('direct-signature oracle mismatch')
result = json.loads((BASE / 'RESULT.normal.json').read_text())
if result['minimum_alphabets'] != expected:
    raise AssertionError('partition checker differs from direct oracle')
source = code_path.read_text()
mutations = {
    'erase_named_work_operations': ('for action in actions:', 'for action in ["copy"]:'),
    'erase_voice_distinction': ("roles = [r['role'].startswith('direct_exposition') for r in records]", 'roles = [False for r in records]'),
}
reports=[]
for name,(old,new) in mutations.items():
    if source.count(old) != 1:
        raise AssertionError('mutation target not unique')
    namespace = {'__file__': str(code_path), '__name__': 'deliberate_mutation'}
    try:
        exec(compile(source.replace(old,new), str(code_path), 'exec'), namespace)
        bad = namespace['analyse']()
        if bad['minimum_alphabets'] == expected:
            raise AssertionError('MUTATION_SURVIVED')
        reports.append({'mutation':name,'rejected':True,'reason':'incorrect minimum alphabets', 'observed':bad['minimum_alphabets']})
    except AssertionError as e:
        if str(e)=='MUTATION_SURVIVED':
            raise
        reports.append({'mutation':name,'rejected':True,'reason':str(e)})
print(json.dumps({'status':'PASS','direct_signature_oracle':expected,'deliberately_false_models':reports,
 'scope':'Own independent code-path control, not independent person/reviewer or source interpretation validation.'},indent=2))
