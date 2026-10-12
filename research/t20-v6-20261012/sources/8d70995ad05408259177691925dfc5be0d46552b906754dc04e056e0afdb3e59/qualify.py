"""Read-only source binding and isolated replay for the received Pro packets."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,time,zipfile,re,importlib.util
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
INTAKE=BASE/'t20-synthesis-owner-input-20261011/r3'
LARGE=next(INTAKE.glob('*Reconciled*.zip')); SMALL=next(INTAKE.glob('*111min*.zip'))
CORRECTED=BASE/'recovery-20261011/remaining-archives/safe-extracts/authorial-synthesis-response-preservation-20261011/authorial-synthesis-response-preservation-20261011/payload/authorial-synthesis-root-review-20261011/corrected-reference'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def archive(p):
 z=zipfile.ZipFile(p); members={x.filename:z.read(x) for x in z.infolist() if not x.is_dir()}
 prefix=next(iter(members)).split('/')[0]+'/'
 return {x[len(prefix):]:b for x,b in members.items()}, {'path':str(p.relative_to(BASE)), 'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'file_count':len(members),'crc_all_payload_reads':'pass','root_prefix':prefix}
a,ai=archive(LARGE);b,bi=archive(SMALL)
common=sorted(a.keys()&b.keys())
comparison={'inputs':[ai,bi],'common_files':len(common),'identical_common_files':sum(a[x]==b[x] for x in common),'differing_common_files':[x for x in common if a[x]!=b[x]],'small_only':sorted(b.keys()-a.keys()),'large_only_count':len(a.keys()-b.keys()),'common_bindings':[{'path':x,'sha256':sha(a[x]),'bytes':len(a[x]),'identical':a[x]==b[x]} for x in common]}
write('ARCHIVE_COMPARISON.json',comparison)
write('ACTUAL_MEMBERS.json',[{'path':x,'bytes':len(v),'sha256':sha(v)} for x,v in sorted(a.items())])
# Match the advertised root source-copy inventory against the actually supplied ZIP.
docs=json.loads(a['corpus/documents.json']);bindings=[]
for d in docs:
 cp=d.get('copied_path')
 if not cp:continue
 v=a.get(cp); state='missing' if v is None else ('match' if sha(v)==d['sha256'] and len(v)==d['bytes'] else 'mismatch')
 bindings.append({'id':d['id'],'path':cp,'expected_sha256':d['sha256'],'expected_bytes':d['bytes'],'status':state,'original_names':d.get('names',[]),'archive_ids':d.get('archive_ids',[])})
write('SOURCE_BINDINGS.json',{'scope':'All corpus/documents.json entries with nonempty copied_path; byte inventory only, not semantic reading.','advertised_count':len(bindings),'matched':sum(x['status']=='match' for x in bindings),'missing':sum(x['status']=='missing' for x in bindings),'mismatched':sum(x['status']=='mismatch' for x in bindings),'entries':bindings})
manifest_reports=[]
for name,v in a.items():
 if Path(name).name!='MANIFEST.json': continue
 m=json.loads(v);items=m.get('files');prefix=name[:-len('MANIFEST.json')]
 if isinstance(items,list): items={x['path']:x for x in items}
 if not isinstance(items,dict):continue
 checks=[]
 for p,x in items.items():
  data=a.get(prefix+p)
  status='missing' if data is None else ('match' if sha(data)==x.get('sha256') and len(data)==x.get('bytes') else 'mismatch')
  checks.append({'path':prefix+p,'expected_sha256':x.get('sha256'),'expected_bytes':x.get('bytes'),'status':status})
 manifest_reports.append({'manifest':name,'sha256':sha(v),'entries':checks,'matched':sum(x['status']=='match' for x in checks),'missing':sum(x['status']=='missing' for x in checks),'mismatched':sum(x['status']=='mismatch' for x in checks)})
write('MISSING_MANIFEST_MEMBERS.json',{'root_manifest_present':'MANIFEST.json' in a,'root_manifest_limit':'The original reconciled root manifest is absent. Its full sealed membership cannot be reconstructed. corpus/documents.json provides a separate advertised copied-source inventory.','nested_manifests':manifest_reports,'advertised_source_missing_paths':[x['path'] for x in bindings if x['status']=='missing']})
# Isolated copies contain only inspected current reference code/tests/verifier.
for label,source in [('received-52',a),('recovered-52',b)]:
 dest=OUT/'working'/label;dest.mkdir(parents=True,exist_ok=False)
 for name,data in source.items():
  if name in ['verify_packet.py','research/contracts.py','research/__init__.py'] or name.startswith('tests/'):
   p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
cor=OUT/'working/corrected-55';shutil.copytree(OUT/'working/received-52',cor)
for name in ['research/contracts.py','tests/test_iterator_regression.py']:
 shutil.copyfile(CORRECTED/name,cor/name)
write('REPLAY_COPY_BINDINGS.json',[{'copy':str(p.relative_to(OUT)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in (OUT/'working').rglob('*') if p.is_file()])
runs=[]
def run(label,cmd,cwd):
 started=time.time();r=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=120)
 (OUT/'logs'/f'{label}.stdout').write_text(r.stdout);(OUT/'logs'/f'{label}.stderr').write_text(r.stderr)
 count=re.search(r'Ran (\d+) tests? in',r.stderr+r.stdout)
 rec={'label':label,'command':cmd,'cwd':str(Path(cwd).relative_to(BASE)),'returncode':r.returncode,'duration_seconds':time.time()-started,'observed_unittest_count':int(count.group(1)) if count else None,'stdout':f'logs/{label}.stdout','stderr':f'logs/{label}.stderr','mode':'optimized' if '-O' in cmd else 'normal'};runs.append(rec)
 print(label,r.returncode,rec['observed_unittest_count'])
for label in ['received-52','recovered-52','corrected-55']:
 for mode in ['normal','optimized']:
  cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+['-B','-m','unittest','discover','-s','tests','-v']
  run(label+'-'+mode,cmd,OUT/'working'/label)
for label,path in [('trimmed-reconciled-manifest',LARGE),('recovered-manifest',SMALL)]:
 run(label,[sys.executable,'-B',str(OUT/'working/received-52/verify_packet.py'),str(path)],BASE)
# Controlled reproduction of known direct-helper defect; no new repairs.
helper=[]
for label in ['received-52','corrected-55']:
 p=OUT/'working'/label/'research/contracts.py';spec=importlib.util.spec_from_file_location(label,p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 lists=module.affected_nodes({'second':['first'],'first':['source']},['source'])
 iters=module.affected_nodes({'second':iter(['first']),'first':iter(['source'])},['source'])
 helper.append({'copy':label,'reusable_list_result':sorted(lists),'one_shot_result':sorted(iters),'expected':['first','second'],'iterator_contract_pass':iters=={'first','second'}})
write('HELPER_REPRODUCTION.json',helper)
write('TEST_RUNS.json',{'python':sys.version,'scope':'Current reference suites only. No corpus build, prior-source programs, or Lean compilation. Direct -O invokes optimized tests.','runs':runs})
print('comparison',comparison['common_files'],comparison['identical_common_files'])
print('source_bindings',len(bindings),'missing',sum(x['status']=='missing' for x in bindings))
print('nested_manifests',[(x['manifest'],x['matched'],x['missing'],x['mismatched']) for x in manifest_reports])
