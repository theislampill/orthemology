import OpenDevelopments
import ScalarCertificates

/- A partial rejection certificate for the input domain only. It does not reject
   the scalar-instance target and assigns no logical meaning to resource refusal. -/
namespace NonstandardRejection
open OpenTermStandardness (T Conv)
open OpenDevelopments (Step RedexFree Normal readIteration iter_normal)
open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft)
open P01Certificate (Address)

def normalB : T → Bool
  | .app f a => if (ScalarCertificates.root (.app f a)).isSome then false
    else normalB f && normalB a
  | _ => true

theorem step_normalB_false {t u : T} (h : Step t u) : normalB t = false := by
  induction h with
  | i x => simp [normalB, ScalarCertificates.root]
  | k x y => simp [normalB, ScalarCertificates.root]
  | s f g x => simp [normalB, ScalarCertificates.root]
  | left h x ih => simp [normalB, ih]
  | right f h ih => simp [normalB, ih]

theorem normalB_sound {t : T} (h : normalB t = true) : RedexFree t := by
  intro u hs
  have hf := step_normalB_false hs
  rw [h] at hf
  contradiction

/-- A proved non-iteration normal endpoint excludes precisely closed Church typing. -/
theorem non_iteration_normal_refutes {n : Poly} {z : T}
    (hz : Normal z) (hc : Conv (interp (scalarLeft n) T.var) z)
    (hnone : readIteration z = none) : ¬ HasE [] n N := by
  intro hn
  obtain ⟨k,hk⟩ := ClosedScalarInstances.source_uniform_iteration hn
  have hi := ImportedOpenTermTransport.source_plus_sound hk T.var
  rw [ClosedScalarInstances.iteration_interp] at hi
  have eq := OpenDevelopments.normal_unique hz (iter_normal k) (hc.symm.trans hi)
  have hs := OpenDevelopments.readIteration_iter k
  rw [← eq, hnone] at hs
  contradiction

/-- All negative-certificate checks are decidable computations; successful
    finite checks refute only membership in the closed HasE Church-input domain. -/
theorem checked_non_iteration_refutes (n : Poly) (z : T) (path : List Address)
    (hReplay : (ScalarCertificates.replayTo (interp (scalarLeft n) T.var) z path).isSome = true)
    (hNormal : normalB z = true) (hNone : readIteration z = none) :
    ¬ HasE [] n N :=
  non_iteration_normal_refutes (OpenDevelopments.redexFree_normal (normalB_sound hNormal))
    (ScalarCertificates.optionProof _ hReplay) hNone

def literalZero : Poly := .atom .zero
def literalZeroEndpoint : T := .app (.app .zero (.var 1)) (.var 0)

/-- Concrete checked source-domain rejection; not a scalar-instance nonderivability claim. -/
theorem literal_zero_not_Church_typed : ¬ HasE [] literalZero N :=
  checked_non_iteration_refutes literalZero literalZeroEndpoint [] rfl rfl rfl

#print axioms checked_non_iteration_refutes
#print axioms literal_zero_not_Church_typed
end NonstandardRejection
