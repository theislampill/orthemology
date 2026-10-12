#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parent
ss=json.loads((R/'SCHEMA.json').read_text());types=['OrthemologyV2.Term','OrthemologyV2.TypeCode','P01D.Poly','P01AC.Ty','Nat','P01AC.Tel']+['AuxiliaryCertificates.'+t['type'] if t['sort']<11 else 'JointCertificates.'+t['type'] for t in ss]
head=['import CertificateDescriptions','import DescriptorLemmas','import TelescopeCodeValidity','namespace CertificateCodeValidity','open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability','open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity','set_option maxRecDepth 16384','set_option maxHeartbeats 1000000','attribute [local irreducible] Nat.pair','']
x=head.copy()
x+=['def allDescriptions : List Description := ['+', '.join(t['description'] for t in ss)+']','', '''def certShape (b : Nat × Nat) : Bool :=
  if b.1 < 4 then valid b.1 b.2
  else if b.1 = 4 then true
  else if b.1 = 5 then validTel b.2
  else localShape (allDescriptions[b.1-6]?.getD []) b.2

def certChildren (b : Nat × Nat) : List (Nat × Nat) :=
  if b.1 < 6 then [] else localChildren (allDescriptions[b.1-6]?.getD []) b.2

def certValid (s c : Nat) : Bool := evaluate certShape certChildren (s,c)
''','def CertCanonical (b : Nat × Nat) : Prop :=']
for i,typ in enumerate(types):x+=['  '+('if' if i==0 else 'else if')+' b.1 = '+str(i)+' then ∃ a : '+typ+', encode a = b.2']
x+=['  else False','', '''theorem primrec_certShape : Primrec certShape := by
  have hd : Primrec (fun b : Nat × Nat => allDescriptions[b.1-6]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.const allDescriptions)
      (Primrec.nat_sub.comp Primrec.fst (Primrec.const 6))) (Primrec.const [])
  exact Primrec.ite (Primrec.nat_lt.comp Primrec.fst (Primrec.const 4))
    (primrec_valid.comp Primrec.fst Primrec.snd)
    (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 4)) (Primrec.const true)
      (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 5))
        (primrec_validTel.comp Primrec.snd) (primrec_localShape.comp hd Primrec.snd)))

theorem primrec_certChildren : Primrec certChildren := by
  have hd : Primrec (fun b : Nat × Nat => allDescriptions[b.1-6]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.const allDescriptions)
      (Primrec.nat_sub.comp Primrec.fst (Primrec.const 6))) (Primrec.const [])
  exact Primrec.ite (Primrec.nat_lt.comp Primrec.fst (Primrec.const 6))
    (Primrec.const []) (primrec_localChildren.comp hd Primrec.snd)

theorem primrec_certValid : Primrec₂ certValid :=
  (primrec_evaluate primrec_certShape primrec_certChildren).to₂
''','end CertificateCodeValidity']
(R/'CertificateGrammar.lean').write_text('\n'.join(x)+'\n')
common='localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical'
for t in ss:
 x=['import CertificateGrammar']+head[3:]
 typ=types[t['sort']];desc=t['description'];name=t['type']+'_rule'
 x+=['theorem '+name+' (c : Nat) : (∃ a : '+typ+', encode a = c) ↔', '    localShape '+desc+' c = true ∧ ∀ d ∈ localChildren '+desc+' c, CertCanonical d := by','  constructor','  · rintro ⟨a, rfl⟩','    cases a'+(';' if len(t['ctors'])==1 else ' <;>')+' simp ['+desc+', '+common+']','  · rintro ⟨hs, hc⟩','    unfold localShape at hs','    split_ifs at hs with htag','    have hlt : tag c < '+str(len(t['ctors']))+' := by simpa ['+desc+'] using htag','    have heq : '+' ∨ '.join('tag c = '+str(i) for i in range(len(t['ctors'])))+' := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)', '    rcases heq with '+' | '.join('heq' for _ in t['ctors'])]
 for ct in t['ctors']:
  x+=['    · simp ['+desc+', heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs','      simp [localChildren, '+desc+', heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc']
  nonnat=[i for i,ft in enumerate(ct['fields']) if ft!='Nat']
  if nonnat:
   pats=['⟨a'+str(i)+', h'+str(i)+'⟩' for i in nonnat];pat=pats[0] if len(pats)==1 else '⟨'+', '.join(pats)+'⟩'
   x+=['      rcases hc with '+pat]
  args=['(rest (slot c '+str(i)+'))' if ft=='Nat' else 'a'+str(i) for i,ft in enumerate(ct['fields'])]
  ctor=typ+'.'+ct['name']+(' '+' '.join(args) if args else '')
  rw=', '.join('h'+str(i) for i in nonnat)
  x+=['      refine ⟨'+ctor+', ?_⟩','      simpa ['+rw+'] using hs.symm']
 x+=['','end CertificateCodeValidity']
 (R/(t['type']+'ImageRule.lean')).write_text('\n'.join(x)+'\n')
