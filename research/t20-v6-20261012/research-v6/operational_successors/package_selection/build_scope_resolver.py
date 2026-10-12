"""Build only scope metadata from exact frozen joins; never copies or runs sources.

This extracts explicit fields. Every recorded scope value and range survives
unchanged. It does not turn a reading association into full-body acceptance.
An existing output directory is refused, so reviewed snapshots remain intact.
This is internal fixed-target preparation, not a generally safe public CLI;
it does not implement the materialiser's protected-root/disjointness guards.
"""
from pathlib import Path
import json, hashlib, collections, argparse, re

ROOT = Path.cwd().resolve()
V = ROOT / 't20-v6-20261011'
A = V / 'corpus/admission'
PRIVATE = re.compile(r'Sentinel_(?!primrec\b)|libfile_|https?://chatgpt\.com/(?:c|g)/|file_[a-fA-F0-9]{32}|[?&](?:sig|token|X-Amz-[^=]*)=|-----BEGIN .*PRIVATE KEY', re.I)
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return (json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode()
def read(p): return json.loads(p.read_bytes())
def lines(p):
    return [json.loads(l) for l in p.read_bytes().splitlines() if l.strip()]
def require(x, m):
    if not x: raise ValueError(m)
def safe_ledger_name(value):
    p = Path(value).resolve()
    name = str(p.relative_to(ROOT))
    require(not PRIVATE.search(name), 'private ledger name')
    return name

def build(out):
    require(not out.exists(), 'output already exists')
    files = [A/'V6_READING_ASSOCIATIONS.jsonl', A/'READING_LEDGER_SNAPSHOTS.json',
             A/'TERMINAL_PHYSICAL_SCOPE_OVERLAY.jsonl']
    raw_inputs = [p.read_bytes() for p in files]
    inputs = [{'name':p.name, 'sha256':sha(raw)} for p,raw in zip(files,raw_inputs)]
    associations = [json.loads(l) for l in raw_inputs[0].splitlines() if l.strip()]
    snapshots = json.loads(raw_inputs[1])
    physical = [json.loads(l) for l in raw_inputs[2].splitlines() if l.strip()]
    snapshot_by_name = {str(Path(r['ledger']).resolve()):r for r in snapshots}
    ledger_bindings = {}; by_hash = collections.defaultdict(list); issues = []
    for r in associations:
        name = str(Path(r['ledger']).resolve())
        if name not in ledger_bindings:
            frozen = snapshot_by_name.get(name)
            require(frozen is not None, 'association has no ledger snapshot')
            path = Path(name)
            current = sha(path.read_bytes()) if path.is_file() else None
            ledger_bindings[name] = {'ledger_name':safe_ledger_name(name),
                'reviewed_ledger_sha256':frozen['sha256'],
                'current_ledger_sha256':current,
                'historical_snapshot_drift':current != frozen['sha256']}
            if current != frozen['sha256']:
                issues.append(dict(ledger_bindings[name]))
        scope = r.get('recorded_scope'); ranges = r.get('ranges', [])
        require(not PRIVATE.search(json.dumps(scope, ensure_ascii=False)), 'private scope values require exact review')
        item = dict(ledger_bindings[name]); item.update(pointer=r['pointer'],
            recorded_scope=scope, ranges=ranges,
            scope_value_sha256=sha(canonical(scope)), range_value_sha256=sha(canonical(ranges)),
            qualification=r.get('qualification'))
        require(not PRIVATE.search(item['pointer']), 'private pointer requires exact review')
        by_hash[r['source_sha256']].append(item)
    physical_by_hash = {r['sha256']:r for r in physical}
    physical_indices = {r['sha256']:i+1 for i,r in enumerate(physical)}
    require(len(physical_by_hash)==len(physical), 'duplicate physical identity')
    rows=[]
    for h in sorted(set(physical_by_hash)|set(by_hash)):
        r=physical_by_hash.get(h,{})
        roles=[]
        for e in r.get('scope_evidence',[]):
            # Field-bound summary, with the complete original scope separately bound below.
            v={k:e[k] for k in ('kind','role','qualification','scope_credit') if k in e}
            if v and v not in roles: roles.append(v)
        require(not PRIVATE.search(json.dumps(roles,ensure_ascii=False)), 'private role values require exact review')
        rows.append({'sha256':h, 'bytes':r.get('bytes'),
            'artifact_axis':r.get('artifact_axis','OUTSIDE_PHYSICAL_CENSUS_SCOPED_IDENTITY'),
            'physical_scope_row_binding':({'overlay_sha256':inputs[2]['sha256'],
                'line':physical_indices[h], 'row_sha256':sha(canonical(r))} if r else None),
            'role_evidence_value_sha256':sha(canonical(r.get('scope_evidence',[]))) if r else None,
            'terminal_scope_kind':r.get('terminal_scope_kind','SCOPED_ASSOCIATION_OUTSIDE_PHYSICAL_INPUT_CENSUS'),
            'role_qualifications':roles, 'reading_scopes':by_hash.get(h,[]),
            'fresh_execution_inferred':False, 'import_closure_inferred':False,
            'distribution_eligibility_inferred':False})
    # Verify full multiset preservation of actual scope/range values, including duplicates.
    expected=collections.Counter((r['source_sha256'],r['ledger'],r['pointer'],
        sha(canonical(r.get('recorded_scope'))),sha(canonical(r.get('ranges',[])))) for r in associations)
    reverse={v['ledger_name']:k for k,v in ledger_bindings.items()}
    actual=collections.Counter((row['sha256'],reverse[r['ledger_name']],r['pointer'],
        sha(canonical(r['recorded_scope'])),sha(canonical(r['ranges'])))
        for row in rows for r in row['reading_scopes'])
    # Normalize only the outer ledger locator, never a scope/range value.
    normalized=collections.Counter((h,str(Path(l).resolve()),p,s,rs) for (h,l,p,s,rs),n in expected.items() for _ in range(n))
    require(normalized==actual,'scope/range multiset changed')
    axis_expected=collections.Counter((r['sha256'],r.get('artifact_axis'),sha(canonical(r.get('scope_evidence',[])))) for r in physical)
    axis_actual=collections.Counter((r['sha256'],r['artifact_axis'],r['role_evidence_value_sha256']) for r in rows if r['physical_scope_row_binding'])
    require(axis_expected==axis_actual,'physical artifact axis/role evidence changed')
    payload=b''.join(canonical(r) for r in rows)
    require(not PRIVATE.search(payload.decode()),'full output private marker requires exact review')
    out.mkdir()
    (out/'SOURCE_SCOPE_RESOLVER.jsonl').write_bytes(payload)
    receipt={'schema':'t20-v6-source-scope-resolver-v1','status':'SCOPE_METADATA_PREPARATION_NOT_DISTRIBUTION_SELECTION',
        'inputs':inputs,'identities':len(rows),'exact_association_records':len(associations),
        'scope_and_range_multiset_equal':True,'complete_recorded_scope_values_preserved':True,
        'physical_axis_and_role_evidence_multiset_equal':True,
        'artifact_axes':dict(collections.Counter(r['artifact_axis'] for r in rows)),
        'full_output_private_marker_matches':0,'ledger_drift_records':issues,
        'resolver_sha256':sha(payload),'ledger_count':len(ledger_bindings),
        'limits':['Outer local source paths omitted; exact source selection and aliases are a separate resolver.',
                  'A recorded full/delta/selected/role scope retains its original meaning.',
                  'Ledger identity/pointer is provenance; no whole-ledger publication is inferred.',
                  'Scientific fixtures and actual source bodies were not changed or executed.']}
    (out/'SCOPE_RESOLVER_VERIFICATION.json').write_bytes(canonical(receipt))
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    build(ap.parse_args().output)
