/- Independent exact-interface controls for the two-module successor.
   The universal representer and its two properties remain explicit parameters.
   None of these examples asserts a computability or hierarchy theorem. -/
import EffectivePartialObserver

open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity

-- The carrier, semantics, canonical inputs, and source numeral convention.
example : N = .all (arr (arr (.param 0) (.param 0)) (arr (.param 0) (.param 0))) := rfl
example : C = arr N .raw := rfl
example (p q : Poly) : EndpointValid p q =
    (∀ ρ : OEnv, F C ρ zeroEnv (eval p zeroEnv) (eval q zeroEnv)) := rfl
example (p q : Poly) : IdentityValid p q =
    (∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv .i .i) := rfl
example (n : Nat) : canonical n = eval (inputNumeral n) zeroEnv := rfl
example (p q : Poly) : CanonicalTests p q =
    (∀ n, Conv (.app (eval p zeroEnv) (canonical n))
      (.app (eval q zeroEnv) (canonical n))) := rfl
example : numericB = .app (.app .s (.app .k .s)) .k := rfl
example : numericSucc = .app .s numericB := rfl
example : numeral 0 = .app .k .i := rfl
example (n : Nat) : numeral (n+1) = .app numericSucc (numeral n) := rfl
example (U : Term) (e : Nat) : universalTester U e =
    tester numericSucc (.app U (numeral e)) (numeral 0) := rfl

-- Same-index equality retains both membership/uniformity hypotheses.
example {left right : Term} {ρ : OEnv} {η : Env} {m n : Nat}
    (h : F N ρ η left right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f m x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) : m = n :=
  related_same_index h cl cr
example {left right : Term} {ρ : OEnv} {η : Env} {n : Nat}
    (hl : F N ρ η left left) (hr : F N ρ η right right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f n x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) :
    F N ρ η left right := same_index_related hl hr cl cr
example {left right : Term} {ρ : OEnv} {η : Env} {m n : Nat}
    (hl : F N ρ η left left) (hr : F N ρ η right right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f m x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) :
    F N ρ η left right ↔ m = n := related_iff_same_index hl hr cl cr
example (n : Nat) (ρ : OEnv) : F N ρ zeroEnv (canonical n) (canonical n) :=
  canonical_self n ρ

-- Literal All has two uniformity conjuncts, not merely equal observations.
example (left right : Term) (ρ : OEnv) (η : Env) :
    F N ρ η left right =
      ((∀ (P Q : PER) (R : Link P Q),
          G NBody (extendEnv R (diagEnv ρ)) η η left left) ∧
       (∀ (P Q : PER) (R : Link P Q),
          G NBody (extendEnv R (diagEnv ρ)) η η right right) ∧
       ∀ P, F NBody (P01F.cons P ρ) η left right) := rfl

-- Both current typings, all environments, and independent cross arguments.
example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C) :
    EndpointValid p q ↔ CanonicalTests p q := endpoint_valid_iff_canonical_tests hp hq
example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C)
    (tests : CanonicalTests p q) (ρ : OEnv) (x y : Term)
    (hxy : F N ρ zeroEnv x y) :
    Conv (.app (eval p zeroEnv) x) (.app (eval q zeroEnv) y) := by
  have h := (endpoint_valid_iff_canonical_tests hp hq).mpr tests ρ
  rw [C, F_arr] at h
  exact h x y hxy
example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C) :
    (∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv .i .i) ↔
      CanonicalTests p q := identity_valid_iff_canonical_tests hp hq
example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C) :
    (∀ ρ : OEnv, F (.identity C p q) ρ zeroEnv .i .i) ↔
      CanonicalTests p q :=
  (identity_unary_iff_endpoint_valid p q).trans (endpoint_valid_iff_canonical_tests hp hq)
example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C) :
    (∃ e : Poly, ∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv
      (eval e zeroEnv) (eval e zeroEnv)) ↔ CanonicalTests p q :=
  semantic_proof_exists_iff_canonical_tests hp hq

-- One fixed universal term, no normalization/halting premise on its typing.
example (U : Term) (e : Nat) : Has [] (universalTester U e) C := universalTester_has U e
example : Has [] (constantRaw (numeral 0)) C := constantRaw_has (numeral 0)
example (U : Term) (e : Nat) :
    Form [] (.identity C (universalTester U e) (constantRaw (numeral 0))) :=
  universal_target_formed U e
example (U : Term) (e : Nat) :
    Scoped 0 (universalTester U e) ∧ Scoped 0 (constantRaw (numeral 0)) :=
  universal_target_closed U e
example (U : Term) (e : Nat) :
    TyScoped 0 (.identity C (universalTester U e) (constantRaw (numeral 0))) ∧
    Intensional.TyParamScoped 0
      (.identity C (universalTester U e) (constantRaw (numeral 0))) :=
  universal_target_scope U e
example (n : Nat) : Conv (iterateTerm (stepTerm numericSucc) n (numeral 0)) (numeral n) :=
  repeated_step_numeral n
example (U : Term) (e n : Nat) (t : Term)
    (ht : ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x)) :
    Conv (.app (eval (universalTester U e) zeroEnv) t)
      (.app (.app U (numeral e)) (numeral n)) := universalTester_observation U e n t ht

section ExplicitRepresentation
variable (U : Term) (H : Nat → Nat → Prop)
variable (defined : ∀ e n, H e n →
  Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
variable (undefined : ∀ e n, ¬ H e n →
  ¬ Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))

example (e : Nat) :
    EndpointValid (universalTester U e) (constantRaw (numeral 0)) ↔ ∀ n, H e n :=
  universal_endpoint_valid_iff_total U H defined undefined e
example (e : Nat) :
    (∀ r : REnv, G (.identity C (universalTester U e) (constantRaw (numeral 0)))
      r zeroEnv zeroEnv .i .i) ↔ ∀ n, H e n :=
  original_universal_identity_iff_total U H defined undefined e
example (e : Nat) (valid : IdentityValid (universalTester U e) (constantRaw (numeral 0))) :
    ∀ n, H e n := (original_universal_identity_iff_total U H defined undefined e).mp valid
example (e : Nat) (total : ∀ n, H e n) :
    IdentityValid (universalTester U e) (constantRaw (numeral 0)) :=
  (original_universal_identity_iff_total U H defined undefined e).mpr total
end ExplicitRepresentation

-- Exact inherited raw reduction and marker erasure; external source matching
-- and existence of a universal representer are intentionally not premises here.
example (t : Term) (hn : ¬ ∃ z, Red t z ∧ P01Source.Normal z) :
    ¬ Conv t (numeral 0) := raw_no_normal_form_excludes_zero t hn
example (n : Nat) : MarkerFree (numeral n) := numeral_marker_free n
example (t : Term)
    (hn : ¬ ∃ z, Red (replaceMarkers .i .i t) z ∧ P01Source.Normal z) :
    ¬ Conv t (numeral 0) := erased_no_normal_form_excludes_zero t hn
example (U : Term) (hU : MarkerFree U) (e n : Nat) :
    replaceMarkers .i .i (.app (.app U (numeral e)) (numeral n)) =
      .app (.app U (numeral e)) (numeral n) := pure_universal_observation_erasure U hU e n
example (U : Term) (H : Nat → Nat → Prop)
    (defined : ∀ e n, H e n →
      Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (undefined : ∀ e n, ¬ H e n →
      ¬ ∃ z, Red (replaceMarkers .i .i (.app (.app U (numeral e)) (numeral n))) z ∧
        P01Source.Normal z)
    (e : Nat) : IdentityValid (universalTester U e) (constantRaw (numeral 0)) ↔ ∀ n, H e n :=
  original_universal_identity_iff_total_of_no_normal_form U H defined undefined e

#check @endpoint_valid_iff_canonical_tests
#check @same_index_related
#check @original_universal_identity_iff_total
#check @original_universal_identity_iff_total_of_no_normal_form
#print axioms original_universal_identity_iff_total
#print axioms original_universal_identity_iff_total_of_no_normal_form
