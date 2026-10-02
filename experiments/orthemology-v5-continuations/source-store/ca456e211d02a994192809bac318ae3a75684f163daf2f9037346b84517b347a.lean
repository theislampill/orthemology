import StageTargetOrExit

namespace HiddenParity.Necessity
open HiddenParity.Stage

universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [DecidableEq Model]

instance reachDecidable (source : (State × Action) → State) (succ : (State × Action) → Finset State)
    (E : Finset (State × Action)) (s t : State) : Decidable (Reach source succ E s t) :=
  decidable_of_iff (t ∈ FiniteReachability.reachable (Edge source succ E) s)
    (FiniteReachability.reachable_iff (Edge source succ E) s t)

instance reachableExitDecidable (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (θ : Model) (allowed : Finset (State × Action)) (s : State) :
    Decidable (ReachableExit P B θ allowed s) := by
  unfold ReachableExit
  infer_instance

/-- Actual all-branch stage licensing: hard menu, current region, same-support
successors in W, and every nonempty proper-support successor in its lower region. -/
def regionAllowed (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model)
    (lower : Finset Model → Finset State) (W : Finset State) : Finset (State × Action) :=
  Finset.univ.filter (fun e => e.1 ∈ W ∧ e.2 ∈ menu B e.1 ∧
    ∀ y, (liveUpdate P B e y).Nonempty →
      if liveUpdate P B e y = B then y ∈ W else y ∈ lower (liveUpdate P B e y))

@[simp] theorem mem_regionAllowed (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model)
    (lower : Finset Model → Finset State) (W : Finset State) (e : State × Action) :
    e ∈ regionAllowed P menu B lower W ↔ e.1 ∈ W ∧ e.2 ∈ menu B e.1 ∧
      ∀ y, (liveUpdate P B e y).Nonempty →
        if liveUpdate P B e y = B then y ∈ W else y ∈ lower (liveUpdate P B e y) := by
  simp [regionAllowed]

/-- One finite descending region step. Targets are computed by the proved
exhaustive parity reference; paths use proved finite directed reachability. -/
def regionStep (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) : Finset State :=
  W.filter (fun s => ∀ θ ∈ B,
    ReachableExit P B θ (regionAllowed P menu B lower W) s ∨
      ∃ t ∈ markovTargetStates P Prod.fst B priority θ (regionAllowed P menu B lower W),
        Reach Prod.fst (internalSuccessors P B) (regionAllowed P menu B lower W) s t)

@[simp] theorem mem_regionStep (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) (s : State) :
    s ∈ regionStep P menu priority B lower W ↔ s ∈ W ∧ ∀ θ ∈ B,
      ReachableExit P B θ (regionAllowed P menu B lower W) s ∨
        ∃ t ∈ markovTargetStates P Prod.fst B priority θ (regionAllowed P menu B lower W),
          Reach Prod.fst (internalSuccessors P B) (regionAllowed P menu B lower W) s t := by
  simp [regionStep]

def descend (F : Finset State → Finset State) : ℕ → Finset State → Finset State
  | 0, W => W
  | n+1, W => descend F n (F W)

/-- Bottom-up live-support recursion with bounded state descent. Fuel is at
least the current support cardinality; only proper child supports matter. -/
def computedRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ) :
    ℕ → Finset Model → Finset State
  | 0, _ => ∅
  | n+1, B => if B.Nonempty then
      descend (regionStep P menu priority B (computedRegion P menu priority n))
        (Fintype.card State) Finset.univ else ∅

def winningRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) : Finset State := computedRegion P menu priority B.card B

theorem regionAllowed_mono (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model)
    (lower : Finset Model → Finset State) {W V : Finset State} (hWV : W ⊆ V) :
    regionAllowed P menu B lower W ⊆ regionAllowed P menu B lower V := by
  intro e he
  obtain ⟨hs, hm, hSafe⟩ := (mem_regionAllowed P menu B lower W e).mp he
  apply (mem_regionAllowed P menu B lower V e).mpr
  refine ⟨hWV hs, hm, ?_⟩
  intro y hC
  have h := hSafe y hC
  by_cases heq : liveUpdate P B e y = B
  · simp only [heq, if_true] at h ⊢
    exact hWV h
  · simpa only [heq, if_false] using h

theorem targetStates_mono (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (priority : Model → (State × Action) → ℕ) (θ : Model)
    {D E : Finset (State × Action)} (hDE : D ⊆ E) :
    markovTargetStates P Prod.fst B priority θ D ⊆ markovTargetStates P Prod.fst B priority θ E := by
  intro s hs
  obtain ⟨C, hQ, hsC⟩ := (markovTargetStates_exact P Prod.fst B priority θ D s).mp hs
  exact (markovTargetStates_exact P Prod.fst B priority θ E s).mpr
    ⟨C, ⟨hQ.1.trans hDE, hQ.2⟩, hsC⟩

theorem reachableExit_mono (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (θ : Model) {D E : Finset (State × Action)} (hDE : D ⊆ E)
    {s : State} (h : ReachableExit P B θ D s) : ReachableExit P B θ E s := by
  obtain ⟨e, he, hReach, hExit⟩ := h
  exact ⟨e, hDE he, reach_mono hDE hReach, hExit⟩

theorem regionStep_subset (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) :
    regionStep P menu priority B lower W ⊆ W := Finset.filter_subset _ _

theorem regionStep_mono (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) :
    Monotone (regionStep P menu priority B lower) := by
  intro W V hWV s hs
  obtain ⟨hsW, hAll⟩ := (mem_regionStep P menu priority B lower W s).mp hs
  refine (mem_regionStep P menu priority B lower V s).mpr ⟨hWV hsW, ?_⟩
  intro θ hθ
  have hA := regionAllowed_mono P menu B lower hWV
  rcases hAll θ hθ with hExit | ⟨t, ht, hPath⟩
  · exact Or.inl (reachableExit_mono P B θ hA hExit)
  · exact Or.inr ⟨t, targetStates_mono P B priority θ hA ht, reach_mono hA hPath⟩

/-- Every postfixed set survives all finite descending rounds. -/
theorem postfixed_subset_descend (F : Finset State → Finset State) (hMono : Monotone F)
    {V W : Finset State} (hPost : V ⊆ F V) (hVW : V ⊆ W) (n : ℕ) :
    V ⊆ descend F n W := by
  induction n generalizing W with
  | zero => exact hVW
  | succ n ih => exact ih (hPost.trans (hMono hVW))

theorem descend_eq_of_stable (F : Finset State → Finset State) {W : Finset State}
    (h : F W = W) (n : ℕ) : descend F n W = W := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [descend, h] using ih

/-- Contracting finite state descent stabilizes within the original state count. -/
theorem descend_stable (F : Finset State → Finset State) (hContract : ∀ W, F W ⊆ W)
    (n : ℕ) (W : Finset State) (hBound : W.card ≤ n) :
    F (descend F n W) = descend F n W := by
  induction n generalizing W with
  | zero =>
      have hW : W = ∅ := Finset.card_eq_zero.mp (by omega)
      subst W
      exact Finset.eq_empty_iff_forall_not_mem.mpr (fun e he => Finset.not_mem_empty e (hContract ∅ he))
  | succ n ih =>
      by_cases h : F W = W
      · rw [descend_eq_of_stable F h]
        exact h
      · have hLt := Finset.card_lt_card (Finset.ssubset_iff_subset_ne.mpr ⟨hContract W, h⟩)
        exact ih (F W) (by omega)

theorem computedRegion_fixed_stage (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (n : ℕ) (B : Finset Model) (hB : B.Nonempty) :
    regionStep P menu priority B (computedRegion P menu priority n)
      (computedRegion P menu priority (n+1) B) = computedRegion P menu priority (n+1) B := by
  simp only [computedRegion, if_pos hB]
  exact descend_stable _ (regionStep_subset P menu priority B _) _ _ (by simp)

/-- Only proper lower-support regions are consulted by stage licensing. -/
theorem regionAllowed_congr_lower (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model)
    (lower lower' : Finset Model → Finset State)
    (hEq : ∀ C, C ⊂ B → lower C = lower' C) (W : Finset State) :
    regionAllowed P menu B lower W = regionAllowed P menu B lower' W := by
  ext e
  simp only [mem_regionAllowed]
  have hChild : ∀ y, (if liveUpdate P B e y = B then y ∈ W else y ∈ lower (liveUpdate P B e y)) ↔
      (if liveUpdate P B e y = B then y ∈ W else y ∈ lower' (liveUpdate P B e y)) := by
    intro y
    by_cases h : liveUpdate P B e y = B
    · simp [h]
    · rw [if_neg h, if_neg h]
      have hProper : liveUpdate P B e y ⊂ B :=
        Finset.ssubset_iff_subset_ne.mpr ⟨Finset.filter_subset _ _, h⟩
      rw [hEq (liveUpdate P B e y) hProper]
  simp only [hChild]

theorem regionStep_congr_lower (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower lower' : Finset Model → Finset State)
    (hEq : ∀ C, C ⊂ B → lower C = lower' C) :
    regionStep P menu priority B lower = regionStep P menu priority B lower' := by
  funext W
  simp only [regionStep, regionAllowed_congr_lower P menu B lower lower' hEq W]

/-- Excess recursion fuel does not change the result once it covers support
cardinality. This identifies the bounded reference with true bottom-up support recursion. -/
theorem computedRegion_fuel_irrelevant (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (m n : ℕ) (hm : B.card ≤ m) (hn : B.card ≤ n) :
    computedRegion P menu priority m B = computedRegion P menu priority n B := by
  induction B using Finset.strongInductionOn generalizing m n with
  | _ B ih =>
      by_cases hB : B.Nonempty
      · have hc : 0 < B.card := Finset.card_pos.mpr hB
        cases m with
        | zero => omega
        | succ m =>
            cases n with
            | zero => omega
            | succ n =>
                simp only [computedRegion, if_pos hB]
                have he := regionStep_congr_lower P menu priority B
                  (computedRegion P menu priority m) (computedRegion P menu priority n) (by
                    intro C hC
                    have hCard := Finset.card_lt_card hC
                    exact ih C hC m n (by omega) (by omega))
                rw [he]
      · cases m <;> cases n <;> simp [computedRegion, hB]

/-- The bounded result is a genuine fixed point with canonical child regions. -/
theorem winningRegion_fixed (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (hB : B.Nonempty) :
    regionStep P menu priority B (winningRegion P menu priority) (winningRegion P menu priority B) =
      winningRegion P menu priority B := by
  have hc : 0 < B.card := Finset.card_pos.mpr hB
  obtain ⟨n, hn⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hc)
  have he := regionStep_congr_lower P menu priority B (computedRegion P menu priority n)
    (winningRegion P menu priority) (by
      intro C hC
      have hCard := Finset.card_lt_card hC
      exact computedRegion_fuel_irrelevant P menu priority C n C.card (by omega) (le_refl _))
  change regionStep P menu priority B (winningRegion P menu priority)
    (computedRegion P menu priority B.card B) = computedRegion P menu priority B.card B
  rw [hn, ← he]
  exact computedRegion_fixed_stage P menu priority n B hB

end HiddenParity.Necessity
