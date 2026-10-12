import JointRecursorCongruence

namespace JointCompletion.RecursorUniqueness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality InductionComputation
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- A commuting-square argument: each side's law plus congruence of the SAME
operation. It does not assume the desired comparison conclusion or step. -/
theorem compare_algebra_values {Γ : Tel} {A B : Ty} {f x y l r exy el er : Poly}
    (hc : CtxJ Γ) (hA : FormJ Γ A) (hB : FormJ Γ B)
    (hf : HasJ Γ f (arr A B)) (hx : HasJ Γ x A) (hy : HasJ Γ y A)
    (hl : HasJ Γ l B) (hr : HasJ Γ r B)
    (hexy : HasJ Γ exy (.identity A x y))
    (hel : HasJ Γ el (.identity B l (.app f x)))
    (her : HasJ Γ er (.identity B r (.app f y))) :
    HasJ Γ ident (.identity B l r) := by
  have hfx := app_has (form_arr hA hB) hB hf hx
  have hfy := app_has (form_arr hA hB) hB hf hy
  have cong := arrow_congr hc hA hB hf hx hy hexy
  have rback := ExtractionFidelity.identity_sym hc hB hr hfy her
  have mid := ExtractionFidelity.identity_trans hc hB hl hfx hfy hel cong
  have full := ExtractionFidelity.identity_trans hc hB hl hfy hr mid rback
  have reverse := ExtractionFidelity.identity_sym hc hB hl hr full
  exact ExtractionFidelity.identity_sym hc hB hr hl reverse

/-- Shared zero laws give the comparison seed by symmetry and transitivity. -/
theorem comparison_seed {Γ : Tel} {P : Ty} {p u v zu zv : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero))
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hzu : HasJ Γ zu (.identity (inst P zero) (.app u zero) p))
    (hzv : HasJ Γ zv (.identity (inst P zero) (.app v zero) p)) :
    HasJ Γ zu (inst (comparisonFamily P u v) zero) := by
  rw [comparison_at]
  have huz := section_value hc hP hu (zero_has_N hc)
  have hvz := section_value hc hP hv (zero_has_N hc)
  exact ExtractionFidelity.identity_trans hc (has_form hp) huz hp hvz hzu
    (ExtractionFidelity.identity_sym hc (has_form hp) hvz hp hzv)

/-- Derived comparison step from two ordinary successor-law sections, each
mentioning only its own section and their common supplied step s. -/
theorem comparison_step {Γ : Tel} {P : Ty} {s u v lu lv : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hlu : HasJ Γ lu (.pi N (successorLawFamily P s u)))
    (hlv : HasJ Γ lv (.pi N (successorLawFamily P s v))) :
    HasJ Γ (abstract (abstract ident))
      (dependentStepType (comparisonFamily P u v)) := by
  let C := comparisonFamily P u v
  let Q := successorFamily P
  have cn := CtxJ.ext hc (N_form hc)
  have hC : FormJ (N :: Γ) C := comparison_formed hc hP hu hv
  have ce := CtxJ.ext cn hC
  have hQ : FormJ (N :: Γ) Q := successorFamily_form hc hP
  have hQw := form_wk hQ cn hC
  have hPw := form_wk hP cn hC
  have hu0 := section_at_variable hc hP hu
  have hv0 := section_at_variable hc hP hv
  have hf := section_at_variable hc (pi_body_form (has_form hs)) hs
  have hf' : HasJ (N :: Γ) (.app (pren Nat.succ s) (.var 0)) (arr P Q) := hf
  have hlU := section_at_variable hc (pi_body_form (has_form hlu)) hlu
  have hlV := section_at_variable hc (pi_body_form (has_form hlv)) hlv
  have epU := Structural.form_identity_inv (has_form hlU)
  have epV := Structural.form_identity_inv (has_form hlV)
  have hwf : HasJ (C :: N :: Γ)
      (pren Nat.succ (.app (pren Nat.succ s) (.var 0))) (arr (wk P) (wk Q)) := by
    simpa only [wk, subst_arr] using has_wk hf' cn hC
  have hwe : HasJ (C :: N :: Γ) (.var 0)
      (.identity (wk P) (pren Nat.succ (.app (pren Nat.succ u) (.var 0)))
        (pren Nat.succ (.app (pren Nat.succ v) (.var 0)))) := by
    have e : HasJ (C :: N :: Γ) (.var 0) (wk C) := .var (form_wk hC cn hC) .zero
    exact e
  have hlUw := has_wk hlU cn hC
  have hlVw := has_wk hlV cn hC
  have result := compare_algebra_values ce hPw hQw hwf (has_wk hu0 cn hC)
    (has_wk hv0 cn hC) (has_wk epU.2.1 cn hC) (has_wk epV.2.1 cn hC)
    hwe hlUw hlVw
  have eqt : wk (successorFamily C) =
      .identity (wk Q)
        (pren Nat.succ (.app (pren Nat.succ u) (.app succPoly (.var 0))))
        (pren Nat.succ (.app (pren Nat.succ v) (.app succPoly (.var 0)))) := by
    simp only [C, Q, successorFamily, comparisonFamily, subst, wk, pren,
      psub, psub_comp, cons, psub_id]
  have hSC := successorFamily_form hc hC
  apply HasJ.piIntro (.pi (N_form hc) (form_arr hC hSC))
  · apply HasJ.piIntro (form_arr hC hSC)
    · exact eqt.symm ▸ result
    · exact scoped_abstract trivial
  · exact scoped_abstract (scoped_abstract trivial)

/-- Source-level uniqueness for the same typed seed and curried step, on every
actual Joint family. The only law premises are each section's own zero and
successor algebra laws. The conclusion is typed function identity. -/
theorem recursor_unique {Γ : Tel} {P : Ty} {p s u v zu zv lu lv : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hzu : HasJ Γ zu (.identity (inst P zero) (.app u zero) p))
    (hzv : HasJ Γ zv (.identity (inst P zero) (.app v zero) p))
    (hlu : HasJ Γ lu (.pi N (successorLawFamily P s u)))
    (hlv : HasJ Γ lv (.pi N (successorLawFamily P s v))) :
    HasJ Γ ident (.identity (.pi N P) u v) :=
  induction_extensionality hc hP hu hv
    (comparison_seed hc hP hp hu hv hzu hzv)
    (comparison_step hc hP hs hu hv hlu hlv)

/-- Equivalent ordinary-rule presentation: supply each successor law as an
actual derivation in the generic-natural context. Pi introduction constructs
the law sections, so the caller need not prepackage source functions. -/
theorem recursor_unique_generic_laws {Γ : Tel} {P : Ty} {p s u v zu zv lu lv : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hzu : HasJ Γ zu (.identity (inst P zero) (.app u zero) p))
    (hzv : HasJ Γ zv (.identity (inst P zero) (.app v zero) p))
    (hlu : HasJ (N :: Γ) lu (successorLawFamily P s u))
    (hlv : HasJ (N :: Γ) lv (successorLawFamily P s v)) :
    HasJ Γ ident (.identity (.pi N P) u v) :=
  recursor_unique hc hP hp hs hu hv hzu hzv
    (.piIntro (.pi (N_form hc) (has_form hlu)) hlu (scoped_abstract (has_scoped hlu)))
    (.piIntro (.pi (N_form hc) (has_form hlv)) hlv (scoped_abstract (has_scoped hlv)))

#print axioms comparison_step
#print axioms recursor_unique
end JointCompletion.RecursorUniqueness
