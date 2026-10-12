from pathlib import Path
import json,re
R=Path(__file__).resolve().parent
rows=json.loads((R/'rules.json').read_text())
heads={'JointCompletion.CtxJ':'ctxJ','JointCompletion.FormJ':'formJ','JointCompletion.HasJ':'hasJ','P01AC.ExtensionalRepair.CtxE':'ctxE','P01AC.ExtensionalRepair.FormE':'formE','P01AC.ExtensionalRepair.HasE':'hasE'}
aux={'P01AC.Lookup':('LookupCert','checkLookup','checkLookup_sound','lookup_complete'),'OrthemologyV3.FiniteDerives':('FiniteCert','checkFinite','checkFinite_sound','finite_complete'),'P01AC.Intensional.Plus.PolyConvPlus':('PolyCert','checkPoly','checkPoly_sound','poly_complete')}
def norm(s):return re.sub(r'\s+',' ',s).replace('ℕ','Nat')
def claim(s):
 s=norm(s)
 for k,v in heads.items():
  if s.startswith(k+' '):return 'Claim.'+v+s[len(k):]
 raise ValueError(s)
for r in rows:
 r['tag']=r['ctor'].split('.')[-2]+'_'+r['ctor'].split('.')[-1]
 r['params']=[];r['children']=[];r['sides']=[];r['sourceargs']=[];r['auxes']=[]
 for a in r['args']:
  t=norm(a['type'])
  if not a['prop']:
   r['params'].append((a['name'],t));r['sourceargs'].append(a['name']);continue
  h=t.split(' ',1)[0]
  if h in heads:
   n='h'+str(len(r['children']));r['children'].append((n,claim(t)));r['sourceargs'].append(n)
  elif h in aux:
   ac,check,sound,comp=aux[h];cn='aux'+str(len(r['auxes']));sn='s'+str(len(r['sides']))
   r['params'].append((cn,'AuxiliaryCertificates.'+ac))
   condition=f'AuxiliaryCertificates.{check} {cn}{t[len(h):]} = true'
   r['sides'].append((sn,condition));r['sourceargs'].append(f'(AuxiliaryCertificates.{sound} {sn})')
   r['auxes'].append((cn,comp,a['name'],t))
  elif t.startswith('∀ n < τ.length,'):
   r['family']=('n','τ',claim(t.split(', ',1)[1]));r['sourceargs'].append('(fun n hn => hfamily ⟨n,hn⟩)')
  else:
   sn='s'+str(len(r['sides']));r['sides'].append((sn,t));r['sourceargs'].append(sn)
 r['pattern']='.'+r['tag']+' '+ ' '.join(p for p,t in r['params'])
 r['declaration']='  | '+r['tag']+' '+ ' '.join('('+p+' : '+t+')' for p,t in r['params'])
 r['claim']=claim(r['conclusion'])
 r['plist']='['+', '.join(c for n,c in r['children'])+']'
 if 'family' in r:
  r['plist']='(List.ofFn (fun i : Fin τ.length => '+r['family'][2].replace(' τ n',' τ i.val')+')) ++ '+r['plist']
 r['side']=' ∧ '.join('('+s+')' for n,s in r['sides'])+(' ∧ True' if r['sides'] else 'True')
header='''/- Finite rule payloads generated from the actual frozen constructor types.
The generated code itself is kernel checked; no source proof is a payload. -/
import CertificateFramework
import AuxiliaryCertificates
namespace JointCertificates
open P01AC P01D OrthemologyV2 OrthemologyV3
set_option maxRecDepth 16384
set_option maxHeartbeats 16000000
set_option linter.unusedVariables false

inductive Rule where
'''
s=header+'\n'.join(r['declaration'] for r in rows)+'\n\n'
s+='def Rule.conclusion : Rule → Claim\n'+''.join('  | '+r['pattern']+' => '+r['claim']+'\n' for r in rows)+'\n'
s+='def Rule.premises : Rule → List Claim\n'+''.join('  | '+r['pattern']+' => '+r['plist']+'\n' for r in rows)+'\n'
s+='def Rule.checkSide : Rule → Bool\n'+''.join('  | '+r['pattern']+' => decide ('+r['side']+')\n' for r in rows)+'\n'
s+='''theorem Rule.sound (r : Rule) (hs : r.checkSide = true)
    (hp : All Claim.denote r.premises) : r.conclusion.denote := by
  cases r with
'''
for r in rows:
 s+='  | '+r['pattern'][1:]+' =>\n'
 s+='      simp only [Rule.checkSide, decide_eq_true_eq] at hs\n'
 if r['sides']:s+='      rcases hs with ⟨'+', '.join(n for n,t in r['sides'])+', _⟩\n'
 s+='      simp only [Rule.premises, '+('all_append, all_ofFn, ' if 'family' in r else '')+'All, Claim.denote] at hp\n'
 if r['children'] or 'family' in r:
  ns=[n for n,c in r['children']]+['_']
  if 'family' in r: ns=['hfamily','⟨'+', '.join(ns)+'⟩']; # append yields pair
  s+='      rcases hp with ⟨'+', '.join(ns)+'⟩\n'
 s+='      exact @'+r['ctor']+' '+' '.join(r['sourceargs'])+'\n'
s+='''
abbrev DerivationCertificate := Certificate Rule

def check (c : DerivationCertificate) (j : Claim) : Bool :=
  Certificate.checkRoot Rule.conclusion Rule.premises Rule.checkSide c j

theorem check_sound {c : DerivationCertificate} {j : Claim} (h : check c j = true) : j.denote :=
  Certificate.checkRoot_sound _ _ _ Rule.sound c j h

abbrev Proved := Certificate.Proved Rule.conclusion Rule.premises Rule.checkSide

theorem proved_rule (r : Rule) (hs : r.checkSide = true) (hp : All Proved r.premises) :
    Proved r.conclusion := Certificate.proved_rule _ _ _ r hs hp

#print axioms Rule.sound
#print axioms check_sound
end JointCertificates
'''
(R/'CertificateRules.lean').write_text(s)
(R/'generated_rule_metadata.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
print('Generated',len(rows),'actual rules')
