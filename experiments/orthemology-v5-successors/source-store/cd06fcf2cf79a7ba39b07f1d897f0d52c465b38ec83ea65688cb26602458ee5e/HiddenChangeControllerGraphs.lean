import HiddenChangeController
import DirectCycling

/-! Bounded deterministic graph consequences of the submitted body and literal
sorted cycling. All recurrent closure/row-regularity premises are explicit.
This module does not assert an almost-sure controller endpoint. -/
namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open Filter
variable {n k : ℕ}

/-- Exactly the states covered by the submitted ordered component list. -/
def componentTargets (es : List (PairSet n k)) : Region n :=
  es.toFinset.biUnion (usedStates Prod.fst)

@[simp] theorem mem_componentTargets (es : List (PairSet n k)) (s : State n) :
    s ∈ componentTargets es ↔ ∃ E ∈ es, s ∈ usedStates Prod.fst E := by
  simp [componentTargets]

theorem firstContaining_none_iff (s : State n) (es : List (PairSet n k)) :
    firstContaining s es = none ↔ s ∉ componentTargets es := by
  induction es with
  | nil => simp [firstContaining]
  | cons E es ih =>
      by_cases h : s ∈ usedStates Prod.fst E
      · simp [firstContaining, h]
      · simp [firstContaining, h, ih]

theorem uncertainComponents_component_mem (θ : Mode) (os : List (UncertainObligation n k))
    (o : UncertainObligation n k) (ho : o ∈ os) (hc : o.candidate = θ)
    (p : PhysicalPath n k) (E : PairSet n k) (hw : o.witness = .component p E) :
    E ∈ uncertainComponents θ os := by
  induction os with
  | nil => simp at ho
  | cons z os ih =>
      rcases List.mem_cons.mp ho with rfl | ho
      · simp [uncertainComponents, hw, hc]
      · have hi := ih ho
        cases hz : z.witness with
        | component q F =>
            by_cases hc' : z.candidate = θ <;> simp [uncertainComponents, hz, hc', hi]
        | reveal q a y => simpa [uncertainComponents, hz] using hi

/-- Coverage and the submitted path supply reach to an exact known-list target. -/
theorem body_known_target_reach (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (s : State n) (hs : s ∈ c.K) :
    ∃ t ∈ componentTargets (knownComponents c), Reach Prod.fst (succ I 1) c.D1 s t := by
  have hkey : s ∈ (c.known.map KnownObligation.source).toFinset := hc.2.2.2.1.symm ▸ hs
  obtain ⟨o, ho, hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  have hv := hc.2.2.2.2.2.2.1 o ho
  refine ⟨o.route.endpoint, (mem_componentTargets _ _).mpr ?_, ?_⟩
  · exact ⟨o.component, List.mem_map.mpr ⟨o, ho, rfl⟩, hv.2.2.2⟩
  · simpa only [hos] using OrthemicCertificate.Path.valid_sound hv.2.2.1

/-- Exact uncertain-list target reach or a submitted positive candidate edge
whose receipt is impossible in mode 0. There is no live-support deletion. -/
theorem body_uncertain_target_or_revelation_reach (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (θ : Mode) (s : State n) (hs : s ∈ c.W) :
    (∃ t ∈ componentTargets (uncertainComponents θ c.uncertain),
      Reach Prod.fst (internalSucc I θ) c.D s t) ∨
    (∃ e ∈ c.D, ∃ y ∈ c.K, Reach Prod.fst (internalSucc I θ) c.D s e.1 ∧
      0 < I.row θ e y ∧ I.row 0 e y = 0) := by
  have hkey : (s,θ) ∈ (c.uncertain.map uncertainKey).toFinset := by
    rw [hc.2.2.2.2.2.1]
    exact Finset.mem_product.mpr ⟨hs, Finset.mem_univ _⟩
  obtain ⟨o, ho, hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  have hsrc : o.source = s := congrArg Prod.fst hos
  have hcan : o.candidate = θ := congrArg Prod.snd hos
  have hv := hc.2.2.2.2.2.2.2 o ho
  cases hw : o.witness with
  | component p E =>
      simp only [UncertainObligation.Valid, hw] at hv
      refine Or.inl ⟨p.endpoint, (mem_componentTargets _ _).mpr ?_, ?_⟩
      · exact ⟨E, uncertainComponents_component_mem θ _ o ho hcan p E hw, hv.2.2.2⟩
      · simpa only [hsrc,hcan] using OrthemicCertificate.Path.valid_sound hv.2.2.1
  | reveal p a y =>
      simp only [UncertainObligation.Valid, hw] at hv
      refine Or.inr ⟨(p.endpoint,a), hv.2.1, y, hv.2.2.1, ?_, ?_, hv.2.2.2.2⟩
      · simpa only [hsrc,hcan] using OrthemicCertificate.Path.valid_sound hv.1
      · simpa only [hcan] using hv.2.2.2.1

/-- Pure graph propagation; fairness includes every submitted navigation action
at each recurrent source, and closure propagates the submitted path. -/
theorem fair_closed_reachable (D C : PairSet n k) (S : Pair n k → Region n)
    (hClosed : ∀ e ∈ C, S e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ D, e.1 ∈ usedStates Prod.fst C → e ∈ C)
    (s : State n) (hs : s ∈ usedStates Prod.fst C) :
    ∀ t, Reach Prod.fst S D s t → t ∈ usedStates Prod.fst C := by
  intro t ht
  induction ht with
  | refl => exact hs
  | @tail y z hp hyz ih =>
      obtain ⟨e,he,hey,hz⟩ := hyz
      exact hClosed e (hFair e he (by simpa only [hey] using ih)) hz

theorem fair_known_hits_target (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (C : PairSet n k) (hC : C.Nonempty)
    (hRegion : usedStates Prod.fst C ⊆ c.K)
    (hClosed : ∀ e ∈ C, succ I 1 e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ c.D1, e.1 ∈ usedStates Prod.fst C → e ∈ C) :
    ∃ t ∈ componentTargets (knownComponents c), t ∈ usedStates Prod.fst C := by
  obtain ⟨e,he⟩ := hC
  have hs : e.1 ∈ usedStates Prod.fst C := Finset.mem_image.mpr ⟨e,he,rfl⟩
  obtain ⟨t,ht,hpath⟩ := body_known_target_reach I c hc e.1 (hRegion hs)
  exact ⟨t,ht,fair_closed_reachable c.D1 C (succ I 1) hClosed hFair e.1 hs t hpath⟩

/-- A fair candidate-closed recurrent graph hits a submitted target, or contains
a candidate-positive revelation edge. The latter is only a possibility here. -/
theorem fair_uncertain_hits_target_or_revelation (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (θ : Mode) (C : PairSet n k) (hC : C.Nonempty)
    (hRegion : usedStates Prod.fst C ⊆ c.W)
    (hClosed : ∀ e ∈ C, succ I θ e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ c.D, e.1 ∈ usedStates Prod.fst C → e ∈ C) :
    (∃ t ∈ componentTargets (uncertainComponents θ c.uncertain), t ∈ usedStates Prod.fst C) ∨
    (∃ e ∈ C, ∃ y ∈ c.K, 0 < I.row θ e y ∧ I.row 0 e y = 0) := by
  obtain ⟨e,he⟩ := hC
  have hs : e.1 ∈ usedStates Prod.fst C := Finset.mem_image.mpr ⟨e,he,rfl⟩
  have hInternal : ∀ e ∈ C, internalSucc I θ e ⊆ usedStates Prod.fst C := by
    intro e he y hy
    apply hClosed e he
    simpa only [succ, Finset.mem_filter, Finset.mem_univ, true_and] using
      ((Finset.mem_filter.mp hy).2).1
  have hp := fair_closed_reachable c.D C (internalSucc I θ) hInternal hFair e.1 hs
  rcases body_uncertain_target_or_revelation_reach I c hc θ e.1 (hRegion hs) with
    ⟨t,ht,hpath⟩ | ⟨f,hf,y,hy,hpath,hpos,hzero⟩
  · exact Or.inl ⟨t,ht,hp t hpath⟩
  · exact Or.inr ⟨f,hFair f hf (hp f.1 hpath),y,hy,hpos,hzero⟩

/-- Full equality of recurrent rows transfers actual closure to the candidate. -/
theorem matching_recurrent_closed (I : Input n k) (θ σ : Mode) (C : PairSet n k)
    (hClosed : ∀ e ∈ C, succ I σ e ⊆ usedStates Prod.fst C)
    (hMatch : ∀ e ∈ C, I.row θ e = I.row σ e) :
    ∀ e ∈ C, succ I θ e ⊆ usedStates Prod.fst C := by
  intro e he y hy
  apply hClosed e he
  simpa only [succ, hMatch e he] using hy

/-- The finite uncertain component condition already certifies the actual
parity when its full rows match, even if its global candidate is different. -/
theorem fair_retained_candidate_eq_and_parity (I : Input n k) (θ σ : Mode)
    (E : PairSet n k) (hg : UncertainGood I θ E) (x : ℕ → Pair n k)
    (hRetain : ∀ᶠ j in atTop, x j ∈ E)
    (hClosed : ∀ e ∈ recurrentSet x, succ I σ e ⊆ usedStates Prod.fst (recurrentSet x))
    (hFair : ∀ e ∈ E, e.1 ∈ usedStates Prod.fst (recurrentSet x) → e ∈ recurrentSet x)
    (hMatch : ∀ e ∈ recurrentSet x, I.row θ e = I.row σ e) :
    recurrentSet x = E ∧ HiddenParity.Stochastic.ParitySuccess (I.priority σ) x := by
  letI : Inhabited (State n) := ⟨(x 0).1⟩
  have hEq := fair_closed_subset_eq (succ I θ) (recurrentSet x) E hg.1
    (recurrentSet_nonempty x) (recurrentSet_subset_of_eventually_mem x E hRetain)
    (matching_recurrent_closed I θ σ _ hClosed hMatch) hFair
  refine ⟨hEq, ?_⟩
  have hm : Match I.row θ σ E := by
    intro e he
    exact (hMatch e (hEq.symm ▸ he)).symm
  have hp := (evenMinimum_iff I σ E).mp (hg.2.2 σ hm)
  simpa only [HiddenParity.Stochastic.ParitySuccess, hEq] using hp

/-- The explicit sorted cycle and global source-visit counts supply the fairness
premise of the deterministic retained-candidate theorem. -/
theorem cycling_retained_candidate_eq_and_parity (I : Input n k) (θ σ : Mode)
    (E : PairSet n k) (hg : UncertainGood I θ E) (x : ℕ → Pair n k) (fallback : Action k)
    (hRetain : ∀ᶠ j in atTop, x j ∈ E)
    (hClosed : ∀ e ∈ recurrentSet x, succ I σ e ⊆ usedStates Prod.fst (recurrentSet x))
    (hCycle : ∀ᶠ j in atTop, (x j).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions E (x j).1) fallback (visitsBefore (fun i => (x i).1) (x j).1 j))
    (hMatch : ∀ e ∈ recurrentSet x, I.row θ e = I.row σ e) :
    recurrentSet x = E ∧ HiddenParity.Stochastic.ParitySuccess (I.priority σ) x := by
  letI : Inhabited (State n) := ⟨(x 0).1⟩
  exact fair_retained_candidate_eq_and_parity I θ σ E hg x hRetain hClosed
    (OrthemicCertificate.Direct.eventual_cycle_fair x E fallback hCycle) hMatch

/-- Eventual region membership also contains every recurrent source. -/
theorem recurrent_sources_subset_of_eventually (x : ℕ → Pair n k) (W : Region n)
    (hRegion : ∀ᶠ j in atTop, (x j).1 ∈ W) :
    usedStates Prod.fst (recurrentSet x) ⊆ W := by
  intro s hs
  obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hs
  obtain ⟨j,hj,hW⟩ := (((mem_recurrentSet x e).mp he).and_eventually hRegion).exists
  simpa only [hj,hes] using hW

/-- In a known-mode navigation tail, the submitted targets recur. -/
theorem cycling_known_navigation_hits_target (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (x : ℕ → Pair n k) (fallback : Action k)
    (hRegion : ∀ᶠ j in atTop, (x j).1 ∈ c.K)
    (hClosed : ∀ e ∈ recurrentSet x, succ I 1 e ⊆ usedStates Prod.fst (recurrentSet x))
    (hCycle : ∀ᶠ j in atTop, (x j).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions c.D1 (x j).1) fallback (visitsBefore (fun i => (x i).1) (x j).1 j)) :
    ∃ᶠ j in atTop, (x j).1 ∈ componentTargets (knownComponents c) := by
  letI : Inhabited (State n) := ⟨(x 0).1⟩
  obtain ⟨t,ht,htC⟩ := fair_known_hits_target I c hc (recurrentSet x)
    (recurrentSet_nonempty x) (recurrent_sources_subset_of_eventually x c.K hRegion)
    hClosed (OrthemicCertificate.Direct.eventual_cycle_fair x c.D1 fallback hCycle)
  obtain ⟨e,he,het⟩ := Finset.mem_image.mp htC
  exact ((mem_recurrentSet x e).mp he).mono (fun j hj => by simpa only [hj,het] using ht)

/-- Under explicit actual successor recurrence and recurrent full-row agreement,
a navigation tail must visit a submitted target or observe a P0-zero receipt.
With no agreement premise, a recurrent mismatch is the third alternative. -/
theorem cycling_uncertain_navigation_target_or_revelation_or_mismatch
    (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c) (θ σ : Mode)
    (x : ℕ → Pair n k) (fallback : Action k)
    (hRegion : ∀ᶠ j in atTop, (x j).1 ∈ c.W)
    (hClosed : ∀ e ∈ recurrentSet x, succ I σ e ⊆ usedStates Prod.fst (recurrentSet x))
    (hSuccessors : ∀ e ∈ recurrentSet x, ∀ y, 0 < I.row σ e y →
      ∃ᶠ j in atTop, x j = e ∧ (x (j+1)).1 = y)
    (hCycle : ∀ᶠ j in atTop, (x j).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions c.D (x j).1) fallback (visitsBefore (fun i => (x i).1) (x j).1 j)) :
    (∃ᶠ j in atTop, (x j).1 ∈ componentTargets (uncertainComponents θ c.uncertain)) ∨
    (∃ᶠ j in atTop, I.row 0 (x j) (x (j+1)).1 = 0) ∨
    ∃ e ∈ recurrentSet x, I.row θ e ≠ I.row σ e := by
  classical
  letI : Inhabited (State n) := ⟨(x 0).1⟩
  by_cases hm : ∀ e ∈ recurrentSet x, I.row θ e = I.row σ e
  · have hGraph := fair_uncertain_hits_target_or_revelation I c hc θ (recurrentSet x)
      (recurrentSet_nonempty x) (recurrent_sources_subset_of_eventually x c.W hRegion)
      (matching_recurrent_closed I θ σ _ hClosed hm)
      (OrthemicCertificate.Direct.eventual_cycle_fair x c.D fallback hCycle)
    rcases hGraph with ⟨t,ht,htC⟩ | ⟨e,he,y,_,hpos,hzero⟩
    · obtain ⟨e,he,het⟩ := Finset.mem_image.mp htC
      exact Or.inl (((mem_recurrentSet x e).mp he).mono
        (fun j hj => by simpa only [hj,het] using ht))
    · have ha : 0 < I.row σ e y := by simpa only [hm e he] using hpos
      exact Or.inr (Or.inl ((hSuccessors e he y ha).mono
        (fun j hj => by simpa only [hj.1,hj.2] using hzero)))
  · push_neg at hm
    exact Or.inr (Or.inr hm)

/-- Known-mode retention uses the same sorted cycle and actual closed recurrent
support to identify the entire submitted component and its parity minimum. -/
theorem cycling_retained_known_eq_and_parity (I : Input n k) (E : PairSet n k)
    (hg : KnownGood I E) (x : ℕ → Pair n k) (fallback : Action k)
    (hRetain : ∀ᶠ j in atTop, x j ∈ E)
    (hClosed : ∀ e ∈ recurrentSet x, succ I 1 e ⊆ usedStates Prod.fst (recurrentSet x))
    (hCycle : ∀ᶠ j in atTop, (x j).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions E (x j).1) fallback (visitsBefore (fun i => (x i).1) (x j).1 j)) :
    recurrentSet x = E ∧ HiddenParity.Stochastic.ParitySuccess (I.priority 1) x := by
  letI : Inhabited (State n) := ⟨(x 0).1⟩
  have hEq := fair_closed_subset_eq (succ I 1) (recurrentSet x) E hg.1
    (recurrentSet_nonempty x) (recurrentSet_subset_of_eventually_mem x E hRetain)
    hClosed (OrthemicCertificate.Direct.eventual_cycle_fair x E fallback hCycle)
  refine ⟨hEq, ?_⟩
  simpa only [HiddenParity.Stochastic.ParitySuccess, hEq] using (evenMinimum_iff I 1 E).mp hg.2

#print axioms body_known_target_reach
#print axioms body_uncertain_target_or_revelation_reach
#print axioms fair_known_hits_target
#print axioms fair_uncertain_hits_target_or_revelation
#print axioms cycling_retained_candidate_eq_and_parity
#print axioms cycling_known_navigation_hits_target
#print axioms cycling_uncertain_navigation_target_or_revelation_or_mismatch
#print axioms cycling_retained_known_eq_and_parity
end HiddenChange
