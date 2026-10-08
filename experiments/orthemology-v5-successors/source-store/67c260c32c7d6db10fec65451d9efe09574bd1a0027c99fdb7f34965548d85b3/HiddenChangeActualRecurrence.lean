import HiddenChangeKnownProgress
import HiddenChangeContamination

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

/-- Actual next sources and governing-row edges, derived from positive finite
prefix weights. Pre-change edges are never asserted to be P1-supported. -/
theorem fixedPhysicalLaw_supported_path (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      (∀ t, (historyAction d H t).1 = currentState s (H t)) ∧
      (historyAction d H 0).1 = s ∧
      ∀ t, 0 < I.row (fixedMode κ t) (historyAction d H t) (historyAction d H (t+1)).1 := by
  filter_upwards [fixedPhysicalLaw_positive_prefixes I hI κ s ρ π hπ,
    fixedPhysicalLaw_coherent I hI κ s ρ π hπ,
    fixedPhysicalLaw_selected I hI κ s ρ π hπ d] with H hp hc hsel
  have hs : ∀ t, (historyAction d H t).1 = currentState s (H t) :=
    fun t => selected_source s ρ π _ _ (hsel t)
  refine ⟨hs,?_,?_⟩
  · simpa only [hc.1,currentState] using hs 0
  · intro t
    obtain ⟨e,y,he⟩ := hc.2 t
    have hp' := ((positive_prefix_factors I hI κ s ρ π hπ _).mp (hp (t+1))).2
    rw [he,fixedPrefixLikelihood_cons] at hp'
    have hrow := (ENNReal.mul_pos_iff.mp hp').1
    rw [ENNReal.ofReal_pos] at hrow
    have ha : historyAction d H t = e := by simp [historyAction,he]
    have hy : (historyAction d H (t+1)).1 = y := by simpa only [he,currentState] using hs (t+1)
    rw [ha,hy]
    rw [coherentTrace_length hc t] at hrow
    exact_mod_cast hrow

omit [NeZero n] in
/-- Finite initial unsupported edges do not change the recurrent graph theorem.
This is a deterministic adaptation of the retained finite graph argument. -/
theorem recurrent_component_of_eventual_support
    (σ : Mode) (I : Input n k) (x : ℕ → Pair n k) (N : ℕ)
    (hstep : ∀ t, N ≤ t → (x (t+1)).1 ∈ succ I σ (x t))
    (hrecur : ∀ e ∈ recurrentSet x, ∀ y ∈ succ I σ e,
      ∃ᶠ t in atTop, x t = e ∧ (x (t+1)).1 = y) :
    IsEndComponent Prod.fst (succ I σ) (recurrentSet x) := by
  obtain ⟨M,hM⟩ := eventually_atTop.mp (eventually_mem_recurrentSet x)
  refine ⟨recurrentSet_nonempty x,?_,?_,?_⟩
  · intro e he
    obtain ⟨t,ht,heq⟩ := frequently_atTop.mp ((mem_recurrentSet x e).mp he) N
    exact ⟨(x (t+1)).1,by simpa only [heq] using hstep t ht⟩
  · intro e he y hy
    obtain ⟨t,ht,_,heq⟩ := frequently_atTop.mp (hrecur e he y hy) M
    exact Finset.mem_image.mpr ⟨x (t+1),hM (t+1) (by omega),heq⟩
  · intro s hs t ht
    obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hs
    obtain ⟨f,hf,hft⟩ := Finset.mem_image.mp ht
    obtain ⟨a,ha,hea⟩ := frequently_atTop.mp ((mem_recurrentSet x e).mp he) (max M N)
    obtain ⟨b,hab,hfb⟩ := frequently_atTop.mp ((mem_recurrentSet x f).mp hf) a
    have hpath : Reach Prod.fst (succ I σ) (recurrentSet x) (x a).1 (x b).1 := by
      clear hfb
      induction b,hab using Nat.le_induction with
      | base => exact Relation.ReflTransGen.refl
      | succ j hj ih =>
        exact ih.tail ⟨x j,hM j (by omega),rfl,hstep j (by omega)⟩
    simpa only [hea,hfb,hes,hft] using hpath

def PositiveSuccessorsRecur (I : Input n k) (σ : Mode) (d : Pair n k) (H : PairTrace n k) : Prop :=
  ∀ e : Pair n k, Recurs (historyAction d H) e → ∀ y, 0 < I.row σ e y →
    ∃ᶠ t in atTop, historyAction d H t = e ∧ (historyAction d H (t+1)).1 = y

theorem positiveSuccessorsRecur_measurable (I : Input n k) (σ : Mode) (d : Pair n k) :
    MeasurableSet {H : PairTrace n k | PositiveSuccessorsRecur I σ d H} := by
  have ha : ∀ t, Measurable (fun H : PairTrace n k => historyAction d H t) :=
    fun t => (measurable_pi_apply t).comp (historyAction_measurable d)
  simp only [PositiveSuccessorsRecur,imp_iff_not_or,Set.setOf_forall,Set.setOf_or]
  apply MeasurableSet.iInter
  intro e
  apply MeasurableSet.union
  · exact (measurable_recurrence _ ha e).compl
  · apply MeasurableSet.iInter
    intro y
    apply MeasurableSet.union
    · exact MeasurableSet.iInter (fun _ => MeasurableSet.const False)
    · have hr := measurable_recurrence
        (fun H t => (historyAction d H t,(historyAction d H (t+1)).1))
        (fun t => (ha t).prodMk (ha (t+1)).fst) (e,y)
      simpa only [Recurs,Prod.mk.injEq] using hr

theorem fixedPhysicalLaw_positive_successors (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π, PositiveSuccessorsRecur I (finalMode κ) d H := by
  apply (ae_map_iff eraseModeTrace_measurable.aemeasurable
    (positiveSuccessorsRecur_measurable I (finalMode κ) d)).mpr
  exact fixed_law_positive_successors_recur I hI κ s ρ π hπ d

/-- End-component recurrence for each actual fixed law, including finite
pre-change contamination, is derived from the actual row-tape recurrence. -/
theorem fixedPhysicalLaw_recurrent_component (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k) :
    ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
      IsEndComponent Prod.fst (succ I (finalMode κ)) (recurrentSet (historyAction d H)) := by
  filter_upwards [fixedPhysicalLaw_supported_path I hI κ s ρ π hπ d,
    fixedPhysicalLaw_positive_successors I hI κ s ρ π hπ d] with H hs hr
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  apply recurrent_component_of_eventual_support (finalMode κ) I (historyAction d H) N
  · intro t ht
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _,?_⟩
    simpa only [hN t ht] using hs.2.2 t
  · intro e he y hy
    exact hr e ((mem_recurrentSet _ e).mp he) y (Finset.mem_filter.mp hy).2

end HiddenChange
