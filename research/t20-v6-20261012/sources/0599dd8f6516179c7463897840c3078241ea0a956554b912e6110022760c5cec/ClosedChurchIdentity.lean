import ClosedScalarInstances
import EffectiveCanonicalTests
import HasEClosedWeakening

/- Finite source extensionality for closed Church endpoints. The conditional
   construction exposes its exact lifting obligation; the final theorems
   discharge it with actual HasE structural renaming for every closed input. -/
namespace ClosedChurchIdentity
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody iterationPoly inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedScalarInstances (scalarLeft)
open ImportedOpenTermTransport (interp)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

abbrev ctx1 : Ctx [End] := .ext .nil (ExactScalarFusion.End_form .nil)
abbrev ctx2 : Ctx [A,End] := .ext ctx1 (ExactScalarFusion.A_form ctx1)

theorem formEnd {Γ} (h : Ctx Γ) : FormE Γ End :=
  form_inclusion (ExactScalarFusion.End_form h)
theorem formBody {Γ} (h : Ctx Γ) : FormE Γ NBody :=
  form_inclusion (form_arr (ExactScalarFusion.End_form h) (ExactScalarFusion.End_form h))
theorem formN {Γ} (h : Ctx Γ) : FormE Γ N :=
  form_inclusion (EffectiveCompleteness.N_form h)

theorem body_of_N {Γ n} (hΓ : Ctx Γ) (hn : HasE Γ n N) : HasE Γ n NBody :=
  .allElim (formN hΓ) (.param (ctx_inclusion hΓ)) (formBody hΓ) hn

def point (p : Poly) : Poly := .app p (.var 0)

theorem point_has {n} (hn : HasE [End] n NBody) : HasE [End] (point n) End :=
  .piElim (formBody ctx1) (formEnd ctx1) hn (.var (formEnd ctx1) .zero)

theorem observation_has {p} (hp : HasE [] p N) : HasE [A,End] (scalarLeft p) A :=
  (ClosedScalarInstances.scalar_endpoints hp).1

/-- Two applications suffice once the original once-applied endpoints can be
    typed in their one-variable context. No weakening theorem is assumed here. -/
theorem identity_of_observation {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N)
    (lp : HasE [End] p NBody) (lq : HasE [End] q NBody)
    (hc : PolyConvPlus (scalarLeft p) (scalarLeft q)) :
    HasE [] i (.identity N p q) := by
  have sp := ClosedProofCanonicalisation.has_scope hp
  have sq := ClosedProofCanonicalisation.has_scope hq
  have hp1 := point_has lp
  have hq1 := point_has lq
  have hp2 := observation_has hp
  have hq2 := observation_has hq
  have hf2 : FormE [A,End] (.identity A (scalarLeft p) (scalarLeft q)) :=
    .identity (.param (ctx_inclusion ctx2)) hp2 hq2
  have hi2 : HasE [A,End] i (.identity A (scalarLeft p) (scalarLeft q)) :=
    .identityIntro hf2 hp2 hq2 hc
  have ep : .app (pren Nat.succ (point p)) (.var 0) = scalarLeft p := by
    simp [point, scalarLeft, pren, psub, ExactScalarFusion.psub_closed sp]
  have eq : .app (pren Nat.succ (point q)) (.var 0) = scalarLeft q := by
    simp [point, scalarLeft, pren, psub, ExactScalarFusion.psub_closed sq]
  have hfpi : FormE [End] (.pi A (.identity A (scalarLeft p) (scalarLeft q))) :=
    .pi (.param (ctx_inclusion ctx1)) hf2
  have hhpi : HasE [End] (abstract i)
      (.pi A (.identity A (scalarLeft p) (scalarLeft q))) :=
    .piIntro hfpi hi2 (scoped_abstract trivial)
  have hi1 : HasE [End] i (.identity End (point p) (point q)) := by
    apply HasE.piExt (.param (ctx_inclusion ctx1)) (.param (ctx_inclusion ctx2))
      (formEnd ctx1) hp1 hq1
    · simpa only [ep, eq] using hf2
    · simpa only [ep, eq] using hfpi
    · simpa only [ep, eq] using hhpi
    · exact .identity (formEnd ctx1) hp1 hq1
    · exact ClosedProofCanonicalisation.has_scope hp1
    · exact ClosedProofCanonicalisation.has_scope hq1
    · exact scoped_abstract trivial
    · trivial
    · trivial
  have hp0 := body_of_N Ctx.nil hp
  have hq0 := body_of_N Ctx.nil hq
  have hf1 : FormE [End] (.identity End (point p) (point q)) :=
    .identity (formEnd ctx1) hp1 hq1
  have efp : .app (pren Nat.succ p) (.var 0) = point p := by
    rw [ExactScalarFusion.pren_closed sp]; rfl
  have efq : .app (pren Nat.succ q) (.var 0) = point q := by
    rw [ExactScalarFusion.pren_closed sq]; rfl
  have hf0 : FormE [] (.pi End (.identity End (point p) (point q))) :=
    .pi (formEnd .nil) hf1
  have hh0 : HasE [] (abstract i) (.pi End (.identity End (point p) (point q))) :=
    .piIntro hf0 hi1 (scoped_abstract trivial)
  have hi0 : HasE [] i (.identity NBody p q) := by
    apply HasE.piExt (formEnd .nil) (formEnd ctx1) (formBody .nil) hp0 hq0
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

/-- The pre-existing old-Has lifting result is used only on old-Has inputs. -/
theorem old_lift {p : Poly} (hp : Has [] p N) : HasE [End] p NBody := by
  have h : Has [End] p N :=
    BooleanPrimitive.closed_has hp BooleanPrimitive.N_subst ctx1
  exact body_of_N ctx1 (has_inclusion h)

theorem interp_iteration (k : Nat) (f a : OpenTermStandardness.T)
    (η : Nat → OpenTermStandardness.T) :
    interp (iterationPoly k) (OpenTermStandardness.cons a (OpenTermStandardness.cons f η)) =
      OpenTermStandardness.iter f a k := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg (OpenTermStandardness.T.app f) ih

/-- Literal bracket numerals have the required generic-open conversion. -/
theorem numeral_observation (k : Nat) :
    PolyConvPlus (scalarLeft (inputNumeral k)) (iterationPoly k) := by
  apply ClosedScalarInstances.generic_conversion_reflect
  rw [ClosedScalarInstances.iteration_interp]
  have h1 := OpenTermStandardness.Conv.app
    (ImportedOpenTermTransport.interp_abstraction_beta
      (abstract (iterationPoly k)) OpenTermStandardness.T.var (.var 1))
    (OpenTermStandardness.Conv.refl (.var 0))
  have h2 := ImportedOpenTermTransport.interp_abstraction_beta
    (iterationPoly k) (OpenTermStandardness.cons (.var 1) OpenTermStandardness.T.var) (.var 0)
  exact h1.trans ((interp_iteration k _ _ _) ▸ h2)

/-- A conversion at source variables yields every closed raw test by evaluation,
    without any semantic-to-syntactic converse. -/
theorem observation_uniform {p : Poly} {k : Nat} (hp : Scoped 0 p)
    (h : PolyConvPlus (scalarLeft p) (iterationPoly k)) :
    ∀ f a, Conv (.app (.app (eval p zeroEnv) f) a) (iterateTerm f k a) := by
  intro f a
  have h' := Intensional.Plus.polyConvPlus_sound h
    (P01F.cons a (P01F.cons f zeroEnv))
  change Conv (.app (.app (eval p (P01F.cons a (P01F.cons f zeroEnv))) f) a)
    (eval (iterationPoly k) (P01F.cons a (P01F.cons f zeroEnv))) at h'
  rw [BooleanPrimitive.eval_closed hp _ zeroEnv, EffectiveCompleteness.eval_iteration] at h'
  exact h'

/-- Any source identity proof, including a noncanonical witness, forces equal
    counts. This direction needs no endpoint-lifting hypothesis. -/
theorem identity_implies_count_eq {p q r : Poly} {j k : Nat}
    (hp : HasE [] p N) (hq : HasE [] q N)
    (cp : PolyConvPlus (scalarLeft p) (iterationPoly j))
    (cq : PolyConvPlus (scalarLeft q) (iterationPoly k))
    (h : HasE [] r (.identity N p q)) : j = k := by
  have rel : F N (fun _ => rawPER) zeroEnv (eval p zeroEnv) (eval q zeroEnv) :=
    (ExtensionalRepair.unary_fundamental h (ρ := fun _ => rawPER) ⟨rfl,rfl⟩).1
  exact IdentityComplexity.related_same_index rel
    (observation_uniform (ClosedProofCanonicalisation.has_scope hp) cp)
    (observation_uniform (ClosedProofCanonicalisation.has_scope hq) cq)

/-- Canonicity for actual closed HasE n, conditional only on its one-context lift. -/
theorem canonicity_with_lift {n : Poly} {k : Nat} (hn : HasE [] n N)
    (lift : HasE [End] n NBody)
    (count : PolyConvPlus (scalarLeft n) (iterationPoly k)) :
    HasE [] i (.identity N n (inputNumeral k)) :=
  identity_of_observation hn (has_inclusion (EffectiveCompleteness.inputNumeral_has k))
    lift (old_lift (EffectiveCompleteness.inputNumeral_has k))
    (count.trans (numeral_observation k).symm)

/-- A finite source-identity completeness theorem for the inherited old-Has
    closed Church fragment, at the unchanged source endpoints. -/
theorem old_canonicity {n : Poly} (hn : Has [] n N) :
    ∃ k, HasE [] i (.identity N n (inputNumeral k)) := by
  obtain ⟨k,hk⟩ := ClosedScalarInstances.source_uniform_iteration (has_inclusion hn)
  exact ⟨k,canonicity_with_lift (has_inclusion hn) (old_lift hn) hk⟩

theorem identity_iff_count_eq_with_lift {p q : Poly} {j k : Nat}
    (hp : HasE [] p N) (hq : HasE [] q N)
    (lp : HasE [End] p NBody) (lq : HasE [End] q NBody)
    (cp : PolyConvPlus (scalarLeft p) (iterationPoly j))
    (cq : PolyConvPlus (scalarLeft q) (iterationPoly k)) :
    HasE [] i (.identity N p q) ↔ j = k := by
  constructor
  · exact identity_implies_count_eq hp hq cp cq
  · intro e
    subst k
    exact identity_of_observation hp hq lp lq (cp.trans cq.symm)

/-- Every actual closed HasE Church derivation has a finite source identity
    to the standard numeral at its generic-open count. -/
theorem canonicity_at_count {n : Poly} {k : Nat} (hn : HasE [] n N)
    (count : PolyConvPlus (scalarLeft n) (iterationPoly k)) :
    HasE [] i (.identity N n (inputNumeral k)) :=
  canonicity_with_lift hn
    (body_of_N ctx1 (Structural.closed_church_weaken hn)) count

theorem closed_canonicity {n : Poly} (hn : HasE [] n N) :
    ∃ k, HasE [] i (.identity N n (inputNumeral k)) := by
  obtain ⟨k,hk⟩ := ClosedScalarInstances.source_uniform_iteration hn
  exact ⟨k,canonicity_at_count hn hk⟩

/-- Source-identity completeness is restricted to closed, already typed Church
    endpoints. The input derivations and original polynomials are unchanged. -/
theorem identity_iff_count_eq {p q : Poly} {j k : Nat}
    (hp : HasE [] p N) (hq : HasE [] q N)
    (cp : PolyConvPlus (scalarLeft p) (iterationPoly j))
    (cq : PolyConvPlus (scalarLeft q) (iterationPoly k)) :
    HasE [] i (.identity N p q) ↔ j = k :=
  identity_iff_count_eq_with_lift hp hq
    (body_of_N ctx1 (Structural.closed_church_weaken hp))
    (body_of_N ctx1 (Structural.closed_church_weaken hq)) cp cq

theorem identity_exists_iff_count_eq {p q : Poly} {j k : Nat}
    (hp : HasE [] p N) (hq : HasE [] q N)
    (cp : PolyConvPlus (scalarLeft p) (iterationPoly j))
    (cq : PolyConvPlus (scalarLeft q) (iterationPoly k)) :
    (∃ r, HasE [] r (.identity N p q)) ↔ j = k := by
  constructor
  · rintro ⟨r,h⟩
    exact identity_implies_count_eq hp hq cp cq h
  · intro e
    exact ⟨i,(identity_iff_count_eq hp hq cp cq).mpr e⟩

#print axioms canonicity_at_count
#print axioms closed_canonicity
#print axioms identity_iff_count_eq
#print axioms identity_exists_iff_count_eq
#print axioms numeral_observation
#print axioms identity_implies_count_eq
#print axioms canonicity_with_lift
#print axioms old_canonicity
#print axioms identity_iff_count_eq_with_lift
#print axioms identity_of_observation
#print axioms old_lift
end ClosedChurchIdentity
