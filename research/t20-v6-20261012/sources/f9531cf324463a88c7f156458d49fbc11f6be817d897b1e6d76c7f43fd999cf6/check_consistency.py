"""Static custody/interface checks. This program never invokes or impersonates Lean."""
from pathlib import Path
import hashlib,json,re,sys
R=Path(__file__).resolve().parents[1]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
checks=[]
def check(condition,label):
    checks.append({'check':label,'pass':bool(condition)})
    if not condition:raise ValueError(label)
def strip_comments(text):
    # Nested Lean block comments and line comments; preserve code offsets/newlines.
    out=[];i=0;depth=0;string=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):depth+=1;out.extend('  ');i+=2
            elif text.startswith('-/',i):depth-=1;out.extend('  ');i+=2
            else:out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif string:
            if text[i]=='\\' and i+1<len(text):out.extend('  ');i+=2
            else:
                if text[i]=='"':string=False
                out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif text.startswith('/-',i):depth=1;out.extend('  ');i+=2
        elif text.startswith('--',i):
            j=text.find('\n',i)
            if j<0:j=len(text)
            out.extend(' '*(j-i));i=j
        elif text[i]=='"':string=True;out.append(' ');i+=1
        else:out.append(text[i]);i+=1
    if depth:raise ValueError('Unclosed Lean block comment')
    return ''.join(out)
inv=read('provenance/FORMAL_INVENTORY.json');ts=inv['theorems']
check(len(ts)==inv['theorem_count']==130,'130 inventoried explicit theorem candidates')
check(len({t['declaration'] for t in ts})==130,'Unique declaration identities')
check(len({t['module'] for t in ts})==15,'15 inventoried modules')
all_scanned=[]
for p in sorted((R/'formal').rglob('*.lean')):
    text=p.read_text();clean=strip_comments(text)
    check(not re.search(r'\b(sorry|admit|sorryAx|axiom)\b',clean),f'No explicit proof-hole/axiom token: {p.relative_to(R)}')
    for m in re.finditer(r'^\s*(?:private\s+)?(?:protected\s+)?theorem\s+([A-Za-z0-9_\'.]+)',clean,re.M):
        line=clean.count('\n',0,m.start())+1
        all_scanned.append((str(p.relative_to(R)),m.group(1)))
for t in ts:
    p=R/t['source'];check(h(p)==t['source_sha256'],'Candidate source hash: '+t['declaration'])
    check((t['source'],t['declaration'].split('.')[-1]) in all_scanned,'Theorem token present: '+t['declaration'])
    check(t['compilation']=='NOT_EXECUTED_HOST_BLOCKED' and t['observed_type'] is None and t['axiom_audit'] is None and t['olean'] is None,'No invented formal evidence: '+t['declaration'])
check(len(all_scanned)==130,'No unlisted explicit theorem candidate')
check(not list((R/'formal').rglob('*.olean')),'Zero current target olean artifacts')
cat=read('NEW_RESULT_CATALOGUE.json')['result_sections'];byid={x['id']:x for x in cat}
check(len(cat)==len(byid)==39,'39 unique ordinary result sections')
for x in cat:
    p=R/x['proof_file'];check(h(p)==x['proof_file_sha256'],'Proof file hash: '+x['id'])
    check(hashlib.sha256(x['exact_section'].encode()).hexdigest()==x['section_sha256'] and x['exact_section'] in p.read_text(),'Exact section binding: '+x['id'])
binds=read('P03_CONSUMER_BINDINGS.json')['bindings']
check(len(binds)==34,'34 P03 bindings')
for x in binds:
    check(x['id'] in byid and x['section_sha256']==byid[x['id']]['section_sha256'],'P03 section binding: '+x['id'])
    check(not x['kernel_verified'] and not x['automatic_P03_kernel_axiom_permission'],'P03 evidence level: '+x['id'])
for x in read('P03_CONSUMER_BINDINGS.json')['code_bindings']:
    check(h(R/x['path'])==x['sha256'],'P03 code hash: '+x['path'])
dag=read('P02_INTERNAL_DEPENDENCY_MAP.json');ids={x['id'] for x in dag['nodes']}
for e in dag['edges']:
    check(e['source'] in ids and e['target'] in ids,'Dependency endpoints: '+e['source']+' -> '+e['target'])
# Detect cycles with a colour DFS, independently of the documents' DAG claim.
adj={x:[] for x in ids}
for e in dag['edges']:adj[e['source']].append(e['target'])
colour={x:0 for x in ids}
def visit(x):
    if colour[x]==1:raise ValueError('Cycle at '+x)
    if colour[x]==2:return
    colour[x]=1
    for y in adj[x]:visit(y)
    colour[x]=2
for x in ids:visit(x)
check(True,'Research dependency graph acyclic')
for item in read('provenance/PROPOSED_STATEMENT_MAPPING.json')['mappings']:
    for x in item['proposal_outputs']:check(h(R/x['path'])==x['sha256'],'Proposal/preimage map: '+x['path'])
for n in ('FINAL_NORMAL','FINAL_OPTIMISED','FINAL_POST_MUTATION'):
    rec=read('evidence/'+n+'/COMMAND.json')
    check(rec['exit']==0,'Executed suite exit: '+n)
    for p,digest in rec['source_sha256'].items():check(h(R/p)==digest,'Executed source identity: '+n+':'+p)
    stderr=(R/'evidence'/n/'stderr.bin').read_bytes();check(hashlib.sha256(stderr).hexdigest()==rec['stderr_sha256'],'Suite raw stderr hash: '+n)
    check(b'Ran 31 tests' in stderr and stderr.rstrip().endswith(b'OK'),'31-test readback: '+n)
mut=read('evidence/MUTATION_RESULTS.json');check(len(mut)==6,'Six mutation controls')
for m in mut:check(m['detected'] and m['result']['failures']==1 and m['result']['errors']==0 and m['exit']==1,'Genuine assertion kill: '+m['id'])
check(read('FORMAL_COVERAGE.json')['formal_source_complete_for_all_obligations'] is False,'Missing formal source not concealed')
check(read('OBLIGATION_RESULTS.json')['full_exhaustion_certified'] is False,'No false full-exhaustion claim')
summary={'status':'PASS','scope':'STATIC_CUSTODY_INTERFACE_AND_RECORDED_TEST_CONSISTENCY_ONLY','checks':len(checks),'kernel_evidence':False,'rows':checks}
(R/'evidence/FINAL_CONSISTENCY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
