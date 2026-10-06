import PolicySynthesisReduction
import KernelAudit
import RuntimeAudit

open EffectiveRenewal PolicySynthesis Nat.Partrec Encodable Denumerable

namespace IndependentPolicyReview

-- This signature expands the target validity predicate. It is independently
-- assembled from the explicit source and target interfaces, without applying
-- the candidate's final policy_synthesis_reduction theorem.
theorem expanded_code_reduction (R : Matrix) (hR : Computable R) :
    ∃ r : Nat → Nat, Primrec r ∧ ∀ a,
      (∀ n, ∃ b : Bool, Code.eval (ofNat Code (r a)) n = Part.some (bitNat b)) ∧
      codeAccepts (r a) [] ∧ PrefixClosed (codeAccepts (r a)) ∧
      (∃ f : Nat → Bool, ∀ n, codeAccepts (r a) (prefixWord f n)) ∧
      ((∃ x, ∀ y, ∃ z, R (a,x,y,z) = true) ↔
        ∃ f : Nat → Bool, Computable f ∧ ∀ n, codeAccepts (r a) (prefixWord f n)) := by
  obtain ⟨source,hs,he⟩ := computable_matrix_reduction R hR
  obtain ⟨target,ht,hcode⟩ := total_checker_code_family
  refine ⟨fun a => target (source a), ht.comp hs, ?_⟩
  intro a
  have hv := checker_code_valid hcode (source a)
  obtain ⟨f,hf⟩ := synthesis_mathematical_path (source a)
  refine ⟨hv.1, hv.2.1, hv.2.2, ⟨f, fun n => (checker_code_accepts hcode _ _).mpr (hf n)⟩, ?_⟩
  constructor
  · intro ha
    obtain ⟨g,hg,hgp⟩ := (he a).mp ha
    exact ⟨g,hg,fun n => (checker_code_accepts hcode _ _).mpr (hgp n)⟩
  · rintro ⟨g,hg,hgp⟩
    exact (he a).mpr ⟨g,hg,fun n => (checker_code_accepts hcode _ _).mp (hgp n)⟩

-- Cut-free tails really are K, rather than merely another noncomputable tree.
theorem zero_only_component_iff (w : Word) :
    componentTree (fun i => decide (i = 0)) w ↔ diagonalTree w := by
  have hz : ∀ i, lastCut (fun j => decide (j = 0)) i = 0 := by
    intro i
    apply lastCut_eq_of_bounds (by decide) (Nat.zero_le i)
    intro c hc hci
    simp [Nat.ne_of_gt hc]
  have hfull : slice w 0 w.length = w := by
    apply word_ext (by simp)
    intro i hi
    have hw : i < w.length := by simpa using hi
    rw [getD_slice _ _ hw, Nat.zero_add]
  constructor
  · intro hc
    cases hw : w.length with
    | zero => have : w = [] := List.length_eq_zero_iff.mp hw; subst w; exact diagonalTree_empty
    | succ k =>
      have h := (componentTree_iff _ _).mp hc k (by omega)
      rw [hz] at h
      simpa [← hw, hfull] using h
  · intro hk
    rw [componentTree_iff]
    intro i hi
    rw [hz]
    exact diagonalTree_prefix_closed (slice_zero_prefix w (by omega)) hk

-- A structurally different finite parser: the first true control bit exits;
-- later component bits are never parsed as control positions.
def parsedTree (p : Nat) (prior : Word) : Word → Bool
  | [] => treeCheck prior
  | [false] => treeCheck prior
  | false :: b :: tail => parsedTree p (prior ++ [b]) tail
  | true :: tail => treeCheck prior && componentCheck (progressCut (p,prior.length)) tail

def words : Nat → List Word
  | 0 => [[]]
  | n+1 => (words n).flatMap fun w => [false :: w, true :: w]

-- Reference component check visits completed block endpoints and the final
-- partial block, unlike the authored per-coordinate test.
def endpointCheck (cut : Nat → Bool) (w : Word) : Bool := Id.run do
  let mut b := 0
  let mut ok := true
  for c in List.range (w.length+1) do
    if c > 0 && (cut c || c == w.length) then
      ok := ok && treeCheck ((w.drop b).take (c-b))
      b := c
  return ok

def parserChecks : Bool :=
  (List.range 8).all fun p =>
    (List.range 8).all fun n =>
      (words n).all fun w => synthesisCheck p w == parsedTree p [] w

def endpointChecks : Bool :=
  (List.range 16).all fun mask =>
    (List.range 8).all fun n =>
      (words n).all fun w =>
        let cut := fun i => i == 0 || (mask / 2^i) % 2 == 1
        componentCheck cut w == endpointCheck cut w

def snapshotChecks : Bool :=
  (List.range 16).all fun mask =>
    (List.range 12).all fun s =>
      let cut := fun i => i == 0 || (mask / 2^i) % 2 == 1
      let w := blockSnapshots cut s
      w.length == lastCut cut s && componentCheck cut w &&
        decide (w <+: blockSnapshots cut (s+1))

#eval ("INDEPENDENT_FINITE_PARSER_MATCH", parserChecks)
#eval ("INDEPENDENT_ENDPOINT_MATCH", endpointChecks)
#eval ("INDEPENDENT_SNAPSHOT_CHECK", snapshotChecks)
#print axioms expanded_code_reduction
#print axioms zero_only_component_iff
end IndependentPolicyReview
#audit_policy_closure IndependentPolicyReview.expanded_code_reduction
#audit_policy_closure IndependentPolicyReview.zero_only_component_iff
