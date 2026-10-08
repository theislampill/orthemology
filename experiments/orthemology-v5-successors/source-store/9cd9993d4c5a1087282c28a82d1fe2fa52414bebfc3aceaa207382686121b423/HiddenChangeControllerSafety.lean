import HiddenChangeController

namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
variable {n k : ℕ}

def ComponentValid (I : Input n k) (c : PositiveBody n k)
    (m : ControllerMemory n k) (E : PairSet n k) : Prop :=
  if m.known1 then E ⊆ c.D1 ∧ KnownGood I E
  else E ⊆ c.D ∧ UncertainGood I (candidate m.phase) E

def MemoryValid (I : Input n k) (c : PositiveBody n k)
    (s : State n) (m : ControllerMemory n k) : Prop :=
  ∀ E, m.retained = some E → ComponentValid I c m E ∧ s ∈ usedStates Prod.fst E

theorem firstContaining_spec (s : State n) (es : List (PairSet n k)) (E : PairSet n k)
    (h : firstContaining s es = some E) : E ∈ es ∧ s ∈ usedStates Prod.fst E := by
  induction es with
  | nil => simp [firstContaining] at h
  | cons F fs ih =>
      by_cases hs : s ∈ usedStates Prod.fst F
      · simp only [firstContaining, if_pos hs, Option.some.injEq] at h
        subst E
        exact ⟨List.mem_cons_self, hs⟩
      · simp only [firstContaining, if_neg hs] at h
        exact ⟨List.mem_cons_of_mem _ (ih h).1, (ih h).2⟩

theorem firstContaining_eq_none_iff (s : State n) (es : List (PairSet n k)) :
    firstContaining s es = none ↔ ∀ E ∈ es, s ∉ usedStates Prod.fst E := by
  induction es with
  | nil => simp [firstContaining]
  | cons E es ih => by_cases hs : s ∈ usedStates Prod.fst E <;> simp [firstContaining, hs, ih]

theorem mem_uncertainComponents (θ : Mode) (os : List (UncertainObligation n k))
    (E : PairSet n k) : E ∈ uncertainComponents θ os ↔
      ∃ o ∈ os, o.candidate = θ ∧ ∃ p, o.witness = .component p E := by
  induction os with
  | nil => simp [uncertainComponents]
  | cons o os ih =>
      cases hw : o.witness with
      | reveal p a y => simp [uncertainComponents, hw, ih]
      | component p F =>
          by_cases hc : o.candidate = θ <;> simp [uncertainComponents, hw, hc, ih]
          constructor
          · rintro (rfl | h)
            · exact Or.inl rfl
            · exact Or.inr h
          · rintro (h | h)
            · exact Or.inl h.symm
            · exact Or.inr h

theorem availableComponents_valid (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) (m : ControllerMemory n k) (E : PairSet n k)
    (hE : E ∈ availableComponents c m) : ComponentValid I c m E := by
  cases hk : m.known1 with
  | true =>
      simp only [availableComponents, hk, Bool.true_eq, ↓reduceIte, knownComponents] at hE
      obtain ⟨o,ho,rfl⟩ := List.mem_map.mp hE
      simpa [ComponentValid, hk] using
        And.intro (hc.2.2.2.2.2.2.1 o ho).1 (hc.2.2.2.2.2.2.1 o ho).2.1
  | false =>
      simp only [availableComponents, hk, Bool.false_eq_true, ↓reduceIte] at hE
      obtain ⟨o,ho,hθ,p,hw⟩ := (mem_uncertainComponents _ _ _).mp hE
      have hv := hc.2.2.2.2.2.2.2 o ho
      simp only [UncertainObligation.Valid, hw] at hv
      simp only [ComponentValid, hk, Bool.false_eq_true, ↓reduceIte]
      exact ⟨hv.1, hθ ▸ hv.2.1⟩

theorem prepare_valid (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (m : ControllerMemory n k) (hm : MemoryValid I c s m) :
    MemoryValid I c s (prepare c s m) := by
  cases hr : m.retained with
  | some E => simpa [prepare, hr] using hm
  | none =>
      intro E hE
      have he : firstContaining s (availableComponents c m) = some E := by
        simpa [prepare, hr] using hE
      have hs := firstContaining_spec s _ E he
      refine ⟨?_, hs.2⟩
      simpa [ComponentValid] using availableComponents_valid I c hc m E hs.1

theorem advance_valid (I : Input n k) (c : PositiveBody n k)
    (s y : State n) (e : Pair n k) (m : ControllerMemory n k) (b : Bool)
    (hm : MemoryValid I c s m) : MemoryValid I c y (advance I e y m b) := by
  intro E hE
  by_cases hk : m.known1 = true
  · by_cases hl : leaves m y = true
    · simp [advance, hk, hl] at hE
    · have hr : m.retained = some E := by simpa [advance, hk, hl] using hE
      have hy : y ∈ usedStates Prod.fst E := by simpa [leaves, hr] using hl
      exact ⟨by simpa [advance, hk, hl, ComponentValid] using (hm E hr).1, hy⟩
  · by_cases hz : I.row 0 e y = 0
    · simp [advance, hk, hz] at hE
    · by_cases hb : (b || leaves m y) = true
      · simp [advance, hk, hz, hb] at hE
      · have hr : m.retained = some E := by simpa [advance, hk, hz, hb] using hE
        have hl : leaves m y = false := (Bool.or_eq_false_iff.mp (Bool.eq_false_of_not_eq_true hb)).2
        have hy : y ∈ usedStates Prod.fst E := by simpa [leaves, hr] using hl
        simpa [advance, hk, hz, hb] using And.intro (hm E hr).1 hy

theorem memory_valid (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s₀ : State n) (h : PublicHistory n k) :
    MemoryValid I c (observedState s₀ h) (memory I c s₀ h) := by
  induction h with
  | nil => intro E he; cases he
  | cons z h ih =>
      rcases z with ⟨a,y⟩
      exact advance_valid I c _ _ _ _ _ (prepare_valid I c hc _ _ ih)

theorem currentMemory_valid (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s₀ : State n) (h : PublicHistory n k) :
    MemoryValid I c (observedState s₀ h) (currentMemory I c s₀ h) :=
  prepare_valid I c hc _ _ (memory_valid I c hc s₀ h)

theorem body_known_available (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (hs : s ∈ c.K) : s ∈ usedStates Prod.fst c.D1 := by
  have hkey : s ∈ (c.known.map KnownObligation.source).toFinset := hc.2.2.2.1.symm ▸ hs
  obtain ⟨o,ho,hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  have hv := hc.2.2.2.2.2.2.1 o ho
  rw [← hos]
  exact reach_start_used c.D1 _ (OrthemicCertificate.Path.valid_sound hv.2.2.1)
    (usedStates_mono hv.1 hv.2.2.2)

theorem body_uncertain_available (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (hs : s ∈ c.W) : s ∈ usedStates Prod.fst c.D := by
  have hkey : (s,(0 : Mode)) ∈ (c.uncertain.map uncertainKey).toFinset := by
    rw [hc.2.2.2.2.2.1]; simp [hs]
  obtain ⟨o,ho,hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  have hsrc : o.source = s := congrArg Prod.fst hos
  have hv := hc.2.2.2.2.2.2.2 o ho
  rw [← hsrc]
  cases hw : o.witness with
  | component p E =>
      simp only [UncertainObligation.Valid, hw] at hv
      exact reach_start_used c.D _ (OrthemicCertificate.Path.valid_sound hv.2.2.1)
        (usedStates_mono hv.1 hv.2.2.2)
  | reveal p a y =>
      simp only [UncertainObligation.Valid, hw] at hv
      exact reach_start_used c.D _ (OrthemicCertificate.Path.valid_sound hv.1)
        (Finset.mem_image.mpr ⟨(p.endpoint,a),hv.2.1,rfl⟩)

def RegionValid (c : PositiveBody n k) (s : State n) (m : ControllerMemory n k) : Prop :=
  if m.known1 then s ∈ c.K else s ∈ c.W

theorem valid_activePairs (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (m : ControllerMemory n k) (hm : MemoryValid I c s m)
    (hs : RegionValid c s m) :
    activePairs c m ⊆ (if m.known1 then c.D1 else c.D) ∧
      s ∈ usedStates Prod.fst (activePairs c m) := by
  cases hr : m.retained with
  | none =>
      simp only [activePairs, hr, Option.getD_none]
      refine ⟨Finset.Subset.refl _, ?_⟩
      cases hk : m.known1 with
      | false => exact body_uncertain_available I c hc s (by simpa [RegionValid, hk] using hs)
      | true => exact body_known_available I c hc s (by simpa [RegionValid, hk] using hs)
  | some E =>
      simp only [activePairs, hr, Option.getD_some]
      refine ⟨?_, (hm E hr).2⟩
      have h := (hm E hr).1
      cases hk : m.known1 <;> simp only [ComponentValid, hk, Bool.false_eq_true, Bool.true_eq, ↓reduceIte] at h ⊢ <;> exact h.1

theorem activePairs_menu (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (m : ControllerMemory n k) (hm : MemoryValid I c s m)
    (hs : RegionValid c s m) : retainedActions (activePairs c m) s ⊆ commonMenu I s := by
  letI : Inhabited (State n) := ⟨s⟩
  intro a ha
  have he := (valid_activePairs I c hc s m hm hs).1 ((mem_retainedActions _ _ _).mp ha)
  cases hk : m.known1 with
  | false => exact ((mem_uncertainAllowed I _ _ _).mp (hc.2.1 (by simpa [hk] using he))).2.1
  | true => exact ((mem_knownAllowed I _ _).mp (hc.1 (by simpa [hk] using he))).2.1

theorem actionMenu_eq (I : Input n k) (c : PositiveBody n k) (hc : BodyValid I c)
    (s : State n) (m : ControllerMemory n k) (hm : MemoryValid I c s m)
    (hs : RegionValid c s m) : actionMenu I c s m = retainedActions (activePairs c m) s :=
  Finset.inter_eq_left.mpr (activePairs_menu I c hc s m hm hs)

theorem compiled_action_safe (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s₀ : State n) (h : PublicHistory n k)
    (hs : RegionValid c (observedState s₀ h) (currentMemory I c s₀ h)) :
    (observedState s₀ h, compile I hI s₀ c () h) ∈
      (if (currentMemory I c s₀ h).known1 then c.D1 else c.D) := by
  letI : Inhabited (State n) := ⟨s₀⟩
  have hm := currentMemory_valid I c hc s₀ h
  have hv := valid_activePairs I c hc _ _ hm hs
  apply hv.1
  apply (mem_retainedActions _ _ _).mp
  dsimp only [compile]
  rw [actionMenu_eq I c hc _ _ hm hs]
  exact OrthemicCertificate.Direct.cycleAction_mem _ _ (retainedActions_nonempty _ _ hv.2) _

theorem compiled_action_active (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s₀ : State n) (h : PublicHistory n k)
    (hs : RegionValid c (observedState s₀ h) (currentMemory I c s₀ h)) :
    (observedState s₀ h, compile I hI s₀ c () h) ∈ activePairs c (currentMemory I c s₀ h) := by
  letI : Inhabited (State n) := ⟨s₀⟩
  have hm := currentMemory_valid I c hc s₀ h
  have hv := valid_activePairs I c hc _ _ hm hs
  apply (mem_retainedActions _ _ _).mp
  dsimp only [compile]
  rw [actionMenu_eq I c hc _ _ hm hs]
  exact OrthemicCertificate.Direct.cycleAction_mem _ _ (retainedActions_nonempty _ _ hv.2) _

end HiddenChange
