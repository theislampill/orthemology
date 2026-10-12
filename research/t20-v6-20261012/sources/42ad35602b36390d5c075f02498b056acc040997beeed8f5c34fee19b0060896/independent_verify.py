#!/usr/bin/env python3
"""Read-only verification of source bindings and isolated trust-zero build."""
import datetime,hashlib,json,os,pathlib,re,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
WS=ROOT.parent
FROZEN=WS/'hase-imported-compiler-transport-20261010'
LEAN=WS/'.toolchains/lean-4.19.0-linux/bin/lean'
OUT=ROOT/'validation/independent-lib'
OUT.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
gitblob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
source=ROOT/'RawMotiveBoundary.lean'
assert sha(source.read_bytes())=='ace7022513163b11ee3cc3e6114e3ffd654f38b4614bf0463d4bbb9b654e8f57'
manifest=json.loads((FROZEN/'MANIFEST.json').read_text())
before={r['path']:sha((FROZEN/r['path']).read_bytes()) for r in manifest['files']}
for r in manifest['files']:
 assert before[r['path']]==r['sha256'],r['path']
 assert (FROZEN/r['path']).stat().st_size==r['bytes'],r['path']
index_bytes=(FROZEN/'PINNED_SOURCE_INDEX.json').read_bytes()
index=json.loads(index_bytes)
index_receipt=json.loads((FROZEN/'INDEX_ACQUISITION_RECEIPT.json').read_text())
assert gitblob(index_bytes)==index_receipt['response']['git_blob']
acq=json.loads((FROZEN/'ACQUISITION.json').read_text())
assert acq['pin']==index_receipt['pin']=='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
assert len(acq['sources'])==83 and not acq['missing']
index_rows={r['public_path']:r for r in index['sources']}
prior_replay=json.loads((FROZEN/'validation/INDEPENDENT_SOURCE_REPLAY.json').read_text())
replay_checks={r['module']:r for r in prior_replay['source_checks']}
replay_builds={r['module']:r for r in prior_replay['build_records']}
source_bindings=[]
for r in acq['sources']:
 b=(FROZEN/'sources'/f"{r['module']}.lean").read_bytes()
 assert sha(b)==r['sha256'] and gitblob(b)==r['git_blob'],r['module']
 ix=index_rows[r['path']]
 assert ix['projection']=='EXACT' and ix['public_sha256']==ix['original_sha256']==r['sha256']
 assert replay_checks[r['module']]['sha256']==replay_builds[r['module']]['source_sha256']==r['sha256']
 assert replay_builds[r['module']]['exit_code']==0
 lib=FROZEN/'validation/independent-lib'/f"{r['module']}.olean"
 assert lib.is_file()
 source_bindings.append({'module':r['module'],'source_sha256':sha(b),'git_blob':gitblob(b),'import_olean_sha256':sha(lib.read_bytes())})
libs=sorted(p/'.lake/build/lib/lean' for p in (WS/'separating-projection-lean-20261009/.lake/packages').iterdir() if p.is_dir())
LIB=FROZEN/'validation/independent-lib'
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,LIB]+libs))}
cmd=[str(LEAN),'--trust=0','-o',str(OUT/'RawMotiveBoundary.olean'),str(source)]
t=time.time()
p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
log='LEAN_PATH='+env['LEAN_PATH']+'\n$ '+' '.join(cmd)+'\n'+p.stdout+p.stderr
(ROOT/'validation/INDEPENDENT_TRUST_ZERO.log').write_text(log)
assert p.returncode==0,log
assert 'sorryAx' not in log and 'error:' not in log and 'warning:' not in log
axioms=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S)
for a in axioms: assert set(re.sub(r'\s+','',a).split(','))<={'propext','Quot.sound','Classical.choice',''},a
assert len(axioms)==7
assert sha(source.read_bytes())=='ace7022513163b11ee3cc3e6114e3ffd654f38b4614bf0463d4bbb9b654e8f57'
assert {r['path']:sha((FROZEN/r['path']).read_bytes()) for r in manifest['files']}==before
result={'status':'PASS','review_time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':sha(source.read_bytes()),'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'command':cmd,'lean_path':env['LEAN_PATH'],'exit_code':p.returncode,'seconds':round(time.time()-t,3),'trust_zero':True,'prior_manifest_files_verified':len(before),'retained_source_bindings_verified':len(source_bindings),'source_index_git_blob':gitblob(index_bytes),'source_index_remote_refetch':'not repeated; retained acquisition and independent review receipt used','prior_sources_recompiled':False,'reused_prior_independent_source_compilation':True,'frozen_manifest_and_sources_preserved':True,'axiom_print_count':len(axioms),'source_bindings':source_bindings}
(ROOT/'validation/INDEPENDENT_BUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact source bindings and frozen manifest verified; new file compiled with --trust=0.')
print(log)
