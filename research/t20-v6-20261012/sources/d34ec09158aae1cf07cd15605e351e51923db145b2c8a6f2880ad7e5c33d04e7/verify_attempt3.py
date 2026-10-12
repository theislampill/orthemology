#!/usr/bin/env python3
"""Fresh-process P01 integrity, evidence, scope and optional test replay verifier.

Checks cryptographic consistency, not authorship, mathematical truth or external
review. Never executes historical commands. Only --rerun-tests executes the new
proposal unittest files from a freshly extracted limited test surface.
"""
from __future__ import annotations
import argparse,datetime,hashlib,io,json,os,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath

class VerificationError(ValueError):pass
SEALS={'MANIFEST.json','RECEIPT.json','RECEIPT.json.sha256'}
A1_SHA='2564e3b5e994e3676f3b63619bc452f1d297300050f9743454f05f4ff38fcbd6'
INPUT_SHA='e4e89e99bd35326e342761d080a9506c8d2b90780fb0a50c6736343ff172ed4c'
RECOVERY_SHA='f8406a721bffdf1f236963a521cb72b4673491bf60f8ed47764a659e77943d5d'
MAIN='03e2604dfcef278b01c60d19b05370fcec4194b6'
TREE='3d06e80277ce39286c94307e0f14b215bc94ed83'

def H(b):return hashlib.sha256(b).hexdigest()
def need(c,s):
    if not c:raise VerificationError(s)
def strict_loads(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            need(k not in d,'duplicate JSON key: '+k);d[k]=v
        return d
    def bad(x):raise VerificationError('nonfinite JSON: '+x)
    try:return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
    except (TypeError,UnicodeError,ValueError) as e:raise VerificationError(str(e)) from e

def binding(data,row,label):
    need(type(row.get('bytes')) is int and row['bytes']>=0,'invalid size '+label)
    need(len(data)==row['bytes'] and H(data)==row['sha256'],'hash/length mismatch '+label)

def detached(b,name):
    try:lines=b.decode().splitlines()
    except UnicodeError as e:raise VerificationError('invalid detached encoding') from e
    need(len(lines)==1,'detached file line count')
    ps=lines[0].split(maxsplit=1)
    need(len(ps)==2 and re.fullmatch('[0-9a-f]{64}',ps[0]) is not None and
         ps[1].lstrip('*')==name,'detached filename/hash format')
    return ps[0]

def unzip(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        need(len(names)==len(set(names)),'duplicate ZIP names')
        for i in infos:
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and
                 ':' not in i.filename and p.as_posix()==i.filename and not i.is_dir(),
                 'unsafe/noncanonical ZIP member '+i.filename)
            need(not stat.S_ISLNK(i.external_attr>>16) and not(i.flag_bits&1),'symlink/encrypted member')
        need(sum(i.file_size for i in infos)<128*1024*1024,'unexpected uncompressed size')
        need(z.testzip() is None,'ZIP CRC failure')
        return {n:z.read(n) for n in names}

def check_layer(data):
    need(SEALS<=set(data),'missing seal member')
    mb=data['MANIFEST.json'];rb=data['RECEIPT.json']
    need(detached(data['RECEIPT.json.sha256'],'RECEIPT.json')==H(rb),'receipt digest mismatch')
    rec=strict_loads(rb);man=strict_loads(mb)
    need(rec['manifest_binding']['path']=='MANIFEST.json','wrong manifest path')
    binding(mb,rec['manifest_binding'],'manifest')
    need(set(man['excluded_seal_members'])==SEALS,'wrong manifest exclusions')
    rows=man['files'];listed=[r['path'] for r in rows]
    need(len(listed)==len(set(listed)),'duplicate manifest entry')
    need(set(listed)==set(data)-SEALS,'manifest coverage mismatch')
    for r in rows:binding(data[r['path']],r,r['path'])
    return {'payload_members':len(rows),'seal_members':3,'manifest_sha256':H(mb),'receipt_sha256':H(rb)}

def check_statuses(statuses):
    need(set(statuses)=={'U09','U10','U11'},'obligation status coverage')
    for u,r in statuses.items():
        s=r['terminal_status']
        need(s in ('PASS','REFUTED_AS_STATED / REPLACEMENT_PROVED') or
             (s.startswith('PARTIAL — EXACT IRREDUCIBLE BLOCKER: ') and
              len(s)>len('PARTIAL — EXACT IRREDUCIBLE BLOCKER: ')), 'generic/invalid status '+u)
        need(type(r.get('kernel_credit')) is bool,'missing kernel scope '+u)
    return 3

def check_test_evidence(row,data):
    need(type(row['exit_code']) is int and row['exit_code']==0,'test exit nonzero')
    for stream in ('stdout','stderr'):
        r=row[stream];need(r['path'] in data,'missing test stream');binding(data[r['path']],r,r['path'])
    text=(data[row['stdout']['path']]+data[row['stderr']['path']]).decode()
    counts=re.findall(r'^Ran ([0-9]+) tests? in .+$',text,re.M)
    need(len(counts)==1 and int(counts[0])==row['test_count'] and row['test_count']>0,'missing/wrong unittest count')
    need(re.search(r'^OK\s*$',text,re.M) is not None and re.search(r'^FAILED\b',text,re.M) is None,'unittest not OK')
    need(row['source_bindings'],'empty test source bindings')
    for p,r in row['source_bindings'].items():
        need(p in data,'missing tested source '+p);binding(data[p],r,p)
    return row['test_count']

def check_original(raw):
    need(len(raw)==850545 and H(raw)==INPUT_SHA,'original input identity')
    d=unzip(raw)
    man=strict_loads(d['CHECKPOINT_MANIFEST.json'])
    listed={r['path'] for r in man['files']}
    need(listed==set(d)-{'CHECKPOINT_MANIFEST.json'},'original manifest coverage')
    for r in man['files']:binding(d[r['path']],r,'original/'+r['path'])
    rec=strict_loads(d['RECEIPT.json'])
    for r in rec['output_hashes']:binding(d[r['path']],r,'original-receipt/'+r['path'])
    need(detached(d['RECEIPT.json.sha256'],'RECEIPT.json')==H(d['RECEIPT.json']),'original receipt detached')
    src=strict_loads(d['SOURCE_INVENTORY.json'])
    for r in src:
        b=d[r['packet_path']];binding(b,r,'original-source/'+r['packet_path'])
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'] and
             r['main_commit']==MAIN,'original Git blob/commit binding')
    proj=strict_loads(d['accepted-evidence/PROJECTION_BINDINGS.json'])
    for r in proj:binding(d[r['packet_path']],r,'original-evidence/'+r['packet_path'])
    final=strict_loads(d['FINAL_MAIN_IDENTITY.json'])
    need(final['main_commit']==MAIN and final['main_tree']==TREE and final['PR']==28 and
         final['PR_state']=='MERGED' and final['remaining_integration_cells']==[],'canonical pin changed')
    return {'members':len(d),'source_bindings':len(src),'evidence_bindings':len(proj)},d

def check_predecessors(data):
    name='predecessors/Orthemology_P01_Research_Checkpoint.zip';raw=data[name]
    need(len(raw)==984262 and H(raw)==A1_SHA,'attempt1 predecessor identity')
    old=unzip(raw);a1=check_layer(old)
    original=old['inputs/Orthemology_Pro_P01_Foundational_Formal.zip']
    need(original==data['predecessors/Orthemology_Pro_P01_Foundational_Formal.zip'],'original input copies differ')
    orig,origdata=check_original(original)
    for n,b in old.items():need(data['inputs/attempt1/'+n]==b,'attempt1 extracted preimage changed '+n)
    for n,b in origdata.items():need(data['inputs/original/'+n]==b,'original extracted preimage changed '+n)
    rr=data['predecessors/Orthemology_P01_attempt-0002_surviving_files_recovery.zip']
    need(len(rr)==32988 and H(rr)==RECOVERY_SHA,'limited recovery identity')
    rd=unzip(rr);rm=strict_loads(rd['MANIFEST.json'])
    need(set(rm)==set(rd)-{'MANIFEST.json'},'recovery coverage')
    for n,r in rm.items():binding(rd[n],r,'recovery/'+n)
    desc=strict_loads(data['boundary/ATTEMPT2_RECOVERY.json'])
    need(desc['attempt2_archive_recovered'] is False and desc['attempt2_complete_workspace_recovered'] is False,
         'invented attempt2 archive/workspace recovery')
    need(len(desc['surviving_exact_files'])==6,'survivor count')
    for r in desc['surviving_exact_files']:
        n=r['path'];binding(rd[n],r,'survivor/'+n)
        need(data['predecessors/attempt2_surviving_exact/'+n]==rd[n],'surviving document changed '+n)
    return {'attempt1':a1,'original':orig,'attempt2_recovery_members':len(rd),'exact_survivors':6}

def check_formal(data):
    inv=strict_loads(data['formal/SOURCE_INVENTORY.json']);status=strict_loads(data['formal/FORMAL_STATUS.json'])
    need(inv['lean_pin']=='leanprover/lean4:v4.19.0' and inv['mathlib_commit']=='c44e0c8ee63ca166450922a373c7409c5d26b00b','formal pin')
    rows=inv['files'];listed=[r['path'] for r in rows]
    actual={n for n in data if n.startswith('formal/') and
            (n.endswith('.lean') or PurePosixPath(n).name in ('lean-toolchain','lake-manifest.json'))}
    need(len(listed)==len(set(listed)) and set(listed)==actual,'formal file coverage')
    for r in rows:binding(data[r['path']],r,'formal/'+r['path'])
    names=[r['name'] for r in inv['targets']]
    need(names and len(names)==len(set(names)),'formal target coverage')
    audit=data['formal/P01Audit.lean'].decode()
    for n in names:
        for directive in (f'#check {n}\n',f'#ortho_audit {n}\n',f'#print axioms {n}\n'):
            need(audit.count(directive)==1,'audit target missing/duplicated '+n)
    need(len(re.findall(r'^#check ',audit,re.M))==len(names),'extra audit target')
    canonical='inputs/original/source-main/experiments/orthemology-v5/source/lean/'
    for n,b in data.items():
        if n.startswith('formal/vendor/'):
            need(b==data[canonical+PurePosixPath(n).name],'canonical vendor mutated '+n)
    q=strict_loads(data['evidence/LEAN_QUALIFICATION.json'])
    need(q['source_inventory_sha256']==H(data['formal/SOURCE_INVENTORY.json']),'qualification wrong source inventory')
    # This seal contract does not permit unseen outputs to be promoted later by editing a bit.
    need(status['kernel_credit'] is False and q['kernel_credit'] is False,'unexpected kernel promotion')
    need(q['status']=='HOST_EXECUTION_BLOCKED' and q['compiled_artifacts']==[] and q['declarations']=={},'host-only execution boundary differs')
    need(status['compiled_artifacts']==[] and status['axiom_readback']=={} and status['declaration_type_readback']=={},'invented formal evidence')
    need(not any(n.startswith('formal/') and n.endswith(('.olean','.ilean')) for n in data),'unclaimed new compiled artifact')
    return {'candidate_modules':len(inv['build_order'])-12,'public_targets':len(names),
            'formal_source_files':len(rows),'kernel_credit':False,'host_status':q['status']}

def check_dependencies(data):
    m=strict_loads(data['P01_INTERNAL_DEPENDENCY_MAP.json'])
    nodes={n['id']:n for n in m['nodes']};need(len(nodes)==len(m['nodes']),'duplicate dependency nodes')
    active=set();done=set()
    def visit(n):
        need(n in nodes,'unknown prerequisite '+n);need(n not in active,'dependency cycle '+n)
        if n in done:return
        active.add(n)
        for p in nodes[n]['depends_on']:visit(p)
        active.remove(n);done.add(n)
    for n in nodes:visit(n)
    need(m['P02_dependencies']==[] and m['P03_dependencies']==[],'unexpected cross-packet presumption')
    return len(done)

def run_tests_fresh(data,work):
    for n,b in data.items():
        if n.startswith(('executable/','handoff/')) and n.endswith('.py'):
            p=work/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';rows=[]
    for label,extra in [('normal',[]),('optimised',['-O'])]:
        cmd=[sys.executable,*extra,'-B','-m','unittest','discover','-v']
        p=subprocess.run(cmd,cwd=work/'executable',capture_output=True,timeout=120,env=env)
        text=(p.stdout+p.stderr).decode();c=re.findall(r'^Ran ([0-9]+) tests? in .+$',text,re.M)
        need(p.returncode==0 and len(c)==1 and int(c[0])>0 and re.search(r'^OK\s*$',text,re.M),
             'fresh new proposal tests failed '+label+': '+text[-6000:])
        rows.append({'mode':label,'command':cmd,'exit_code':p.returncode,'test_count':int(c[0]),
                     'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),
                     'stdout_sha256':H(p.stdout),'stderr_sha256':H(p.stderr)})
    return rows

def verify(archive,sha_file,ledger_file,rerun=False):
    report={'status':'FAIL','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'mathematical_or_kernel_credit':False,'external_review_credit':False,'errors':[]}
    try:
        raw=archive.read_bytes();h=H(raw)
        need(detached(sha_file.read_bytes(),archive.name)==h,'outer detached SHA mismatch')
        ledger=strict_loads(ledger_file.read_bytes())
        need(ledger['archive_sha256']==h and ledger['archive_bytes']==len(raw),'external every-member ledger archive binding')
        d=unzip(raw);need(set(ledger['members'])==set(d),'every-member ledger coverage')
        for n,r in ledger['members'].items():binding(d[n],r,'ledger/'+n)
        report['seal']=check_layer(d)
        report['predecessors']=check_predecessors(d)
        statuses=strict_loads(d['STATUS_RECORDS.json']);check_statuses(statuses)
        need(not any(s['kernel_credit'] for s in statuses.values()),'status kernel claim differs')
        report['obligation_statuses']={u:r['terminal_status'] for u,r in statuses.items()}
        rec=strict_loads(d['RECEIPT.json'])
        need(rec['canonical']['main']==MAIN and rec['canonical']['tree']==TREE and
             rec['canonical']['PR']==28 and rec['canonical']['integration_remaining']==[], 'receipt canonical boundary')
        need(rec['repository_mutation']=='NONE' and not rec['owner_adoption_credit'] and
             not rec['external_review_credit'] and not rec['new_kernel_credit'],'effect/credit boundary changed')
        need(rec['status_records_sha256']==H(d['STATUS_RECORDS.json']),'receipt status binding')
        report['formal']=check_formal(d)
        report['dependency_nodes']=check_dependencies(d)
        runs=strict_loads(d['evidence/FINAL_TEST_RUNS.json'])
        need({r['mode'] for r in runs}=={'normal','optimised'} and len(runs)==2,'final run coverage')
        report['recorded_tests']=[{'mode':r['mode'],'test_count':check_test_evidence(r,d)} for r in runs]
        ex=strict_loads(d['evidence/export_fixtures.json'])
        need(H(d['formal/P01GeneratedExports.lean'])==ex['generated_source_sha256'],'generated export binding')
        report['export_fixtures']={'finite':len(ex['accepted_finite_fixtures']),
                                   'refused':len(ex['typed_dependent_refusals'])}
        if rerun:
            with tempfile.TemporaryDirectory(prefix='p01-fresh-readback-') as td:
                report['fresh_test_replay']=run_tests_fresh(d,Path(td))
            need({r['test_count'] for r in report['fresh_test_replay']}=={r['test_count'] for r in runs},'fresh test counts differ')
        need(H(archive.read_bytes())==h,'archive changed while verifying')
        report.update(status='PASS',archive=archive.name,archive_bytes=len(raw),archive_sha256=h,
                      members_verified=len(d),zip_crc='PASS',exact_member_coverage=True,
                      uncompressed_bytes=sum(map(len,d.values())))
    except Exception as e:report['errors'].append(type(e).__name__+': '+str(e))
    report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path);p.add_argument('--sha256-file',type=Path,required=True)
    p.add_argument('--member-ledger',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    p.add_argument('--rerun-tests',action='store_true');a=p.parse_args()
    if a.report.exists():p.error('refusing to overwrite existing independent report')
    r=verify(a.archive,a.sha256_file,a.member_ledger,a.rerun_tests)
    a.report.write_text(json.dumps(r,indent=2)+'\n')
    summary={k:v for k,v in r.items() if k!='fresh_test_replay'}
    print(json.dumps(summary,indent=2))
    return 0 if r['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
