import HenkinSoundness
import LiteralCounterexample
import ScalarFusionCore

/- The literal original W is empty in the constructed sound whole-HasE model.
   This is an external nonderivability theorem, not a source negation inhabitant. -/
namespace HomogeneousOriginalW
open CaseOperational
open HenkinSourceTransport (interp)
open HenkinSoundness
open HomogeneousCounterexample (q scalarStep)
open P01AC P01D
open P01AC.EffectiveCompleteness (N)
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def AtomR (x y : T) : Prop := Conv x y ∧ AtomVal x

theorem atomR_eligible : ConcreteUniverse.U AtomR := by
  refine ⟨?_, Or.inr (Or.inl (fun _ xx => xx.2))⟩
  exact {
    sym := by
      rintro x y ⟨xy, hx⟩
      refine ⟨xy.symm, ?_⟩
      rcases hx with h0 | h1
      · exact Or.inl (xy.symm.trans h0)
      · exact Or.inr (xy.symm.trans h1)
    trans := fun h k => ⟨h.1.trans k.1,h.2⟩
    saturated := by
      rintro x y x' y' xx' yy' ⟨xy, hx⟩
      refine ⟨xx'.symm.trans (xy.trans yy'), ?_⟩
      rcases hx with h0 | h1
      · exact Or.inl (xx'.symm.trans h0)
      · exact Or.inr (xx'.symm.trans h1) }

def atomPER : SatPER := ⟨AtomR, atomR_eligible⟩

theorem atom0_related : AtomR T.a0 T.a0 := ⟨.refl _,Or.inl (.refl _)⟩

theorem scalarStep_related : Arrow AtomR AtomR scalarStep scalarStep := by
  intro x y _
  exact ⟨(Conv.k T.a1 x).trans (Conv.k T.a1 y).symm,Or.inr (Conv.k T.a1 x)⟩

theorem nu_N (ρ : REnv) (η : HenkinSoundness.Env) : F N ρ η T.nu T.nu := by
  change ∀ P : SatPER, Arrow (Arrow P.rel P.rel) (Arrow P.rel P.rel) T.nu T.nu
  intro P
  exact ConcreteUniverse.concrete_nu_church P.rel P.property

def originalQ : Poly := P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed

/-- No pair of realizers inhabits the actual original W type in this model. -/
theorem W_empty (ρ : REnv) (η : HenkinSoundness.Env) (u v : T) : ¬F (W originalQ) ρ η u v := by
  intro hw
  have h := hw T.nu T.nu (nu_N ρ η) atomPER
    scalarStep scalarStep scalarStep_related T.a0 T.a0 atom0_related
  have bad := h.1
  change AtomR (T.nu ⬝ scalarStep ⬝ T.a0)
    (interp originalQ (cons T.a0 (cons scalarStep (cons T.nu η)))
      ⬝ T.nu ⬝ scalarStep ⬝ T.a0) at bad
  unfold originalQ at bad
  rw [HomogeneousCounterexample.original_q_eval] at bad
  exact HomogeneousCounterexample.scalar_not_convertible bad.1

def emptyTypes : REnv := fun _ _ _ => False

theorem emptyTypes_admissible : admissible emptyTypes :=
  fun _ => ConcreteUniverse.bottom_eligible

/-- The original source has no proof term of the literal universal scalar-fusion type. -/
theorem original_W_uninhabited (p : Poly) :
    ¬P01AC.ExtensionalRepair.HasE [] p (W originalQ) := by
  intro h
  exact W_empty emptyTypes zeroEnv (interp p zeroEnv) (interp p zeroEnv)
    (fundamental h emptyTypes zeroEnv zeroEnv emptyTypes_admissible ⟨rfl,rfl⟩)

theorem original_c3_not_W : ¬P01AC.ExtensionalRepair.HasE [] c3
    (W P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed) :=
  original_W_uninhabited c3

#print axioms nu_N
#print axioms W_empty
#print axioms original_W_uninhabited
#print axioms original_c3_not_W
end HomogeneousOriginalW
