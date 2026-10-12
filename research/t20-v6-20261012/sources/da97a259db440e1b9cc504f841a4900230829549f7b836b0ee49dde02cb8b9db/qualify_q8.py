import pathlib,json,re,hashlib,subprocess,os,time
ROOT=pathlib.Path(__file__).resolve().parent; TOOL=pathlib.Path('private-locator:d97af50b47918e94879b'); ORIGINAL=pathlib.Path('private-locator:ed0f0021a1fad46fb3c4')
ENV={**os.environ,'PATH':str(TOOL)+':'+os.environ['PATH']};ENV.pop('LEAN_NUM_THREADS',None)
R=ROOT/'receipts'/('q8-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));R.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,cmd,cwd=ROOT):
 t=time.time();p=subprocess.run(cmd,cwd=cwd,env=ENV,capture_output=True);(R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr);(R/(label+'.command.json')).write_text(json.dumps({'command':cmd,'cwd':str(cwd),'start_unix':t,'end_unix':time.time(),'exit':p.returncode},indent=2));assert p.returncode==0,(label,p.stdout.decode(),p.stderr.decode());return p.stdout.decode()+p.stderr.decode()
assert 'version 4.19.0' in run('version',['lean','--version'])
mods=['Q8Measure','Q8Machine','Q8Compiler','Q8Witnesses'];sources={m:sha(ROOT/(m+'.lean')) for m in mods};targets=[];art=[]
for m in mods:
 p=ROOT/(m+'.lean'); ns=re.search(r'^namespace (\S+)',p.read_text(),re.M).group(1)
 for n in re.findall(r'^theorem (\w+)',p.read_text(),re.M):targets.append({'module':m,'declaration':ns+'.'+n})
 o=ROOT/'.lake/build/lib/lean'/(m+'.olean');start=time.time();run('build-'+m,['lake','env','lean','-o',str(o),str(p)]);assert o.stat().st_size and o.stat().st_mtime>=start-2;art.append({'module':m,'bytes':o.stat().st_size,'sha256':sha(o)});print('BUILT',m,flush=True)
audit=ROOT/'Q8Audit.lean';audit.write_text('import Q8Witnesses\n'+''.join('#check @'+t['declaration']+'\n#print axioms '+t['declaration']+'\n' for t in targets));out=run('types-and-axioms',['lake','env','lean',str(audit)]);assert 'sorryAx' not in out and not re.search(r'\berror:',out);seen={}
for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):assert n not in seen;seen[n]=[x.strip() for x in a.split(',') if x.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):assert n not in seen;seen[n]=[]
assert set(seen)=={t['declaration'] for t in targets}
for n,a in seen.items():
 assert set(a)<={'propext','Classical.choice','Quot.sound'},(n,a)
 assert any(l.lstrip('@').startswith(n+' :') or l.lstrip('@').startswith(n+'.{') for l in out.splitlines()),n
assert sources=={m:sha(ROOT/(m+'.lean')) for m in mods}
base=ROOT/'receipts/qualification-20260930T134433Z/QUALIFIED_RESULT.json'
r={'status':'Q8_ACTUAL_MEASURE_MACHINE_AND_STRUCTURAL_COMPILER_KERNEL_CHECKED','theorem_count':len(targets),'targets':targets,'axioms':seen,'source_sha256':sources,'artifacts':art,'audit_sha256':sha(audit),'base_130_target_receipt_sha256':sha(base),'base_import_sources':{m:sha(ROOT/'P02A2'/(m+'.lean')) for m in ['MeasureCore','ObserverCore']},'source_python_sha256':sha(ORIGINAL/'code/prcodec.py'),'fresh_source_machine_witnesses':['immediate halt, defect 1','increment forever, defect 0'],'ordinary_correspondence_boundary':'The Lean compiler implements the recovered Python compiler construction with its register numbering and sequence/skip normalization. Python interpreter and full byte codec are not formally simulated.','still_open':['Canonical P02-L1 byte/numeric encoder-parser refinement','Formal primitive-recursive/computable index-map theorem','Undecidability proof for the source counter-machine indexing','General CV-C soft-mass/hierarchy reductions'],'canonical_adoption':False,'whole_obligation_closure':False}
p=R/'Q8_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');(R/'Q8_RESULT.json.sha256').write_text(sha(p)+'  Q8_RESULT.json\n');(ROOT/'LATEST_Q8_QUALIFICATION.txt').write_text(str(p)+'\n');print(json.dumps({'status':r['status'],'theorem_count':len(targets),'receipt':str(p),'sha256':sha(p)},indent=2))
