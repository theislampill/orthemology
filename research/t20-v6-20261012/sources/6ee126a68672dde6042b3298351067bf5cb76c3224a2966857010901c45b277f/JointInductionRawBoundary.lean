import JointInductionLaws
import SourceTransport

namespace JointCompletion.InductionComputation.RawBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.InternalGraph
open P01AC.Intensional.Plus (PolyConvPlus polyConv_inclusion)
open SourceRigidity RigidityInitiality
open CaseOperational HenkinSourceTransport
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def environment : Nat → CaseOperational.T := fun _ => .nu
def D : Poly := totalStep (uncurriedStep (.atom .k))
def seed : Poly := totalSeed zero
def run : Poly := .app (.app (.var 0) D) seed
def left : Poly := .app (sectionPoly zero (.atom .k)) (.app succPoly (.var 0))
def right : Poly := .app (.app (.atom .k) (.var 0)) (.app (sectionPoly zero (.atom .k)) (.var 0))

theorem left_to_projection : P01DF.PolyConv left (fstPoly run) :=
  ((section_application_beta zero (.atom .k) (.app succPoly (.var 0))).trans
    (section_succ_beta zero (.atom .k) (.var 0))).trans (.k _ _)

theorem right_to_input : P01DF.PolyConv right (.var 0) := .k _ _

theorem seed_function : FunVal (interp seed environment) := raw_fun_val (.s2 _ _)

theorem run_one_step : Conv (interp run environment) (interp (.app D seed) environment) :=
  nu_fun _ seed_function

theorem projection_one : Conv (interp (fstPoly run) environment)
    (interp (.app succPoly zero) environment) := by
  have hproj := source_plus_sound (polyConv_inclusion (totalStep_projection (uncurriedStep (.atom .k)) seed)) environment
  have hseed := source_plus_sound (polyConv_inclusion (pair_first zero zero)) environment
  exact (fst_congr run_one_step).trans
    (hproj.trans (Conv.app (.refl _) hseed))

theorem left_observation : Conv
    (interp left environment ⬝ (.k ⬝ .a1) ⬝ .a0) .a1 := by
  have hl := (source_plus_sound (polyConv_inclusion left_to_projection) environment).trans projection_one
  let f : Poly := .app (.atom .k) (.atom .one)
  let a : Poly := .atom .zero
  have hcalc : P01DF.PolyConv (.app (.app (.app succPoly zero) f) a) (.atom .one) :=
    ((succ_beta zero f a).trans (.app (.refl _) (zero_beta f a))).trans (.k _ _)
  exact (Conv.app (Conv.app hl (.refl _)) (.refl _)).trans
    (source_plus_sound (polyConv_inclusion hcalc) environment)

theorem right_observation : Conv
    (interp right environment ⬝ (.k ⬝ .a1) ⬝ .a0) .a0 := by
  have hr := source_plus_sound (polyConv_inclusion right_to_input) environment
  exact (Conv.app (Conv.app hr (.refl _)) (.refl _)).trans (nu_atom0 _)

/-- The literal successor equation is genuinely not an unrestricted Raw
conversion law. This valuation is used only to test raw conversion; it is
not asserted to realize the Joint context [N]. -/
theorem successor_not_raw : ¬ PolyConvPlus left right := by
  intro h
  have hs := source_plus_sound h environment
  have ho := Conv.app (Conv.app hs (.refl (.k ⬝ .a1))) (.refl .a0)
  exact atom_distinct (right_observation.symm.trans (ho.symm.trans left_observation))

/-- Nevertheless both endpoints are source-typed and propositionally equal
in the actual Joint context with a variable natural input. -/
theorem successor_typed_identity : ∃ e, HasJ [N] e (.identity N left right) := by
  have hc : CtxJ [N] := .ext .nil (N_form .nil)
  have hP : FormJ (N :: [N]) N := N_form (.ext hc (N_form hc))
  have hp : HasJ [N] zero (inst N zero) := by simpa only [inst, N_subst] using zero_has_N hc
  have hs : HasJ [N] (.atom .k) (dependentStepType N) := by
    have hh := HasJ.k (N_form hc) (N_form hc)
      (form_arr (N_form hc) (form_arr (N_form hc) (N_form hc)))
    simpa only [dependentStepType, successorFamily, N_subst, arr, wk, subst, N_subst] using hh
  have hn : HasJ [N] (.var 0) N := .var (N_form hc) .zero
  obtain ⟨e, he⟩ := induction_successor hc hP hp hs hn
  exact ⟨e, by simpa only [inst, N_subst, left, right] using he⟩

#print axioms successor_not_raw
#print axioms successor_typed_identity
end JointCompletion.InductionComputation.RawBoundary
