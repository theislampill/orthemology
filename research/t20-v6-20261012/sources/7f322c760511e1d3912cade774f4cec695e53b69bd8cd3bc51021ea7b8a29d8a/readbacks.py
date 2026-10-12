from pathlib import Path
import re,json,subprocess,hashlib
R=Path(__file__).resolve().parent;j=json.loads((R/'RESULT.json').read_text());ns=[]
for m in j['main_modules']+['IndependentDependentControls']:
 nsname='IndependentDependentAudit' if m=='IndependentDependentControls' else 'P01DF'
 for kind,n in re.findall(r'^(?:noncomputable )?(def|theorem|abbrev|structure|inductive)\s+(\w+)',(R/'sources'/(m+'.lean')).read_text(),re.M):ns.append((nsname+'.'+n,kind,m))
(R/'AUDIT_TARGETS.json').write_text(json.dumps(ns,indent=2)+'\n')
s='\n'.join('import '+m for m in j['main_modules']+['IndependentDependentControls'])+'\nset_option pp.universes true\nset_option pp.explicit true\nset_option format.width 180\n#print P01DF.Ty\n#print P01DF.Has\n'+''.join('#check @'+n+'\n#print axioms '+n+'\n' for n,_,_ in ns)
(R/'sources/IndependentAudit.lean').write_text(s)
p=subprocess.run(['python',str(R/'run_control.py'),'IndependentAudit'],capture_output=True);(R/'readbacks.log').write_bytes(p.stdout+p.stderr);assert p.returncode==0
out=p.stdout.decode();h=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",out);empty=re.findall(r"'([^']+)' does not depend on any axioms",out);ax={n:[a.strip() for a in vals.split(',') if a.strip()] for n,vals in h};ax.update({n:[] for n in empty});assert set(ax)=={n for n,_,_ in ns};assert all(set(a)<={'propext','Quot.sound','Classical.choice'} for a in ax.values());(R/'AXIOMS.json').write_text(json.dumps(ax,indent=2)+'\n')
print(len(ns),'targets;',sum(k=='theorem' for _,k,_ in ns),'theorems;',sorted({a for li in ax.values() for a in li}))
