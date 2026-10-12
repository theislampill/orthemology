#!/usr/bin/env python3
"""Read-only, standard-library fresh ZIP verification. No research code executes."""
from __future__ import annotations
from pathlib import Path,PurePosixPath
import argparse,datetime,hashlib,io,json,re,stat,zipfile
P03_SHA='d984a85387bf15d2da4abfdb388fbeb83a1f27339aa593d7f4123c1569b6e280'
P02_SHA='365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(x,msg):
    if not x:raise ValueError(msg)
def safe_zip(z):
    names=z.namelist();require(len(names)==len(set(names)),'duplicate ZIP members');require(z.testzip() is None,'ZIP CRC failure')
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'unsafe/non-file member '+i.filename)
    return names
def bindings(z,rows,prefix=''):
    for r in rows:
        name=r.get('path',r.get('packet_path'));b=z.read(prefix+name)
        require(sha(b)==r['sha256'] and ('bytes' not in r or len(b)==r['bytes']),'binding mismatch '+name)
        if 'git_blob' in r:require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'Git blob mismatch '+name)
    return len(rows)
def exact_receipt_schema(r,s):
    # Implements the complete small keyword subset used by the bound P02 schema.
    def check(x,d):
        if 'const' in d:require(json.dumps(x,sort_keys=True)==json.dumps(d['const'],sort_keys=True),'schema const')
        if 'enum' in d:require(x in d['enum'],'schema enum')
        t=d.get('type')
        if t:require(type(x) is {'object':dict,'array':list,'string':str,'integer':int}[t],'schema type')
        if isinstance(x,dict):
            require(set(d.get('required',[]))<=set(x),'schema required')
            for k,v in d.get('properties',{}).items():
                if k in x:check(x[k],v)
            if d.get('additionalProperties') is False:require(set(x)<=set(d.get('properties',{})),'schema extra field')
        if isinstance(x,list):
            require(len(x)>=d.get('minItems',0) and len(x)<=d.get('maxItems',len(x)),'schema array size')
            if d.get('uniqueItems'):require(len({json.dumps(v,sort_keys=True) for v in x})==len(x),'schema unique')
            if 'items' in d:
                for v in x:check(v,d['items'])
        if 'minimum' in d:require(x>=d['minimum'],'schema minimum')
        if 'pattern' in d:require(re.fullmatch(d['pattern'],x) is not None,'schema pattern')
    check(r,s)
def verify_previous(data,kind):
    require(sha(data)==(P03_SHA if kind=='P03' else P02_SHA),'predecessor outer SHA '+kind)
    require(len(data)==(1868354 if kind=='P03' else 4192393),'predecessor bytes '+kind)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=safe_zip(z);mn='MANIFEST.json' if kind=='P03' else 'CHECKPOINT_MANIFEST.json';m=json.loads(z.read(mn));r=json.loads(z.read('RECEIPT.json'))
        require(z.read('RECEIPT.json.sha256').decode().split()[0]==sha(z.read('RECEIPT.json')),'receipt sidecar '+kind)
        bindings(z,m['files']);require(len({x['path'] for x in m['files']})==len(m['files']),'duplicate manifest row '+kind)
        controls=set(m['control_exclusions']) if kind=='P03' else {mn}
        require(set(names)=={x['path'] for x in m['files']}|controls,'predecessor population '+kind)
        if kind=='P03':
            require(sha(z.read(mn))==r['manifest_sha256'],'P03 manifest receipt')
            require(z.read('MANIFEST.json.sha256').decode().split()[0]==sha(z.read(mn)),'P03 manifest sidecar')
            require(sha(z.read('MANIFEST.json.sha256'))==r['manifest_sidecar_sha256'],'P03 manifest sidecar receipt')
            bindings(z,list(r['statement_reports'].values()));bindings(z,json.loads(z.read('inputs/SUPPLEMENTAL_IDENTITIES.json')))
            inner=r['input']['embedded_path'];ii=r['input']
        else:
            bindings(z,r['output_hashes']);exact_receipt_schema(r,json.loads(z.read('RECEIPT.schema.json')))
            require(r['obligation_statuses']==dict.fromkeys(['U05','U08','CV-R','CV-C','Q1c'],'PARTIAL'),'P02 status drift')
            inner=r['input_identity']['path'];ii=r['input_identity']
        ib=z.read(inner);require(sha(ib)==ii['sha256'] and len(ib)==ii['bytes'],'nested original identity')
        nested={}
        with zipfile.ZipFile(io.BytesIO(ib)) as n:
            nn=safe_zip(n);nested['members']=len(nn)
            for mf,key in [('CHECKPOINT_MANIFEST.json','files'),('RECEIPT.json','output_hashes')]:nested[mf]=bindings(n,json.loads(n.read(mf))[key])
            require(n.read('RECEIPT.json.sha256').decode().split()[0]==sha(n.read('RECEIPT.json')),'original receipt sidecar')
            for f in ['SOURCE_INVENTORY.json','accepted-evidence/PROJECTION_BINDINGS.json']:nested[f]=bindings(n,json.loads(n.read(f)))
            for o in json.loads(n.read('OBLIGATIONS.json')):bindings(n,o['source_bindings'])
            if kind=='P02':
                for name in nn:require(n.read(name)==z.read('inputs/packet/'+name),'P02 extracted original drift '+name)
        return {'kind':kind,'status':'PASS','bytes':len(data),'sha256':sha(data),'members':len(names),'manifest_bindings':len(m['files']),'nested':nested}
def verify(archive,seal):
    data=archive.read_bytes();require(sha(data)==seal['sha256'] and len(data)==seal['bytes'],'outer seal identity')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=safe_zip(z);mbytes=z.read('MANIFEST.json');m=json.loads(mbytes);rbytes=z.read('RECEIPT.json');r=json.loads(rbytes)
        require(sha(mbytes)==seal['manifest_sha256']==r['manifest_sha256'],'new manifest seal/receipt')
        require(sha(rbytes)==seal['receipt_sha256'],'new receipt seal')
        require(z.read('MANIFEST.json.sha256').decode().split()[0]==sha(mbytes),'new manifest sidecar')
        require(z.read('RECEIPT.json.sha256').decode().split()[0]==sha(rbytes),'new receipt sidecar')
        require(sha(z.read('MANIFEST.json.sha256'))==r['manifest_sidecar_sha256'],'new manifest sidecar binding')
        rows=m['files'];require(len({x['path'] for x in rows})==len(rows),'new duplicate manifest path')
        require(set(names)=={x['path'] for x in rows}|set(m['control_exclusions']),'new payload population')
        bindings(z,rows);member_hashes=[{'path':n,'bytes':len(z.read(n)),'sha256':sha(z.read(n))} for n in names]
        require(len(names)==seal['members']==r['archive_members'],'new member count')
        require(sum(x['bytes'] for x in member_hashes)==seal['uncompressed_bytes'],'new uncompressed size')
        old={p['kind']:z.read(p['path']) for p in r['predecessors']};predecessors=[verify_previous(old[k],k) for k in ['P03','P02']]
        for p in r['predecessors']:require(sha(old[p['kind']])==p['sha256'] and len(old[p['kind']])==p['bytes'],'receipt predecessor binding')
        dep=json.loads(z.read('P02_P03_DEPENDENCY_MAP.json'));require(dep['P02_actual_statuses']==dict.fromkeys(['U05','U08','CV-R','CV-C','Q1c'],'PARTIAL'),'dependency P02 statuses')
        with zipfile.ZipFile(io.BytesIO(old['P02'])) as p02:
            for edge in dep['edges']:
                e=edge['evidence'];require(e['archive_sha256']==P02_SHA and sha(p02.read(e['member']))==e['sha256'],'P02 result-level dependency binding')
            interfaces=json.loads(z.read('inputs/P02_EXACT_RESULT_INTERFACES.json'))
            for row in interfaces['interfaces']:
                b=p02.read(row['source_member']);require(sha(b)==row['sha256'] and len(b)==row['bytes'],'exact P02 interface')
                require(b.decode('utf-8')==row['exact_statement_and_proof_text'],'P02 interface text differs')
                require(b==z.read('inputs/p02-analysis/'+PurePosixPath(row['source_member']).name),'P02 copied note differs')
        expected=json.loads(z.read('formal/EXPECTED_TARGETS.json'))
        for name,h in expected['source_sha256'].items():require(sha(z.read('formal/'+name))==h,'formal frozen source '+name)
        require(expected['observed_types']==0 and expected['nonempty_olean_artifacts']==0,'unearned formal credit')
        command_count=0
        for n in names:
            if n.endswith('/command.json'):
                c=json.loads(z.read(n));base=n.rsplit('/',1)[0]+'/'
                for stream in ['stdout','stderr']:
                    b=z.read(base+stream+'.bin');require(sha(b)==c[stream+'_sha256'] and len(b)==c[stream+'_bytes'],'command raw stream '+n)
                command_count+=1
        require(not r['canonical_mutation'] and not r['kernel_credit'] and not r['external_review_credit'],'effect/credit drift')
        summary=json.loads(z.read('evidence/EVIDENCE_SUMMARY.json'))
        bindings(z,summary['new_source_hashes'])
        mini=z.read('handoff/P03_Lean419_Execution_Packet.zip')
        mini_record=json.loads(z.read('handoff/P03_Lean419_Execution_Packet.READBACK.json'))
        require(sha(mini)==mini_record['sha256'] and len(mini)==mini_record['bytes'],'minimal formal packet binding')
        with zipfile.ZipFile(io.BytesIO(mini)) as mz:
            mini_names=safe_zip(mz);mm=json.loads(mz.read('MANIFEST.json'));bindings(mz,mm['files'])
            require(set(mini_names)=={x['path'] for x in mm['files']}|set(mm['control_exclusions']),'minimal packet population')
            require(mz.read('MANIFEST.json.sha256').decode().split()[0]==sha(mz.read('MANIFEST.json')),'minimal manifest sidecar')
            for rel in expected['source_sha256']:
                require(mz.read('formal/'+rel)==z.read('formal/'+rel),'minimal/full source drift '+rel)
        for c in summary['required_final_commands']:
            rec=json.loads(z.read(c['path']));require(rec['exit_code']==c['expected_exit'],'unexpected final command '+c['path'])
        require(r['statuses']==json.loads(z.read('TERMINAL_STATUSES.json'))['statuses'],'status receipt mismatch')
        return {'status':'PASS','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive.name,'bytes':len(data),'sha256':sha(data),'members':len(names),'uncompressed_bytes':sum(x['bytes'] for x in member_hashes),
            'manifest_sha256':sha(mbytes),'receipt_sha256':sha(rbytes),'manifest_payload_members':len(rows),'all_member_hashes_checked':True,
            'command_stream_bindings':command_count,'predecessors':predecessors,'P02_dependency_edges_checked':len(dep['edges']),'minimal_formal_packet_members_checked':len(mini_names),
            'member_hashes':member_hashes,'scope':'Fresh-process custody/content consistency, not independent expert review, kernel proof or canonical adoption.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--seal',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    try:result=verify(a.archive,json.loads(a.seal.read_text()))
    except Exception as e:result={'status':'FAIL','error':repr(e)}
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='member_hashes'},indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)
