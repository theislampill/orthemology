import HiddenChangeTaggedLaw
import RationalTest

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped BigOperators ENNReal Topology
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical HiddenParity.Sufficiency

namespace HiddenChange
variable {n k : ℕ} {R : Type*}

theorem actionCount_append (e : Pair n k) (tail pre : PairHistory n k) :
    actionCount e (tail ++ pre) = actionCount e tail + actionCount e pre := by
  simp [actionCount, List.countP_append]

theorem historySymbolMass_append (e : Pair n k) (y : State n) (tail pre : PairHistory n k) :
    historySymbolMass e y (tail ++ pre) =
      historySymbolMass e y tail + historySymbolMass e y pre := by
  simp [historySymbolMass]

/-- Adding fixed finite numerator and denominator offsets preserves a ratio
limit when the natural denominator diverges. No bounded-count claim is made. -/
theorem ratio_tendsto_finite_offsets (a : ℕ → ℝ) (b : ℕ → ℕ) (A : ℝ) (B : ℕ) (p : ℝ)
    (hb : Tendsto b atTop atTop)
    (hf : Tendsto (fun t => a t / (b t : ℝ)) atTop (𝓝 p)) :
    Tendsto (fun t => (a t + A) / ((b t : ℝ) + B)) atTop (𝓝 p) := by
  have hA := (tendsto_const_div_atTop_nhds_zero_nat A).comp hb
  have hB := (tendsto_const_div_atTop_nhds_zero_nat (B : ℝ)).comp hb
  have hlim := (hf.add hA).div (tendsto_const_nhds.add hB) (by norm_num : (1 : ℝ) + 0 ≠ 0)
  simp only [add_zero, div_one] at hlim
  apply hlim.congr'
  filter_upwards [hb.eventually (eventually_gt_atTop 0)] with t ht
  have hbt : (b t : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt ht)
  have hsum : (b t : ℝ) + B ≠ 0 := by positivity
  field_simp


open OrthemicCertificate.Direct

theorem symbolCount_append (e : Pair n k) (y : State n) (tail pre : PairHistory n k) :
    symbolCount e y (tail ++ pre) = symbolCount e y tail + symbolCount e y pre := by
  induction tail with
  | nil => simp [symbolCount]
  | cons z tail ih => simp only [List.cons_append, symbolCount, ih]; omega

variable [NeZero n]

theorem historyFrequency_tendsto_append (e : Pair n k) (y : State n)
    (pre : PairHistory n k) (H : ℕ → PairHistory n k) (p : ℝ)
    (hcount : Tendsto (fun t => actionCount e (H t)) atTop atTop)
    (hfreq : Tendsto (fun t => historyFrequency e y (H t)) atTop (𝓝 p)) :
    Tendsto (fun t => historyFrequency e y (H t ++ pre)) atTop (𝓝 p) := by
  simpa only [historyFrequency, historySymbolMass_append, actionCount_append, Nat.cast_add]
    using ratio_tendsto_finite_offsets (fun t => historySymbolMass e y (H t))
      (fun t => actionCount e (H t)) (historySymbolMass e y pre)
      (actionCount e pre) p hcount hfreq

/-- A deterministic bridge with the exact all-time strict gate. Earlier times
are covered by length, bounded rows by their finite bound, and only divergent
rows invoke their limits. -/
theorem uniform_true_gate_of_pairwise_limits
    (I : Input n k) (hI : I.Valid) (σ : Mode) (δ : ℝ) (hδ : 0 < δ)
    (H : ℕ → PairHistory n k) (hlen : ∀ t, (H t).length = t)
    (hcounts : ∀ e, (∃ B : ℕ, ∀ t, actionCount e (H t) ≤ B) ∨
      Tendsto (fun t => actionCount e (H t)) atTop atTop)
    (hfreq : ∀ e, Tendsto (fun t => actionCount e (H t)) atTop atTop →
      ∀ y, Tendsto (fun t => historyFrequency e y (H t)) atTop
        (𝓝 (realRows (I.kernel hI) σ e y))) :
    ∃ K : ℕ, ∀ r, K ≤ r → ∀ t,
      empiricalReject (I.kernel hI) δ σ r (H t) = false := by
  classical
  have hlocal : ∀ e : Pair n k, ∃ K : ℕ, ∀ r, K ≤ r → ∀ t y,
      r < actionCount e (H t) →
      |historyFrequency e y (H t) - realRows (I.kernel hI) σ e y| < δ := by
    intro e
    rcases hcounts e with ⟨B,hB⟩ | hc
    · exact ⟨B, fun r hr t y ht => False.elim (by have := hB t; omega)⟩
    · have hall : ∀ᶠ t in atTop, ∀ y,
          |historyFrequency e y (H t) - realRows (I.kernel hI) σ e y| < δ := by
        apply Filter.eventually_all.mpr
        intro y
        have hd := ((hfreq e hc y).sub (tendsto_const_nhds (x := realRows (I.kernel hI) σ e y))).abs
        simpa using hd.eventually (eventually_lt_nhds (by simpa using hδ))
      obtain ⟨T,hT⟩ := eventually_atTop.mp hall
      refine ⟨T, fun r hr t y ht => ?_⟩
      apply hT t _ y
      have hle : actionCount e (H t) ≤ t := by
        exact (List.countP_le_length).trans (hlen t).le
      omega
  choose K hK using hlocal
  refine ⟨Finset.univ.sup K, fun r hr t => ?_⟩
  apply Bool.eq_false_iff.mpr
  intro hbad
  obtain ⟨e,y,hc,hd⟩ := (empiricalReject_iff _ _ _ _ _).mp hbad
  have he : K e ≤ r := (Finset.le_sup (f := K) (Finset.mem_univ e)).trans hr
  exact not_le_of_gt (hK e r he t y hc) hd

/-- Observations with a tag other than the chosen final mode. This list is
used only in proofs; it is not exposed to the controller. -/
def otherHistory (σ : Mode) (h : TaggedHistory n k) : PairHistory n k :=
  eraseMode (h.filter (fun z => z.1.1 ≠ σ))

theorem actionCount_eraseMode (σ : Mode) (e : Pair n k) (h : TaggedHistory n k) :
    actionCount e (eraseMode h) = actionCount (σ,e) h + actionCount e (otherHistory σ h) := by
  induction h with
  | nil => simp [eraseMode, otherHistory, actionCount]
  | cons z h ih =>
    rcases z with ⟨⟨τ,f⟩,y⟩
    by_cases ht : τ = σ <;> by_cases he : f = e <;>
      simp [otherHistory, eraseMode, actionCount_cons, ht, he, Prod.mk.injEq] at ih ⊢ <;> omega

theorem historySymbolMass_eraseMode (σ : Mode) (e : Pair n k) (y : State n)
    (h : TaggedHistory n k) :
    historySymbolMass e y (eraseMode h) = historySymbolMass (σ,e) y h +
      historySymbolMass e y (otherHistory σ h) := by
  induction h with
  | nil => simp [eraseMode, otherHistory]
  | cons z h ih =>
    rcases z with ⟨⟨τ,f⟩,w⟩
    by_cases ht : τ = σ <;> by_cases he : f = e <;>
      simp [otherHistory, eraseMode, historySymbolMass_cons, ht, he, Prod.mk.injEq] at ih ⊢ <;>
      linarith

theorem fixed_stack_tag (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (t : ℕ) :
    (stackActionTrajectory (fixedPolicy κ s π) z t).1 = fixedMode κ t := by
  change fixedMode κ (stackHistoryTrajectory (fixedPolicy κ s π) z t).length = fixedMode κ t
  congr 1
  exact observedHistory_length _ _ _ _ _ _

theorem otherHistory_fixed_after (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (σ : Mode) (N : ℕ)
    (hconstant : ∀ t, N ≤ t → fixedMode κ t = σ) (t : ℕ) (ht : N ≤ t) :
    otherHistory σ (stackHistoryTrajectory (fixedPolicy κ s π) z t) =
      otherHistory σ (stackHistoryTrajectory (fixedPolicy κ s π) z N) := by
  induction t, ht using Nat.le_induction with
  | base => rfl
  | succ t ht ih =>
    rw [stackHistoryTrajectory_succ_receipt]
    have hg : (stackActionTrajectory (fixedPolicy κ s π) z t).1 = σ :=
      (fixed_stack_tag κ s π z t).trans (hconstant t ht)
    simpa only [otherHistory, List.filter_cons, hg, ne_eq, not_true_eq_false,
      decide_false, Bool.false_eq_true, ↓reduceIte] using ih

/-- Every monotone natural count either has a uniform finite bound or diverges.
This is a pathwise dichotomy, not a probabilistic conditioning step. -/
theorem monotone_count_dichotomy (c : ℕ → ℕ) (hc : Monotone c) :
    (∃ B : ℕ, ∀ t, c t ≤ B) ∨ Tendsto c atTop atTop := by
  by_cases hb : ∃ B : ℕ, ∀ t, c t ≤ B
  · exact Or.inl hb
  · right
    apply hc.tendsto_atTop_atTop
    intro B
    push_neg at hb
    obtain ⟨t,ht⟩ := hb B
    exact ⟨t,ht.le⟩

theorem physical_stack_count_mono (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (e : Pair n k) :
    Monotone (fun t => actionCount e (eraseMode
      (stackHistoryTrajectory (fixedPolicy κ s π) z t))) := by
  apply monotone_nat_of_le_succ
  intro t
  rw [stackHistoryTrajectory_succ_receipt, eraseMode_cons, actionCount_cons]
  split_ifs <;> omega

/-- Pathwise finite-contamination transfer from the actual final-tag tape.
The only convergence premise concerns a deterministic raw tape frequency. -/
theorem fixed_stack_frequency_tendsto (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (σ : Mode) (N : ℕ)
    (hconstant : ∀ t, N ≤ t → fixedMode κ t = σ) (e : Pair n k) (y : State n) (p : ℝ)
    (hraw : Tendsto (fun j => rawFrequency (σ,e) y j z) atTop (𝓝 p))
    (hcount : Tendsto (fun t => actionCount e (eraseMode
      (stackHistoryTrajectory (fixedPolicy κ s π) z t))) atTop atTop) :
    Tendsto (fun t => historyFrequency e y (eraseMode
      (stackHistoryTrajectory (fixedPolicy κ s π) z t))) atTop (𝓝 p) := by
  let H := stackHistoryTrajectory (fixedPolicy κ s π) z
  let pre := otherHistory σ (H N)
  have hc : Tendsto (fun t => actionCount (σ,e) (H t)) atTop atTop := by
    apply ((tendsto_sub_atTop_nat (actionCount e pre)).comp hcount).congr'
    filter_upwards [eventually_ge_atTop N] with t ht
    have he := actionCount_eraseMode σ e (H t)
    have ho := otherHistory_fixed_after κ s π z σ N hconstant t ht
    change otherHistory σ (H t) = pre at ho
    rw [ho] at he
    dsimp only [Function.comp_def]
    change actionCount e (eraseMode (H t)) - actionCount e pre = _
    omega
  have hf : Tendsto (fun t => historyFrequency (σ,e) y (H t)) atTop (𝓝 p) := by
    simpa only [H, historyFrequency_eq_rawFrequency] using hraw.comp hc
  have hl := ratio_tendsto_finite_offsets (fun t => historySymbolMass (σ,e) y (H t))
    (fun t => actionCount (σ,e) (H t)) (historySymbolMass e y pre)
    (actionCount e pre) p hc hf
  apply hl.congr'
  filter_upwards [eventually_ge_atTop N] with t ht
  have ho := otherHistory_fixed_after κ s π z σ N hconstant t ht
  change otherHistory σ (H t) = pre at ho
  change _ = historyFrequency e y (eraseMode (H t))
  rw [historyFrequency, historySymbolMass_eraseMode σ, actionCount_eraseMode σ, ho, Nat.cast_add]

theorem fixed_eventually_final (κ : ChangeIndex) :
    ∃ N : ℕ, ∀ t, N ≤ t → fixedMode κ t = finalMode κ := by
  cases κ with
  | none => exact ⟨0, fun _ _ => rfl⟩
  | some N => exact ⟨N, fun t ht => by simp [fixedMode, finalMode, Nat.not_lt.mpr ht]⟩

/-- The strict true-row gate holds under the constructed actual one-change
law, for the unchanged arbitrary private-seed policy. The raw strong law is
inherited and applied to the finite tagged stack; it is not an endpoint premise. -/
theorem fixed_law_true_gate [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (δ : ℝ) (hδ : 0 < δ) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π,
      ∃ K : ℕ, ∀ r, K ≤ r → ∀ t,
        empiricalReject (I.kernel hI) δ (finalMode κ) r (eraseMode (H t)) = false := by
  rw [fixedLaw_eq_stack I hI κ s ρ π hπ]
  have hm : MeasurableSet {H : TaggedTrace n k | ∃ K : ℕ, ∀ r, K ≤ r → ∀ t,
      empiricalReject (I.kernel hI) δ (finalMode κ) r (eraseMode (H t)) = false} := by
    simp only [Set.setOf_exists, Set.setOf_forall]
    exact MeasurableSet.iUnion (fun K => MeasurableSet.iInter (fun r =>
      MeasurableSet.iInter (fun _ => MeasurableSet.iInter (fun t =>
        ((measurable_of_countable (fun h : TaggedHistory n k =>
          empiricalReject (I.kernel hI) δ (finalMode κ) r (eraseMode h))).comp
          (measurable_pi_apply t)) (measurableSet_singleton false)))))
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)] with z hz
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  apply uniform_true_gate_of_pairwise_limits I hI (finalMode κ) δ hδ
    (fun t => eraseMode (stackHistoryTrajectory (fixedPolicy κ s π) z t))
  · intro t
    rw [eraseMode_length]
    exact observedHistory_length _ _ _ _ _ _
  · intro e
    exact monotone_count_dichotomy _ (physical_stack_count_mono κ s π z e)
  · intro e he y
    exact fixed_stack_frequency_tendsto κ s π z (finalMode κ) N hN e y
      (taggedRows I (finalMode κ,e) y) (hz (finalMode κ,e) y) he

/-- Actual fixed-schedule consistency is asserted only on divergent physical
counts. Finitely sampled rows are deliberately excluded. -/
theorem fixed_law_frequencies_tendsto [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π, ∀ e : Pair n k,
      Tendsto (fun t => actionCount e (eraseMode (H t))) atTop atTop →
      ∀ y, Tendsto (fun t => historyFrequency e y (eraseMode (H t))) atTop
        (𝓝 (realRows (I.kernel hI) (finalMode κ) e y)) := by
  rw [fixedLaw_eq_stack I hI κ s ρ π hπ]
  have hm : MeasurableSet {H : TaggedTrace n k | ∀ e : Pair n k,
      Tendsto (fun t => actionCount e (eraseMode (H t))) atTop atTop →
      ∀ y, Tendsto (fun t => historyFrequency e y (eraseMode (H t))) atTop
        (𝓝 (realRows (I.kernel hI) (finalMode κ) e y))} := by
    simp only [imp_iff_not_or, Set.setOf_forall, Set.setOf_or]
    apply MeasurableSet.iInter
    intro e
    apply MeasurableSet.union
    · exact (measurableSet_tendsto atTop (fun t =>
        (measurable_of_countable (fun h : TaggedHistory n k => actionCount e (eraseMode h))).comp
          (measurable_pi_apply t))).compl
    · apply MeasurableSet.iInter
      intro y
      exact measurableSet_tendsto (𝓝 (realRows (I.kernel hI) (finalMode κ) e y)) (fun t =>
        (measurable_of_countable (fun h : TaggedHistory n k => historyFrequency e y (eraseMode h))).comp
          (measurable_pi_apply t))
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  filter_upwards [seeded_all_rawFrequencies_tendsto ρ (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)] with z hz
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  intro e he y
  exact fixed_stack_frequency_tendsto κ s π z (finalMode κ) N hN e y
    (taggedRows I (finalMode κ,e) y) (hz (finalMode κ,e) y) he

/-- A separated recurrent wrong row triggers the literal test eventually at
any fixed phase. Discrepancy equality is rejected by the same test. -/
theorem empiricalReject_eventually_of_separated_limit
    (I : Input n k) (hI : I.Valid) (θ : Mode) (δ : ℝ)
    (H : ℕ → PairHistory n k) (e : Pair n k) (y : State n) (p : ℝ) (r : ℕ)
    (hc : Tendsto (fun t => actionCount e (H t)) atTop atTop)
    (hf : Tendsto (fun t => historyFrequency e y (H t)) atTop (𝓝 p))
    (hsep : δ < |p - realRows (I.kernel hI) θ e y|) :
    ∀ᶠ t in atTop, empiricalReject (I.kernel hI) δ θ r (H t) = true := by
  have hd := (hf.sub (tendsto_const_nhds (x := realRows (I.kernel hI) θ e y))).abs
  filter_upwards [hc.eventually (eventually_gt_atTop r),
    hd.eventually (eventually_gt_nhds hsep)] with t ht hd
  exact (empiricalReject_iff _ _ _ _ _).mpr ⟨e,y,ht,hd.le⟩

theorem fixed_law_wrong_row_eventually_rejected [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π, ∀ e : Pair n k,
      Tendsto (fun t => actionCount e (eraseMode (H t))) atTop atTop →
      ∀ θ y δ, δ < |realRows (I.kernel hI) (finalMode κ) e y - realRows (I.kernel hI) θ e y| →
      ∀ r, ∀ᶠ t in atTop,
        empiricalReject (I.kernel hI) δ θ r (eraseMode (H t)) = true := by
  filter_upwards [fixed_law_frequencies_tendsto I hI κ s ρ π hπ] with H hH
  intro e he θ y δ hsep r
  exact empiricalReject_eventually_of_separated_limit I hI θ δ (fun t => eraseMode (H t))
    e y _ r he (hH e he y) hsep

theorem physical_stack_action (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (d : Pair n k) (t : ℕ) :
    historyAction d (eraseModeTrace (stackHistoryTrajectory (fixedPolicy κ s π) z)) t =
      (stackActionTrajectory (fixedPolicy κ s π) z t).2 := by
  unfold historyAction eraseModeTrace
  rw [stackHistoryTrajectory_succ_receipt, eraseMode_cons]
  rfl

theorem fixed_stack_source_next (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (t : ℕ) :
    (stackActionTrajectory (fixedPolicy κ s π) z (t+1)).2.1 =
      stackReceipt (fixedPolicy κ s π) z t := by
  change currentState s (eraseMode (stackHistoryTrajectory (fixedPolicy κ s π) z (t+1))) = _
  rw [stackHistoryTrajectory_succ_receipt, eraseMode_cons]
  rfl

theorem fixed_stack_positive_successors_recur (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : R × FlatStack (TaggedPair n k) (State n)) (d : Pair n k)
    (hTape : ∀ g y, 0 < taggedRows I g y → ∃ᶠ j in atTop, z.2 (g,j) = y) :
    ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace
        (stackHistoryTrajectory (fixedPolicy κ s π) z)) t = e) →
      ∀ y, 0 < I.row (finalMode κ) e y →
      ∃ᶠ t in atTop, historyAction d (eraseModeTrace
        (stackHistoryTrajectory (fixedPolicy κ s π) z)) t = e ∧
        (historyAction d (eraseModeTrace
          (stackHistoryTrajectory (fixedPolicy κ s π) z)) (t+1)).1 = y := by
  intro e he y hy
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  have hr : ∃ᶠ t in atTop, stackActionTrajectory (fixedPolicy κ s π) z t = (finalMode κ,e) := by
    apply frequently_atTop.mpr
    intro L
    obtain ⟨t,ht,he⟩ := frequently_atTop.mp he (max N L)
    refine ⟨t, (le_max_right N L).trans ht, ?_⟩
    apply Prod.ext
    · exact (fixed_stack_tag κ s π z t).trans (hN t ((le_max_left N L).trans ht))
    · simpa only [physical_stack_action] using he
  have hpos : 0 < taggedRows I (finalMode κ,e) y := by
    change (0 : ℝ) < (I.row (finalMode κ) e y : ℝ)
    exact_mod_cast hy
  have hb := recurrent_action_observes_recurrent_symbol (fixedPolicy κ s π) z
    (finalMode κ,e) y hr (hTape _ y hpos)
  exact hb.mono (fun t ht => by
    simp only [physical_stack_action, fixed_stack_source_next]
    exact ⟨congrArg Prod.snd ht.1,ht.2⟩)

/-- Every positive final-row successor of a physically recurrent pair occurs
infinitely often, under the actual fixed law and the unchanged private policy. -/
theorem fixed_law_positive_successors_recur [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π, ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e) →
      ∀ y, 0 < I.row (finalMode κ) e y →
      ∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e ∧
        (historyAction d (eraseModeTrace H) (t+1)).1 = y := by
  rw [fixedLaw_eq_stack I hI κ s ρ π hπ]
  have ha : ∀ t, Measurable (fun H : TaggedTrace n k => historyAction d (eraseModeTrace H) t) := by
    intro t
    exact (measurable_of_countable (fun h : TaggedHistory n k =>
      ((eraseMode h).headD (d,default)).1)).comp (measurable_pi_apply (t+1))
  have hm : MeasurableSet {H : TaggedTrace n k | ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e) →
      ∀ y, 0 < I.row (finalMode κ) e y →
      ∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e ∧
        (historyAction d (eraseModeTrace H) (t+1)).1 = y} := by
    simp only [imp_iff_not_or, Set.setOf_forall, Set.setOf_or]
    apply MeasurableSet.iInter
    intro e
    apply MeasurableSet.union
    · exact (Orthemology.Tranche2.RecurrentSupport.measurable_recurrence _ ha e).compl
    · apply MeasurableSet.iInter
      intro y
      apply MeasurableSet.union
      · exact MeasurableSet.iInter (fun _ => MeasurableSet.const False)
      · have hrec := Orthemology.Tranche2.RecurrentSupport.measurable_recurrence
          (fun H t => (historyAction d (eraseModeTrace H) t,
            (historyAction d (eraseModeTrace H) (t+1)).1))
          (fun t => (ha t).prodMk (ha (t+1)).fst) (e,y)
        simpa only [Orthemology.Tranche2.RecurrentSupport.Recurs, Prod.mk.injEq] using hrec
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  filter_upwards [seeded_all_tapes_recurrent ρ (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)] with z hz
  exact fixed_stack_positive_successors_recur I hI κ s π z d hz

theorem physical_stack_recurrent_count_tendsto (κ : ChangeIndex) (s : State n)
    (π : Policy R n k) (z : R × FlatStack (TaggedPair n k) (State n))
    (d e : Pair n k)
    (he : ∃ᶠ t in atTop, historyAction d (eraseModeTrace
      (stackHistoryTrajectory (fixedPolicy κ s π) z)) t = e) :
    Tendsto (fun t => actionCount e (eraseMode
      (stackHistoryTrajectory (fixedPolicy κ s π) z t))) atTop atTop := by
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  have hr : ∃ᶠ t in atTop, stackActionTrajectory (fixedPolicy κ s π) z t = (finalMode κ,e) := by
    apply frequently_atTop.mpr
    intro L
    obtain ⟨t,ht,he⟩ := frequently_atTop.mp he (max N L)
    refine ⟨t, (le_max_right N L).trans ht, ?_⟩
    apply Prod.ext
    · exact (fixed_stack_tag κ s π z t).trans (hN t ((le_max_left N L).trans ht))
    · simpa only [physical_stack_action] using he
  apply tendsto_atTop_mono _ (recurrent_count_tendsto (fixedPolicy κ s π) z (finalMode κ,e) hr)
  intro t
  rw [actionCount_eraseMode (finalMode κ)]
  exact Nat.le_add_right _ _

theorem fixed_law_recurrent_counts [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π, ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e) →
      Tendsto (fun t => actionCount e (eraseMode (H t))) atTop atTop := by
  rw [fixedLaw_eq_stack I hI κ s ρ π hπ]
  have hm : MeasurableSet {H : TaggedTrace n k | ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e) →
      Tendsto (fun t => actionCount e (eraseMode (H t))) atTop atTop} := by
    simp only [imp_iff_not_or, Set.setOf_forall, Set.setOf_or]
    apply MeasurableSet.iInter
    intro e
    apply MeasurableSet.union
    · apply MeasurableSet.compl
      exact Orthemology.Tranche2.RecurrentSupport.measurable_recurrence _ (fun t =>
        (measurable_of_countable (fun h : TaggedHistory n k =>
          ((eraseMode h).headD (d,default)).1)).comp (measurable_pi_apply (t+1))) e
    · exact measurableSet_tendsto atTop (fun t =>
        (measurable_of_countable (fun h : TaggedHistory n k => actionCount e (eraseMode h))).comp
          (measurable_pi_apply t))
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  exact ae_of_all _ (fun z e he => physical_stack_recurrent_count_tendsto κ s π z d e he)

/-- Literal rational tolerance corollary for every recurrent unequal row;
complete numerical row inequality is used, not a support-only comparison. -/
theorem fixed_law_rational_wrong_row_eventually_rejected [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π, ∀ e : Pair n k,
      (∃ᶠ t in atTop, historyAction d (eraseModeTrace H) t = e) →
      ∀ θ, I.row θ e ≠ I.row (finalMode κ) e →
      ∀ r, ∀ᶠ t in atTop,
        rationalReject I (tolerance I Finset.univ) θ r (eraseMode (H t)) = true := by
  filter_upwards [fixed_law_wrong_row_eventually_rejected I hI κ s ρ π hπ,
    fixed_law_recurrent_counts I hI κ s ρ π hπ d] with H hH hc
  intro e he θ hrow r
  obtain ⟨y,hy⟩ := tolerance_real_separates I hI Finset.univ (finalMode κ)
    (Finset.mem_univ _) θ (Finset.mem_univ _) e hrow
  have h := hH e (hc e he) θ y (tolerance I Finset.univ) hy r
  simpa only [rationalReject_eq_empiricalReject I hI] using h

/-- The exact executable rational test inherits the same all-time true barrier. -/
theorem fixed_law_rational_true_gate [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedLaw I hI κ s ρ π,
      ∃ K : ℕ, ∀ r, K ≤ r → ∀ t,
        rationalReject I (tolerance I Finset.univ) (finalMode κ) r (eraseMode (H t)) = false := by
  have htol : (0 : ℝ) < (tolerance I Finset.univ : ℝ) := by
    exact_mod_cast tolerance_positive I Finset.univ
  simpa only [rationalReject_eq_empiricalReject I hI] using
    fixed_law_true_gate I hI κ s ρ π hπ (tolerance I Finset.univ) htol

end HiddenChange
