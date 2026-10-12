from pathlib import Path
import subprocess,tempfile,shutil,json,hashlib,re
A=Path(__file__).resolve().parent;P=A.parents[1]/'t20-consolidation-20261011/projection/package-v4';V=P.with_name('package-v3')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
for name,cmd in [('package',['validate_package.py']),('depth',['validate_depth.py']),('tools',['-m','unittest','discover','-s','tool-tests','-v'])]:
 r=subprocess.run(['python','-B',*cmd],cwd=P,capture_output=True,text=True);(A/(name+'-final.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,(name,r.stdout,r.stderr);checks[name]='PASS'
with tempfile.TemporaryDirectory(prefix='v4-final-whitespace-') as d:
 root=Path(d);shutil.copytree(P,root/'candidate');subprocess.run(['git','init','-q',str(root)],check=True);subprocess.run(['git','-C',str(root),'add','--all'],check=True)
 r=subprocess.run(['git','-C',str(root),'diff','--cached','--check'],capture_output=True,text=True);rows=[]
 for line in r.stdout.splitlines():
  m=re.match(r'candidate/(.+):(\d+): (.+)',line)
  if m:rows.append({'path':m[1],'line':int(m[2]),'diagnostic':m[3]})
 known=[x for row in json.loads((P/'depth/WHITESPACE_VERIFICATION.json').read_text())['advisories'] for x in row['diagnostics']]
 assert sorted(rows,key=str)==sorted(known,key=str),'unaccounted final whitespace'
checks['final_whitespace']='exact source advisories only: '+str(len(rows))
for row in json.loads((V/'PACKAGE_CONTENTS.json').read_text())['files']:assert h(V/row['path'])==row['sha256']
checks['immutable_v3']='PASS'
private=[]
for p in P.rglob('*'):
 if p.is_file():
  text=p.read_text(errors='ignore')
  if re.search(r'/(workspace/scratch|home/agent)/[^\s\"\']+',text):private.append(p.relative_to(P).as_posix())
  for match in re.findall(r'/tmp/[^\s`\"\']+',text):
   allowed={'private-locator:3eb3920439375ada6738','private-locator:d6808ce252611792fe1b','private-locator:046fed374acdc0119f19','private-locator:39866fa4df145aa06ba3','private-locator:5198022b8c2d094ce857','private-locator:ff65c22270810eeb9ec1','private-locator:71c3ac0c0a1e3f35edfd'}
   if match.rstrip(';.,') not in allowed:private.append(p.relative_to(P).as_posix()+':'+match)
assert not private,private
checks['private_absolute_paths']='none found; seven inherited generic /tmp output-directory examples explicitly allowed, not private custody locators'
out={'status':'PASS','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'checks':checks,'scope':'Candidate integrity, current binding, tools, source preservation and public-projection safeguards. No repository or theorem verification.'}
(A/'FINAL_LOCAL_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
