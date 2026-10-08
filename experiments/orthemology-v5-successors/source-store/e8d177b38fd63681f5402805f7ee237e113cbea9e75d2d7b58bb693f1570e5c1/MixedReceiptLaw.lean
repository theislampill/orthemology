import CanonicalHistoryBinding

set_option autoImplicit false

/-!
# Executed-policy / decoder-policy receipt-law bridge

The implementation certificate below belongs only to the executed policy `a0`.
The independently chosen decoder `a` labels the same physical receipts with its
own generated action history. No equality of these two histories is assumed.
-/

noncomputable section
namespace Orthemology.Eighth.SemanticControls

open MeasureTheory Set Preorder
open scoped ENNReal BigOperators
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw Orthemology.RationalLaw.RuntimeBinding
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

attribute [local instance] Classical.propDecidable

/-- The receipt row of the actual runtime while its action equals the actual
model. The decoder's state, action and model arguments do not affect this row. -/
def blindKernel : RationalKernel Bool (Bool × Bool) Bool where
  row _ _ y := if y then 1/3 else 2/3
  nonnegative := by intro σ e y; cases y <;> norm_num
  normalized := by intro σ e; norm_num [Fintype.sum_bool]

theorem blindKernel_positive (σ : Bool) (e : Bool × Bool) (y : Bool) :
    0 < blindKernel.row σ e y := by
  cases y <;> norm_num [blindKernel]

theorem blindKernel_normalized (σ : Bool) (e : Bool × Bool) :
    ∑ y, blindKernel.row σ e y = 1 := blindKernel.normalized σ e

theorem matched_weight_eq_blind (σ : Bool) (e : Bool × Bool) (y : Bool) :
    (weight 3 (RuntimeBinding.row σ σ) y : ℝ≥0∞) / 3 =
      ENNReal.ofReal (blindKernel.row σ e y) := by
  rw [row_weight]
  cases y <;> norm_num [blindKernel, ENNReal.ofReal_div_of_pos]

/-- Executed receipt weights agree with the likelihood of the decoder-labelled
history solely because every executed row is the fixed blind row. -/
theorem generatedHistory_blind_likelihood (σ : Bool) (a0 a : ℕ → Bool)
    (hconstant : ∀ h : History Bool Bool, historyPolicy a0 () h = σ)
    (n : ℕ) (ys : Fin n → Bool) :
    RowLikelihood (realRows blindKernel σ) (generatedHistory a n ys) =
      historyMass 3 (adaptiveRow σ a0) (RuntimeBinding.update a0) n [] ys := by
  induction n with
  | zero => simp [generatedHistory, foldReceipts, RowLikelihood, historyMass]
  | succ n ih =>
      rw [generatedHistory_snoc, rowLikelihood_cons, ih, historyMass_snoc]
      rw [mul_comm]
      congr 1
      simp only [adaptiveRow, hconstant]
      exact (matched_weight_eq_blind σ _ _).symm

def blindHistoryLaw (σ : Bool) (a : ℕ → Bool) : Measure (ℕ → PairHistory) :=
  markovHistoryLaw blindKernel σ false (historyPolicy a) (Measure.dirac ())

theorem blindHistoryLaw_marginal (σ : Bool) (a : ℕ → Bool) (n : ℕ)
    (h : PairHistory) :
    ((blindHistoryLaw σ a).map (fun H => H n)) {h} =
      if n = h.length then
        (if ActionCompatible (fun (_ : Unit) h => pairSelector a h) () h then 1 else 0) *
        RowLikelihood (realRows blindKernel σ) h else 0 := by
  classical
  let π := pairPolicy false (historyPolicy a)
  let P := realRows blindKernel σ
  have hP := realRows_nonnegative blindKernel σ
  have hN := realRows_normalized blindKernel σ
  have hπ : Measurable (fun z : Unit × PairHistory => π z.1 z.2) := measurable_of_countable _
  have hm := history_marginal_formula ∅ π hπ (Measure.dirac ()) P P hP hN hP hN
    (by intro q hq; simp at hq) n h
  unfold blindHistoryLaw markovHistoryLaw observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply n) (historyTrajectory_measurable ∅ π hπ)]
  have hs : MeasurableSet {r : Unit | ActionCompatible π r h} := (Set.toFinite _).measurableSet
  simpa only [Measure.dirac_apply' _ hs, Set.mem_setOf_eq, RowLikelihood] using hm

/-- The marginal uses the executed policy for physical receipt probabilities and
the separately chosen decoder for action compatibility. -/
theorem mixed_decodedHistory_marginal (p : P02A2.PRProgram.Program 1)
    (a0 a : ℕ → Bool) (hp : PolicyImplements p a0) (σ : Bool)
    (hconstant : ∀ h : History Bool Bool, historyPolicy a0 () h = σ) (n : ℕ) :
    fairCantor.map (fun x => decodedHistory p a σ x n) =
      (blindHistoryLaw σ a).map (fun H => H n) := by
  classical
  apply Measure.ext_of_singleton
  intro h
  rw [blindHistoryLaw_marginal]
  have hm : Measurable (fun x => decodedHistory p a σ x n) :=
    (measurable_pi_apply n).comp (decodedHistory_measurable p a σ)
  rw [Measure.map_apply hm (measurableSet_singleton _)]
  by_cases hr : ∃ ys : Fin n → Bool, generatedHistory a n ys = h
  · obtain ⟨ys, rfl⟩ := hr
    have he : (fun x => decodedHistory p a σ x n) ⁻¹' {generatedHistory a n ys} =
        (runtimeReceiptPath p σ) ⁻¹' receiptCylinder n ys := by
      ext x
      simp only [Set.mem_preimage, Set.mem_singleton_iff, decodedHistory,
        receiptCylinder, Set.mem_setOf_eq]
      constructor
      · intro hh i
        exact congrFun (generatedHistory_injective a n hh) i
      · intro hh
        rw [funext hh]
    rw [he, ← Measure.map_apply (runtimeReceiptPath_measurable p σ)
      (measurableSet_receiptCylinder n ys), runtime_receipt_path_cylinder_probability p a0 hp,
      generatedHistory_length, if_pos rfl, if_pos (generatedHistory_compatible a n ys),
      one_mul, generatedHistory_blind_likelihood σ a0 a hconstant]
  · have he : (fun x => decodedHistory p a σ x n) ⁻¹' {h} = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro x hx
      exact hr ⟨_, hx⟩
    rw [he, measure_empty]
    by_cases hl : n = h.length
    · subst n
      have hc : ¬ActionCompatible (fun (_ : Unit) h => pairSelector a h) () h := by
        intro hc
        exact hr (compatible_generatedHistory a h hc)
      simp [hc]
    · simp [hl]

instance blindHistoryLaw_probability (σ : Bool) (a : ℕ → Bool) :
    IsProbabilityMeasure (blindHistoryLaw σ a) := by
  unfold blindHistoryLaw markovHistoryLaw observedTraceLaw
  exact isProbabilityMeasure_map (historyTrajectory_measurable ∅ _
    (measurable_of_countable _)).aemeasurable

theorem blindHistoryLaw_prefix_from_last (σ : Bool) (a : ℕ → Bool) (N : ℕ) :
    (blindHistoryLaw σ a).map (frestrictLe N) =
      ((blindHistoryLaw σ a).map (fun H => H N)).map (reconstructPrefix N) := by
  unfold blindHistoryLaw markovHistoryLaw
  rw [observed_prefix_map_from_last ∅ _ (measurable_of_countable _)]
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply N)
    (historyTrajectory_measurable ∅ _ (measurable_of_countable _))]
  rfl

/-- Exact mixed law: the source executes `a0`, while the output is decoded with
arbitrary `a`. Only `a0` has an implementation certificate. -/
theorem mixed_runtime_blind_history_law (p : P02A2.PRProgram.Program 1)
    (a0 a : ℕ → Bool) (hp : PolicyImplements p a0) (σ : Bool)
    (hconstant : ∀ h : History Bool Bool, historyPolicy a0 () h = σ) :
    fairCantor.map (decodedHistory p a σ) =
      markovHistoryLaw blindKernel σ false (historyPolicy a) (Measure.dirac ()) := by
  change fairCantor.map (decodedHistory p a σ) = blindHistoryLaw σ a
  apply measure_eq_of_prefix_maps
  intro N
  rw [blindHistoryLaw_prefix_from_last]
  have hm : Measurable (fun x => decodedHistory p a σ x N) :=
    (measurable_pi_apply N).comp (decodedHistory_measurable p a σ)
  rw [← mixed_decodedHistory_marginal p a0 a hp σ hconstant N]
  rw [Measure.map_map (measurable_frestrictLe N) (decodedHistory_measurable p a σ),
    Measure.map_map (measurable_of_countable
      (reconstructPrefix (A := Bool × Bool) (Y := Bool) N)) hm]
  congr 1
  funext x
  exact decodedHistory_prefix_from_last p a σ x N

/-- The same mixed law expressed directly through the physical P02 output and
the existing common output-only decoder. -/
theorem mixed_physical_runtime_blind_history_law (p : P02A2.PRProgram.Program 1)
    (a0 a : ℕ → Bool) (hp : PolicyImplements p a0) (σ : Bool)
    (hconstant : ∀ h : History Bool Bool, historyPolicy a0 () h = σ) :
    (fairCantor.map (Orthemology.CertifiedObserver.Indexed.runtimeOutput (runtimeIndex p σ))).map
        (canonicalHistoryDecoder a) =
      markovHistoryLaw blindKernel σ false (historyPolicy a) (Measure.dirac ()) := by
  rw [Measure.map_map (canonicalHistoryDecoder_measurable a)
    (Orthemology.CertifiedObserver.Indexed.runtime_output_measurable _),
    canonicalHistoryDecoder_on_runtime]
  exact mixed_runtime_blind_history_law p a0 a hp σ hconstant

end Orthemology.Eighth.SemanticControls
