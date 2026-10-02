import GeneratedSliceAlignment

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.HistoryPMF
attribute [local instance] Classical.propDecidable
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity
universe u w
variable {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Nonzero mass in the constructed actual-history PMF entails both action
compatibility and a nonzero literal row-product likelihood. -/
theorem historyPMF_support (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
    (π : History A Y → A) (n : ℕ) (h : History A Y)
    (hne : historyPMF P hP hN π n h≠0) :
    ActionCompatible (fun (_ : Unit) h => π h) () h ∧ RowLikelihood P h≠0 := by
  rw [historyPMF_mass] at hne
  by_cases hl : n=h.length
  · rw [if_pos hl] at hne
    by_cases hc : ActionCompatible (fun (_ : Unit) h => π h) () h
    · simpa only [if_pos hc,one_mul] using And.intro hc hne
    · simp only [if_neg hc,zero_mul,ne_eq,not_true_eq_false] at hne
  · simp only [if_neg hl,ne_eq,not_true_eq_false] at hne

theorem rowLikelihood_nonzero_rows (P : A → Y → ℝ) (h : History A Y)
    (hne : RowLikelihood P h≠0) : ∀ ey ∈ h, 0 < P ey.1 ey.2 := by
  induction h with
  | nil => simp
  | cons ay h ih =>
      rw [rowLikelihood_cons] at hne
      have hh := (mul_ne_zero_iff.mp hne)
      intro ey hey
      rcases List.mem_cons.mp hey with he | he
      · subst ey
        exact ENNReal.ofReal_ne_zero_iff.mp hh.1
      · exact ih hh.2 ey he

theorem unit_prefix_compatible (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1) (h : History A Y)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) P hP hN (PrefixEvent (fun (_ : Unit) h => π h) h)) :
    ActionCompatible (fun (_ : Unit) h => π h) () h := by
  let πu : Unit → History A Y → A := fun _ h => π h
  have hπ : Measurable (fun z : Unit × History A Y => πu z.1 z.2) := measurable_of_countable _
  have hseeds := positive_prefix_compatible_seeds πu (Measure.dirac ()) P hP hN h hpos
  by_contra hnot
  have hz : (Measure.dirac ()) (CompatibleSeeds πu h)=0 := by
    rw [Measure.dirac_apply' _ (compatibleSeeds_measurable πu hπ h)]
    simp [CompatibleSeeds,πu,hnot]
  rw [hz] at hseeds
  exact lt_irrefl 0 hseeds

variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- At every finite horizon under the actual positive-prefix conditional law,
the appended complete history is policy-compatible and retains the true model.
This removes the apparent compatibility/live guards from probabilistic uses of
the deterministic generated-slice alignment theorem. -/
theorem conditional_history_compatible_live
    (P : RationalKernel Model (State × Action) State) (B₀ : Finset Model) (σ : Model) (hσ : σ ∈ B₀)
    (π : History (State × Action) State → State × Action) (base : History (State × Action) State)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) (PrefixEvent (fun (_ : Unit) h => π h) base))
    (n : ℕ) :
    ∀ᵐ H ∂conditionalContinuationLaw (fun (_ : Unit) h => π h) (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) base,
      ActionCompatible (fun (_ : Unit) h => π h) () (H n++base) ∧ σ ∈ liveHistory P B₀ (H n++base) := by
  let πu : Unit → History (State × Action) State → State × Action := fun _ h => π h
  let μ := conditionalContinuationLaw πu (Measure.dirac ()) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) base
  let tailπ := fun tail => π (tail++base)
  have hBaseComp := unit_prefix_compatible π (realRows P σ) (realRows_nonnegative P σ)
    (realRows_normalized P σ) base hpos
  have hBaseL : RowLikelihood (realRows P σ) base≠0 := by
    intro hz
    have hh := hpos
    rw [prefix_probability,hz,mul_zero] at hh
    exact lt_irrefl 0 hh
  have hBaseRows := rowLikelihood_nonzero_rows (realRows P σ) base hBaseL
  have hmap : μ.map (fun H => H n) =
      (historyPMF (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) tailπ n).toMeasure := by
    dsimp [μ,πu,tailπ]
    rw [unit_conditionalContinuationLaw π (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ) base hpos,actual_history_marginal_eq_pmf]
  have hAE : ∀ᵐ tail ∂(historyPMF (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) tailπ n).toMeasure,
      ActionCompatible πu () (tail++base) ∧ σ ∈ liveHistory P B₀ (tail++base) := by
    apply ae_iff_of_countable.mpr
    intro tail hmass
    rw [PMF.toMeasure_apply_singleton _ tail (measurableSet_singleton tail)] at hmass
    obtain ⟨hTailComp,hTailL⟩ := historyPMF_support (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ) tailπ n tail hmass
    have hTailRows := rowLikelihood_nonzero_rows (realRows P σ) tail hTailL
    refine ⟨(compatible_append πu () base tail).mpr ⟨hBaseComp,hTailComp⟩,?_⟩
    apply (mem_liveHistory P B₀ (tail++base) σ).mpr
    refine ⟨hσ,?_⟩
    intro ey hey
    have hr : 0 < realRows P σ ey.1 ey.2 := by
      rcases List.mem_append.mp hey with h | h
      · exact hTailRows ey h
      · exact hBaseRows ey h
    change (0 : ℝ) < (P.row σ ey.1 ey.2 : ℝ) at hr
    exact_mod_cast hr
  rw [← hmap] at hAE
  exact ae_of_ae_map (measurable_pi_apply n).aemeasurable hAE

end HiddenParity.Cost.HistoryPMF
