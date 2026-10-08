/- Isolated finite positive gate. The nonhalting direction is not asserted here. -/
import BareBooleanGateSyntax
namespace P01AC.BareBooleanGatePositive
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.BooleanIdentity P01AC.IdentityComplexity
open P01AC.BareBooleanGateSyntax
open P01F (cons)

def countTerm : Nat → Term
  | 0 => canonical 0
  | n+1 => .app succTerm (countTerm n)

theorem count_obs (n : Nat) : NatObs (countTerm n) n := by
  induction n with
  | zero => exact canonical_obs 0
  | succ n ih => exact succ_obs ih

theorem family_input_obs (f : PR 2) (e n : Nat) {t : Term} (ht : NatObs t n) (x y : Term) :
    Conv (.app (.app (.app (eval (simFamily f e) zeroEnv) t) x) y)
      (pick (decide (f.denote (inputs n e) ≠ 0)) x y) := by
  let η : Env := cons t (cons (canonical e) zeroEnv)
  have h1 := (P01Source.red_conv (abstraction_beta (abstract (.app zeroDiscriminator f.compile)) zeroEnv (canonical e))).left t
  have h2 := P01Source.red_conv (abstraction_beta (.app zeroDiscriminator f.compile) (cons (canonical e) zeroEnv) t)
  have hc : Conv (.app (eval (simFamily f e) zeroEnv) t) (.app discriminatorTerm (eval f.compile η)) := by
    have h := h1.trans h2
    change Conv (.app (eval (simFamily f e) zeroEnv) t)
      (.app (eval zeroDiscriminator η) (eval f.compile η)) at h
    rw [eval_closed (has_scoped discriminator_has) η zeroEnv] at h
    exact h
  have hn : NatObs (eval f.compile η) (f.denote (inputs n e)) := by
    apply f.compile_obs
    intro i hi
    cases i with
    | zero => exact ht
    | succ i =>
      cases i with
      | zero => exact canonical_obs e
      | succ i => omega
  exact ((hc.left x).left y).trans (discriminator_obs hn x y)

/-- Context is n at zero and recursive self at one. All other terms are closed. -/
def searchBody (p : Poly) : Poly :=
  .app (.app (.app p (.var 0))
    (.app (.app (.var 1) (.var 1)) (.app succPoly (.var 0)))) (.atom .i)
def searchAbs (p : Poly) : Poly := abstract (abstract (searchBody p))
def searchTerm (p : Poly) : Term := eval (searchAbs p) zeroEnv
def state (p : Poly) (n : Nat) : Term :=
  .app (.app (searchTerm p) (searchTerm p)) (countTerm n)
def gate (p : Poly) : Poly := .app (.app (searchAbs p) (searchAbs p)) (inputNumeral 0)

lemma scoped_mono {p : Poly} {k l : Nat} (h : Scoped k p) (hk : k ≤ l) : Scoped l p := by
  induction p with
  | var i => exact Nat.lt_of_lt_of_le h hk
  | atom t => trivial
  | app f a hf ha => exact ⟨hf h.1, ha h.2⟩

theorem search_closed {p : Poly} (hp : Scoped 0 p) : Scoped 0 (searchAbs p) := by
  apply scoped_abstract
  apply scoped_abstract
  exact ⟨⟨⟨scoped_mono hp (by decide), (show 0 < 2 by decide)⟩,
    ⟨⟨(show 1 < 2 by decide), (show 1 < 2 by decide)⟩, ⟨scoped_mono (has_scoped succ_has) (by decide), (show 0 < 2 by decide)⟩⟩⟩, trivial⟩

theorem gate_closed {p : Poly} (hp : Scoped 0 p) : Scoped 0 (gate p) :=
  ⟨⟨search_closed hp, search_closed hp⟩, has_scoped (inputNumeral_has 0)⟩

theorem search_pure {p : Poly} (hp : Pure p) : Pure (searchAbs p) :=
  pure_abstract (pure_abstract ⟨⟨⟨hp, trivial⟩,
    ⟨⟨trivial, trivial⟩, ⟨pure_succPoly, trivial⟩⟩⟩, Or.inl rfl⟩)

theorem gate_pure {p : Poly} (hp : Pure p) : Pure (gate p) :=
  ⟨⟨search_pure hp, search_pure hp⟩, pure_inputNumeral 0⟩

theorem unfold_state {p : Poly} (hp : Scoped 0 p) (n : Nat) :
    Conv (state p n)
      (.app (.app (.app (eval p zeroEnv) (countTerm n)) (state p (n+1))) .i) := by
  have h1 := (P01Source.red_conv (abstraction_beta (abstract (searchBody p)) zeroEnv (searchTerm p))).left (countTerm n)
  have h2 := P01Source.red_conv (abstraction_beta (searchBody p) (cons (searchTerm p) zeroEnv) (countTerm n))
  have h := h1.trans h2
  change Conv (state p n)
    (.app (.app (.app (eval p (cons (countTerm n) (cons (searchTerm p) zeroEnv))) (countTerm n))
      (.app (.app (searchTerm p) (searchTerm p))
        (.app (eval succPoly (cons (countTerm n) (cons (searchTerm p) zeroEnv))) (countTerm n)))) .i) at h
  rw [eval_closed hp _ zeroEnv, eval_closed (has_scoped succ_has) _ zeroEnv] at h
  exact h

theorem state_choice (f : PR 2) (e n : Nat) :
    Conv (state (simFamily f e) n)
      (pick (decide (f.denote (inputs n e) ≠ 0)) (state (simFamily f e) (n+1)) .i) :=
  (unfold_state (has_scoped (simFamily_has f e)) n).trans
    (family_input_obs f e n (count_obs n) _ _)

theorem state_halts (f : PR 2) (e : Nat) (t : Nat) : ∀ k,
    f.denote (inputs (k+t) e) ≠ 0 → Conv (state (simFamily f e) k) .i := by
  induction t with
  | zero =>
    intro k h
    have hk : f.denote (inputs k e) ≠ 0 := by simpa only [Nat.add_zero] using h
    simpa [hk, pick] using state_choice f e k
  | succ t ih =>
    intro k h
    by_cases hk : f.denote (inputs k e) ≠ 0
    · simpa [hk, pick] using state_choice f e k
    · have hc : Conv (state (simFamily f e) k) (state (simFamily f e) (k+1)) := by
        simpa [hk, pick] using state_choice f e k
      exact hc.trans (ih (k+1) (by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h))

theorem gate_halts (f : PR 2) (e : Nat) (h : ∃ n, f.denote (inputs n e) ≠ 0) :
    Conv (eval (gate (simFamily f e)) zeroEnv) .i := by
  obtain ⟨n, hn⟩ := h
  exact state_halts f e n 0 (by simpa only [Nat.zero_add] using hn)

/-- Finite halting evidence gives an actual current Has derivation for the gate
    applied to any closed pure endpoint whose current typing is already known. -/
theorem gated_has (f : PR 2) (e : Nat) {q : Poly} (hq : Has [] q CB) (pq : Pure q)
    (h : ∃ n, f.denote (inputs n e) ≠ 0) :
    Has [] (.app (gate (simFamily f e)) q) CB := by
  have hp := simFamily_pure f e
  have sp := has_scoped (simFamily_has f e)
  have sc : Scoped 0 (.app (gate (simFamily f e)) q) := ⟨gate_closed sp, has_scoped hq⟩
  have cv : Conv (eval (.app (gate (simFamily f e)) q) zeroEnv) (eval q zeroEnv) :=
    ((gate_halts f e h).left _).trans (.step (.i _))
  have pc := pure_closed_conversion (p := .app (gate (simFamily f e)) q) (q := q) ⟨gate_pure hp, pq⟩ pq sc (has_scoped hq) cv
  exact .conv (form_arr (N_form .nil) (B_form .nil)) hq (.symm pc) sc

/-- Halting preserves the original F-based endpoint equality, not just typing. -/
theorem gated_valid_iff (f : PR 2) (e : Nat) {q r : Poly}
    (hq : Has [] q CB) (pq : Pure q) (hr : Has [] r CB)
    (h : ∃ n, f.denote (inputs n e) ≠ 0) :
    BoolValid (.app (gate (simFamily f e)) q) r ↔ BoolValid q r := by
  rw [bool_valid_iff_tests (gated_has f e hq pq h) hr, bool_valid_iff_tests hq hr]
  have cv : Conv (eval (.app (gate (simFamily f e)) q) zeroEnv) (eval q zeroEnv) :=
    ((gate_halts f e h).left _).trans (.step (.i _))
  have obs : ∀ n, Conv (observationAt (.app (gate (simFamily f e)) q) n)
      (observationAt q n) := fun n => ((cv.left (canonical n)).left .zero).left .one
  exact ⟨fun ht n => (obs n).symm.trans (ht n), fun ht n => (obs n).trans (ht n)⟩

/-- Exact semantic non-typability interface needed from the operational proof. -/
theorem noHas_of_no_observation {p : Poly}
    (h : ∀ b, ¬ Conv (observationAt p 0) (pick b .zero .one)) : ¬ Has [] p CB := by
  intro hp
  obtain ⟨b, hb⟩ := boolean_standardness (output_self hp 0 (fun _ => rawPER))
  exact h b (hb .zero .one)

#print axioms family_input_obs
#print axioms gated_has
#print axioms gated_valid_iff
#print axioms noHas_of_no_observation
end P01AC.BareBooleanGatePositive
