from pathlib import Path
import json,hashlib,re,subprocess
R=Path(__file__).resolve().parent;F=Path('private-locator:4895465318e5977e697d');H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads((R/'RESULT.json').read_text());qpath=F/'qualification-final/QUALIFICATION.json';q=json.loads(qpath.read_text());old=json.load(open('private-locator:c93a515a32e97cb518f7'));ax=json.loads((R/'AXIOMS.json').read_text());targets=json.loads((R/'AUDIT_TARGETS.json').read_text())
assert q['status']=='KERNEL_VERIFIED_SCOPED_DEPENDENT_SUCCESSOR' and q['kernel_credit'];assert j['status']=='FRESH_INDEPENDENT_BUILD_AND_AXIOM_READBACK_PASS'
assert H(j['compiler_path'])==j['compiler_sha256']==q['compiler_binary_sha256']=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
assert H('private-locator:3537146eb78a87f8f527')==q['successor_archive_sha256']=='e4698d9acf9f2b3ab637c0b35bbfb361b8c31a58368bef4ddbace53693867f24'
for n,row in j['sources'].items():
 assert q['source_bindings'][n]['sha256']==row['sha256']==H(R/'sources'/(n+'.lean'))==H(row['origin']),n
 assert H(R/'lib'/(n+'.olean'))==row['olean_sha256']
 if n not in j['main_modules']:assert old['sources'][n]['sha256']==row['sha256'],n
names={n for n,k,m in targets if m!='IndependentDependentControls'};assert names==set(q['declarations'])
for n in names:assert set(ax[n])==set(q['declarations'][n]['axioms']),n
assert all(x['exit_code']==0 for x in j['builds']);assert all(x['expected_failure_observed'] for x in json.loads((R/'MUTATION_CONTROLS.json').read_text()))
def strip_lean(s):
 out=[];i=0;depth=0;string=False
 while i<len(s):
  if depth:
   if s.startswith('/-',i):depth+=1;i+=2
   elif s.startswith('-/',i):depth-=1;i+=2
   else:i+=1
  elif string:
   if s[i]=='\\':i+=2
   elif s[i]=='"':string=False;i+=1
   else:i+=1
  elif s.startswith('/-',i):depth=1;out.append(' ');i+=2
  elif s.startswith('--',i):
   e=s.find('\n',i);i=len(s) if e<0 else e;out.append(' ')
  elif s[i]=='"':string=True;out.append(' ');i+=1
  else:out.append(s[i]);i+=1
 assert not depth and not string
 return ''.join(out)
hyg=[]
for n in j['main_modules']:
 p=R/'sources'/(n+'.lean');hits=re.findall(r'\b(?:sorry|admit|axiom|unsafe|native_decide)\b',strip_lean(p.read_text()));assert not hits,(n,hits);hyg.append({'module':n,'source_sha256':H(p),'disallowed_code_tokens':hits})
(R/'SOURCE_HYGIENE.json').write_text(json.dumps(hyg,indent=2)+'\n')
P=Path('private-locator:941dcb26d2a0fbcb9927');deps=[]
for row in q['dependencies']:
 name=row['name'];commit=subprocess.check_output(['git','-C',str(P/name),'rev-parse','HEAD'],text=True).strip();status=subprocess.check_output(['git','-C',str(P/name),'status','--porcelain','--untracked-files=no'],text=True);assert commit==row['revision'] and not status;deps.append({'name':name,'commit':commit,'tracked_clean':not status})
actual_dependencies=[]
expected={row['name']:row['revision'] for row in q['dependencies']}
for entry in j['lean_path'].split(':')[1:]:
 root=Path(entry).parents[3];name='mathlib' if root.name=='mathlib4' else root.name
 commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip();status=subprocess.check_output(['git','-C',str(root),'status','--porcelain','--untracked-files=no'],text=True);assert commit==expected[name] and not status
 actual_dependencies.append({'name':name,'source_root':str(root),'commit':commit,'tracked_clean':not status})
canon=Path('private-locator:36fb2027a2cd56fb6b89');commit=subprocess.check_output(['git','-C',str(canon),'rev-parse','HEAD'],text=True).strip();status=subprocess.check_output(['git','-C',str(canon),'status','--porcelain'],text=True);assert commit=='03e2604dfcef278b01c60d19b05370fcec4194b6' and not status
out={'status':'PASS','qualification_receipt_sha256':H(qpath),'main_sources':{n:j['sources'][n]['sha256'] for n in j['main_modules']},'local_modules':len(j['sources']),'main_targets':len(names),'main_theorems':sum(k=='theorem' and m!='IndependentDependentControls' for n,k,m in targets),'independent_targets':sum(m=='IndependentDependentControls' for n,k,m in targets),'independent_theorems':sum(k=='theorem' and m=='IndependentDependentControls' for n,k,m in targets),'axiom_union':sorted({a for li in ax.values() for a in li}),'dependencies':deps,'actual_readonly_dependencies':actual_dependencies,'canonical_commit':commit,'canonical_clean':True}
(R/'INPUT_IDENTITY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='main_sources' and k!='dependencies'},indent=2))
