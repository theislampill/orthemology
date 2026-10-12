#!/usr/bin/env python3
"""Finite owner archive assembly. No repository mutation or scientific execution.

Stage may retain explicit pending integration fields. Seal requires complete exact
integration bindings and root's approval of the exact source-contract digest.
No command downloads, installs, uploads, invokes Git, Lean, or scientific models.
Python 3.11+ standard library. Use -B to avoid bytecode caches.
"""
import argparse
from collections import Counter
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import zipfile

_spec=importlib.util.spec_from_file_location('archive_safety',Path(__file__).with_name('archive_safety.py'))
S=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(S)
MANIFEST='OWNER_ARCHIVE_MANIFEST.json'
SUMS='SHA256SUMS'
READY='READY_FOR_OWNER_DELIVERY_WITH_DISCLOSED_LIMITS'


def public_contract_projection(contract):
    """All deliverable bytes, statuses and bindings; omit local input-path plumbing."""
    result={k:v for k,v in contract.items()if k not in ['protected_roots','files','source_contract_sha256']}
    result['schema']='orthemology-owner-manifest-v1'
    result['files']=sorted([{k:v for k,v in r.items()if k!='source'}for r in contract['files']],key=lambda x:x['path'])
    result['self_exclusions']=[MANIFEST,SUMS]
    return result


def contract_digest(contract):
    # This same projection is recomputed from the actual manifest during verify/seal.
    return S.digest(S.canonical_json(public_contract_projection(contract)))


def fresh_output(output, protected=()):
    output=S.no_symlink_path(output)
    S.require(not output.exists() and not output.is_symlink(),'Output must be fresh')
    S.require(output.parent.is_dir(),'Output parent must exist')
    for root in protected:
        root=S.no_symlink_path(root)
        S.require(not output.is_relative_to(root),'Output lies within a protected input tree')
    return output


def check_payload_structure(document, bodies):
    rows=document['files'];by_path={r['path']:r for r in rows}
    S.check_names(list(by_path)+[MANIFEST,SUMS])
    S.require(len(by_path)==len(rows),'Duplicate declared payload')
    for role,count in document.get('required_role_counts',{}).items():
        S.require(sum(r.get('role')==role for r in rows)==count,'Required role count differs: '+role)
    for row in rows:
        S.require(row.get('mode',0o644)in(0o644,0o755),'Unsupported payload permissions')
        b=bodies[row['path']]
        S.require(len(b)==row['bytes'] and S.digest(b)==row['sha256'],'Payload identity differs: '+row['path'])
    reconstructed=[]
    source=document.get('source_reconstruction')
    if source:
        m=json.loads(bodies[source['path']])
        S.require(m['allowlist_sha256']==source['expected_allowlist_sha256'],'Frozen science allowlist differs')
        expected=m['members'];S.require(len(expected)==source['expected_members'],'Source count differs')
        S.require(len({r['sha256']for r in expected})==source['unique_hashes'],'Source hash count differs')
        for row in expected:
            S.require(row['path']in by_path,'Source map member absent: '+row['path'])
            actual=by_path[row['path']]
            S.require(all(actual[k]==row[k]for k in ['bytes','sha256']),'Source map identity differs')
        S.require({r['path']for r in expected}=={r['path']for r in rows if r.get('role')=='t20-selected-source'},'Scientific source membership differs')
        reconstructed.append({'kind':'effective-t20-science','members':len(expected),'status':'PASS'})
    for package in document.get('package_checks',[]):
        base=S.safe_relative(package['root'])
        manifest=json.loads(bodies[base+'/'+S.safe_relative(package['manifest'])])
        records=manifest[package['record_key']]
        S.check_names(r['path']for r in records)
        prefix=package.get('member_prefix','')
        if prefix:S.safe_relative(prefix)
        for row in records:
            name='/'.join(x for x in [base,prefix,row['path']]if x)
            S.require(name in by_path,'Package member absent: '+name)
            S.require(S.digest(bodies[name])==row['sha256'] and len(bodies[name])==row['bytes'],'Package manifest differs: '+name)
        reconstructed.append({'root':base,'manifest':package['manifest'],'members':len(records),'status':'PASS'})
    return reconstructed


def check_integration(document,bodies):
    S.require(document['status']in('PENDING_INTEGRATION','READY_TO_SEAL'),'Unknown assembly status')
    integration=document['integration']
    if document['status']!='READY_TO_SEAL':
        S.require(bool(document['pending']),'Pending preparation must identify its unresolved inputs')
        return {'status':'PENDING_INTEGRATION','pending':document['pending']}
    S.require(not document['pending'],'Pending inputs prohibit final sealing')
    S.require(integration['status']==READY,'Integration is not ready for owner delivery')
    for field in ['base_commit','base_tree']:
        S.require(len(integration[field])==40 and all(c in '0123456789abcdef'for c in integration[field]),'Invalid exact '+field)
    patch=S.safe_relative(integration['patch_path'])
    S.require(patch in bodies,'Patch is not in finite payload')
    patch_sha=S.digest(bodies[patch])
    S.require(patch_sha==integration['patch_sha256']==integration['clean_apply_patch_sha256'],'Clean application is not bound to this exact patch')
    required={'changed-file-map','clean-apply','whole-diff-review','gate-results','apply-helper'}
    evidence=integration.get('evidence_bindings',[])
    S.require(required <= {r['kind']for r in evidence},'Required integration evidence binding absent')
    for item in evidence:
        name=S.safe_relative(item['path'])
        S.require(name in bodies and S.digest(bodies[name])==item['sha256'],'Integration evidence changed: '+name)
    for check in document.get('required_ready_text_checks',[]):
        text=bodies[S.safe_relative(check['path'])].decode('utf-8')
        S.require(not any(token in text for token in check.get('forbidden',[])),'Prefinal wording remains in final entry point')
    return {'status':READY,'patch_sha256':patch_sha,'exact_base_commit':integration['base_commit'],
            'bound_evidence_records':len(evidence),'scope':'Digest bindings only; no new patch application or full-gate execution by this helper.'}


def sums_bytes(rows,manifest_bytes):
    records=[(r['path'],r['sha256'])for r in rows]+[(MANIFEST,S.digest(manifest_bytes))]
    return ''.join(h+'  '+n+'\n'for n,h in sorted(records)).encode('utf-8')


def stage(input_root,contract,output):
    root=S.no_symlink_path(input_root)
    S.require(contract.get('schema')=='orthemology-owner-assembly-v1','Unexpected source contract')
    S.safe_relative(contract['archive_name']);S.safe_relative(contract['zip_root'])
    S.require('/'not in contract['archive_name'] and '/'not in contract['zip_root'],'Archive name/root must be a single component')
    protected=[root/S.safe_relative(p)for p in contract.get('protected_roots',[])]
    output=fresh_output(output,protected)
    rows=contract['files'];S.check_names([r['path']for r in rows]+[MANIFEST,SUMS])
    bodies={}
    for row in rows:
        p=S.source_path(root,row['source'])
        S.require(not p.is_relative_to(output),'Source lies within proposed output')
        bodies[row['path']]=S.checked_bytes(p,row)
    check_payload_structure(contract,bodies);check_integration(contract,bodies)
    for name,body in bodies.items():
        if name.lower().endswith(('.zip','.docx')):S.inspect_zip(body,name)
    manifest=public_contract_projection(contract)
    manifest['source_contract_sha256']=contract_digest(contract)
    manifest['files']=sorted([{k:v for k,v in r.items()if k!='source'}for r in rows],key=lambda x:x['path'])
    manifest['self_exclusions']=[MANIFEST,SUMS]
    manifest_bytes=S.canonical_json(manifest)
    all_bodies={**bodies,MANIFEST:manifest_bytes,SUMS:sums_bytes(rows,manifest_bytes)}
    output.mkdir()
    for name,body in sorted(all_bodies.items()):
        p=output/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb')as f:f.write(body)
        mode=next((r.get('mode',0o644)for r in rows if r['path']==name),0o644)
        p.chmod(mode);os.utime(p,(S.EPOCH,S.EPOCH))
    for parent,dirs,files in os.walk(output,topdown=False):
        for name in dirs:
            p=Path(parent)/name;p.chmod(0o755);os.utime(p,(S.EPOCH,S.EPOCH))
    os.utime(output,(S.EPOCH,S.EPOCH))
    for row in rows:S.checked_bytes(S.source_path(root,row['source']),row)
    return verify_tree(output)


def verify_tree(root):
    root=S.no_symlink_path(root)
    manifest_bytes=S.source_path(root,MANIFEST).read_bytes();d=json.loads(manifest_bytes)
    S.require(d.get('schema')=='orthemology-owner-manifest-v1','Unknown owner manifest')
    S.require(d.get('self_exclusions')==[MANIFEST,SUMS],'Unexpected manifest self-exclusion scope')
    S.require(d.get('source_contract_sha256')==contract_digest(d),'Actual manifest is not bound to its recorded contract digest')
    expected=[r['path']for r in d['files']]+[MANIFEST,SUMS]
    actual=[];directories=[]
    for parent,dirs,files in os.walk(root,followlinks=False):
        for name in dirs+files:
            p=Path(parent)/name;S.require(not p.is_symlink(),'Symlink in archive tree')
            rel=p.relative_to(root).as_posix()
            if p.is_dir():directories.append(rel)
            else:
                S.require(stat.S_ISREG(p.stat().st_mode),'Nonregular archive object');actual.append(rel)
    S.check_names(actual,directories)
    S.require(set(actual)==set(expected),'Owner tree finite membership differs')
    allowed={p.as_posix()for name in expected for p in Path(name).parents}
    S.require(set(directories)<=allowed,'Unselected empty directory')
    if os.name != 'nt':
        modes={r['path']:r.get('mode',0o644)for r in d['files']}
        modes.update({MANIFEST:0o644,SUMS:0o644})
        for name,mode in modes.items():
            S.require(stat.S_IMODE((root/name).stat().st_mode)==mode,'Staged file permission mode differs: '+name)
    bodies={r['path']:S.checked_bytes(S.source_path(root,r['path']),r)for r in d['files']}
    S.require(S.source_path(root,SUMS).read_bytes()==sums_bytes(d['files'],manifest_bytes),'Checksum manifest differs')
    structure=check_payload_structure(d,bodies);integration=check_integration(d,bodies)
    archives=[]
    for name,body in bodies.items():
        if name.lower().endswith(('.zip','.docx')):
            checked=S.inspect_zip(body,name)
            archives.append({'path':name,'archives_checked':checked['archive_count'],'regular_members':checked['regular_member_count'],'status':'PASS'})
    return {'schema':'orthemology-owner-archive-verification-v1','status':'PASS_PREPARED_TREE',
            'assembly_status':d['status'],'payload_files':len(d['files']),
            'payload_bytes':sum(r['bytes']for r in d['files']),
            'manifest_sha256':S.digest(manifest_bytes),'source_contract_sha256':d['source_contract_sha256'],
            'role_counts':dict(sorted(Counter(r.get('role','unspecified')for r in d['files']).items())),
            'source_reconstruction_checks':structure,'original_container_checks':archives,
            'integration':integration,'scientific_execution':False}


def seal(root,output,approved_contract_sha256):
    root=S.no_symlink_path(root);verification=verify_tree(root)
    d=json.loads((root/MANIFEST).read_bytes())
    S.require(d['status']=='READY_TO_SEAL' and not d['pending'],'Final integration inputs remain pending')
    S.require(approved_contract_sha256==d['source_contract_sha256'],'Root approval must bind the exact ready contract digest')
    output=fresh_output(output,[root])
    S.require(output.name==d['archive_name'],'Final ZIP filename differs from approved contract')
    rows={r['path']:r for r in d['files']}
    names=sorted([*rows,MANIFEST,SUMS]);S.check_names([d['zip_root']+'/'+x for x in names])
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True)as z:
        for name in names:
            info=zipfile.ZipInfo(d['zip_root']+'/'+name,date_time=(1980,1,1,0,0,0))
            info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(stat.S_IFREG|rows.get(name,{}).get('mode',0o644))<<16
            z.writestr(info,(root/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    # Detect unexpected source change during archive creation; never silently certify it.
    S.require(verify_tree(root)==verification,'Prepared tree changed while writing ZIP')
    return {'status':'ZIP_CREATED_FRESH_EXTRACTION_STILL_REQUIRED','bytes':output.stat().st_size,
            'sha256':S.digest(output.read_bytes()),'members':len(names),'filename':output.name}


def verify_zip(archive_path,extract_to):
    archive_path=S.no_symlink_path(archive_path)
    extract_to=fresh_output(extract_to,[archive_path.parent]if Path(extract_to).is_relative_to(archive_path)else[])
    raw=archive_path.read_bytes();S.require(len(raw)<=256*1024*1024,'Archive exceeds verification bound')
    inventory=S.inspect_zip(raw,archive_path.name)
    with zipfile.ZipFile(io.BytesIO(raw))as z:
        names=z.namelist();S.require(all(not x.endswith('/')for x in names),'Outer ZIP must contain only finite file entries')
        roots={n.split('/')[0]for n in names};S.require(len(roots)==1,'Outer ZIP requires exactly one root')
        prefix=next(iter(roots))+'/'
        manifest_name=prefix+MANIFEST;S.require(manifest_name in names,'Owner manifest missing')
        d=json.loads(z.read(manifest_name));S.require(d.get('schema')=='orthemology-owner-manifest-v1','Unknown owner ZIP manifest')
        S.require(d.get('source_contract_sha256')==contract_digest(d),'ZIP manifest contract digest differs')
        S.require(d['zip_root']+'/'==prefix,'ZIP root differs from manifest')
        expected=[prefix+r['path']for r in d['files']]+[prefix+MANIFEST,prefix+SUMS]
        S.check_names(expected);S.require(set(names)==set(expected),'Outer ZIP has unselected or missing members')
        payload={r['path']:z.read(prefix+r['path'])for r in d['files']}
        check_payload_structure(d,payload);check_integration(d,payload)
        S.require(d['status']=='READY_TO_SEAL' and not d['pending'],'ZIP has prefinal pending state')
        S.require(z.read(prefix+SUMS)==sums_bytes(d['files'],z.read(manifest_name)),'Outer checksum manifest differs')
        modes={r['path']:r.get('mode',0o644)for r in d['files']}
        for info in z.infolist():
            expected_mode=modes.get(info.filename[len(prefix):],0o644)
            S.require(info.create_system==3 and info.external_attr==((stat.S_IFREG|expected_mode)<<16),'Outer ZIP permission metadata differs from the declared contract')
        # Verify every finite byte before creating the extraction destination.
        bodies={n:z.read(n)for n in names}
        extract_to.mkdir()
        for name,body in sorted(bodies.items()):
            p=extract_to/name;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb')as f:f.write(body)
            p.chmod(modes.get(name[len(prefix):],0o644));os.utime(p,(S.EPOCH,S.EPOCH))
    result=verify_tree(extract_to/prefix.rstrip('/'))
    return {'status':'PASS_FRESH_EXTRACTION','zip_sha256':S.digest(raw),'zip_bytes':len(raw),
            'outer_members':len(names),'crc':'PASS','safe_paths':'PASS',
            'nested_zip_archives_checked':inventory['archive_count']-1,'tree_verification':result}


def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('stage');p.add_argument('--input-root',required=True,type=Path);p.add_argument('--contract',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    p=sub.add_parser('verify-tree');p.add_argument('--root',required=True,type=Path)
    p=sub.add_parser('seal');p.add_argument('--root',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--approved-contract-sha256',required=True)
    p=sub.add_parser('verify-zip');p.add_argument('--archive',required=True,type=Path);p.add_argument('--extract-to',required=True,type=Path)
    args=ap.parse_args()
    if args.command=='stage':result=stage(args.input_root,json.loads(args.contract.read_bytes()),args.output)
    elif args.command=='verify-tree':result=verify_tree(args.root)
    elif args.command=='seal':result=seal(args.root,args.output,args.approved_contract_sha256)
    else:result=verify_zip(args.archive,args.extract_to)
    print(S.canonical_json(result).decode(),end='')

if __name__=='__main__':main()
