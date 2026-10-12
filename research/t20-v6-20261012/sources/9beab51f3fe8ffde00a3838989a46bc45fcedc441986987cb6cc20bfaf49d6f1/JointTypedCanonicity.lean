import JointNumeralExtraction

/- Actual source canonicity for the frozen Joint calculus. The observed
conversion is replayed through its original Pi and All extensionality rules. -/
namespace JointCompletion.DependentExtraction
open OrthemologyV2 OrthemologyV3 P01D P01AC P01R
open P01AC.ExtensionalRepair (ctx_inclusion)
open P01AC.EffectiveCompleteness (N NBody iterationPoly inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedScalarInstances (scalarLeft)
open ClosedChurchIdentity (ctx1 ctx2 point)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem closed_has {p A Γ} (hp : HasJ [] p A) (hΓ : CtxJ Γ) : HasJ Γ p A := by
  have hs : Structural.TypedSubstitution [] Γ Poly.var := by
    constructor
    intro n B hn
    cases hn
  simpa only [psub_id, subst_id] using
    Structural.has_subst hp hΓ hs

theorem formEnd {Γ} (h : Ctx Γ) : FormJ Γ End :=
  .formBase (ClosedChurchIdentity.formEnd h)
theorem formBody {Γ} (h : Ctx Γ) : FormJ Γ NBody :=
  .formBase (ClosedChurchIdentity.formBody h)
theorem formN {Γ} (h : Ctx Γ) : FormJ Γ N :=
  .formBase (ClosedChurchIdentity.formN h)

theorem body_of_N {Γ n} (hΓ : Ctx Γ) (hn : HasJ Γ n N) : HasJ Γ n NBody :=
  .allElim (formN hΓ) (.param (.ctxBase (ctx_inclusion hΓ))) (formBody hΓ) hn

theorem point_has {n} (hn : HasJ [End] n NBody) : HasJ [End] (point n) End :=
  .piElim (formBody ctx1) (formEnd ctx1) hn (.var (formEnd ctx1) .zero)

theorem observation_has {p} (hp : HasJ [] p N) : HasJ [A,End] (scalarLeft p) A := by
  have hn := body_of_N ctx2 (closed_has hp (.ctxBase (ctx_inclusion ctx2)))
  have hf : HasJ [A,End] (.var 1) End := .var (formEnd ctx2) (.succ .zero)
  have ha : HasJ [A,End] (.var 0) A :=
    .var (.param (.ctxBase (ctx_inclusion ctx2))) .zero
  have first : HasJ [A,End] (.app p (.var 1)) End :=
    .piElim (formBody ctx2) (formEnd ctx2) hn hf
  exact .piElim (formEnd ctx2) (.param (.ctxBase (ctx_inclusion ctx2))) first ha

theorem identity_of_observation {p q : Poly}
    (hp : HasJ [] p N) (hq : HasJ [] q N)
    (lp : HasJ [End] p NBody) (lq : HasJ [End] q NBody)
    (hc : PolyConvPlus (scalarLeft p) (scalarLeft q)) :
    HasJ [] i (.identity N p q) := by
  have sp := Structural.has_scoped hp
  have sq := Structural.has_scoped hq
  have hp1 := point_has lp
  have hq1 := point_has lq
  have hp2 := observation_has hp
  have hq2 := observation_has hq
  have hf2 : FormJ [A,End] (.identity A (scalarLeft p) (scalarLeft q)) :=
    .identity (.param (CtxJ.ctxBase (ctx_inclusion ctx2))) hp2 hq2
  have hi2 : HasJ [A,End] i (.identity A (scalarLeft p) (scalarLeft q)) :=
    .identityIntro hf2 hp2 hq2 hc
  have ep : .app (pren Nat.succ (point p)) (.var 0) = scalarLeft p := by
    simp [point, scalarLeft, pren, psub, P01AC.ExtensionalRepair.ExactScalarFusion.psub_closed sp]
  have eq : .app (pren Nat.succ (point q)) (.var 0) = scalarLeft q := by
    simp [point, scalarLeft, pren, psub, P01AC.ExtensionalRepair.ExactScalarFusion.psub_closed sq]
  have hfpi : FormJ [End] (.pi A (.identity A (scalarLeft p) (scalarLeft q))) :=
    .pi (.param (CtxJ.ctxBase (ctx_inclusion ctx1))) hf2
  have hhpi : HasJ [End] (abstract i)
      (.pi A (.identity A (scalarLeft p) (scalarLeft q))) :=
    .piIntro hfpi hi2 (scoped_abstract trivial)
  have hi1 : HasJ [End] i (.identity End (point p) (point q)) := by
    apply HasJ.piExt (.param (CtxJ.ctxBase (ctx_inclusion ctx1))) (.param (CtxJ.ctxBase (ctx_inclusion ctx2)))
      (formEnd ctx1) hp1 hq1
    · simpa only [ep, eq] using hf2
    · simpa only [ep, eq] using hfpi
    · simpa only [ep, eq] using hhpi
    · exact .identity (formEnd ctx1) hp1 hq1
    · exact Structural.has_scoped hp1
    · exact Structural.has_scoped hq1
    · exact scoped_abstract trivial
    · trivial
    · trivial
  have hp0 := body_of_N Ctx.nil hp
  have hq0 := body_of_N Ctx.nil hq
  have hf1 : FormJ [End] (.identity End (point p) (point q)) :=
    .identity (formEnd ctx1) hp1 hq1
  have efp : .app (pren Nat.succ p) (.var 0) = point p := by
    rw [P01AC.ExtensionalRepair.ExactScalarFusion.pren_closed sp]; rfl
  have efq : .app (pren Nat.succ q) (.var 0) = point q := by
    rw [P01AC.ExtensionalRepair.ExactScalarFusion.pren_closed sq]; rfl
  have hf0 : FormJ [] (.pi End (.identity End (point p) (point q))) :=
    .pi (formEnd .nil) hf1
  have hh0 : HasJ [] (abstract i) (.pi End (.identity End (point p) (point q))) :=
    .piIntro hf0 hi1 (scoped_abstract trivial)
  have hi0 : HasJ [] i (.identity NBody p q) := by
    apply HasJ.piExt (formEnd .nil) (formEnd ctx1) (formBody .nil) hp0 hq0
    · simpa only [efp,efq] using hf1
    · simpa only [efp,efq] using hf0
    · simpa only [efp,efq] using hh0
    · exact .identity (formBody .nil) hp0 hq0
    · exact sp
    · exact sq
    · exact scoped_abstract trivial
    · exact ⟨trivial,trivial⟩
    · exact ⟨trivial,trivial⟩
  exact .allExt (formBody .nil) (formN .nil) hp hq
    (.identity (formBody .nil) hp0 hq0) hi0 (.identity (formN .nil) hp hq)
    sp sq trivial ⟨⟨trivial,trivial⟩,⟨trivial,trivial⟩⟩

/-- Applied conversion suffices for actual typed identity; no bare raw
conversion to a numeral is asserted. -/
theorem canonicity_at_count {n : Poly} {k : Nat} (hn : HasJ [] n N)
    (count : PolyConvPlus (scalarLeft n) (iterationPoly k)) :
    HasJ [] i (.identity N n (inputNumeral k)) :=
  identity_of_observation hn (.hasBase (EffectiveNumerals.old_numeral_has k))
    (body_of_N ctx1 (closed_has hn (.ctxBase (ctx_inclusion ctx1))))
    (body_of_N ctx1 (closed_has (.hasBase (EffectiveNumerals.old_numeral_has k))
      (.ctxBase (ctx_inclusion ctx1))))
    (count.trans (ClosedChurchIdentity.numeral_observation k).symm)

/-- The actual computationally returned count, now with source identity. -/
theorem extracted_identity (n : Poly) (hn : HasJ [] n N) :
    HasJ [] i (.identity N n (inputNumeral (EffectiveNumerals.extractIteration n hn).val)) :=
  canonicity_at_count hn (EffectiveNumerals.extractIteration n hn).property

/-- Any actual Joint identity proof has the same extracted count. This uses
faithful FullPER soundness only in the negative/checking direction. -/
theorem identity_implies_count_eq {p q r : Poly} {j k : Nat}
    (hp : HasJ [] p N) (hq : HasJ [] q N)
    (cp : PolyConvPlus (scalarLeft p) (iterationPoly j))
    (cq : PolyConvPlus (scalarLeft q) (iterationPoly k))
    (h : HasJ [] r (.identity N p q)) : j = k := by
  let raw : OpenTermStandardness.SatPER :=
    ⟨OpenTermStandardness.Conv, OpenTermStandardness.Conv.symm,
      OpenTermStandardness.Conv.trans,
      fun ha hb hc => ha.symm.trans (hc.trans hb)⟩
  have rel : OpenTermStandardness.churchPER.rel
      (ImportedOpenTermTransport.interp p FullPER.zeroEnv)
      (ImportedOpenTermTransport.interp q FullPER.zeroEnv) :=
    (JointCompletion.fundamental h FullPER.Application.emptyEnv _ _
      FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩).1
  rw [← ClosedScalarInstances.interp_closed (Structural.has_scoped hp)
        OpenTermStandardness.T.var FullPER.zeroEnv,
      ← ClosedScalarInstances.interp_closed (Structural.has_scoped hq)
        OpenTermStandardness.T.var FullPER.zeroEnv] at rel
  have hh := rel raw (.var 1) (.var 1)
    (fun a b hab => OpenTermStandardness.Conv.app (.refl _) hab)
    (.var 0) (.var 0) (OpenTermStandardness.Conv.refl _)
  have hc := (ImportedOpenTermTransport.source_plus_sound cp OpenTermStandardness.T.var).symm.trans
    (hh.trans (ImportedOpenTermTransport.source_plus_sound cq OpenTermStandardness.T.var))
  rw [ClosedScalarInstances.iteration_interp, ClosedScalarInstances.iteration_interp] at hc
  exact OpenDevelopments.iter_conv_injective hc

/-- Completeness for closed, already typed Joint Church identity. It makes
no global source-completeness or arbitrary-typing decision claim. -/
theorem identity_iff_extracted_count {p q : Poly} (hp : HasJ [] p N) (hq : HasJ [] q N) :
    (∃ r, HasJ [] r (.identity N p q)) ↔
      (EffectiveNumerals.extractIteration p hp).val = (EffectiveNumerals.extractIteration q hq).val := by
  constructor
  · rintro ⟨r,hr⟩
    exact identity_implies_count_eq hp hq
      (EffectiveNumerals.extractIteration p hp).property
      (EffectiveNumerals.extractIteration q hq).property hr
  · intro e
    refine ⟨i, identity_of_observation hp hq
      (body_of_N ctx1 (closed_has hp (.ctxBase (ctx_inclusion ctx1))))
      (body_of_N ctx1 (closed_has hq (.ctxBase (ctx_inclusion ctx1)))) ?_⟩
    exact (EffectiveNumerals.extractIteration p hp).property.trans
      (e ▸ (EffectiveNumerals.extractIteration q hq).property).symm

/-- A total identity decision on supplied closed Joint natural typings. -/
def decideTypedIdentity {p q : Poly} (hp : HasJ [] p N) (hq : HasJ [] q N) :
    Decidable (∃ r, HasJ [] r (.identity N p q)) :=
  decidable_of_iff
    ((EffectiveNumerals.extractIteration p hp).val = (EffectiveNumerals.extractIteration q hq).val)
    (identity_iff_extracted_count hp hq).symm

#print axioms decideTypedIdentity
#print axioms identity_implies_count_eq
#print axioms identity_iff_extracted_count
#print axioms identity_of_observation
#print axioms canonicity_at_count
#print axioms extracted_identity
end JointCompletion.DependentExtraction
