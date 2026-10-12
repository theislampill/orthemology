from pathlib import Path
import hashlib,json,collections,os,shutil,re,subprocess,tempfile
B=Path(__file__).resolve().parents[2];P=B/'projection/package'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
manifest=json.loads((P/'PUBLIC_PROJECTION.json').read_text());rows=manifest['files'];byhash={r['original_sha256']:r for r in rows}
# Actual copied upstream/adapted source headers are retained. Add licence copies at their declared location.
lic=byhash['b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1'];raw=(P/lic['public_path']).read_bytes()
for source in P.rglob('PolyCertificateEncoding.lean'):
 rel=(source.parent/'vendor/LICENSE').relative_to(P).as_posix();dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 lic.setdefault('required_replay_copies',[])
 lic['required_replay_copies']=[x for x in lic['required_replay_copies'] if x['path']!=rel]
 lic['required_replay_copies'].append({'path':rel,'sha256':sha(raw),'bytes':len(raw),'reason':'Apache license at the adapted source header’s declared vendor location.'})
third=[]
for name,origin,kind in [('LocalFintypeProd.lean','Mathlib/Data/Fintype/Prod.lean','exact upstream source'),('CodecDeriveEncodable.lean','Mathlib/Tactic/DeriveEncodable.lean','exact upstream source'),('PolyCertificateEncoding.lean','Mathlib data-encoding interface and Lean Encoding API','explicitly attributed adaptation')]:
 files=[p.relative_to(P).as_posix() for p in P.rglob(name)]
 if files:third.append({'module':name,'kind':kind,'upstream':origin,'mathlib_commit':'c44e0c8ee63ca166450922a373c7409c5d26b00b','license':'LICENSES/Mathlib-LICENSE.txt','copied_paths':files})
(P/'THIRD_PARTY_ATTRIBUTION.json').write_text(json.dumps({'sources':third,'note':'No package-wide relicensing claim. Original author/copyright headers retained; original constructive notice preserved in LICENSES.'},indent=2)+'\n')
(P/'THIRD_PARTY_NOTICES.md').write_text('# Third-party source notices\n\nThe copied LocalFintypeProd and CodecDeriveEncodable source bodies are unchanged pinned Mathlib files. PolyCertificateEncoding is explicitly identified as an adaptation in its source header. Original copyright and attribution headers remain intact. The exact [Apache 2.0 licence](LICENSES/Mathlib-LICENSE.txt) is included. [THIRD_PARTY_ATTRIBUTION](THIRD_PARTY_ATTRIBUTION.json) lists each actual copy and upstream owner. The original constructive packet notice is preserved separately; its internal locators describe that original packet. No new licence is asserted for other research.\n')
# Public formal replay map: preserve all cluster-specific source identities and execution boundaries.
formal=json.loads((B/'proofs/FORMAL_REPLAY_MAP.json').read_text())
def binding(x):
 h=x['sha256'];r=byhash.get(h)
 if r is None:return {'original_sha256':h,'bytes':x['bytes'],'disposition':'original-custody-only; not required source closure unless explicitly stated'}
 return {'original_sha256':h,'original_bytes':x['bytes'],'public_source':r.get('public_path',r.get('public_url')),'public_sha256':r['public_sha256'],'public_bytes':r['public_bytes'],'original_module_filename':Path(x['path']).name}
clusters=[]
for c in formal['clusters']:
 out={k:c[k] for k in ['cluster_id','formal','notes','replay_recipe','fresh_consolidation_lean_build','public_execution_promise','runtime','closure_status','scope'] if k in c}
 for k in ['selected_entry_modules','historical_entrypoints','source_scripts','dependency_binding_records']:
  if k in c:out[k]=[binding(x) for x in c[k]]
 clo=c.get('minimal_unchanged_source_closure')
 if clo:
  out['minimal_unchanged_source_closure']={k:v for k,v in clo.items() if k!='source_files'}
  out['minimal_unchanged_source_closure']['source_files']=[binding(x) for x in clo['source_files']]
 out['source_layout']='See PROOF_FAMILY_LAYOUTS and PUBLIC_PROJECTION required_replay_copies for the retained isolated original layouts; do not flatten modules by basename. Public source addresses bind exact selected bytes.'
 clusters.append(out)
# Strip source-only private pin-source paths from external configuration.
env={k:v for k,v in formal['external_toolchain'].items() if k not in {'pin_source','repository_source_pin'}}
(P/'proofs/FORMAL_REPLAY_MAP.json').write_text(json.dumps({'schema':'t20-public-replay-map-v1','clusters':clusters,'external_toolchain':env,'global_warning':formal['global_warning'],'source_family_dispositions':[{'family':x['family'],'role':x['role'],'sources':[binding(z) for z in x['lean_sources']],'coverage':x['coverage']} for x in formal['source_family_dispositions']]},indent=2)+'\n')
# Family dispositions record actual closure reconciliation rather than adjacency-based absence inference.
f=P/'FAMILY_DISPOSITIONS.json';d=json.loads(f.read_text())
for row in d['families']:
 if row['disposition']=='written_result_owner':
  row['implementation']='This source selection is a written owner. Adjacency is not evidence of absent code: consult all source bindings and the reconciled formal-family map.'
 d['formal_reconciliation']='All selected entry/source closure hashes in the final 31-cluster track map were reconciled to PUBLIC_PROJECTION; available copied or pinned bytes, not adjacency, controls inclusion.'
f.write_text(json.dumps(d,indent=2)+'\n')
# Root typed dependency interface and kickoff handoff, prepared outside repository payload.
for name in ['DEPENDENCY_INDEX.json','CROSS_FRONT_INTERFACES.json']:
 if (B/name).exists():shutil.copyfile(B/name,P/name)
if (B/'CODEX_KICKOFF_PROMPT.txt').exists():shutil.copyfile(B/'CODEX_KICKOFF_PROMPT.txt',B/'projection/CODEX_KICKOFF_PROMPT.txt')
# Explicit finite-suite scope (source preservation elsewhere is not a runnable claim).
import sys
sys.path.insert(0,str(P));from replay_selected import SUITES
(P/'REPLAY_SCOPE.json').write_text(json.dumps({'integrity_command':'python -B validate_package.py','finite_control_runner':'python -B replay_selected.py --suite NAME','suites':SUITES,'dependency_versions_observed_in_consolidation':{'python':'3.12.14','sympy':'1.14.0','mpmath':'1.3.0'},'kernel_sources':'31-cluster source/replay map includes 23 formal clusters; no fresh compilation of the entire projected source corpus is asserted. Literal46-module closure checked statically. Selected historical receipts remain inherited.','other_scientific_scripts':'Included to carry later work; old source-specific drivers may need external pins, bound snapshots or path relocation. No suite-wide replay PASS is inferred.'},indent=2)+'\n')
(P/'PUBLIC_PROJECTION.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
# Reproducible package-tool negative controls operate in fresh disposable repositories.
for src in (B/'projection/tests').glob('test_*.py'):
 text=src.read_text().replace("ROOT/'package'/", "ROOT/").replace("ROOT/'package'", "ROOT").replace("dir=ROOT/'private'", "").replace("fixture@example.invalid", "fixture.invalid")
 if src.name=='test_replay.py':text=text.replace("parents[1]/'package'", "parents[1]")
 dest=P/'tool-tests'/src.name;dest.parent.mkdir(exist_ok=True);dest.write_text(text)
# Fresh selected replay evidence, summarized without runtime paths or raw logs.
checks=[]
for receipt in sorted((B/'projection/private/replay-results').glob('*.json')):
 data=json.loads(receipt.read_text())
 checks.append({k:data[k] for k in ['status','suite','python_version','dependencies','scope']})
 checks[-1]['commands']=[{k:r[k] for k in ['python_arguments','exit_code','output_sha256']} for r in data['results']]
 checks[-1]['receipt_sha256']=sha(receipt.read_bytes())
 checks[-1]['scope_note']='Fresh execution of the projected selected finite suite in a disposable copy; no whole-corpus or new kernel claim.'
(P/'SELECTED_REPLAY_VERIFICATION.json').write_text(json.dumps({'runs':checks},indent=2)+'\n')
# Public scientific review: exact report/findings/snapshot, with review scope intact.
review=P/'reviews';review.mkdir(exist_ok=True)
review_bindings=[]
for original,destination in [('REVIEW.md','SCIENTIFIC_REVIEW.md'),('FINDINGS.json','SCIENTIFIC_FINDINGS.json'),('FINAL_REVIEW_SNAPSHOT.json','SCIENTIFIC_ASSEMBLY_SNAPSHOT.json')]:
 source=B/'review/scientific'/original;raw=source.read_bytes();(review/destination).write_bytes(raw)
 review_bindings.append({'path':'reviews/'+destination,'original_sha256':sha(raw),'public_sha256':sha(raw),'bytes':len(raw),'projection':'EXACT'})
(review/'REVIEW_BINDINGS.json').write_text(json.dumps({'scope':'The scientific review snapshot binds the reviewed assembly originals; READER_PROJECTION separately binds their public copies. Review was selective, not entire-corpus semantic re-certification or fresh kernel execution.','files':review_bindings},indent=2)+'\n')
# Actual staged-delta whitespace audit in a disposable checkout. Source exceptions are
# individually bound; no root attributes are applied by this preparation.
with tempfile.TemporaryDirectory(dir=B/'projection/private',prefix='whitespace-') as temp:
 root=Path(temp);shutil.copytree(P,root/'candidate')
 subprocess.run(['git','init','-q',str(root)],check=True)
 subprocess.run(['git','-C',str(root),'add','--all'],check=True)
 result=subprocess.run(['git','-C',str(root),'diff','--cached','--check'],capture_output=True,text=True)
 diagnostics=[]
 for line in result.stdout.splitlines():
  match=re.match(r'candidate/(.+):(\d+): (.+)',line)
  if match:diagnostics.append({'path':match[1],'line':int(match[2]),'diagnostic':match[3]})
source_by_path={}
for row in rows:
 if row['disposition']=='included':
  source_by_path[row['public_path']]=row
  for extra in row.get('required_replay_copies',[]):source_by_path[extra['path']]=row
advisories=[]
for rel in sorted({x['path'] for x in diagnostics}):
 raw=(P/rel).read_bytes();row=source_by_path.get(rel)
 if row is None or sha(raw)!=row['original_sha256']:
  raise ValueError('Whitespace issue in authored/amended bytes: '+rel)
 advisories.append({'path':rel,'original_sha256':row['original_sha256'],'public_sha256':sha(raw),'bytes':len(raw),'diagnostics':[x for x in diagnostics if x['path']==rel],'disposition':'Inherited exact-source formatting retained; not a new authored/amended whitespace defect.'})
(P/'EXACT_SOURCE_WHITESPACE.json').write_text(json.dumps({'whole_delta_strict_exit_code':result.returncode,'whole_delta_strict_pass':result.returncode==0,'authored_and_amended_files_strict_pass':True,'advisories':advisories,'policy':'No whitespace normalization of original Lean or unapplied patch bytes. This is not a whole-delta whitespace PASS. Exact per-file attribute proposals are supplied for later integration review only.'},indent=2)+'\n')
(P/'PROPOSED_EXACT_SOURCE_ATTRIBUTES.txt').write_text('# Proposed only; not applied. Each exact path and hash is inventoried in EXACT_SOURCE_WHITESPACE.json.\n# Existing baseline uses scoped exact-source -text/whitespace attributes; these entries require integration review.\n'+'\n'.join('research/t20-consolidated-20261011/'+x['path']+' -text whitespace=-trailing-space' for x in advisories)+'\n')
# Inventory includes every actual payload member, excluding its own self-reference.
files=[]
for path in sorted(P.rglob('*')):
 if path.is_symlink():raise ValueError('symlink')
 if path.is_file() and path.name!='PACKAGE_CONTENTS.json':
  raw=path.read_bytes();files.append({'path':path.relative_to(P).as_posix(),'sha256':sha(raw),'bytes':len(raw)})
(P/'PACKAGE_CONTENTS.json').write_text(json.dumps({'schema':'t20-consolidated-package-contents-v1','scope':'Integrity of this exact public candidate; source hash identity is not scientific verification. This manifest excludes itself; delivery seal binds its hash.','files':files},indent=2)+'\n')
print(json.dumps({'files':len(files)+1,'bytes':sum(x['bytes'] for x in files)+(P/'PACKAGE_CONTENTS.json').stat().st_size,'manifest_sha256':sha((P/'PACKAGE_CONTENTS.json').read_bytes())}))
