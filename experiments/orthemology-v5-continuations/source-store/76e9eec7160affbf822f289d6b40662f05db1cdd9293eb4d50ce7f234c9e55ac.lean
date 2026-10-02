import RuntimeReceiptPath
import MarkovSeedPosterior
import ConditionalPrefix
import PolicyObservedLaw

set_option autoImplicit false

namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
variable {H Y : Type*}

def foldReceipts (step : H → Y → H) : (n : ℕ) → H → (Fin n → Y) → H
  | 0, h, _ => h
  | n+1, h, ys => foldReceipts step n (step h (ys 0)) (fun i => ys i.succ)

theorem foldReceipts_snoc (step : H → Y → H) (n : ℕ) (h : H) (ys : Fin (n+1) → Y) :
    foldReceipts step (n+1) h ys =
      step (foldReceipts step n h (fun i => ys i.castSucc)) (ys (Fin.last n)) := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
      simp only [foldReceipts]
      exact ih _ (fun i => ys i.succ)

variable [DecidableEq Y]
theorem historyMass_snoc (D : ℕ) (row : H → Fin D → Y) (step : H → Y → H)
    (n : ℕ) (h : H) (ys : Fin (n+1) → Y) :
    historyMass D row step (n+1) h ys =
      historyMass D row step n h (fun i => ys i.castSucc) *
      ((weight D (row (foldReceipts step n h (fun i => ys i.castSucc))) (ys (Fin.last n)) : ℝ≥0∞)/D) := by
  induction n generalizing h with
  | zero => simp [historyMass,foldReceipts]
  | succ n ih =>
      have hh := congrArg (fun z : ℝ≥0∞ => (weight D (row h) (ys 0) : ℝ≥0∞)/D * z)
        (ih (step h (ys 0)) (fun i => ys i.succ))
      simpa only [historyMass,foldReceipts,mul_assoc] using hh

end Orthemology.RationalLaw

namespace Orthemology.RationalLaw.CanonicalBinding
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.RuntimeBinding

abbrev PairHistory := History (Bool × Bool) Bool

def pairSelector (a : ℕ → Bool) : PairHistory → Bool × Bool :=
  pairPolicy false (historyPolicy a) ()

def pairUpdate (a : ℕ → Bool) (h : PairHistory) (y : Bool) : PairHistory := (pairSelector a h,y)::h

def pairRow (σ : Bool) (a : ℕ → Bool) (h : PairHistory) : Fin 3 → Bool :=
  RuntimeBinding.row σ (pairSelector a h).2

def generatedHistory (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) : PairHistory :=
  foldReceipts (pairUpdate a) n [] ys

theorem generatedHistory_snoc (a : ℕ → Bool) (n : ℕ) (ys : Fin (n+1) → Bool) :
    generatedHistory a (n+1) ys =
      (pairSelector a (generatedHistory a n (fun i => ys i.castSucc)),ys (Fin.last n)) ::
        generatedHistory a n (fun i => ys i.castSucc) := foldReceipts_snoc _ _ _ _

theorem generatedHistory_length (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) :
    (generatedHistory a n ys).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [generatedHistory_snoc,List.length_cons,ih]

theorem generatedHistory_injective (a : ℕ → Bool) (n : ℕ) :
    Function.Injective (generatedHistory a n) := by
  induction n with
  | zero => intro ys zs h; exact Subsingleton.elim _ _
  | succ n ih =>
      intro ys zs h
      rw [generatedHistory_snoc,generatedHistory_snoc] at h
      have htail := ih (List.cons.inj h).2
      have hlast := congrArg Prod.snd (List.cons.inj h).1
      funext i
      exact Fin.lastCases hlast (fun j => congrFun htail j) i

theorem generatedHistory_compatible (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) :
    ActionCompatible (fun (_ : Unit) h => pairSelector a h) () (generatedHistory a n ys) := by
  induction n with
  | zero => trivial
  | succ n ih =>
      rw [generatedHistory_snoc]
      exact ⟨ih _,rfl⟩

theorem compatible_generatedHistory (a : ℕ → Bool) (h : PairHistory)
    (hc : ActionCompatible (fun (_ : Unit) h => pairSelector a h) () h) :
    ∃ ys : Fin h.length → Bool, generatedHistory a h.length ys = h := by
  induction h with
  | nil => exact ⟨Fin.elim0,rfl⟩
  | cons ey h ih =>
      obtain ⟨ys,hy⟩ := ih hc.1
      refine ⟨Fin.snoc ys ey.2, ?_⟩
      simp only [List.length_cons]
      rw [generatedHistory_snoc]
      simp only [Fin.snoc_castSucc,Fin.snoc_last,hy]
      congr 1
      exact Prod.ext hc.2 rfl

theorem pair_mass_eq_runtime (σ : Bool) (a : ℕ → Bool) (n : ℕ) (h : PairHistory) (ys : Fin n → Bool) :
    historyMass 3 (pairRow σ a) (pairUpdate a) n h ys =
      historyMass 3 (adaptiveRow σ a) (RuntimeBinding.update a) n (erasePairSources h) ys := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
      simp only [historyMass]
      rw [ih]
      rfl

theorem generatedHistory_likelihood (σ : Bool) (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) :
    RowLikelihood (realRows Orthemology.RuntimeBridge.Controller.Fixture.kernel σ) (generatedHistory a n ys) =
      historyMass 3 (adaptiveRow σ a) (RuntimeBinding.update a) n [] ys := by
  have hh : RowLikelihood (realRows Orthemology.RuntimeBridge.Controller.Fixture.kernel σ)
      (generatedHistory a n ys) = historyMass 3 (pairRow σ a) (pairUpdate a) n [] ys := by
    induction n with
    | zero => simp [generatedHistory,foldReceipts,RowLikelihood,historyMass]
    | succ n ih =>
        rw [generatedHistory_snoc,rowLikelihood_cons,ih,historyMass_snoc]
        rw [mul_comm]
        congr 1
        exact (weight_div_three_eq_kernel σ _ _ _).symm
  exact hh.trans (pair_mass_eq_runtime σ a n [] ys)

end Orthemology.RationalLaw.CanonicalBinding

namespace Orthemology.RationalLaw.CanonicalBinding
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.RuntimeBinding
open Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

attribute [local instance] Classical.propDecidable

noncomputable def canonicalLaw (σ : Bool) (a : ℕ → Bool) : Measure (ℕ → PairHistory) :=
  markovHistoryLaw Orthemology.RuntimeBridge.Controller.Fixture.kernel σ false (historyPolicy a) (Measure.dirac ())

theorem canonicalLaw_marginal (σ : Bool) (a : ℕ → Bool) (n : ℕ) (h : PairHistory) :
    ((canonicalLaw σ a).map (fun H => H n)) {h} =
      if n=h.length then
        (if ActionCompatible (fun (_ : Unit) h => pairSelector a h) () h then 1 else 0) *
        RowLikelihood (realRows Orthemology.RuntimeBridge.Controller.Fixture.kernel σ) h else 0 := by
  classical
  let π := pairPolicy false (historyPolicy a)
  let P := realRows Orthemology.RuntimeBridge.Controller.Fixture.kernel σ
  have hP := realRows_nonnegative Orthemology.RuntimeBridge.Controller.Fixture.kernel σ
  have hN := realRows_normalized Orthemology.RuntimeBridge.Controller.Fixture.kernel σ
  have hπ : Measurable (fun z : Unit × PairHistory => π z.1 z.2) := measurable_of_countable _
  have hm := history_marginal_formula ∅ π hπ (Measure.dirac ()) P P hP hN hP hN
    (by intro q hq; simp at hq) n h
  unfold canonicalLaw markovHistoryLaw observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply n) (historyTrajectory_measurable ∅ π hπ)]
  have hs : MeasurableSet {r : Unit | ActionCompatible π r h} := (Set.toFinite _).measurableSet
  simpa only [Measure.dirac_apply' _ hs,Set.mem_setOf_eq,RowLikelihood] using hm

noncomputable def decodedHistory (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool) (σ : Bool)
    (x : Cantor) (n : ℕ) : PairHistory :=
  generatedHistory a n (fun i => runtimeReceiptPath p σ x i)

theorem decodedHistory_measurable (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool) (σ : Bool) :
    Measurable (decodedHistory p a σ) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable (generatedHistory a n)).comp
    (measurable_pi_lambda _ (fun i : Fin n => (measurable_pi_apply (i : ℕ)).comp (runtimeReceiptPath_measurable p σ)))

/-- The literal complete source receipt path induces exactly the canonical
newest-first full-history marginal at every logical receipt count. -/
theorem decodedHistory_marginal (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (n : ℕ) :
    (fairCantor.map (fun x => decodedHistory p a σ x n)) =
      (canonicalLaw σ a).map (fun H => H n) := by
  classical
  apply Measure.ext_of_singleton
  intro h
  rw [canonicalLaw_marginal]
  have hm : Measurable (fun x => decodedHistory p a σ x n) :=
    (measurable_pi_apply n).comp (decodedHistory_measurable p a σ)
  rw [Measure.map_apply hm (measurableSet_singleton _)]
  by_cases hr : ∃ ys : Fin n → Bool, generatedHistory a n ys = h
  · obtain ⟨ys,rfl⟩ := hr
    have he : (fun x => decodedHistory p a σ x n) ⁻¹' {generatedHistory a n ys} =
        (runtimeReceiptPath p σ) ⁻¹' receiptCylinder n ys := by
      ext x
      simp only [Set.mem_preimage,Set.mem_singleton_iff,decodedHistory,receiptCylinder,Set.mem_setOf_eq]
      constructor
      · intro hh i
        exact congrFun (generatedHistory_injective a n hh) i
      · intro hh
        rw [funext hh]
    rw [he, ← Measure.map_apply (runtimeReceiptPath_measurable p σ) (measurableSet_receiptCylinder n ys),
      runtime_receipt_path_cylinder_probability p a hp, generatedHistory_length,
      if_pos rfl, if_pos (generatedHistory_compatible a n ys),one_mul,generatedHistory_likelihood]
  · have he : (fun x => decodedHistory p a σ x n) ⁻¹' {h} = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro x hx
      exact hr ⟨_,hx⟩
    rw [he,measure_empty]
    by_cases hl : n=h.length
    · subst n
      have hc : ¬ActionCompatible (fun (_ : Unit) h => pairSelector a h) () h := by
        intro hc
        exact hr (compatible_generatedHistory a h hc)
      simp [hc]
    · simp [hl]

end Orthemology.RationalLaw.CanonicalBinding

namespace Orthemology.RationalLaw.CanonicalBinding
open MeasureTheory Set Preorder
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.RuntimeBinding
open Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

theorem generatedHistory_drop (a : ℕ → Bool) (n m : ℕ) (hmn : m ≤ n) (ys : Fin n → Bool) :
    (generatedHistory a n ys).drop (n-m) =
      generatedHistory a m (fun i => ys (Fin.castLE hmn i)) := by
  induction n generalizing m with
  | zero =>
      have hm : m=0 := by omega
      subst m
      rfl
  | succ n ih =>
      by_cases he : m=n+1
      · subst m
        simp
      · have hm : m ≤ n := by omega
        have hs : n+1-m=(n-m)+1 := by omega
        rw [generatedHistory_snoc,hs,List.drop_succ_cons,ih m hm]
        rfl

theorem decodedHistory_prefix_from_last (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (σ : Bool) (x : Cantor) (N : ℕ) :
    frestrictLe N (decodedHistory p a σ x) = reconstructPrefix N (decodedHistory p a σ x N) := by
  funext i
  exact (generatedHistory_drop a N i.val (Finset.mem_Iic.mp i.property)
    (fun j => runtimeReceiptPath p σ x j)).symm

instance canonicalLaw_probability (σ : Bool) (a : ℕ → Bool) : IsProbabilityMeasure (canonicalLaw σ a) := by
  unfold canonicalLaw markovHistoryLaw observedTraceLaw
  exact isProbabilityMeasure_map (historyTrajectory_measurable ∅ _ (measurable_of_countable _)).aemeasurable

theorem canonicalLaw_prefix_from_last (σ : Bool) (a : ℕ → Bool) (N : ℕ) :
    (canonicalLaw σ a).map (frestrictLe N) =
      ((canonicalLaw σ a).map (fun H => H N)).map (reconstructPrefix N) := by
  unfold canonicalLaw markovHistoryLaw
  rw [observed_prefix_map_from_last ∅ _ (measurable_of_countable _)]
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply N) (historyTrajectory_measurable ∅ _ (measurable_of_countable _))]
  rfl

/-- Complete equality with the retained canonical Markov newest-first history
path law. It is derived from original fair-bit cylinders and actual source output. -/
theorem actual_runtime_canonical_history_law (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) :
    fairCantor.map (decodedHistory p a σ) =
      markovHistoryLaw Orthemology.RuntimeBridge.Controller.Fixture.kernel σ false (historyPolicy a) (Measure.dirac ()) := by
  change fairCantor.map (decodedHistory p a σ) = canonicalLaw σ a
  apply measure_eq_of_prefix_maps
  intro N
  rw [canonicalLaw_prefix_from_last]
  have hm : Measurable (fun x => decodedHistory p a σ x N) :=
    (measurable_pi_apply N).comp (decodedHistory_measurable p a σ)
  rw [← decodedHistory_marginal p a hp σ N]
  rw [Measure.map_map (measurable_frestrictLe N) (decodedHistory_measurable p a σ),
    Measure.map_map (measurable_of_countable (reconstructPrefix (A := Bool × Bool) (Y := Bool) N)) hm]
  congr 1
  funext x
  exact decodedHistory_prefix_from_last p a σ x N

end Orthemology.RationalLaw.CanonicalBinding

namespace Orthemology.RationalLaw.CanonicalBinding
open MeasureTheory Set
open Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.RuntimeBinding
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic
open P02A2.Q8Measure (fairCantor)

/-- Read acknowledgments and values from the physical output stream itself. -/
def physicalProposals (z : Cantor) (k : ℕ) : Option Bool :=
  if z (8*k+4) then some (z (8*k+7)) else none

theorem physicalProposals_event_measurable (k : ℕ) (y : Option Bool) :
    MeasurableSet {z : Cantor | physicalProposals z k = y} := by
  have hm : Measurable (fun z : Cantor => (z (8*k+4),z (8*k+7))) :=
    (measurable_pi_apply _).prodMk (measurable_pi_apply _)
  exact hm ((Set.toFinite {b : Bool × Bool | (if b.1 then some b.2 else none) = y}).measurableSet)

/-- Common decoder for both hidden models. It takes only the physical output
stream and the common history policy, not the hidden model or input tape. -/
noncomputable def canonicalHistoryDecoder (a : ℕ → Bool) (z : Cantor) (n : ℕ) : PairHistory :=
  generatedHistory a n (fun i => decodeReports (physicalProposals z) i)

theorem canonicalHistoryDecoder_measurable (a : ℕ → Bool) : Measurable (canonicalHistoryDecoder a) := by
  have hm := measurable_decodeReports physicalProposals physicalProposals_event_measurable
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable (generatedHistory a n)).comp
    (measurable_pi_lambda _ (fun i : Fin n => (measurable_pi_apply (i : ℕ)).comp hm))

theorem canonicalHistoryDecoder_on_runtime (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool) (σ : Bool) :
    (canonicalHistoryDecoder a) ∘ Indexed.runtimeOutput (runtimeIndex p σ) = decodedHistory p a σ := rfl

/-- The actual physical P02 law, under a common measurable output-only history
readout, equals the exact retained complete canonical Markov history law. -/
theorem physical_runtime_projected_canonical_law (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) :
    (fairCantor.map (Indexed.runtimeOutput (runtimeIndex p σ))).map (canonicalHistoryDecoder a) =
      markovHistoryLaw Orthemology.RuntimeBridge.Controller.Fixture.kernel σ false (historyPolicy a) (Measure.dirac ()) := by
  rw [Measure.map_map (canonicalHistoryDecoder_measurable a) (Indexed.runtime_output_measurable _),
    canonicalHistoryDecoder_on_runtime]
  exact actual_runtime_canonical_history_law p a hp σ

end Orthemology.RationalLaw.CanonicalBinding
