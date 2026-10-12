from pathlib import Path
import re,json,os,subprocess,hashlib,sys
A=Path(sys.argv[1]).resolve();B=A.parents[2];mods=sys.argv[2:];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();targets=[]
for mod in mods:
 text=(A/'snapshot'/(mod.replace('.','/')+'.lean')).read_text()
 text=re.sub(r'/-[\s\S]*?-/|--[^\n]*','',text)
 scopes=[]
 for line in text.splitlines():
  s=line.strip()
  m=re.match(r'namespace\s+(\S+)',s)
  if m:scopes.append(('namespace',m[1]));continue
  m=re.match(r'(?:noncomputable\s+)?section(?:\s+(\S+))?$',s)
  if m:scopes.append(('section',m[1]));continue
  if re.match(r'end(?:\s+\S+)?$',s):
   assert scopes,(mod,s)
   scopes.pop();continue
  m=re.match(r'(?:@\[[^]]*\]\s*)*(?:noncomputable\s+)?(?:def|abbrev|lemma|theorem|instance|structure|inductive)\s+([A-Za-z_][\w]*)',s)
  if m:targets.append('.'.join([v for k,v in scopes if k=='namespace']+[m[1]]))
 assert all(k=='section' and v is None for k,v in scopes),(mod,scopes)
assert len(targets)==len(set(targets))
p=A/'Readback.lean';p.write_text('\n'.join('import '+m for m in mods)+'\nset_option pp.universes true\nset_option pp.explicit true\n'+''.join('#check '+t+'\n#print '+t+'\n#print axioms '+t+'\n' for t in targets))
env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip());cmd=[str(B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean'),'-j1',str(p)];r=subprocess.run(cmd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs/Readback.log';log.write_text(r.stdout)
entries=re.findall(r"'([^']+)' (depends on axioms: \[[^\]]*\]|does not depend on any axioms)",r.stdout)
assert r.returncode==0 and [n for n,_ in entries]==targets,(r.returncode,len(entries),len(targets),r.stdout[-1200:])
for name,line in entries:
 if '[' in line:assert all(v.strip() in ['propext','Classical.choice','Quot.sound'] for v in line.split('[')[1].strip(']').split(',')),(name,line)
assert 'sorryAx' not in r.stdout
rec={'status':'PASS','targets':targets,'target_count':len(targets),'axiom_readback_count':len(entries),'axiom_free_count':sum('does not depend' in x for _,x in entries),'source_sha256':sha(p),'log_sha256':sha(log),'exit':r.returncode,'command':cmd,'allowed_axioms':['propext','Classical.choice','Quot.sound']}
(A/'READBACK_RESULT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
