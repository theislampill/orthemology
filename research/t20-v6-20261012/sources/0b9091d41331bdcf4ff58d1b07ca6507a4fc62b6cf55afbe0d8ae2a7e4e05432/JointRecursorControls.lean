import JointCanonicalRecursor
import JointInductionControls

namespace JointCompletion.RecursorUniqueness.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality InductionComputation
open InductionComputation.Controls
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- This is the retained genuinely new, literally index-dependent family;
its carrier cannot be formed in old E. -/
theorem new_family_not_old : ¬ FormE [N] family := family_not_old

theorem direct_zero : HasJ [] ident
    (.identity (inst family zero) (.app (abstract ident) zero) ident) := by
  have hl := section_value CtxJ.nil family_formed direct_section (zero_has_N .nil)
  apply identityIntro_raw (.identity (has_form family_seed) hl family_seed) hl family_seed
  simpa only [ident, abstract, freeZero, drop, pren, psub] using
    (P01DF.PolyConv.k (.atom .i) zero)

/-- An independently supplied ordinary law for the direct section. It mentions
neither the canonical recursor nor any comparison family. -/
theorem direct_successor_laws : HasJ [] (abstract ident)
    (.pi N (successorLawFamily family step (abstract ident))) := by
  have hL := successor_law_formed CtxJ.nil family_formed family_step direct_section
  have ep := Structural.form_identity_inv hL
  have beta_left : P01DF.PolyConv
      (.app (pren Nat.succ (abstract ident)) (.app succPoly (.var 0))) ident := by
    simpa only [ident, abstract, freeZero, drop, pren, psub] using
      (P01DF.PolyConv.k (.atom .i) (.app succPoly (.var 0)))
  have beta_right : P01DF.PolyConv
      (.app (.app (pren Nat.succ step) (.var 0))
        (.app (pren Nat.succ (abstract ident)) (.var 0))) ident := by
    have first : P01DF.PolyConv (.app (pren Nat.succ step) (.var 0)) (abstract ident) := by
      simpa [step, ident, abstract, freeZero, drop, pren, psub] using
        (P01DF.PolyConv.k (.app (.atom .k) (.atom .i)) (.var 0))
    exact (P01DF.PolyConv.app first (.refl _)).trans (by
      simpa only [ident, abstract, freeZero, drop, pren, psub] using
        (P01DF.PolyConv.k (.atom .i) (.app (pren Nat.succ (abstract ident)) (.var 0))))
  have proof := identityIntro_raw hL ep.2.1 ep.2.2 (beta_left.trans beta_right.symm)
  exact .piIntro (.pi (N_form .nil) hL) proof (scoped_abstract trivial)

/-- Same actual seed and step, two different displayed sections, and no
comparison-law premise: the new uniqueness theorem supplies typed identity. -/
theorem new_family_uniqueness : HasJ [] ident
    (.identity (.pi N family) (abstract ident) (sectionPoly ident step)) :=
  unique_to_canonical .nil family_formed family_seed family_step
    direct_section direct_zero direct_successor_laws

/-- The tested source family really has different literal indexed instances. -/
theorem new_family_varies : inst family zero ≠ inst family (.app succPoly zero) :=
  family_distinct_instances

/-- The input-scope discrimination applies to both data interfaces. -/
theorem no_old_seed (p : Poly) : ¬ HasE [] p (inst family zero) := seed_not_old p

theorem no_old_step (s : Poly) : ¬ HasE [] s (dependentStepType family) := step_not_old s

#print axioms direct_successor_laws
#print axioms new_family_uniqueness
end JointCompletion.RecursorUniqueness.Controls
