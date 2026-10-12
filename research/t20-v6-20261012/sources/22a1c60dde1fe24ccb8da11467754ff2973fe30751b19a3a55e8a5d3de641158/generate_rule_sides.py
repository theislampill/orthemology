#!/usr/bin/env python3
"""Generate actual Rule.checkSide code branches from frozen metadata expressions."""
from pathlib import Path
R=Path('private-locator:b0c4b69a3c11fe06ef59')
ns={};exec((R/'generate_rule_maps.py').read_text().split('for kind,key in')[0],{'__file__':str(R/'generate_rule_maps.py')},ns)
# exec with one globals dictionary for helper function lookup.
ns={'__file__':str(R/'generate_rule_maps.py')};exec((R/'generate_rule_maps.py').read_text().split('for kind,key in')[0],ns)
rows,Parser,conv,app,ops=(ns[k] for k in ['rows','Parser','conv','app','ops'])
ops.update({
'AuxiliaryCertificates.checkLookup':('checkLookupCode','primrec_checkLookupCode'),
'AuxiliaryCertificates.checkFinite':('checkFiniteCode','primrec_checkFiniteCode'),
'AuxiliaryCertificates.checkPoly':('checkPolyCode','primrec_checkPolyCode'),
'P01AC.finSupport':('finSupportCode','primrec_finSupportCode'),
'P01AC.Scoped':('checkScope','primrec_checkScope'),
'P01AC.TyScoped':('checkTyScope','primrec_checkTyScope'),
'List.length':('telLengthCode','primrec_telLengthCode'),
'method.length':('telLengthCode','primrec_telLengthCode'),
'lengthSucc':('(fun c => telLengthCode c + 1)','(Primrec.succ.comp primrec_telLengthCode)')})
lines=[ns['header'].replace('import RuleCodeBasics','import RuleCodeBasics\nimport LookupCode\nimport PolyExact')]
names=[]
for idx,row in enumerate(rows):
 ps=[p for p,t in row['params']];clauses=row['side'].split(' ∧ ');xs=[]
 for raw in clauses:
  if raw=='True':xs.append(('true','(Primrec.const true)'));continue
  assert raw[0]=='(' and raw[-1]==')',raw;raw=raw[1:-1]
  raw=raw.replace('(List.length Γ + 1)','(lengthSucc Γ)')
  if raw.endswith(' = true'):raw=raw[:-7]
  if ' ≤ ' in raw:
   a,b=raw.split(' ≤ ');aa=conv(Parser(a,ps).parse(),ps);bb=conv(Parser(b,ps).parse(),ps)
   xs.append((f'decide ({aa[0]} ≤ {bb[0]})',f'(Primrec.nat_le.comp {aa[1]} {bb[1]})'))
  else:xs.append(conv(Parser(raw,ps).parse(),ps))
 c,h=xs[-1]
 for cc,hh in xs[-2::-1]:c=f'({cc} && {c})';h=f'(Primrec.and.comp {hh} {h})'
 n='side_'+row['tag'];names.append(n)
 lines +=[f'\ndef {n} (c : Nat) : Bool := {c}',f'theorem primrec_{n} : Primrec {n} := by',f'  have h := {h}',f'  exact h.of_eq (by intro c; simp only [{n},id,Nat.succ_eq_add_one])']
 # Unannotated composition above leaves the domain underconstrained. Add exact domain on the final primitive.
 lines[-2]=f'  have h := {h}' if len(xs)>1 else '  have h : Primrec (fun _ : Nat => true) := Primrec.const true'
 bind=' '.join(f'({p} : {t})' for p,t in row['params']);r='Rule.'+row['tag']+' '+' '.join(ps)
 lines +=[f'@[simp] theorem {n}_exact {bind} : {n} (encode ({r})) = ({r}).checkSide := by',f'  simp only [{n},Rule.checkSide,encode_Rule_{row["tag"]},ruleField,slot,iterRest_succ,iterRest_zero,pack,', '''    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]''']
prev=None
for idx,n in reversed(list(enumerate(names))):
 dn=f'sideDispatch{idx}';tail=prev+' c' if prev else 'false'
 lines +=[f'\ndef {dn} (c : Nat) : Bool := if tag c = {idx} then {n} c else {tail}',f'theorem primrec_{dn} : Primrec {dn} :=',f'  Primrec.ite (Primrec.eq.comp primrec_tag (.const {idx})) primrec_{n} '+(f'primrec_{prev}' if prev else '(.const false)')];prev=dn
lines +=['\ndef checkSideCode := sideDispatch0','theorem primrec_checkSideCode : Primrec checkSideCode := primrec_sideDispatch0']
for idx,row in enumerate(rows):
 ps=[p for p,t in row['params']];bind=' '.join(f'({p} : {t})' for p,t in row['params']);r='Rule.'+row['tag']+' '+' '.join(ps)
 lines +=[f'@[simp] theorem checkSideCode_{row["tag"]} {bind} : checkSideCode (encode ({r})) = {names[idx]} (encode ({r})) := by',f'  have ht : tag (encode ({r})) = {idx} := by rw [encode_Rule_{row["tag"]}]; exact tag_pack _ _', '  simp only [checkSideCode,'+', '.join('sideDispatch'+str(i) for i in range(idx+1))+', ht, Nat.reduceEqDiff, ↓reduceIte]']
lines +=['\ntheorem checkSideCode_exact (r : Rule) : checkSideCode (encode r) = r.checkSide := by','  cases r <;> simp only ['+', '.join('checkSideCode_'+r['tag'] for r in rows)+', '+', '.join(n+'_exact' for n in names)+']','\n#print axioms primrec_checkSideCode','#print axioms checkSideCode_exact','end CodedRuleTemplates']
(R/'RuleSideCode.lean').write_text('\n'.join(lines)+'\n');print('side',len(rows))
