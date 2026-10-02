import SourceRepresentation
namespace P03Source
open OrthemologyV2 OrthemologyV3

def proofVisits : SourceProof → Nat
  | .app p q => 1 + proofVisits p + proofVisits q
  | .allI p | .allE p _ | .reduce p _ => 1 + proofVisits p
  | _ => 1

def proofCallHeight : SourceProof → Nat
  | .app p q => 1 + max (proofCallHeight p) (proofCallHeight q)
  | .allI p | .allE p _ | .reduce p _ => 1 + proofCallHeight p
  | _ => 0

theorem proofVisits_le_transport_nodes (p : SourceProof) :
    proofVisits p ≤ (proofShape p).nodes := by
  induction p <;> simp_all [proofVisits, proofShape] <;> omega

theorem proofCallHeight_le_transport_height (p : SourceProof) :
    proofCallHeight p ≤ (proofShape p).height := by
  induction p <;> simp_all [proofCallHeight, proofShape] <;> omega

theorem sourceCheck_input_guards {p : SourceProof} {d : Nat} {out : Term × TypeCode}
    (h : sourceCheck d p = some out) :
    d ≤ 100 ∧ shapeFits (wireShape (proofTree p)) = true ∧
      proofVisits p ≤ 20000 ∧ proofCallHeight p ≤ 100 := by
  unfold sourceCheck at h
  split at h
  next hs =>
    simp only [Bool.and_eq_true, decide_eq_true_eq] at hs
    have hf := hs.2
    simp only [shapeFits, Bool.and_eq_true, decide_eq_true_eq] at hf
    have hv := proofVisits_le_transport_nodes p
    have hh := proofCallHeight_le_transport_height p
    refine ⟨hs.1, ?_, ?_, ?_⟩
    · simpa only [proofTree_shape] using hs.2
    · exact Nat.le_trans hv hf.1.1
    · exact Nat.le_trans hh hf.1.2
  next hn => contradiction

#print axioms sourceCheck_input_guards
end P03Source
