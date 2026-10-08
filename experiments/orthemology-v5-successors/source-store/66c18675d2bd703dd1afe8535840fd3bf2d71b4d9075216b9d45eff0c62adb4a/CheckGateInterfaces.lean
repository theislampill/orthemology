/- Independent review controls. OperationalExclusion is an explicit premise,
   NOT an axiom, proved negative result, or full classification formalization. -/
import BareBooleanGatePositive
import EffectiveBooleanInterfaces
namespace P01AC.BareBooleanReview
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.BooleanIdentity P01AC.IdentityComplexity
open P01AC.BareBooleanGateSyntax P01AC.BareBooleanGatePositive

theorem constant_pure : Pure constantChoice := pure_abstract (choice_pure false)

/-- A compound raw atom is outside the lifting lemma's fragment. -/
example : ¬ Pure (.atom (.app .i .i)) := by simp [P01AC.BareBooleanGateSyntax.Pure]
example : expose (eval (.atom (.app .i .i)) zeroEnv) ≠ .atom (.app .i .i) := by decide
example : expose (eval (.app (.atom .i) (.atom .i)) zeroEnv) =
    .app (.atom .i) (.atom .i) := rfl

/-- Empty composition cannot expose the default zero marker. -/
def emptyComposition : PR 2 := .comp (.zero 0) (fun i => Fin.elim0 i)
example : Pure emptyComposition.compile := compile_pure _
example : emptyComposition.compile = inputNumeral 0 := by
  simp [emptyComposition, PR.compile, inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub]

/-- Explicit successful gate, with zero bound and no search for a certificate. -/
def onePredicate : PR 2 := .comp .succ (fun _ => .zero 2)
theorem one_halts (e : Nat) : ∃ n, onePredicate.denote (inputs n e) ≠ 0 := by
  exact ⟨0, by change 1 ≠ 0; decide⟩
example (e : Nat) : Has [] (.app (gate (simFamily onePredicate e)) constantChoice) CB :=
  gated_has onePredicate e constantChoice_has constant_pure (one_halts e)
example (e : Nat) : BoolValid (.app (gate (simFamily onePredicate e)) constantChoice)
    constantChoice := by
  apply (gated_valid_iff onePredicate e constantChoice_has constant_pure
    constantChoice_has (one_halts e)).mpr
  exact (bool_valid_iff_tests constantChoice_has constantChoice_has).mpr
    (fun _ => .refl _)

/-- Marker-free counters needed by the fresh-variable head argument. -/
theorem count_markerFree (n : Nat) : MarkerFree (countTerm n) := by
  induction n with
  | zero =>
      exact pure_closed_markerFree (pure_inputNumeral 0)
        (has_scoped (inputNumeral_has 0)) zeroEnv
  | succ n ih =>
      exact ⟨pure_closed_markerFree pure_succPoly
        (has_scoped succ_has) zeroEnv, ih⟩

theorem simulator_markerFree (f : PR 2) (e : Nat) :
    MarkerFree (eval (simFamily f e) zeroEnv) :=
  pure_closed_markerFree (simFamily_pure f e) (has_scoped (simFamily_has f e)) zeroEnv

/-- Noncanonical counter inputs are accepted, including at successor depth three. -/
example (f : PR 2) (e : Nat) (x y : Term) :
    Conv (.app (.app (.app (eval (simFamily f e) zeroEnv) (countTerm 3)) x) y)
      (pick (decide (f.denote (inputs 3 e) ≠ 0)) x y) :=
  family_input_obs f e 3 (count_obs 3) x y

def AllZero (f : PR 2) (e : Nat) : Prop := ∀ n, f.denote (inputs n e) = 0
def SomeNonzero (f : PR 2) (e : Nat) : Prop := ∃ n, f.denote (inputs n e) ≠ 0
def gated (f : PR 2) (e : Nat) (q : Poly) : Poly := .app (gate (simFamily f e)) q

/-- This exact missing kernel premise is the written head argument's output. -/
def OperationalExclusion (f : PR 2) : Prop :=
  ∀ e, AllZero f e → ∀ q b,
    ¬ Conv (observationAt (gated f e q) 0) (pick b .zero .one)

def BareValid (p q : Poly) : Prop :=
  Scoped 0 p ∧ Scoped 0 q ∧ Has [] p CB ∧ Has [] q CB ∧ BoolValid p q

theorem typed_iff_some_nonzero (f : PR 2) (op : OperationalExclusion f)
    (e : Nat) {q : Poly} (hq : Has [] q CB) (pq : Pure q) :
    Has [] (gated f e q) CB ↔ SomeNonzero f e := by
  constructor
  · intro hp
    apply Classical.byContradiction
    intro hn
    have hz : AllZero f e := by
      intro n
      apply Classical.byContradiction
      intro hv
      exact hn ⟨n, hv⟩
    exact noHas_of_no_observation (op e hz q) hp
  · exact gated_has f e hq pq

/-- Conditional full pair equivalence checks the formal/written seam only. -/
theorem pair_iff_difference (f : PR 2) (op : OperationalExclusion f) (e j : Nat) :
    BareValid (gated f e (simFamily f j)) constantChoice ↔
      SomeNonzero f e ∧ AllZero f j := by
  constructor
  · rintro ⟨_, _, hp, _, hv⟩
    have he := (typed_iff_some_nonzero f op e (simFamily_has f j)
      (simFamily_pure f j)).mp hp
    refine ⟨he, ?_⟩
    exact (sim_valid_iff_all_zero f j).mp
      ((gated_valid_iff f e (simFamily_has f j) (simFamily_pure f j)
        constantChoice_has he).mp hv)
  · rintro ⟨he, hj⟩
    have hp := gated_has f e (simFamily_has f j) (simFamily_pure f j) he
    exact ⟨has_scoped hp, has_scoped constantChoice_has, hp, constantChoice_has,
      (gated_valid_iff f e (simFamily_has f j) (simFamily_pure f j)
        constantChoice_has he).mpr ((sim_valid_iff_all_zero f j).mpr hj)⟩

#print axioms typed_iff_some_nonzero
#print axioms pair_iff_difference
#check P01AC.Has.conv
#check P01DF.PolyConv
#print axioms P01AC.BareBooleanGatePositive.gate_halts
#print axioms P01AC.BareBooleanGatePositive.noHas_of_no_observation
#print axioms P01AC.BooleanIdentity.identity_valid_iff_endpoint_valid
#print axioms P01AC.BooleanIdentity.identity_unary_iff_endpoint_valid
#print axioms P01AC.BooleanIdentity.semantic_proof_exists_iff_valid
end P01AC.BareBooleanReview
