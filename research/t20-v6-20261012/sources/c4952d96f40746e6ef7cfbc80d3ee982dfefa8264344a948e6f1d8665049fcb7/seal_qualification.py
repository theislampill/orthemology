import pathlib,json,re,hashlib,subprocess,os
R=pathlib.Path('receipts/qualification-20260930T134433Z'); O=pathlib.Path('private-locator:ed0f0021a1fad46fb3c4');T=pathlib.Path('private-locator:d97af50b47918e94879b')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (R/'all-types-and-axioms-corrected.exit').read_text().strip()=='0'
out=(R/'all-types-and-axioms-corrected.stdout').read_text()+(R/'all-types-and-axioms-corrected.stderr').read_text()
assert not re.search(r'\berror:|sorryAx',out)
inv=json.loads((O/'provenance/FORMAL_INVENTORY.json').read_text())['theorems'];names={t['declaration'] for t in inv};seen={}
for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):assert n not in seen;seen[n]=[x.strip() for x in a.split(',') if x.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):assert n not in seen;seen[n]=[]
assert set(seen)==names
for n,a in seen.items():
 assert set(a)<= {'propext','Classical.choice','Quot.sound'}
 assert any(l.lstrip('@').startswith(n+' :') or l.lstrip('@').startswith(n+'.{') for l in out.splitlines()),n
ss=json.loads((R/'SourceStatements.json').read_text())
for r in ss:assert sha(pathlib.Path(r['source']))==r['repaired_sha256'];assert r['statement_headers_whitespace_equivalent']
assert sum(r['theorems'] for r in ss)==130
modules=sorted({t['module'] for t in inv});art=[]
for m in modules:
 c=json.loads((R/('fresh-build-'+m+'.command.json')).read_text());assert c['exit']==0
 p=pathlib.Path('.lake/build/lib/lean')/pathlib.Path(*m.split('.')).with_suffix('.olean')
 assert p.stat().st_size>0 and p.stat().st_mtime>=c['started']-2
 art.append({'module':m,'sha256':sha(p),'bytes':p.stat().st_size})
deps=[]
for p in json.loads((O/'formal/lake-manifest.json').read_text())['packages']:
 name=p['name'];assert (R/('pin-'+name+'.stdout')).read_text().strip()==p['rev'];assert not (R/('clean-'+name+'.stdout')).read_text().strip();deps.append({'name':name,'revision':p['rev']})
r={'status':'REPAIRED_130_TARGETS_KERNEL_CHECKED','compiled_target_count':130,'new_attempt2_target_count':119,'predecessor_target_count':11,'source_statements_unchanged':True,'dependencies':deps,'sources':ss,'artifacts':art,'axioms':seen,'lean_binary_sha256':sha(T/'lean'),'lake_binary_sha256':sha(T/'lake'),'audit_source_sha256':sha(pathlib.Path('QualificationAudit.lean')),'audit_output_sha256':sha(R/'all-types-and-axioms-corrected.stdout'),'qualification_program_sha256':sha(pathlib.Path('qualify.py')),'input_zip_sha256':'f90e399269ccd33c1df42b13c085f09d4e85ea6e2ecfd6f6ee9501de6671d0e2','canonical_adoption':False,'obligation_completion':False,'scope':'Previously authored candidates only; new Q8 extension is separately qualified','retained_prior_failures':['Parallel clean rebuild interrupted; suspected resource contention','Audit option pp.width unsupported; all theorem readbacks occurred but nonzero exit excluded from pass credit'],'repair_audit':'All 130 theorem headers unchanged up to whitespace; source proofs and missing scope declarations corrected without changing definitions or theorem domains'}
p=R/'QUALIFIED_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');(R/'QUALIFIED_RESULT.json.sha256').write_text(sha(p)+'  QUALIFIED_RESULT.json\n');print(json.dumps({'status':r['status'],'targets':130,'receipt':str(p.resolve()),'sha256':sha(p)},indent=2))
