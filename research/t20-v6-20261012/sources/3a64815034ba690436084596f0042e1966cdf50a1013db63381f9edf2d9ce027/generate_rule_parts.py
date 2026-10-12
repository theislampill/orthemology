from pathlib import Path
import json
R=Path(__file__).resolve().parent;t=next(t for t in json.loads((R/'SCHEMA.json').read_text()) if t['type']=='Rule')
types={'Term':'OrthemologyV2.Term','TypeCode':'OrthemologyV2.TypeCode','Poly':'P01D.Poly','Ty':'P01AC.Ty','Nat':'Nat','Tel':'P01AC.Tel','List P01AC.Ty':'List P01AC.Ty'}
for typ in ['StepCert','RedCert','FiniteCert','PolyCert','LookupCert']:types[typ]='AuxiliaryCertificates.'+typ
head=['namespace CertificateCodeValidity','open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability','open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity','set_option maxRecDepth 16384','set_option maxHeartbeats 200000','attribute [local irreducible] Nat.pair','']
common='ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical'
x=['import CertificateGrammar']+head
bounds=['import RuleImageRule']+head
for ct in t['ctors']:
 k=ct['tag'];ns=['a'+str(i) for i in range(len(ct['fields']))];bs=' '.join('('+n+' : '+types[ty]+')' for n,ty in zip(ns,ct['fields']));ctor='(Rule.'+ct['name']+(' '+' '.join(ns) if ns else '')+')'
 x+=['theorem rule_complete_'+str(k)+' '+bs+' :','    localShape ruleDescription (encode '+ctor+') = true ∧','    ∀ d ∈ localChildren ruleDescription (encode '+ctor+'), CertCanonical d := by','  simp ['+common+']','']
 x+=['theorem rule_sound_'+str(k)+' (c : Nat) (heq : tag c = '+str(k)+')','    (hs : localShape ruleDescription c = true)','    ('+('hc' if ct['fields'] else '_hc')+' : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by','  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs']
 if ct['fields']:x+=['  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc']
 inds=[i for i,ft in enumerate(ct['fields']) if ft!='Nat']
 if inds:
  pats=['⟨a'+str(i)+', h'+str(i)+'⟩' for i in inds];pat=pats[0] if len(pats)==1 else '⟨'+', '.join(pats)+'⟩'
  x+=['  rcases hc with '+pat]
 args=['(rest (slot c '+str(i)+'))' if ft=='Nat' else 'a'+str(i) for i,ft in enumerate(ct['fields'])]
 x+=['  refine ⟨Rule.'+ct['name']+(' '+' '.join(args) if args else '')+', ?_⟩','  simpa ['+', '.join('h'+str(i) for i in inds)+'] using hs.symm','']
 bounds+=['theorem rule_bounds_'+str(k)+' '+bs+' :','    ∀ d ∈ localChildren ruleDescription (encode '+ctor+'), d.2 < encode '+ctor+' := by','  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]']
 if len(ct['fields'])>1:bounds+=['  all_goals repeat\' apply And.intro']
 if ct['fields']:bounds+=['  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp']
 bounds+=['']
x+=['theorem Rule_rule (c : Nat) : (∃ a : Rule, encode a = c) ↔','    localShape ruleDescription c = true ∧ ∀ d ∈ localChildren ruleDescription c, CertCanonical d := by','  constructor','  · rintro ⟨a, rfl⟩','    cases a with']
bounds+=['theorem Rule_bounds (c : Nat) (h : ∃ a : Rule, encode a = c) :','    ∀ d ∈ localChildren ruleDescription c, d.2 < c := by','  obtain ⟨a,rfl⟩ := h','  cases a with']
for ct in t['ctors']:
 args=' '.join('a'+str(i) for i in range(len(ct['fields'])))
 x+=['    | '+ct['name']+' '+args+' => exact rule_complete_'+str(ct['tag'])+' '+args]
 bounds+=['  | '+ct['name']+' '+args+' => exact rule_bounds_'+str(ct['tag'])+' '+args]
x+=['  · rintro ⟨hs,hc⟩','    have hlt : tag c < 63 := by','      by_contra h','      simp [localShape, ruleDescription, h] at hs','    have heq : '+' ∨ '.join('tag c = '+str(i) for i in range(63))+' := by','      simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)','    rcases heq with '+' | '.join('heq' for _ in range(63))]
for k in range(63):x+=['    · exact rule_sound_'+str(k)+' c heq hs hc']
x+=['','end CertificateCodeValidity'];bounds+=['','end CertificateCodeValidity']
(R/'RuleImageRule.lean').write_text('\n'.join(x)+'\n');(R/'RuleBounds.lean').write_text('\n'.join(bounds)+'\n')
