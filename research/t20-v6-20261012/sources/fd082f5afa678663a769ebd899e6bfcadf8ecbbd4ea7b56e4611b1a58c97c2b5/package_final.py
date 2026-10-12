"""Preserve only the scoped probability checkpoint and verify its archive safely."""
from pathlib import Path, PurePosixPath
import hashlib,json,shutil,stat,subprocess,sys,zipfile
R=Path(__file__).resolve().parent.parent
P=Path(__file__).resolve().parent
A=R/'literal-shift-probability-20261011';V=R/'literal-shift-probability-independent-review-20261011'
NAME='literal-shift-probability-checkpoint-20261011'
S=P/'staged'/NAME

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def req(b,s):
    if not b:raise RuntimeError(s)
def copy(src,dst):
    req(src.is_file() and not src.is_symlink(),'Unsafe/missing input '+str(src))
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)

def stage():
    req(not S.exists(),'Stage already exists')
    S.mkdir(parents=True)
    for name in ['LiteralShiftPersistence.lean','LiteralShiftWeights.lean','LiteralShiftMixture.lean',
                 'LiteralShiftDefect.lean','LiteralShiftFirstBit.lean','RESULT.md','SOURCE_BRIDGE.md',
                 'SOURCE_PINS.json','INPUT_BINDINGS.json','BASELINE_SOURCE_CHECK.json','OWNER_INSPECTION.json',
                 'PREREQUISITE_REBUILD.json','FINAL_REPLAY.json','build_prerequisites.py','verify_final.py']:
        copy(A/name,S/name)
    for folder in ['inputs','inherited/literal','negative-controls']:
        for src in sorted((A/folder).rglob('*')):
            if src.is_file():copy(src,S/src.relative_to(A))
    for entry in json.loads((A/'PREREQUISITE_REBUILD.json').read_text())['modules']:
        rel=Path(entry['module'].replace('.','/')).with_suffix('.lean')
        copy(A/'inherited/baseline'/rel,S/'inherited/baseline'/rel)
        copy(A/'logs'/('baseline-'+entry['module']+'.log'),S/'evidence/prerequisite-logs'/('baseline-'+entry['module']+'.log'))
    run=Path(json.loads((A/'FINAL_REPLAY.json').read_text())['run_directory'])
    for sub in ['sources','logs']:
        for src in (run/sub).rglob('*'):
            if src.is_file():copy(src,S/'evidence/author-replay'/src.relative_to(run))
    copy(run/'RECEIPT.json',S/'evidence/author-replay/RECEIPT.json')
    req((V/'REVIEW.md').exists() and (V/'BINDINGS.json').exists(),'Independent binding not final')
    for src in V.rglob('*'):
        if src.is_file() and src.name!='REPLAY_IN_PROGRESS.json':
            copy(src,S/'evidence/independent-review'/src.relative_to(V))
    rootcheck=R/'literal-shift-probability-root-check-20261011'
    for src in rootcheck.rglob('*'):
        if src.is_file():copy(src,S/'evidence/supplementary-root-main-check'/src.relative_to(rootcheck))
    verifier=(R/'literal-shift-universal-invariant-20261011/verify_integrity.py').read_text()
    verifier=verifier.replace('literal-shift-ordinary-proof-integrity-v1','literal-shift-probability-proof-integrity-v1')
    (S/'verify_integrity.py').write_text(verifier)
    (S/'README.md').write_text('''# Literal shift probability checkpoint

Read `RESULT.md` for the exact theorem, original proof credit and remaining Python/host/bytecode boundaries. The five new modules are frozen in `SOURCE_PINS.json`.

This scoped supplement contains the five new source modules, the seven unchanged literal source inputs, the 34-source prerequisite build closure, source provenance, and observed author/independent-review logs and receipts. It does not duplicate the earlier ZIP or bundle the Lean/Mathlib installations. One copy of the independently observed objects is preserved with its review binding; duplicate author objects are omitted. All sources needed for a fresh replay are included.

Independent review: `evidence/independent-review/REVIEW.md`. The root's main-module replay in `evidence/supplementary-root-main-check` is supplementary and is not another independent whole-dependency replay.

Run `python verify_integrity.py` (or `python -O verify_integrity.py`) to check frozen member bytes. This does not check mathematical proofs. To rebuild the proof, use a working copy, set the pinned Lean/Mathlib environment, then run `python build_prerequisites.py` and `python verify_final.py`. These are the portable replay entry points. The preserved independent-review script is the historical workspace harness and records its original paths; it is not the portable entry point.

The dependency acquisition record pins official Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. The original ordinary universal correspondence and probability proofs retain their credit. No protected repository edit, upload, integration or owner acceptance is implied.
''')
    print(S)

def archive():
    req(S.exists(),'No stage')
    req(sha(R/'literal-shift-kernel-checkpoint-20261011.zip')=='7f4fc218565854d4f23e0da530bdc3061c3e026f7dd0c3cea2b5e255809cb46d','Prior ZIP changed')
    if (P/'PORTABLE_REPLAY.json').exists():copy(P/'PORTABLE_REPLAY.json',S/'evidence/PORTABLE_REPLAY.json')
    files=[]
    for p in sorted(S.rglob('*')):
        req(not p.is_symlink(),'Symlink in stage')
        if p.is_file() and p.name!='MANIFEST.json':files.append({'path':p.relative_to(S).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    (S/'MANIFEST.json').write_text(json.dumps({'schema':'literal-shift-probability-proof-integrity-v1','scope':'Frozen source/evidence bytes only; proof evidence is separately logged.','files':files},indent=2)+'\n')
    z=R/(NAME+'.zip');req(not z.exists(),'Archive already exists')
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for p in sorted(S.rglob('*')):
            if p.is_file():out.write(p,NAME+'/'+p.relative_to(S).as_posix())
    E=P/'safe-extraction';req(not E.exists(),'Extraction already exists');E.mkdir()
    with zipfile.ZipFile(z) as arc:
        req(arc.testzip() is None,'CRC failure');seen=set();total=0
        for i in arc.infolist():
            q=PurePosixPath(i.filename)
            req(not q.is_absolute() and '..' not in q.parts and '\\' not in i.filename and q.as_posix()==i.filename,'Unsafe ZIP member')
            req(i.filename not in seen,'Duplicate ZIP member');seen.add(i.filename)
            req(q.parts[0]==NAME and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'Unsafe ZIP type/root')
            total+=i.file_size;req(total<256*1024*1024,'Unexpected ZIP expansion')
            target=E/q;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(arc.read(i))
    B=E/NAME;results=[]
    for flag in [[],['-O']]:
        p=subprocess.run([sys.executable,*flag,str(B/'verify_integrity.py')],capture_output=True,text=True)
        req(p.returncode==0,'Integrity failure '+p.stdout+p.stderr)
        results.append({'optimized':bool(flag),'exit_code':p.returncode,'output':p.stdout})
    # Exercise all integrity controls in isolated disposable copies, under both modes.
    controls=[]
    for mode in [False,True]:
        for kind in ['missing','corrupt','extra','symlink']:
            C=P/('control-'+str(mode)+'-'+kind);shutil.copytree(B,C)
            f=C/'RESULT.md'
            if kind=='missing':f.unlink()
            elif kind=='corrupt':f.write_bytes(f.read_bytes()+b'\nCORRUPTED\n')
            elif kind=='extra':(C/'EXTRA').write_text('unexpected')
            else:f.unlink();f.symlink_to('README.md')
            p=subprocess.run([sys.executable,*(['-O'] if mode else []),str(C/'verify_integrity.py')],capture_output=True,text=True)
            req(p.returncode!=0,'Integrity accepted '+kind)
            controls.append({'optimized':mode,'control':kind,'exit_code':p.returncode})
            shutil.rmtree(C)
    receipt={'status':'PASS','archive':str(z),'archive_sha256':sha(z),'bytes':z.stat().st_size,'members':len(seen),'manifest_sha256':sha(B/'MANIFEST.json'),'safe_extraction':str(B),'integrity':results,'negative_integrity_controls':controls,'prior_zip_sha256':sha(R/'literal-shift-kernel-checkpoint-20261011.zip'),'scope':'Safe preservation and byte integrity; no extra theorem credit.'}
    (P/'SAFE_EXTRACTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    if sys.argv[1:] == ['stage']:stage()
    elif sys.argv[1:] == ['archive']:archive()
    else:raise RuntimeError('Use stage or archive')
