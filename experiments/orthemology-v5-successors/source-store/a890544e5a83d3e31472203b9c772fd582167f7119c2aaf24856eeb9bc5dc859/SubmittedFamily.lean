import StageFamily

/-! Read only the actual submitted node/obligation/component syntax. Collection
is by literal list order. On accepted bodies there is at most one node per
support; union-based total projections avoid any partial lookup off-domain. -/
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Stage HiddenParity.Necessity HiddenParity.Sufficiency
variable {q n k : ℕ}

/-- All members are explicit input syntax. -/
def collectSets {α β : Type*} [DecidableEq β] (f : α → Finset β) : List α → Finset β
  | [] => ∅
  | a :: as => f a ∪ collectSets f as

@[simp] theorem mem_collectSets {α β : Type*} [DecidableEq β] (f : α → Finset β)
    (as : List α) (b : β) : b ∈ collectSets f as ↔ ∃ a ∈ as, b ∈ f a := by
  induction as with
  | nil => simp [collectSets]
  | cons a as ih => simp [collectSets, ih, or_and_right, exists_or]

def submittedNodes (c : Body q n k) (B : Support q) : List (Node q n k) :=
  c.filter (fun N => N.support == B)

@[simp] theorem mem_submittedNodes (c : Body q n k) (B : Support q) (N : Node q n k) :
    N ∈ submittedNodes c B ↔ N ∈ c ∧ N.support = B := by simp [submittedNodes]

def obligationComponent (θ : Fin q) (o : Obligation q n k) : Option (Component n k) :=
  if o.candidate = θ then
    match o.witness with
    | .exit .. => none
    | .target _ E _ => some E
  else none

@[simp] theorem obligationComponent_eq_some (θ : Fin q) (o : Obligation q n k) (E : Component n k) :
    obligationComponent θ o = some E ↔ o.candidate = θ ∧ ∃ p entry, o.witness = .target p E entry := by
  unfold obligationComponent
  split_ifs with h
  · cases hw : o.witness <;> simp [h]
  · simp [h]

def submittedPool (c : Body q n k) (B : Support q) (θ : Fin q) : List (Component n k) :=
  (submittedNodes c B).flatMap (fun N => N.obligations.filterMap (obligationComponent θ))

@[simp] theorem mem_submittedPool (c : Body q n k) (B : Support q) (θ : Fin q) (E : Component n k) :
    E ∈ submittedPool c B θ ↔ ∃ N ∈ c, N.support = B ∧
      ∃ o ∈ N.obligations, o.candidate = θ ∧ ∃ p entry, o.witness = .target p E entry := by
  simp only [submittedPool, List.mem_flatMap, mem_submittedNodes, List.mem_filterMap,
    obligationComponent_eq_some]
  aesop

def submittedStates (c : Body q n k) (B : Support q) : Finset (Fin n) :=
  collectSets Node.states (submittedNodes c B)

def submittedPairs (c : Body q n k) (B : Support q) : Finset (Pair n k) :=
  collectSets Node.pairs (submittedNodes c B)

def submittedTargets (c : Body q n k) (B : Support q) (θ : Fin q) : Finset (Fin n) :=
  collectSets Component.used (submittedPool c B θ)

def submittedChoice (c : Body q n k) (B : Support q) (θ : Fin q) (s : Fin n) : Finset (Pair n k) :=
  ((submittedPool c B θ).find? (fun E => s ∈ E.used)).map Component.pairs |>.getD ∅

def submittedFamily (c : Body q n k) : StageData (Fin q) (Fin n) (Fin k) where
  states := submittedStates c
  pairs := submittedPairs c
  targets := submittedTargets c
  choose := submittedChoice c

@[simp] theorem mem_submittedStates (c : Body q n k) (B : Support q) (s : Fin n) :
    s ∈ submittedStates c B ↔ ∃ N ∈ c, N.support = B ∧ s ∈ N.states := by
  simp only [submittedStates, mem_collectSets, mem_submittedNodes]
  aesop

@[simp] theorem mem_submittedPairs (c : Body q n k) (B : Support q) (e : Pair n k) :
    e ∈ submittedPairs c B ↔ ∃ N ∈ c, N.support = B ∧ e ∈ N.pairs := by
  simp only [submittedPairs, mem_collectSets, mem_submittedNodes]
  aesop

@[simp] theorem mem_submittedTargets (c : Body q n k) (B : Support q) (θ : Fin q) (s : Fin n) :
    s ∈ submittedTargets c B θ ↔ ∃ E ∈ submittedPool c B θ, s ∈ E.used := by
  exact mem_collectSets Component.used _ s

theorem nodePairs_subset {c : Body q n k} {N : Node q n k} (hN : N ∈ c) :
    N.pairs ⊆ submittedPairs c N.support := by
  intro e he
  exact (mem_submittedPairs c N.support e).mpr ⟨N,hN,rfl,he⟩

/-- Navigation targets refer to components literally present in the body. -/
theorem submitted_reach {I : Input q n k} {c : Body q n k} (hc : BodyValid I c)
    (B : Support q) (θ : Fin q) (hθ : θ ∈ B) (s : Fin n) (hs : s ∈ submittedStates c B) :
    ReachableExit (I.kernel hc.1) B θ (submittedPairs c B) s ∨
      ∃ t ∈ submittedTargets c B θ,
        Reach Prod.fst (internalSuccessors (I.kernel hc.1) B) (submittedPairs c B) s t := by
  obtain ⟨N,hN,hNB,hsN⟩ := (mem_submittedStates c B s).mp hs
  subst B
  have hv := hc.2.2 N hN
  obtain ⟨o,ho,hos,hoθ⟩ := Node.obligation_exists hv.2.1 hsN hθ
  have hw := hv.2.2.2 o ho
  rw [hos,hoθ] at hw
  cases heq : o.witness with
  | exit p e y =>
    rw [heq] at hw
    obtain ⟨hp,he,hy,hproper⟩ := hw
    left
    refine ⟨e,nodePairs_subset hN he,?_,y,hy,?_,?_⟩
    · simpa only [← Input.internal_kernel I hc.1 N.support] using
        reach_mono (nodePairs_subset hN) (Path.valid_sound hp)
    · exact ⟨θ,Finset.mem_filter.mpr ⟨hθ,hy⟩⟩
    · simpa using hproper
  | target p E entry =>
    rw [heq] at hw
    obtain ⟨hp,hE⟩ := hw
    right
    refine ⟨entry,?_,?_⟩
    · apply (mem_submittedTargets c N.support θ entry).mpr
      exact ⟨E,(mem_submittedPool c N.support θ E).mpr ⟨N,hN,rfl,o,ho,hoθ,p,entry,heq⟩,hE.2.2.2.1⟩
    · simpa only [← Input.internal_kernel I hc.1 N.support] using
        reach_mono (nodePairs_subset hN) (Path.valid_sound hp)

/-- Availability is extracted from the submitted path endpoint, not a solver. -/
theorem submitted_available {I : Input q n k} {c : Body q n k} (hc : BodyValid I c)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (hs : s ∈ submittedStates c B) :
    s ∈ usedStates Prod.fst (submittedPairs c B) := by
  obtain ⟨N,hN,hNB,hsN⟩ := (mem_submittedStates c B s).mp hs
  subst B
  obtain ⟨θ,hθ⟩ := hB
  have hv := hc.2.2 N hN
  obtain ⟨o,ho,hos,hoθ⟩ := Node.obligation_exists hv.2.1 hsN hθ
  have hw := hv.2.2.2 o ho
  rw [hos,hoθ] at hw
  have hsUsed : s ∈ usedStates Prod.fst N.pairs := by
    cases heq : o.witness with
    | exit p e y =>
      rw [heq] at hw
      exact reach_start_used N.pairs _ (Path.valid_sound hw.1)
        (Finset.mem_image.mpr ⟨e,hw.2.1,rfl⟩)
    | target p E entry =>
      rw [heq] at hw
      have hE := hw.2
      exact reach_start_used N.pairs _ (Path.valid_sound hw.1)
        (Finset.image_mono Prod.fst hE.2.1 hE.2.2.2.1)
  exact Finset.image_mono Prod.fst (nodePairs_subset hN) hsUsed

theorem pool_qualifying {I : Input q n k} {c : Body q n k} (hc : BodyValid I c)
    {B : Support q} {θ : Fin q} {E : Component n k} (hE : E ∈ submittedPool c B θ) :
    MarkovQualifying (I.kernel hc.1) Prod.fst B I.priority θ (submittedPairs c B) E.pairs := by
  obtain ⟨N,hN,hNB,o,ho,hoθ,p,entry,hw⟩ := (mem_submittedPool c B θ E).mp hE
  subst B
  have hv := (hc.2.2 N hN).2.2.2 o ho
  rw [hw] at hv
  have hq := (Component.valid_sound hc.1 hv.2).1
  rw [hoθ] at hq
  exact ⟨hq.1.trans (nodePairs_subset hN),hq.2⟩

theorem submitted_choice_spec {I : Input q n k} {c : Body q n k} (hc : BodyValid I c)
    (B : Support q) (θ : Fin q) (s : Fin n) (hs : s ∈ submittedTargets c B θ) :
    MarkovQualifying (I.kernel hc.1) Prod.fst B I.priority θ (submittedPairs c B)
      (submittedChoice c B θ s) ∧ s ∈ usedStates Prod.fst (submittedChoice c B θ s) := by
  obtain ⟨E,hE,hsE⟩ := (mem_submittedTargets c B θ s).mp hs
  have hex : ((submittedPool c B θ).find? (fun F => s ∈ F.used)).isSome := by
    apply List.find?_isSome.mpr
    exact ⟨E,hE,by simpa using hsE⟩
  cases heq : (submittedPool c B θ).find? (fun F => s ∈ F.used) with
  | none => simp [heq] at hex
  | some F =>
    have hF : F ∈ submittedPool c B θ := List.mem_of_find?_eq_some heq
    have hsF : s ∈ F.used := by simpa using List.find?_some heq
    simpa only [submittedChoice,heq,Option.map_some,Option.getD_some] using
      And.intro (pool_qualifying hc hF) hsF

/-- Every certification premise is discharged by the actual accepted syntax. -/
def submitted_certified {I : Input q n k} {c : Body q n k} (hc : BodyValid I c) :
    CertifiedStageFamily (I.kernel hc.1) I.menu I.priority (submittedFamily c) where
  available := submitted_available hc
  menu := by
    intro B e he
    obtain ⟨N,hN,hNB,heN⟩ := (mem_submittedPairs c B e).mp he
    simpa only [← hNB] using ((hc.2.2 N hN).2.2.1 e heN).2.1
  successor := by
    intro B e he y hy
    obtain ⟨N,hN,hNB,heN⟩ := (mem_submittedPairs c B e).mp he
    subst B
    have hraw : (I.live N.support e y).Nonempty := by simpa using hy
    have hnext := ((hc.2.2 N hN).2.2.1 e heN).2.2 y hraw
    apply (mem_submittedStates c _ y).mpr
    by_cases heq : I.live N.support e y = N.support
    · simp only [heq,if_true] at hnext
      exact ⟨N,hN,by simpa using heq.symm,hnext⟩
    · rw [if_neg heq] at hnext
      obtain ⟨_,child,hchild,hB,hyc⟩ := hnext
      exact ⟨child,hchild,by simpa using hB,hyc⟩
  target := submitted_choice_spec hc
  reach := submitted_reach hc

end OrthemicCertificate.Direct
