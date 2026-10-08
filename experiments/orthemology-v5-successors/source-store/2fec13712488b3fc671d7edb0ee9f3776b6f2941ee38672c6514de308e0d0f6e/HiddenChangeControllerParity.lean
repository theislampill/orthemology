import HiddenChangeControllerStability

set_option maxHeartbeats 1200000
open Filter
namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
variable {n k : ℕ}

theorem recurrent_closed_of_successors (I : Input n k) (σ : Mode) (x : ℕ → Pair n k)
    (hrec : ∀ e ∈ recurrentSet x, ∀ y, 0 < I.row σ e y →
      ∃ᶠ t in atTop, x t = e ∧ (x (t+1)).1 = y) :
    ∀ e ∈ recurrentSet x, succ I σ e ⊆ usedStates Prod.fst (recurrentSet x) := by
  obtain ⟨N,hN⟩ := eventually_atTop.mp (eventually_mem_recurrentSet x)
  intro e he y hy
  obtain ⟨t,ht,_,hyt⟩ := frequently_atTop.mp (hrec e he y (Finset.mem_filter.mp hy).2) N
  exact Finset.mem_image.mpr ⟨x (t+1),hN (t+1) (by omega),hyt⟩

theorem stable_uncertain_rows_match (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (s : State n) (H : ℕ → PublicHistory n k)
    (hf : Follows I hI c s H) (σ : Mode) (r : ℕ)
    (hk : ∀ᶠ t in atTop, (runMemory I c s H t).known1 = false)
    (hr : ∀ᶠ t in atTop, (runMemory I c s H t).phase = r)
    (hwrong : ∀ e ∈ recurrentSet (runPair I hI c s H), ∀ θ,
      I.row θ e ≠ I.row σ e → ∀ j, ∀ᶠ t in atTop,
      OrthemicCertificate.Direct.rationalReject I (OrthemicCertificate.Direct.tolerance I Finset.univ)
        θ j (augmentHistory s (H t)) = true) :
    ∀ e ∈ recurrentSet (runPair I hI c s H), I.row (candidate r) e = I.row σ e := by
  intro e he
  by_contra hne
  obtain ⟨N,hN⟩ := eventually_atTop.mp (hk.and hr)
  obtain ⟨M,hM⟩ := eventually_atTop.mp (hwrong e he (candidate r) hne r)
  let t := max N M
  have ht : N ≤ t := le_max_left _ _
  have ht1 : N ≤ t+1 := by omega
  have hfalse := run_stable_false_not_rejected I hI c s H hf t (hN t ht).1
    (hN (t+1) ht1).1 ((hN (t+1) ht1).2.trans (hN t ht).2.symm)
  have htrue := hM (t+1) (by dsimp [t]; omega)
  simp only [rejectHistory, (hN t ht).2] at hfalse
  rw [hfalse] at htrue
  contradiction

/-- Deterministic literal-controller sufficiency on the row-regularity event.
The explicit hypotheses are actual support, the gate consequences, and positive
successor recurrence. The final law endpoint must discharge every one. -/
theorem run_parity_of_regular (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s : State n) (hs : s ∈ c.W)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s H)
    (mode : ℕ → Mode) (hpersist : ∀ t, mode t = 1 → mode (t+1) = 1)
    (hsupport : ∀ t, 0 < I.row (mode t) (runPair I hI c s H t) (observedState s (H (t+1))))
    (σ : Mode) (N : ℕ) (hfinal : ∀ t, N ≤ t → mode t = σ)
    (htrue : ∃ K, ∀ r, K ≤ r → ∀ t, OrthemicCertificate.Direct.rationalReject I
      (OrthemicCertificate.Direct.tolerance I Finset.univ) σ r (augmentHistory s (H t)) = false)
    (hwrong : ∀ e ∈ recurrentSet (runPair I hI c s H), ∀ θ,
      I.row θ e ≠ I.row σ e → ∀ r, ∀ᶠ t in atTop,
      OrthemicCertificate.Direct.rationalReject I (OrthemicCertificate.Direct.tolerance I Finset.univ)
        θ r (augmentHistory s (H t)) = true)
    (hrec : ∀ e ∈ recurrentSet (runPair I hI c s H), ∀ y, 0 < I.row σ e y →
      ∃ᶠ t in atTop, runPair I hI c s H t = e ∧ (runPair I hI c s H (t+1)).1 = y) :
    ParitySuccess (I.priority σ) (runPair I hI c s H) := by
  let x := runPair I hI c s H
  let m := runMemory I c s H
  let fallback := firstMenuAction I hI s
  have hinv := run_invariant I hI c hc s hs H hf mode hpersist hsupport
  have hregion : ∀ t, RegionValid c (observedState s (H t)) (m t) := fun t => (hinv t).1
  have hknownpos : ∀ t, (m t).known1 = true → 0 < I.row 1 (x t) (observedState s (H (t+1))) := by
    intro t ht
    simpa only [(hinv t).2 ht] using hsupport t
  obtain ⟨K,hK⟩ := htrue
  have hphase := run_phase_stabilizes I hI c hc s H hf σ N K hregion
    (fun t ht => by simpa only [hfinal t ht] using hsupport t) hK
  obtain ⟨b,r,hb,hr,hret⟩ := run_layer_phase_component_stabilizes I hI c hc s H hf
    hregion hknownpos hphase
  change (∀ᶠ t in atTop, (m t).known1 = b) at hb
  change (∀ᶠ t in atTop, (m t).phase = r) at hr
  change ((∀ᶠ t in atTop, (m t).retained = none) ∨ ∃ E, ∀ᶠ t in atTop, (m t).retained = some E) at hret
  have hclosed := recurrent_closed_of_successors I σ x hrec
  have hσ1 : b = true → σ = 1 := by
    intro hbt
    obtain ⟨t,htN,htb⟩ := ((eventually_ge_atTop N).and hb).exists
    have ht1 : (m t).known1 = true := htb.trans hbt
    exact (hfinal t htN).symm.trans ((hinv t).2 ht1)
  have hmatch : b = false → ∀ e ∈ recurrentSet x, I.row (candidate r) e = I.row σ e := by
    intro hbf
    exact stable_uncertain_rows_match I hI c s H hf σ r (by simpa [hbf] using hb) hr hwrong
  have hcycle : ∀ t, (x t).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions (activePairs c (m t)) (x t).1) fallback
      (visitsBefore (fun j => (x j).1) (x t).1 t) :=
    fun t => run_cycle I hI c hc s H hf t (hregion t) fallback
  rcases hret with hnav | ⟨E,hE⟩
  · have havoid : ∀ᶠ t in atTop, (x t).1 ∉
        componentTargets (if b then knownComponents c else uncertainComponents (candidate r) c.uncertain) := by
      filter_upwards [hnav,hb,hr] with t hnone hbt hrt
      have ha := prepare_none_avoids c (observedState s (H t)) (memory I c s (H t)) hnone
      change (x t).1 ∉ componentTargets (availableComponents c (m t)) at ha
      simpa only [availableComponents,hbt,hrt] using ha
    have hcy : ∀ᶠ t in atTop, (x t).2 = OrthemicCertificate.Direct.cycleAction
        (retainedActions (if b then c.D1 else c.D) (x t).1) fallback
        (visitsBefore (fun j => (x j).1) (x t).1 t) := by
      filter_upwards [hnav,hb] with t hnone hbt
      simpa only [activePairs,hnone,Option.getD_none,hbt] using hcycle t
    cases b with
    | true =>
        have hreg : ∀ᶠ t in atTop, (x t).1 ∈ c.K := by
          filter_upwards [hb] with t ht
          simpa only [x,runPair,RegionValid,ht,↓reduceIte] using hregion t
        have hhit := cycling_known_navigation_hits_target I c hc x fallback hreg
          (by simpa only [hσ1 rfl] using hclosed) (by simpa using hcy)
        obtain ⟨t,ht,ha⟩ := (hhit.and_eventually havoid).exists
        exact (ha ht).elim
    | false =>
        have hreg : ∀ᶠ t in atTop, (x t).1 ∈ c.W := by
          filter_upwards [hb] with t ht
          simpa only [x,runPair,RegionValid,ht,Bool.false_eq_true,↓reduceIte] using hregion t
        have hnav' := cycling_uncertain_navigation_target_or_revelation_or_mismatch I c hc
          (candidate r) σ x fallback hreg hclosed hrec (by simpa using hcy)
        rcases hnav' with hhit | hrev | ⟨e,he,hmismatch⟩
        · obtain ⟨t,ht,ha⟩ := (hhit.and_eventually havoid).exists
          exact (ha ht).elim
        · obtain ⟨M,hM⟩ := eventually_atTop.mp hb
          obtain ⟨t,ht,hzero⟩ := frequently_atTop.mp hrev M
          exact (run_false_no_revelation I hI c s H hf t (hM (t+1) (by omega)) hzero).elim
        · exact (hmismatch (hmatch rfl e he)).elim
  · have hretain : ∀ᶠ t in atTop, x t ∈ E := by
      filter_upwards [hE] with t ht
      have ha : x t ∈ activePairs c (m t) := compiled_action_active I hI c hc s (H t) (hregion t)
      simpa only [activePairs,ht,Option.getD_some] using ha
    have hcy : ∀ᶠ t in atTop, (x t).2 = OrthemicCertificate.Direct.cycleAction
        (retainedActions E (x t).1) fallback (visitsBefore (fun j => (x j).1) (x t).1 t) := by
      filter_upwards [hE] with t ht
      simpa only [activePairs,ht,Option.getD_some] using hcycle t
    obtain ⟨t,htE,htb,htr⟩ := (hE.and (hb.and hr)).exists
    have hm := (currentMemory_valid I c hc s (H t)) E htE
    have hg : ComponentValid I c (m t) E := hm.1
    cases b with
    | true =>
        have hgood : KnownGood I E := by
          simp only [ComponentValid,htb,↓reduceIte] at hg
          exact hg.2
        have hp := (cycling_retained_known_eq_and_parity I E hgood x fallback hretain
          (by simpa only [hσ1 rfl] using hclosed) hcy).2
        simpa only [hσ1 rfl] using hp
    | false =>
        have hgood : UncertainGood I (candidate r) E := by
          simp only [ComponentValid,htb,Bool.false_eq_true,↓reduceIte,htr] at hg
          exact hg.2
        exact (cycling_retained_candidate_eq_and_parity I (candidate r) σ E hgood x fallback
          hretain hclosed hcy (hmatch rfl)).2

#print axioms stable_uncertain_rows_match
#print axioms run_parity_of_regular
end HiddenChange
