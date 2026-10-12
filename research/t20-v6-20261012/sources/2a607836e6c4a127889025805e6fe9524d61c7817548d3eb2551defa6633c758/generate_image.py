from pathlib import Path
import json
R=Path(__file__).resolve().parent;ss=json.loads((R/'SCHEMA.json').read_text())
types=['OrthemologyV2.Term','OrthemologyV2.TypeCode','P01D.Poly','P01AC.Ty','Nat','P01AC.Tel']+['AuxiliaryCertificates.'+t['type'] if t['sort']<11 else 'JointCertificates.'+t['type'] for t in ss]
header=['namespace CertificateCodeValidity','open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability','open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity','set_option maxRecDepth 16384','set_option maxHeartbeats 1000000','attribute [local irreducible] Nat.pair','']
for t in ss:
 x=['import '+t['type']+'ImageRule']+header
 x+=['theorem '+t['type']+'_bounds (c : Nat) (h : ∃ a : '+types[t['sort']]+', encode a = c) :','    ∀ d ∈ localChildren '+t['description']+' c, d.2 < c := by','  obtain ⟨a, rfl⟩ := h','  cases a'+(';' if len(t['ctors'])==1 else ' <;>')+' simp [localChildren, '+t['description']+', dependencies, fieldCode, List.range_succ]','  all_goals repeat\' apply And.intro','  all_goals first','    | solve | apply field_lt_pack; simp','    | apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp','','end CertificateCodeValidity']
 if t['type']=='SerialCertList':
  k=x.index('  all_goals first');x[k:k+3]=['  all_goals apply field_lt_pack; simp']
 (R/(t['type']+'Bounds.lean')).write_text('\n'.join(x)+'\n')
x=['import '+t['type']+'Bounds' for t in ss]+header
x+=['theorem certCanonical_sort_lt (s c : Nat) (h : CertCanonical (s,c)) : s < 15 := by','  by_contra hs'] + ['  have h'+str(i)+' : s ≠ '+str(i)+' := by omega' for i in range(15)] + ['  simp [CertCanonical, '+', '.join('h'+str(i) for i in range(15))+'] at h','']
x+=['theorem cert_canonical_rule (b : Nat × Nat) :','    CertCanonical b ↔ certShape b = true ∧ ∀ d ∈ certChildren b, CertCanonical d := by','  obtain ⟨s,c⟩ := b','  by_cases hs : s < 15','  · have hcases : '+' ∨ '.join('s = '+str(i) for i in range(15))+' := by omega','    rcases hcases with '+' | '.join('rfl' for _ in range(15))]
for i in range(15):
 if i<4:
  n=['valid_term','valid_typeCode','valid_poly','valid_ty'][i]
  x+=['    · simpa [CertCanonical, certShape, certChildren] using ('+n+' c).symm']
 elif i==4:x+=['    · simp [CertCanonical, certShape, certChildren]']
 elif i==5:x+=['    · simpa [CertCanonical, certShape, certChildren] using (validTel_exact c).symm']
 else:x+=['    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using '+ss[i-6]['type']+'_rule c']
x+=['  · have hd : allDescriptions[s-6]? = none := by','      apply List.getElem?_eq_none','      simp only [allDescriptions, List.length_cons, List.length_nil]','      omega','    have hp : ¬ CertCanonical (s,c) := by','      intro hp','      exact hs (certCanonical_sort_lt s c hp)','    have h4 : ¬s < 4 := by omega','    have he4 : s ≠ 4 := by omega','    have he5 : s ≠ 5 := by omega','    simp [hp, certShape, h4, he4, he5, hd, localShape]','', 'theorem cert_canonical_bounds (b : Nat × Nat) (hb : CertCanonical b) :','    ∀ d ∈ certChildren b, d.2 < b.2 := by','  obtain ⟨s,c⟩ := b','  have hs : s < 15 := certCanonical_sort_lt s c hb','  have hcases : '+' ∨ '.join('s = '+str(i) for i in range(15))+' := by omega','  rcases hcases with '+' | '.join('rfl' for _ in range(15))]
for i in range(15):
 if i<6:x+=['  · simp [certChildren]']
 else:
  t=ss[i-6];x+=['  · have ha : ∃ a : '+types[i]+', encode a = c := by simpa [CertCanonical] using hb','    simpa [certChildren, allDescriptions] using '+t['type']+'_bounds c ha']
x+=['', 'theorem certValid_exact (s c : Nat) : certValid s c = true ↔ CertCanonical (s,c) :=','  evaluate_exact_of_image cert_canonical_rule cert_canonical_bounds (s,c)','']
for i in range(15):
 n=(['term','typeCode','poly','ty','nat','tel']+[t['type'] for t in ss])[i]
 x+=['theorem valid_'+n+' (c : Nat) : certValid '+str(i)+' c = true ↔ ∃ a : '+types[i]+', encode a = c := by','  simpa [CertCanonical] using certValid_exact '+str(i)+' c','']
x+=['end CertificateCodeValidity']
(R/'CertificateImage.lean').write_text('\n'.join(x)+'\n')
