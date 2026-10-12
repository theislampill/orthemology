#!/usr/bin/env python3
import ast,hashlib,json,os,platform,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath

ROOT=Path('private-locator:f0a43fb1181206830296')
OUT=Path('/mnt/data')
NAME='Orthemology_T20_Whole_Corpus_Synthesis_20261010'

def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b:break
            h.update(b)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read_json(p,default=None):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return default

def execute(args,cwd,timeout=120):
    try:
        r=subprocess.run(args,cwd=str(cwd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        return {'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    except Exception as e:return {'exit_code':None,'error':str(e)}

required=['START_HERE.md','DOT_MESSAGE.md','COVERAGE_AND_LIMITS.md',
          'documents/FULL_T20_FIELD_GUIDE.md','documents/CROSS_FRONT_SYNTHESIS.md',
          'documents/FOUNDATIONS_CROSSWALK.md','research/contracts.py','research/test_contracts.py',
          'research/exhaustive_oracle.py','verification/verify_packet.py','verification/test_verifier.py']
missing=[x for x in required if not (ROOT/x).is_file()]
if missing:raise RuntimeError('Missing generated payload: '+str(missing))

# Retain preparation programs as research-generation evidence, not portable input
# acquisition promises. They use the original mounted input paths.
for original in ('t20_build_register.py','t20_finalize_synthesis.py'):
    p=OUT/original
    if p.is_file():shutil.copy2(p,ROOT/'verification'/original)

summary=read_json(ROOT/'inventory/CORPUS_SUMMARY.json',{'failures':[{'reason':'No corpus summary was produced'}]})
archives=read_json(ROOT/'inventory/ARCHIVES.json',[])
if not (ROOT/'CORPUS_REGISTER.md').exists():
    (ROOT/'CORPUS_REGISTER.md').write_text('# Corpus register unavailable\n\nThe source inventory did not complete. Read `evidence/CORPUS_BUILD.stderr.log`. No completeness is claimed.\n')
if not (ROOT/'SOURCE_REPORT_INDEX.md').exists():
    (ROOT/'SOURCE_REPORT_INDEX.md').write_text('# Source index unavailable\n\nThe extraction did not complete. This is not evidence that the corpus lacks sources.\n')

runs={}
commands={
 'research_normal':[sys.executable,'-B','-m','unittest','discover','-s','research','-p','test_contracts.py','-v'],
 'research_optimised':[sys.executable,'-O','-B','-m','unittest','discover','-s','research','-p','test_contracts.py','-v'],
 'oracle_normal':[sys.executable,'-B','research/exhaustive_oracle.py'],
 'oracle_optimised':[sys.executable,'-O','-B','research/exhaustive_oracle.py'],
 'verifier_fixtures_normal':[sys.executable,'-B','-m','unittest','discover','-s','verification','-p','test_verifier.py','-v'],
 'verifier_fixtures_optimised':[sys.executable,'-O','-B','-m','unittest','discover','-s','verification','-p','test_verifier.py','-v'],
}
for key,args in commands.items():
    result=execute(args,ROOT)
    runs[key]={'command':args,'exit_code':result.get('exit_code'),'error':result.get('error')}
    (ROOT/'evidence'/f'FINAL_{key}.stdout.log').write_text(result.get('stdout',''),encoding='utf-8')
    (ROOT/'evidence'/f'FINAL_{key}.stderr.log').write_text(result.get('stderr',result.get('error','')),encoding='utf-8')
    if key.startswith('oracle'):
        try:runs[key]['result']=json.loads(result.get('stdout',''))
        except Exception:runs[key]['result']=None
runs['oracle_outputs_identical']=((ROOT/'evidence/FINAL_oracle_normal.stdout.log').read_bytes()==(ROOT/'evidence/FINAL_oracle_optimised.stdout.log').read_bytes())
runs['assistant_observed_stdout']='NO: result stream unavailable in resumed execution'
runs['external_independent_review']='NOT_PERFORMED'
runs['inherited_lean_rebuild']='NOT_PERFORMED'
runs['runtime_python']=platform.python_version()
dump(ROOT/'evidence'/'MACHINE_REPLAY_RECEIPT.json',runs)

# Crosswalk exact archive references mentioned in the written documents.
def normalise(s):return re.sub(r'\(\d+\)(?=\.zip$)','',s).casefold()
refs={}
for p in (ROOT/'documents').glob('*.md'):
    for name in re.findall(r'`([^`\n]+\.zip)`',p.read_text(encoding='utf-8')):
        refs.setdefault(name,set()).add(p.name)
cross=[]
for name,documents in sorted(refs.items()):
    matches=[r['archive_id'] for r in archives if any(normalise(n)==normalise(name) for n in r['names'])]
    cross.append({'reference':name,'documents':sorted(documents),'archive_ids':matches,
                  'status':'MATCHED_NAME_IDENTITY' if matches else 'NO_EXACT_NAME_MATCH_IN_REGISTER'})
dump(ROOT/'inventory'/'DOCUMENT_SOURCE_CROSSWALK.json',cross)

claimrows=[
 ('D1','Coarsest finite joint-contract refinement','Written proof; standard probabilistic abstraction construction','research_normal, oracle_normal','Finite declared state/kernel contract; semantic warrant is input'),
 ('D2','Minimum sidecar alphabet and fixed-length bits','Written counting argument developed for this synthesis','research_normal, oracle_normal','Minimum only among deterministic finite sidecars for the stated strong contract'),
 ('D3','Finite histories, values and fixed-policy eventual reachability','Written induction and limiting-event argument','research_normal','No access to erased/hidden state; policy and information-state assumptions explicit'),
 ('D4','Finite-horizon value error and conditioning amplification','Written bounds and exact counterexamples','oracle_normal, research_normal','No infinite-horizon conclusion from arbitrarily small approximation'),
 ('D5','Cometric fibre criterion for every pulled-back objective','Written necessity/sufficiency proof','research_normal','Smooth positive-definite metric, full-rank linear coarse map, all-objectives quantifier'),
 ('D6','Conditional hybrid flow/jump preservation','Written finite-composition proof','No general hybrid implementation','Requires actual projectability, guards, kernel transport, costs and non-explosion'),
 ('D7','Arbitrary-depth positive-moment monitor counterexample','Written polynomial-square proof','research_normal','Static finite witness family, not predecessor ODE or interval proof'),
 ('D8','Target/update-relative linear closure','Written observability proof; acknowledged classical ancestry','research_normal','All linear states, declared linear updates; no empirical network guarantee'),
]
dump(ROOT/'CLAIM_LEDGER.json',[{'id':i,'claim':c,'evidence':e,'controls':t,'limits':l,
        'lean':'NOT_FORMALISED_HERE','prior_art_novelty':'NOT_CERTIFIED','full_corpus_nonduplication':'NOT_EXHAUSTIVELY_CHECKED'} for i,c,e,t,l in claimrows])

wordcounts={p.name:len(p.read_text(encoding='utf-8').split()) for p in (ROOT/'documents').glob('*.md')}
all_tests=all(runs[k].get('exit_code')==0 for k in commands)
bs=['# Machine-generated build summary','',
    '**This is a program-generated receipt, not a claim that its output was visible to the assistant.**','',
    f"Recursive ZIP objects inventoried: {summary.get('unique_zip_objects','unavailable')}.",
    f"Selected unchanged source reports: {summary.get('unique_selected_source_reports','unavailable')}.",
    f"Corpus read failures recorded: {len(summary.get('failures',[]))}.",
    f"All six new-code/fixture command runs exited successfully: {all_tests}.",'',
    '## New document word counts','']+[f'- `{n}`: {v:,}' for n,v in wordcounts.items()]
bs+=['','## Research limits','',
    'No fresh inherited Lean build, Arabic-volume collation, external specialist review, empirical noetic validation or exhaustive originality assessment was performed. The final assistant-visible verification readback remains unavailable.','',
    'Inspect `evidence/MACHINE_REPLAY_RECEIPT.json`, the logs, and `COVERAGE_AND_LIMITS.md`.']
(ROOT/'BUILD_SUMMARY.md').write_text('\n'.join(bs)+'\n',encoding='utf-8')

# Remove only generated Python caches, never original source inputs.
for p in list(ROOT.rglob('__pycache__')):
    if p.is_dir():shutil.rmtree(p)
files=[];dirs=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_symlink():raise RuntimeError('Unexpected symlink in generated packet')
    rel=p.relative_to(ROOT).as_posix()
    if p.is_dir():dirs.append(rel)
    elif p.is_file() and rel not in ('MANIFEST.json','MANIFEST.sha256'):
        files.append({'path':rel,'bytes':p.stat().st_size,'sha256':sha_file(p)})
m={'format':'t20-synthesis-manifest-v1','files':files,'directories':dirs}
dump(ROOT/'MANIFEST.json',m)
(ROOT/'MANIFEST.sha256').write_text(sha_file(ROOT/'MANIFEST.json')+'  MANIFEST.json\n',encoding='ascii')
base=execute([sys.executable,'-B','verification/verify_packet.py','.'],ROOT)
base_o=execute([sys.executable,'-O','-B','verification/verify_packet.py','.'],ROOT)

zip_path=OUT/(NAME+'.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for d in dirs:z.writestr(NAME+'/'+d+'/',b'')
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():z.write(p,NAME+'/'+p.relative_to(ROOT).as_posix())

# Reopen and safely extract to a disposable path; verify in both Python modes.
with tempfile.TemporaryDirectory(prefix='t20_synthesis_reopen_',dir=str(OUT)) as tmp:
    dest=Path(tmp)
    with zipfile.ZipFile(zip_path) as z:
        bad=z.testzip()
        if bad is not None:raise RuntimeError('Generated ZIP CRC failure: '+bad)
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in info.filename:raise RuntimeError('Unsafe generated ZIP path')
            target=dest.joinpath(*p.parts)
            if info.is_dir():target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(z.read(info))
    fresh=dest/NAME
    fresh_result=execute([sys.executable,'-B','verification/verify_packet.py','.'],fresh)
    fresh_optimised=execute([sys.executable,'-O','-B','verification/verify_packet.py','.'],fresh)
    # Real-packet corruption probes, with exact restoration between probes.
    checks=[]
    vp=fresh/'verification/verify_packet.py'
    def rejected(label):
        r=execute([sys.executable,'-O','-B',str(vp),str(fresh)],fresh)
        checks.append({'control':label,'rejected':r.get('exit_code') not in (None,0),'exit_code':r.get('exit_code')})
    target=fresh/'documents/CROSS_FRONT_SYNTHESIS.md';old=target.read_bytes()
    target.write_bytes(old+b'\nTAMPER\n');rejected('changed payload');target.write_bytes(old)
    target.unlink();rejected('missing payload');target.write_bytes(old)
    extra=fresh/'UNLISTED.txt';extra.write_text('x');rejected('unlisted file');extra.unlink()
    extra=fresh/'UNLISTED_DIR';extra.mkdir();rejected('unlisted directory');extra.rmdir()
    link=fresh/'UNLISTED_LINK';link.symlink_to(target);rejected('symlink');link.unlink()
    mp=fresh/'MANIFEST.json';sp=fresh/'MANIFEST.sha256';mb=mp.read_bytes();sb=sp.read_bytes()
    sp.write_text('0'*64+'  MANIFEST.json\n');rejected('wrong manifest digest');sp.write_bytes(sb)
    d=json.loads(mb);d['files'][0]['path']='../escape';dump(mp,d);sp.write_text(sha_file(mp)+'  MANIFEST.json\n');rejected('path traversal in authenticated local manifest');mp.write_bytes(mb);sp.write_bytes(sb)
    d=json.loads(mb);d['files'].append(d['files'][0]);dump(mp,d);sp.write_text(sha_file(mp)+'  MANIFEST.json\n');rejected('duplicate manifest path');mp.write_bytes(mb);sp.write_bytes(sb)
    restored=execute([sys.executable,'-B','verification/verify_packet.py','.'],fresh)

standalone={
 'Orthemology_T20_All_Delivered_Research_Field_Guide_20261010.md':'documents/FULL_T20_FIELD_GUIDE.md',
 'Orthemology_T20_Cross_Front_Mathematical_Synthesis_20261010.md':'documents/CROSS_FRONT_SYNTHESIS.md',
 'Orthemology_T20_Foundational_Crosswalk_20261010.md':'documents/FOUNDATIONS_CROSSWALK.md',
 'Orthemology_T20_Dot_Synthesis_Handoff_20261010.md':'DOT_MESSAGE.md',
 'Orthemology_T20_Corpus_Register_20261010.md':'CORPUS_REGISTER.md',
}
for name,rel in standalone.items():shutil.copy2(ROOT/rel,OUT/name)
receipt={'archive':zip_path.name,'bytes':zip_path.stat().st_size,'sha256':sha_file(zip_path),
 'payload_files':len(files),'directories':len(dirs),'corpus_summary':summary,'document_words':wordcounts,
 'new_code_test_commands':runs,'direct_verify_normal':base,'direct_verify_optimised':base_o,
 'fresh_extraction_normal':fresh_result,'fresh_extraction_optimised':fresh_optimised,
 'real_packet_rejections':checks,'restored_extraction_verify':restored,
 'assistant_visible_readback':'NOT_AVAILABLE','original_lean_or_source_research_replayed':False,
 'external_review':'NOT_PERFORMED','standalone_files':standalone}
receipt_path=OUT/(NAME+'.VERIFICATION.json');dump(receipt_path,receipt)
print(json.dumps({'created_files':[str(zip_path),str(receipt_path)]+[str(OUT/n) for n in standalone],
 'zip_bytes':zip_path.stat().st_size,'payload_files':len(files),
 'recursive_archives':summary.get('unique_zip_objects'),'source_reports':summary.get('unique_selected_source_reports'),
 'new_code_test_success':all_tests,'direct_inventory_exit':base.get('exit_code'),
 'fresh_inventory_exit':fresh_result.get('exit_code'),'rejection_controls':checks,
 'notice':'Machine output; not observed by assistant because the tool-result stream is unavailable'},indent=2))
