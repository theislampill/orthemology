import GeneratedChargeBudget

noncomputable section
namespace HiddenParity.Cost

/-- Progress endpoints before the current action. -/
def progressCount (progress : ℕ → Prop) [DecidablePred progress] (t : ℕ) : ℕ :=
  ((Finset.range t).filter progress).card

/-- Last chronological interval start, retaining physical time while allowing
zero-cost intervals to be skipped by a separate danger predicate. -/
def lastIntervalStart (progress : ℕ → Prop) [DecidablePred progress] : ℕ → ℕ
  | 0 => 0
  | t+1 => if progress t then t+1 else lastIntervalStart progress t

theorem progressCount_succ (progress : ℕ → Prop) [DecidablePred progress] (t : ℕ) :
    progressCount progress (t+1)=progressCount progress t+if progress t then 1 else 0 := by
  simp only [progressCount,Finset.range_add_one,Finset.filter_insert,Finset.mem_filter,Finset.mem_range,lt_self_iff_false,false_and,not_false_eq_true]
  split_ifs  <;> simp_all

theorem progressCount_mono (progress : ℕ → Prop) [DecidablePred progress] : Monotone (progressCount progress) := by
  intro i j hij
  exact Finset.card_le_card (Finset.filter_subset_filter _ (Finset.range_mono hij))

theorem lastIntervalStart_le (progress : ℕ → Prop) [DecidablePred progress] (t : ℕ) :
    lastIntervalStart progress t ≤ t := by
  induction t with
  | zero => rfl
  | succ t ih => dsimp [lastIntervalStart];split_ifs  <;> omega

theorem lastIntervalStart_is_start (progress : ℕ → Prop) [DecidablePred progress] (t : ℕ) :
    lastIntervalStart progress t=0 ∨ progress (lastIntervalStart progress t-1) := by
  induction t with
  | zero => exact Or.inl rfl
  | succ t ih =>
      dsimp [lastIntervalStart]
      split_ifs with h
      · exact Or.inr (by simpa using h)
      · exact ih

theorem no_progress_since_start (progress : ℕ → Prop) [DecidablePred progress] (t : ℕ) :
    ∀ i, lastIntervalStart progress t ≤ i → i < t → ¬progress i := by
  induction t with
  | zero => intro i hi ht;omega
  | succ t ih =>
      dsimp [lastIntervalStart]
      split_ifs with h
      · intro i hi ht;omega
      · intro i hi hit
        by_cases he : i=t
        · simpa only [he] using h
        · exact ih i hi (by omega)

theorem progressCount_eq_implies_same_start (progress : ℕ → Prop) [DecidablePred progress]
    {i j : ℕ} (hij : i ≤ j) (he : progressCount progress i=progressCount progress j) :
    lastIntervalStart progress i=lastIntervalStart progress j := by
  induction j,hij using Nat.le_induction with
  | base => rfl
  | succ j hij ih =>
      have hm := progressCount_mono progress hij
      rw [progressCount_succ] at he
      by_cases hp : progress j
      · simp only [if_pos hp] at he;omega
      · simp only [if_neg hp,add_zero] at he
        simpa only [lastIntervalStart,if_neg hp] using ih he

/-- Chronological index and within-interval offset never identify two action
times. This is deterministic, before any conditional probability argument. -/
theorem chronological_coordinates_injective (progress : ℕ → Prop) [DecidablePred progress] :
    Function.Injective (fun t => (progressCount progress t,t-lastIntervalStart progress t)) := by
  intro i j he
  have hc := congrArg Prod.fst he
  have ht := congrArg Prod.snd he
  dsimp only at hc ht
  have hs : lastIntervalStart progress i=lastIntervalStart progress j := by
    rcases le_total i j with h | h
    · exact progressCount_eq_implies_same_start progress h hc
    · exact (progressCount_eq_implies_same_start progress h hc.symm).symm
  have hi := lastIntervalStart_le progress i
  have hj := lastIntervalStart_le progress j
  omega

theorem lastIntervalStart_eq_self_of_start (progress : ℕ → Prop) [DecidablePred progress]
    (t : ℕ) (hs : t=0 ∨ progress (t-1)) : lastIntervalStart progress t=t := by
  cases t with
  | zero => rfl
  | succ t =>
      have hp : progress t := by simpa using hs
      simp only [lastIntervalStart,if_pos hp]

/-- Two chronological starts at the same progress index coincide. -/
theorem start_eq_of_progressCount_eq (progress : ℕ → Prop) [DecidablePred progress]
    (i j : ℕ) (hi : i=0 ∨ progress (i-1)) (hj : j=0 ∨ progress (j-1))
    (hc : progressCount progress i=progressCount progress j) : i=j := by
  apply chronological_coordinates_injective progress
  simp only [lastIntervalStart_eq_self_of_start progress i hi,
    lastIntervalStart_eq_self_of_start progress j hj,Nat.sub_self,hc]

/-- Endpoint census with the final physical transition included exactly once. -/
def truncatedProgressEnds (progress : ℕ → Prop) [DecidablePred progress] (T : ℕ) : Finset ℕ :=
  (Finset.range T).filter (fun t => t+1=T ∨ progress t)

theorem progressCount_lt_endpoint_card (progress : ℕ → Prop) [DecidablePred progress]
    (t T : ℕ) (ht : t < T) : progressCount progress t  <  (truncatedProgressEnds progress T).card := by
  apply Finset.card_lt_card
  apply Finset.ssubset_iff_subset_ne.mpr
  constructor
  · intro i hi
    obtain ⟨hi,hp⟩ := Finset.mem_filter.mp hi
    exact Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (lt_trans (Finset.mem_range.mp hi) ht),Or.inr hp⟩
  · intro he
    have hm : T-1 ∈ truncatedProgressEnds progress T := Finset.mem_filter.mpr
      ⟨Finset.mem_range.mpr (by omega),Or.inl (by omega)⟩
    rw [← he] at hm
    have hh := Finset.mem_range.mp (Finset.mem_filter.mp hm).1
    omega

/-- If every counted action lies within d steps of its last progress start,
then J bounded endpoint slots cover at most J*d counted actions. -/
theorem chronological_count_bound
    (progress bad : ℕ → Prop) [DecidablePred progress] [DecidablePred bad]
    (T J d : ℕ) (hJ : (truncatedProgressEnds progress T).card ≤ J)
    (hage : ∀ t, t < T → bad t → t-lastIntervalStart progress t < d) :
    ((Finset.range T).filter bad).card ≤ J*d := by
  let f : ((Finset.range T).filter bad) → Fin J × Fin d := fun t =>
    ⟨⟨progressCount progress t,(progressCount_lt_endpoint_card progress t T
      (Finset.mem_range.mp (Finset.mem_filter.mp t.property).1)).trans_le hJ⟩,
     ⟨(t:ℕ)-lastIntervalStart progress t,hage t
       (Finset.mem_range.mp (Finset.mem_filter.mp t.property).1) (Finset.mem_filter.mp t.property).2⟩⟩
  have hf : Function.Injective f := by
    intro i j he
    apply Subtype.ext
    apply chronological_coordinates_injective progress
    exact congrArg (fun p : Fin J × Fin d => (p.1.val,p.2.val)) he
  simpa only [Fintype.card_coe,Fintype.card_prod,Fintype.card_fin] using Fintype.card_le_of_injective f hf

/-- Contrapositive coverage certificate: an excessive actual count yields a
long interval started chronologically, with no progress for its first d steps. -/
theorem long_interval_of_excess_count
    (progress bad : ℕ → Prop) [DecidablePred progress] [DecidablePred bad]
    (T J d : ℕ) (hJ : (truncatedProgressEnds progress T).card ≤ J)
    (hex : J*d < ((Finset.range T).filter bad).card) :
    ∃ t, t < T ∧ bad t ∧ d ≤ t-lastIntervalStart progress t ∧
      (lastIntervalStart progress t=0 ∨ progress (lastIntervalStart progress t-1)) ∧
      ∀ i, lastIntervalStart progress t ≤ i → i < lastIntervalStart progress t+d → ¬progress i := by
  have hnot : ¬∀ t,t < T → bad t → t-lastIntervalStart progress t < d := by
    intro h
    exact (not_lt_of_ge (chronological_count_bound progress bad T J d hJ h)) hex
  push_neg at hnot
  obtain ⟨t,ht,hbad,hage⟩ := hnot
  refine ⟨t,ht,hbad,hage,lastIntervalStart_is_start progress t,?_⟩
  intro i hi hid
  exact no_progress_since_start progress t i hi (by have := lastIntervalStart_le progress t;omega)

end HiddenParity.Cost
