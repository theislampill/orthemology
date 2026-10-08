/- Complete executable normalisation of arbitrary nested unary equality tests. -/
import UnaryFiniteDescription
import UnaryExpressions

namespace P01AC.UnaryIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness

def tailData : Expr → Nat × List Nat
  | .constant c => (0, [c])
  | .variable => (0, [0, 1])
  | .add a b =>
      (max (tailData a).1 (tailData b).1, polyAdd (tailData a).2 (tailData b).2)
  | .mul a b =>
      (max (tailData a).1 (tailData b).1, polyMul (tailData a).2 (tailData b).2)
  | .ifEq a b yes no =>
      (max (tailData a).1 (max (tailData b).1
        (max (tailData yes).1 (max (tailData no).1
          (separationBound (tailData a).2 (tailData b).2)))),
       if polyEqual (tailData a).2 (tailData b).2 then (tailData yes).2 else (tailData no).2)

theorem tailData_correct (e : Expr) :
    ∀ n, (tailData e).1 ≤ n → e.denote n = polyEval (tailData e).2 n := by
  induction e with
  | constant c => intro n _; simp [tailData, Expr.denote, polyEval]
  | «variable» => intro n _; simp [tailData, Expr.denote, polyEval]
  | add a b ha hb =>
    intro n hn
    have hna : (tailData a).1 ≤ n := by simp only [tailData] at hn; omega
    have hnb : (tailData b).1 ≤ n := by simp only [tailData] at hn; omega
    simp only [tailData, Expr.denote, polyAdd_eval, ha n hna, hb n hnb]
  | mul a b ha hb =>
    intro n hn
    have hna : (tailData a).1 ≤ n := by simp only [tailData] at hn; omega
    have hnb : (tailData b).1 ≤ n := by simp only [tailData] at hn; omega
    simp only [tailData, Expr.denote, polyMul_eval, ha n hna, hb n hnb]
  | ifEq a b yes no ha hb hy hf =>
    intro n hn
    have hna : (tailData a).1 ≤ n := by simp only [tailData] at hn; omega
    have hnb : (tailData b).1 ≤ n := by simp only [tailData] at hn; omega
    have hny : (tailData yes).1 ≤ n := by simp only [tailData] at hn; omega
    have hnf : (tailData no).1 ≤ n := by simp only [tailData] at hn; omega
    have hcut : separationBound (tailData a).2 (tailData b).2 ≤ n := by
      simp only [tailData] at hn; omega
    have hguard : a.denote n = b.denote n ↔ polyEqual (tailData a).2 (tailData b).2 = true := by
      rw [ha n hna, hb n hnb]
      exact eval_eq_iff_polyEqual_of_bound _ _ hcut
    by_cases h : polyEqual (tailData a).2 (tailData b).2 = true
    · have hsource := hguard.mpr h
      simpa only [tailData, h, if_true, Expr.denote, if_pos hsource] using hy n hny
    · have hsource : a.denote n ≠ b.denote n := fun he => h (hguard.mp he)
      simpa only [tailData, h, if_false, Expr.denote, if_neg hsource] using hf n hnf

def normalise (e : Expr) : Description :=
  makeDescription (tailData e).2 (tailData e).1 e.denote

theorem normalise_correct (e : Expr) (n : Nat) : (normalise e).denote n = e.denote n :=
  makeDescription_correct _ _ _ (tailData_correct e) n

theorem normalise_canonical (e : Expr) : (normalise e).Canonical :=
  makeDescription_canonical _ _ _

theorem normalise_eq_iff_denote (e f : Expr) :
    normalise e = normalise f ↔ ∀ n, e.denote n = f.denote n := by
  rw [canonical_description_eq_iff _ _ (normalise_canonical e) (normalise_canonical f)]
  simp only [normalise_correct]

def identityCheck (e f : Expr) : Bool := decide (normalise e = normalise f)

theorem identityCheck_iff_denote (e f : Expr) :
    identityCheck e f = true ↔ ∀ n, e.denote n = f.denote n := by
  simp only [identityCheck, decide_eq_true_eq, normalise_eq_iff_denote]

theorem identityCheck_iff_valid (e f : Expr) :
    identityCheck e f = true ↔ Valid e f :=
  (identityCheck_iff_denote e f).trans (valid_iff_denote e f).symm

theorem identityCheck_iff_F_identity (e f : Expr) :
    identityCheck e f = true ↔
      ∀ ρ, F (.identity (arr N N) e.closed f.closed) ρ zeroEnv .i .i :=
  (identityCheck_iff_denote e f).trans (F_identity_iff_denote e f).symm

theorem identityCheck_iff_G_identity (e f : Expr) :
    identityCheck e f = true ↔
      ∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv .i .i :=
  (identityCheck_iff_denote e f).trans (G_identity_iff_denote e f).symm

theorem identityCheck_iff_semantic_witness (e f : Expr) :
    identityCheck e f = true ↔
      ∃ w : Poly, ∀ R : REnv,
        G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv
          (eval w zeroEnv) (eval w zeroEnv) :=
  (identityCheck_iff_denote e f).trans (semantic_witness_iff_denote e f).symm

theorem identityCheck_bound_G (e f : Expr) (p q : Poly) (h : LiteralEndpoints e f p q) :
    identityCheck e f = true ↔
      ∀ R : REnv, G (.identity (arr N N) p q) R zeroEnv zeroEnv .i .i :=
  (identityCheck_iff_denote e f).trans (bound_G_identity_iff_denote e f p q h).symm

def identityDecidable (e f : Expr) : Decidable (Valid e f) :=
  if h : identityCheck e f = true then isTrue ((identityCheck_iff_valid e f).mp h)
  else isFalse (fun hv => h ((identityCheck_iff_valid e f).mpr hv))

abbrev Certificate := Description

def verifyCertificate (e f : Expr) (c : Certificate) : Bool :=
  decide (normalise e = c) && decide (normalise f = c)

def makeCertificate (e : Expr) : Certificate := normalise e

theorem verifyCertificate_sound (e f : Expr) (c : Certificate)
    (h : verifyCertificate e f c = true) : Valid e f := by
  simp only [verifyCertificate, Bool.and_eq_true, decide_eq_true_eq] at h
  apply (valid_iff_denote e f).mpr
  exact (normalise_eq_iff_denote e f).mp (h.1.trans h.2.symm)

theorem makeCertificate_complete (e f : Expr) (h : Valid e f) :
    verifyCertificate e f (makeCertificate e) = true := by
  have hn := (normalise_eq_iff_denote e f).mpr ((valid_iff_denote e f).mp h)
  simp [verifyCertificate, makeCertificate, hn]

theorem finite_certificate_complete (e f : Expr) :
    (∃ c : Certificate, verifyCertificate e f c = true) ↔ Valid e f :=
  ⟨fun ⟨c,h⟩ => verifyCertificate_sound e f c h,
    fun h => ⟨makeCertificate e, makeCertificate_complete e f h⟩⟩

theorem certificate_canonical (e f : Expr) (c : Certificate)
    (h : verifyCertificate e f c = true) : c.Canonical := by
  have he : normalise e = c := by
    simp only [verifyCertificate, Bool.and_eq_true, decide_eq_true_eq] at h
    exact h.1
  rw [← he]
  exact normalise_canonical e

theorem identityCheck_substitute (outer₁ outer₂ inner₁ inner₂ : Expr)
    (ho : identityCheck outer₁ outer₂ = true) (hi : identityCheck inner₁ inner₂ = true) :
    identityCheck (outer₁.substitute inner₁) (outer₂.substitute inner₂) = true := by
  apply (identityCheck_iff_denote _ _).mpr
  intro n
  rw [Expr.substitute_denote, Expr.substitute_denote,
    (identityCheck_iff_denote inner₁ inner₂).mp hi n]
  exact (identityCheck_iff_denote outer₁ outer₂).mp ho _

def exceptionalExample : Expr := .ifEq .variable (.constant 2) (.constant 7) .variable

example : normalise exceptionalExample = ⟨[0, 1], [none, none, some 7]⟩ := rfl
example : identityCheck exceptionalExample .variable = false := rfl
example : normalise (exceptionalExample.substitute (.constant 2)) = ⟨[7], []⟩ := rfl
example : identityCheck (.ifEq exceptionalExample .variable (.constant 1) (.constant 0))
    (.ifEq .variable (.constant 2) (.constant 0) (.constant 1)) = true := rfl
example : identityCheck (.ifEq (.add .variable (.constant 0)) .variable
    exceptionalExample (.constant 91)) exceptionalExample = true := rfl
example : verifyCertificate .variable .variable ⟨[0, 1], [none, some 1]⟩ = false := rfl
example : verifyCertificate exceptionalExample exceptionalExample (makeCertificate exceptionalExample) = true := rfl

#print axioms tailData_correct
#print axioms normalise_eq_iff_denote
#print axioms identityCheck_iff_G_identity
#print axioms finite_certificate_complete
end P01AC.UnaryIdentity
