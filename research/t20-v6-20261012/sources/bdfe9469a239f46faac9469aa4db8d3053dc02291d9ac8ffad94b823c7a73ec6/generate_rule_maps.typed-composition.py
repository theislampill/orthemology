#!/usr/bin/env python3
"""Translate retained constructor metadata to explicitly proved code maps.
Every emitted equation is checked against the original Rule functions in Lean.
This generator is not trusted by the theorems.
"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parent
rows=json.loads((R.parent/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json').read_text())
class Parser:
 def __init__(self,s,params):
  ts=re.findall(r'::|\+\+|[()\[\],]|[^\s()\[\],]+',s);self.ts=[]
  for t in ts:
   bits=t.split('.')
   if len(bits)>1 and bits[0] in params:
    self.ts += [bits[0]]+['.'+x for x in bits[1:]]
   elif len(bits)>1 and bits[-1] in ['all','pi','sigma','identity','app'] and bits[-2] not in ['Ty','Poly']:
    self.ts += ['.'.join(bits[:-1]),'.'+bits[-1]]
   else:self.ts.append(t)
  self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def pop(self):t=self.peek();self.i+=1;return t
 def atom(self):
  t=self.pop()
  if t=='(':
   e=self.expr();assert self.pop()==')'
  elif t=='[':
   es=[]
   while self.peek()!=']':
    es.append(self.expr())
    if self.peek()!=',':break
    self.pop()
   assert self.pop()==']';e=('list',es)
  else:e=('var',t)
  while self.peek() and self.peek().startswith('.'):
   m=self.pop()[1:];e=('app',('var','method.'+m),[e])
  return e
 def expr(self):
  e=self.atom()
  while self.peek() not in [None,')',']',',','::','++']:
   a=self.atom()
   if e[0]=='app':e=('app',e[1],e[2]+[a])
   else:e=('app',e,[a])
  if self.peek() in ['::','++']:
   op=self.pop();e=('app',('var',op),[e,self.expr()])
  return e
 def parse(self):
  e=self.expr();assert self.peek() is None,(self.ts,self.i);return e

def app(code,proof,args):
 cs=[a[0] for a in args]; hs=[a[1] for a in args]
 c='('+code+''.join(' ('+x+')' for x in cs)+')'
 if len(hs)==1:h=f'({proof}.comp {hs[0]})'
 elif len(hs)==2:h=f'({proof}.comp {hs[0]} {hs[1]})'
 else:
  p=hs[-1]
  for h in hs[-2::-1]:p=f'({h}.pair {p})'
  h=f'({proof}.comp {p})'
 return c,h
ops={
'P01AC.Ty.param':('paramCode','primrec_paramCode'),
'P01D.Poly.var':('varCode','primrec_varCode'),
'P01D.Poly.atom':('polyAtom','primrec_polyAtom'),
'method.all':('allTyCode','primrec_allTyCode'),
'method.pi':('piCode','primrec_piCode'),
'method.sigma':('sigmaTyCode','primrec_sigmaTyCode'),
'method.identity':('identityTyCode','primrec_identityTyCode'),
'method.app':('appCode','primrec_appCode'),
'P01AC.arr':('arrCode','primrec_arrCode'),
'P01AC.twkTel':('twkTelCode','primrec_twkTelCode'),
'P01AC.theta':('thetaCode','primrec_thetaCode'),
'P01AC.motiveAt':('motiveAtCode','primrec_motiveAtCode'),
'P01D.abstract':('abstractCode','primrec_abstractCode'),
'P01D.pairPoly':('pairPolyCode','primrec_pairPolyCode'),
'P01D.fstPoly':('fstPolyCode','primrec_fstPolyCode'),
'P01D.sndPoly':('sndPolyCode','primrec_sndPolyCode'),
'P01D.jPoly':('jPolyCode','primrec_jPolyCode'),
'SigmaCompletion.branchAt':('branchAtCode','primrec_branchAtCode'),
'SigmaCompletion.branchType':('branchTypeCode','primrec_branchTypeCode'),
'RigidityInitiality.dependentStepType':('dependentStepTypeCode','primrec_dependentStepTypeCode'),
'RigidityInitiality.sectionPoly':('sectionPolyCode','primrec_sectionPolyCode'),
'P01AC.fin':('finCode','primrec_finCode'),
'::':('telConsCode','primrec_telConsCode'),
'++':('List.append','Primrec.list_append')}
for n,t in [('ctxJ',0),('formJ',1),('hasJ',2),('ctxE',3),('formE',4),('hasE',5)]:
 k=n[:-1];ops['Claim.'+n]=(k+'Code '+str(t),'(primrec_'+k+'Code '+str(t)+')')
for e,t in [('J',1),('E',4)]:ops['formImages'+e]=('formImagesCode '+str(t),'(primrec_formImagesCode '+str(t)+')')

def conv(e,params,toplist=False):
 if e[0]=='var':
  v=e[1]
  if v in params:
   i=params.index(v);return f'ruleField c {i}',f'(primrec_ruleField.comp Primrec.id (.const {i}))'
  if v.isdigit():return v,f'(Primrec.const {v})'
  return f'encode ({v})',f'(Primrec.const (encode ({v})))'
 if e[0]=='list':
  if not toplist:
   assert not e[1];return 'encode ([] : Tel)','(Primrec.const (encode ([] : Tel)))'
  xs=[conv(x,params) for x in e[1]];c='['+', '.join(x[0] for x in xs)+']';h='(Primrec.const ([] : List Nat))'
  for x in xs[::-1]:h=f'(Primrec.list_cons.comp {x[1]} {h})'
  return c,h
 _,fn,args=e;assert fn[0]=='var',e
 name=fn[1]
 if name=='P01D.pren':
  assert args[0]==('var','Nat.succ');return app('shiftCode 1','(primrec_shiftCode.comp (.const 1) Primrec.id)',[conv(args[1],params)])
 if name=='P01AC.tsubst':
  assert args[0][1]==('var','P01AC.typeImages');return app('tsubstTelCode','primrec_tsubstTelCode',[conv(args[0][2][0],params),conv(args[1],params)])
 if name in ['P01AC.inst','P01AC.tinst']:
  k='instTyCode' if name.endswith('.inst') else 'tinstCode'
  return app(k,'primrec_'+k,[conv(args[1],params),conv(args[0],params)])
 op,pr=ops[name]
 return app(op,pr,[conv(a,params,name=='++') for a in args])

header='''import RuleCodeBasics
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 12000000
set_option linter.unusedVariables false
attribute [local irreducible] Nat.pair
'''
exact_simp='''polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append'''
for kind,key in [('conclusion','claim'),('premises','plist')]:
 lines=[header]; names=[]
 for idx,row in enumerate(rows):
  tag=row['tag'];ps=[x[0] for x in row['params']];raw=row[key]
  if kind=='premises' and '_finite' in tag:
   end='J' if 'HasJ' in tag else 'E'
   raw=re.sub(r'\(List.ofFn .*?\)\)\) \+\+',f'formImages{end} Γ τ ++',raw)
  e=Parser(raw,ps).parse();c,h=conv(e,ps,kind=='premises')
  typ='Nat' if kind=='conclusion' else 'List Nat';n=kind+'_'+tag;names.append(n)
  lines += [f'\ndef {n} (c : Nat) : {typ} := {c}',f'theorem primrec_{n} : Primrec {n} := by',f'  have h : Primrec (fun c : Nat => {c}) := {h}',f'  exact h.of_eq (by intro c; rfl)']
  bind=' '.join(f'({p} : {t})' for p,t in row['params']);r='Rule.'+tag+' '+ ' '.join(ps)
  rhs=f'encode (({r}).conclusion)' if kind=='conclusion' else f'(({r}).premises).map encode'
  lines +=[f'@[simp] theorem {n}_exact {bind} : {n} (encode ({r})) = {rhs} := by',f'  simp only [{n},Rule.{kind},encode_Rule_{tag},ruleField,slot,iterRest_succ,iterRest_zero,pack,', f'    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,{exact_simp}]']
 # dispatch increments allow independently small PR compositional steps.
 default='0' if kind=='conclusion' else '[]'
 prev=None
 for idx,n in reversed(list(enumerate(names))):
  dn=f'{kind}Dispatch{idx}'; tail=prev+' c' if prev else default
  lines +=[f'\ndef {dn} (c : Nat) : {typ} := if tag c = {idx} then {n} c else {tail}',f'theorem primrec_{dn} : Primrec {dn} :=',f'  Primrec.ite (Primrec.eq.comp primrec_tag (.const {idx})) primrec_{n} '+(f'primrec_{prev}' if prev else f'(.const {default})')]
  prev=dn
 lines +=[f'\ndef {kind}Code := {kind}Dispatch0',f'theorem primrec_{kind}Code : Primrec {kind}Code := primrec_{kind}Dispatch0']
 for idx,row in enumerate(rows):
  ps=[x[0] for x in row['params']];bind=' '.join(f'({p} : {t})' for p,t in row['params']);r='Rule.'+row['tag']+' '+' '.join(ps)
  lines +=[f'@[simp] theorem {kind}Code_{row["tag"]} {bind} : {kind}Code (encode ({r})) = {names[idx]} (encode ({r})) := by',f'  have ht : tag (encode ({r})) = {idx} := by rw [encode_Rule_{row["tag"]}]; exact tag_pack _ _',f'  simp only [{kind}Code,'+', '.join(kind+'Dispatch'+str(i) for i in range(idx+1))+', ht, Nat.reduceEqDiff, ↓reduceIte]']
 rhs='encode r.conclusion' if kind=='conclusion' else 'r.premises.map encode'
 lines +=[f'\ntheorem {kind}Code_exact (r : Rule) : {kind}Code (encode r) = {rhs} := by', '  cases r <;> simp only ['+', '.join(kind+'Code_'+r['tag'] for r in rows)+', '+', '.join(n+'_exact' for n in names)+']',f'\n#print axioms primrec_{kind}Code',f'#print axioms {kind}Code_exact','end CodedRuleTemplates']
 (R/('Rule'+kind.title()+'Code.lean')).write_text('\n'.join(lines)+'\n')
 print(kind,len(rows))
