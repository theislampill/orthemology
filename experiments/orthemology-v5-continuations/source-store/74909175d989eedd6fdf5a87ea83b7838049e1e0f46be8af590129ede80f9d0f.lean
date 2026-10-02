import SingletonControllerSpecialization

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
namespace Orthemology.RuntimeBridge.Controller.Fixture
open HiddenParity HiddenParity.Stochastic HiddenParity.Necessity
open HiddenParity.Sufficiency HiddenParity.Adaptive HiddenParity.Stage

/-- Full rows, including off-menu pairs, exactly match the executable fixture. -/
def kernel : RationalKernel Bool (Bool × Bool) Bool where
  row σ e y := if y then (if e.2 = σ then 1/3 else 2/3) else (if e.2 = σ then 2/3 else 1/3)
  nonnegative := by intro σ e y; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> cases y <;> norm_num
  normalized := by intro σ e; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> norm_num [Fintype.sum_bool]

def zeroPriority (_ : Bool) (_ : Bool × Bool) : ℕ := 0

theorem selected_lawful :
    Lawful kernel (singletonMenu (Model := Bool) id) Finset.univ false
      (selectedPolicy id false) (Measure.dirac ()) := by
  intro h hLive
  apply ae_of_all
  intro r hComp
  simp [pair_selectedPolicy, singletonMenu]

theorem every_path_zero_parity (x : ℕ → Bool × Bool) : ParitySuccess (zeroPriority false) x := by
  obtain ⟨e,he⟩ := recurrentSet_nonempty x
  exact ⟨0, ⟨⟨e,he,rfl⟩,fun _ _ => le_refl 0⟩,rfl⟩

def simpleWinner : WinningPolicy (R := Unit) kernel (singletonMenu id) zeroPriority
    (false,false) Finset.univ false where
  nonempty := ⟨false,Finset.mem_univ _⟩
  seedLaw := Measure.dirac ()
  probability := inferInstance
  policy := selectedPolicy id false
  measurable := selectedPolicy_measurable id false
  lawful := selected_lawful
  parity := by
    intro σ hσ
    apply ae_of_all
    intro H
    exact every_path_zero_parity _

theorem initial_winning : false ∈ winningRegion kernel (singletonMenu id) zeroPriority Finset.univ :=
  winning_policy_mem_winningRegion kernel (singletonMenu id) zeroPriority (false,false) Finset.univ false simpleWinner

/-- The literal accepted controller with its actual empirical history test,
for any positive tolerance, has this fixture's executable action/history law. -/
theorem accepted_fixture_law (σ : Bool) (ε : ℝ) :
    markovHistoryLaw kernel σ false
      (generatedPhasePolicy kernel (singletonMenu id) zeroPriority Finset.univ false false false
        (empiricalReject kernel ε)) (Measure.dirac ()) =
    markovHistoryLaw kernel σ false (selectedPolicy id false) (Measure.dirac ()) :=
  generated_singleton_law kernel id zeroPriority Finset.univ false initial_winning
    false false (empiricalReject kernel ε) σ (Finset.mem_univ _)

end Orthemology.RuntimeBridge.Controller.Fixture
