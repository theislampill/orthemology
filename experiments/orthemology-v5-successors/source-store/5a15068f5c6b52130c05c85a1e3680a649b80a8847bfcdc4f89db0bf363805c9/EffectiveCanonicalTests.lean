/- Typed original-F/G endpoint equality is exactly its canonical raw tests.
   This is a semantic theorem, not an arithmetical-hierarchy declaration. -/
import EffectiveRuleBoundary

namespace P01AC.IdentityComplexity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness

/-- Original-related naturals have the same iteration index. -/
theorem related_same_index {left right : Term} {ρ : OEnv} {η : Env}
    (h : F N ρ η left right) {m n : Nat}
    (hl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f m x))
    (hr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) : m = n := by
  have hb := h.2.2 rawPER
  change F NBody (P01F.cons rawPER ρ) η left right at hb
  rw [NBody, F_arr] at hb
  have hz : F (arr (.param 0) (.param 0)) (P01F.cons rawPER ρ) η .zero .zero := by
    rw [F_arr]
    intro a b hab
    exact Conv.right .zero hab
  have h1 := hb .zero .zero hz
  rw [F_arr] at h1
  have hc := h1 .one .one (Conv.refl .one)
  exact marker_conv_injective ((hl .zero .one).symm.trans (hc.trans (hr .zero .one)))

/-- Both original endpoint-uniformity conjuncts are supplied explicitly. -/
theorem same_index_related {left right : Term} {ρ : OEnv} {η : Env} {n : Nat}
    (hl : F N ρ η left left) (hr : F N ρ η right right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f n x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) :
    F N ρ η left right := by
  refine ⟨hl.1, hr.1, ?_⟩
  intro P
  change F NBody (P01F.cons P ρ) η left right
  rw [NBody, F_arr]
  intro f g hfg
  rw [F_arr] at hfg
  rw [F_arr]
  intro x y hxy
  change P.rel x y at hxy
  change P.rel (.app (.app left f) x) (.app (.app right g) y)
  have hi : ∀ k, P.rel (iterateTerm f k x) (iterateTerm g k y) := by
    intro k
    induction k with
    | zero => exact hxy
    | succ k ih => exact hfg _ _ ih
  exact P.raw (cl f x).symm (cr g y).symm (hi n)

theorem related_iff_same_index {left right : Term} {ρ : OEnv} {η : Env} {m n : Nat}
    (hl : F N ρ η left left) (hr : F N ρ η right right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f m x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) :
    F N ρ η left right ↔ m = n := by
  constructor
  · intro h
    exact related_same_index h cl cr
  · intro h
    subst n
    exact same_index_related hl hr cl cr

def canonical (n : Nat) : Term := eval (inputNumeral n) zeroEnv

theorem canonical_self (n : Nat) (ρ : OEnv) :
    F N ρ zeroEnv (canonical n) (canonical n) :=
  unary_fundamental (inputNumeral_has n) ⟨rfl, rfl⟩

def CanonicalTests (p q : Poly) : Prop :=
  ∀ n, Conv (.app (eval p zeroEnv) (canonical n)) (.app (eval q zeroEnv) (canonical n))

/-- Both current endpoint typings remain visible. The reverse proof uses
    their soundness at arbitrary cross-related semantic arguments. -/
theorem endpoint_valid_iff_canonical_tests {p q : Poly}
    (hp : Has [] p C) (hq : Has [] q C) :
    EndpointValid p q ↔ CanonicalTests p q := by
  constructor
  · intro h n
    have hv := h (fun _ => rawPER)
    rw [C, F_arr] at hv
    exact hv (canonical n) (canonical n) (canonical_self n _)
  · intro tests ρ
    rw [C, F_arr]
    intro x y hxy
    have laws := ((form_sound (N_form Ctx.nil)).2.laws.per
      (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
    have hx := laws.left hxy
    obtain ⟨n, hn⟩ := semantic_church_standardness hx
    have hxc : F N ρ zeroEnv x (canonical n) :=
      same_index_related hx (canonical_self n ρ) hn
        (fun f a => inputNumeral_applied n f a zeroEnv)
    have hcy := laws.trans (laws.sym hxc) hxy
    have hpF := unary_fundamental hp (ρ := ρ) ⟨rfl, rfl⟩
    have hqF := unary_fundamental hq (ρ := ρ) ⟨rfl, rfl⟩
    rw [C, F_arr] at hpF hqF
    exact (hpF x (canonical n) hxc).trans ((tests n).trans (hqF (canonical n) y hcy))

theorem identity_valid_iff_canonical_tests {p q : Poly}
    (hp : Has [] p C) (hq : Has [] q C) :
    IdentityValid p q ↔ CanonicalTests p q :=
  (identity_valid_iff_endpoint_valid p q).trans (endpoint_valid_iff_canonical_tests hp hq)

theorem semantic_proof_exists_iff_canonical_tests {p q : Poly}
    (hp : Has [] p C) (hq : Has [] q C) :
    (∃ e : Poly, ∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv
      (eval e zeroEnv) (eval e zeroEnv)) ↔ CanonicalTests p q :=
  (semantic_proof_exists_iff_valid p q).trans (identity_valid_iff_canonical_tests hp hq)

end P01AC.IdentityComplexity
