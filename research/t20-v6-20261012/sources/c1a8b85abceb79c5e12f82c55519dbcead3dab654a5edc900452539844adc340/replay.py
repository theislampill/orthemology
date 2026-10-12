from pathlib import Path
import os,sys,json,hashlib,datetime,subprocess,importlib.util,re
W=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent; C=W/'hase-actual-source-enumerability-20261010'; O=R/'fresh-output'; O.mkdir(exist_ok=False)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()
def record(p):return {'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)}
def load(p):
 s=importlib.util.spec_from_file_location('candidate',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load(C/'verify.py');P=json.loads((C/'validation/INPUT_PINS.json').read_text())['inputs'];freeze=C/'validation/CORE_SOURCE_FREEZE.json'
assert sha(freeze)=='4aef4bb73919a5e2d0304ade94bb57c614d882c3aeb11a336c669dac18d631c5'
assert sha(C/'validation/INPUT_PINS.json')=='5570b2356f0ba60722663c44028c059f1e6ad4e55512effb5dc989e44b2fd706'
extra=[W/'hase-joint-certificate-checker-20261010'/f'{n}.lean' for n in ['CertificateFramework','CertificateRules','CertificateCompleteness']]+[W/'hase-joint-certificate-codec-20261010/SerializedCertificateCodec.lean']
P+= [record(p) for p in extra if str(p.relative_to(W)) not in {x['path'] for x in P}]
(R/'REVIEW_INPUT_PINS.json').write_text(json.dumps(P,indent=2)+'\n')
def check():
 for e in P:
  p=W/e['path'];assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path']
check();print(f'PRECHECK PASS {len(P)} pins',flush=True)
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[O]+m.b.inherited_paths())));(R/'environment.json').write_text(json.dumps({'LEAN_PATH':env['LEAN_PATH'],'lean':str(m.b.LEAN)},indent=2)+'\n')
records=[]
for src in extra+m.SOURCES:
 cmd=[str(m.b.LEAN),'--trust=0','-s','65536','-o',str(O/(src.stem+'.olean')),str(src)]
 p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=O/(src.stem+'.log');log.write_text(p.stdout)
 assert p.returncode==0 and not any(x in p.stdout for x in ['sorryAx','error:','warning:']),(src,p.returncode,str(log))
 if src.stem=='SourceSearchControls': assert re.findall(r'^(true|false)$',p.stdout,re.M)==['true','false','false','false']
 if src.stem=='SourceSearchAudit': assert len(re.findall(r'^PASS ActualSourceEnumerability\.',p.stdout,re.M))==29
 records.append({'module':src.stem,'source':record(src),'object':record(O/(src.stem+'.olean')),'log':record(log),'exit_code':p.returncode});print('PASS '+src.stem,flush=True)
check()
receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'stack_kb':65536,'source_count':len(records),'pins_before_after':len(P),'candidate_unchanged':True,'actual_retained_sources_freshly_checked':[p.stem for p in extra],'baseline_rebuilt':False,'records':records,'lean_version':subprocess.check_output([str(m.b.LEAN),'--version'],text=True).strip()}
(R/'REVIEW_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('DONE PASS',flush=True)
