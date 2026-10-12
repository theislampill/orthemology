from pathlib import Path
import datetime,hashlib,json,os,subprocess,re
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-auxiliary-checker-computability-20261010';e=json.loads((R/'env.json').read_text());env={**os.environ,'LEAN_PATH':e['LEAN_PATH']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
neg=[]
cached={x['name']:x for x in json.loads((R/'INDEPENDENT_NEGATIVE_RESULTS.json').read_text())} if (R/'INDEPENDENT_NEGATIVE_RESULTS.json').exists() else {}
for name in json.loads((R/'INDEPENDENT_NEGATIVE_TARGETS.json').read_text()):
 src=R/'negative'/(name+'.lean')
 if name in cached:
  r=cached[name];assert rec(src)==r['source'] and rec(W/r['log']['path'])==r['log'];neg.append(r);continue
 p=subprocess.run([e['lean'],'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=R/'output'/(name+'.log');log.write_text(p.stdout)
 expected="tactic 'decide' proved that the proposition"
 assert p.returncode!=0 and expected in p.stdout and not any(x in p.stdout for x in ['unknown identifier','unexpected token','failed to import','unknown module']),log
 neg.append({'name':name,'source':rec(src),'log':rec(log),'exit_code':p.returncode,'expected_rejection':expected});print('REJECTED',name,flush=True)
(R/'INDEPENDENT_NEGATIVE_RESULTS.json').write_text(json.dumps(neg,indent=2)+'\n')
names=json.loads((R/'ALL_HELPER_TARGETS.json').read_text());audit=(R/'output/AllHelperAudit.log').read_text();rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",audit)
assert len(rows)==len(names)==83 and {x[0] for x in rows}==set(names)
assert all(set(ax.split(', '))<={'propext','Classical.choice','Quot.sound'} for _,ax in rows)
positive=[]
for name in ['IndependentSourceControls','IndependentCodeControls','AllHelperAudit']:
 src=R/'sources'/(name+'.lean');obj=R/'output'/(name+'.olean');log=R/'output'/(name+'.log');assert obj.exists()
 assert not any(x in log.read_text() for x in ['warning:','sorryAx','error:']),log
 if name!='AllHelperAudit':assert not re.search(r'check(?:Step|Red|Finite|Poly|Lookup)Code_exact',src.read_text())
 positive.append({'name':name,'source':rec(src),'object':rec(obj),'log':rec(log),'theorem_count':len(re.findall(r'^theorem ',src.read_text(),re.M))})
(R/'INDEPENDENT_POSITIVE_RESULTS.json').write_text(json.dumps(positive,indent=2)+'\n')
# Mechanically guard exact direct imports and the first actual object path.
imports={}
search=[Path(x) for x in e['LEAN_PATH'].split(':')]
selected=json.loads((R/'SELECTIVE_REPLAY.json').read_text())['positive']
pdict={x['path']:x for x in json.loads((R/'REVIEW_INPUT_PINS.json').read_text())}
for item in selected:
 src=W/item['source']['path'];deps=[]
 for m in re.findall(r'^import\s+(\S+)',src.read_text(),re.M):
  matches=[d/(m.replace('.','/')+'.olean') for d in search if (d/(m.replace('.','/')+'.olean')).exists()];assert matches,(src,m)
  obj=matches[0];pin=rec(obj)
  if obj.parent!=R/'output':assert pin==pdict.get(pin['path']),(src,m,pin)
  deps.append({'module':m,'selected_object':pin})
 imports[item['module']]=deps
(R/'EXACT_IMPORT_GUARDS.json').write_text(json.dumps(imports,indent=2)+'\n')
# Every candidate source is frozen, no replacement codecs or unsafe proof escapes.
for src in C.glob('*.lean'):
 assert rec(src)==pdict[str(src.relative_to(W))],src
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b|instance\s+.*(?:Encodable|Primcodable)',src.read_text()),src
for p in pdict.values():
 f=W/p['path'];assert sha(f)==p['sha256'] and f.stat().st_size==p['bytes'],f
print('PASS_EVIDENCE',len(positive),'positive controls',len(neg),'negative controls',len(names),'axiom targets',flush=True)
