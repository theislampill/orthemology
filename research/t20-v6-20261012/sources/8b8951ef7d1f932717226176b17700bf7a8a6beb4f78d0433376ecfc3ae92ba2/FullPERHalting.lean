import FullPERTests
import BoundedHaltingPR

namespace FullPERTests
open P01AC P01D P01AC.ExtensionalRepair
open P01AC.BooleanPrimitive P01AC.BooleanIdentity
open OpenTermStandardness (T Conv)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def rawEnv : FullPER.REnv := fun _ => Conv

theorem rawEnv_admissible : FullPER.admissible rawEnv :=
  fun _ => ⟨Conv.symm, Conv.trans, fun ha hb h => ha.symm.trans (h.trans hb)⟩

/-- The actual unchanged source type associated with a PR program and machine index. -/
def programType (f : PR 2) (e : Nat) : Ty := testType (simFamily f e)

theorem programType_form (f : PR 2) (e : Nat) : Form [] (programType f e) :=
  testType_form (simFamily_has f e)

theorem programType_formE (f : PR 2) (e : Nat) : FormE [] (programType f e) :=
  testType_formE (simFamily_has f e)

theorem simulator_observation_iff (f : PR 2) (e k : Nat) :
    OrthemologyV3.Conv (observationAt (simFamily f e) k) .zero ↔ f.denote (inputs k e) = 0 := by
  constructor
  · intro h
    have hc : OrthemologyV3.Conv
        (pick (decide (f.denote (inputs k e) ≠ 0)) .zero .one) (pick false .zero .one) :=
      (simFamily_obs f e k).symm.trans h
    have he := pick_conv_injective hc
    by_contra hn
    exact (of_decide_eq_false he) hn
  · intro h
    simpa only [h, ne_eq, not_true_eq_false, decide_false, pick, Bool.false_eq_true, ↓reduceIte]
      using simFamily_obs f e k

theorem program_inhabited_iff (f : PR 2) (e : Nat)
    (ρ : FullPER.REnv) (r : FullPER.admissible ρ) :
    (∃ t, FullPER.F (programType f e) ρ FullPER.zeroEnv t t) ↔
      ∀ k, f.denote (inputs k e) = 0 := by
  rw [programType, inhabited_iff_observations (simFamily_has f e) ρ r]
  exact forall_congr' (fun k => simulator_observation_iff f e k)

theorem program_holds_iff (f : PR 2) (e : Nat) :
    Holds (programType f e) ↔ ∀ k, f.denote (inputs k e) = 0 := by
  constructor
  · intro h
    exact (program_inhabited_iff f e rawEnv rawEnv_admissible).mp (h rawEnv rawEnv_admissible)
  · intro h ρ r
    exact (program_inhabited_iff f e ρ r).mpr h

/-- This is fixed-term validity as well as existential semantic inhabitation. -/
def FixedValid (A : Ty) : Prop := ∀ ρ, FullPER.admissible ρ →
  FullPER.F A ρ FullPER.zeroEnv uniformWitness uniformWitness

theorem program_fixed_iff (f : PR 2) (e : Nat) :
    FixedValid (programType f e) ↔ Holds (programType f e) := by
  constructor
  · intro h ρ r
    exact ⟨uniformWitness,h ρ r⟩
  · intro h ρ r
    exact observations_imply_uniform (simFamily_has f e)
      (fun k => (simulator_observation_iff f e k).mpr ((program_holds_iff f e).mp h k)) ρ r

/-- No assumed machine representation: the witness comes from the actual checked
    primitive-recursive bounded evaluator and retained PR compiler. -/
theorem exists_nonhalting_family : ∃ f : PR 2,
    (∀ e, Form [] (programType f e)) ∧
    (∀ e, Holds (programType f e) ↔ ¬ (Nat.Partrec.Code.eval (machineCode e) 0).Dom) ∧
    (∀ e, FixedValid (programType f e) ↔ ¬ (Nat.Partrec.Code.eval (machineCode e) 0).Dom) := by
  obtain ⟨f, _, hf⟩ := exists_bounded_nonhalting_program
  refine ⟨f,programType_form f,?_,?_⟩
  · intro e
    exact (program_holds_iff f e).trans (hf e)
  · intro e
    exact (program_fixed_iff f e).trans ((program_holds_iff f e).trans (hf e))

/-- A concrete semantic non-enumerability theorem on original well-formed syntax.
    This quantifies over actual PR-compiled families, not stipulated predicates. -/
theorem exists_non_re_formed_family : ∃ f : PR 2,
    (∀ e, FormE [] (programType f e)) ∧
    ¬ REPred (fun e => Holds (programType f e)) ∧
    ¬ REPred (fun e => FixedValid (programType f e)) := by
  obtain ⟨f, _, hf, hfixed⟩ := exists_nonhalting_family
  refine ⟨f,programType_formE f,?_,?_⟩
  · intro h
    apply machine_nonhalting_not_re
    convert h using 1
    funext e
    exact propext (hf e).symm
  · intro h
    apply machine_nonhalting_not_re
    convert h using 1
    funext e
    exact propext (hfixed e).symm

/-- The exact effective-presentation boundary. Any r.e. accepted-index predicate
    that is sound on this actual family necessarily omits a valid instance.
    No claim that a particular source derivability relation is r.e. is hidden here. -/
theorem no_re_sound_complete_acceptance : ∃ f : PR 2,
    (∀ e, FormE [] (programType f e)) ∧
    ∀ accepts : Nat → Prop, REPred accepts →
      (∀ e, accepts e → Holds (programType f e)) →
      ¬ (∀ e, Holds (programType f e) → accepts e) := by
  obtain ⟨f, formed, hnre, _⟩ := exists_non_re_formed_family
  refine ⟨f,formed,?_⟩
  intro accepts hre sound complete
  apply hnre
  convert hre using 1
  funext e
  exact propext ⟨complete e,sound e⟩

#print axioms programType_formE
#print axioms exists_non_re_formed_family
#print axioms no_re_sound_complete_acceptance
end FullPERTests
