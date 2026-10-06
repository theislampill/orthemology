import CertificateSyntax
import GlobalParitySufficiency

namespace OrthemicCertificate
open HiddenParity HiddenParity.Stage HiddenParity.Necessity

variable {q n k : ℕ}

@[simp] theorem Input.live_kernel (I : Input q n k) (hI : I.Valid) (B : Support q)
    (e : Pair n k) (y : Fin n) : I.live B e y = liveUpdate (I.kernel hI) B e y := by
  ext σ
  simp [Input.live, liveUpdate, Input.kernel]

theorem Component.link_exists {c : Component n k} {s : Fin n}
    (hkeys : (c.links.map Link.state).toFinset = c.used) (hs : s ∈ c.used) :
    ∃ l ∈ c.links, l.state = s := by
  rw [← hkeys, List.mem_toFinset, List.mem_map] at hs
  exact hs

/-- Submitted graph evidence establishes the inherited actual Markov component,
including full numerical rows and the candidate's actual no-exit condition. -/
theorem Component.valid_sound {I : Input q n k} (hI : I.Valid) {B : Support q}
    {θ : Fin q} {A : Finset (Pair n k)} {c : Component n k} {entry : Fin n}
    (h : c.Valid I B θ A entry) :
    MarkovQualifying (I.kernel hI) Prod.fst B I.priority θ A c.pairs ∧
      entry ∈ usedStates Prod.fst c.pairs := by
  rcases h with ⟨hne,hsub,_,hentry,_,hkeys,hlinks,hedges,hparity⟩
  refine ⟨⟨hsub, ?_, ⟨hne, ?_, ?_, ?_⟩, ?_⟩, hentry⟩
  · intro e he y hy
    simpa using (hedges e he).2.2 y hy
  · intro e he
    simpa only [← Input.internal_kernel I hI B] using (hedges e he).1
  · intro e he
    simpa only [← Input.internal_kernel I hI B] using (hedges e he).2.1
  · intro s hs t ht
    obtain ⟨ls,hls,hss⟩ := Component.link_exists hkeys hs
    obtain ⟨lt,hlt,htt⟩ := Component.link_exists hkeys ht
    have hsroot := Path.valid_sound (hlinks ls hls).1
    have hroott := Path.valid_sound (hlinks lt hlt).2
    rw [hss] at hsroot
    rw [htt] at hroott
    simpa only [← Input.internal_kernel I hI B] using hsroot.trans hroott
  · intro σ hσ hm
    obtain ⟨e,he,hev,hmin⟩ := hparity σ hσ (fun f hf y => congrFun (hm f hf) y)
    exact ⟨I.priority σ e, ⟨⟨e,he,rfl⟩,hmin⟩,hev⟩

theorem Witness.valid_sound {I : Input q n k} (hI : I.Valid) {B : Support q}
    {A : Finset (Pair n k)} {s : Fin n} {θ : Fin q} (hθ : θ ∈ B)
    {w : Witness n k} (h : w.Valid I B A s θ) :
    ReachableExit (I.kernel hI) B θ A s ∨
      ∃ t ∈ markovTargetStates (I.kernel hI) Prod.fst B I.priority θ A,
        Reach Prod.fst (internalSuccessors (I.kernel hI) B) A s t := by
  cases w with
  | exit p e y =>
    rcases h with ⟨hp,he,hy,hproper⟩
    refine Or.inl ⟨e,he,?_,y,hy,?_,?_⟩
    · simpa only [← Input.internal_kernel I hI B] using Path.valid_sound hp
    · exact ⟨θ, Finset.mem_filter.mpr ⟨hθ,hy⟩⟩
    · simpa using hproper
  | target p c entry =>
    obtain ⟨hp,hc⟩ := h
    obtain ⟨hq,he⟩ := Component.valid_sound hI hc
    refine Or.inr ⟨entry, (markovTargetStates_exact _ _ _ _ _ _ _).mpr ⟨c.pairs,hq,he⟩,?_⟩
    simpa only [← Input.internal_kernel I hI B] using Path.valid_sound hp

theorem Node.obligation_exists {N : Node q n k} (hkeys : N.KeysValid)
    {s : Fin n} {θ : Fin q} (hs : s ∈ N.states) (hθ : θ ∈ N.support) :
    ∃ o ∈ N.obligations, o.state = s ∧ o.candidate = θ := by
  have hm : (s,θ) ∈ N.states ×ˢ N.support := Finset.mem_product.mpr ⟨hs,hθ⟩
  rw [← hkeys.2, List.mem_toFinset, List.mem_map] at hm
  obtain ⟨o,ho,heq⟩ := hm
  exact ⟨o,ho,congrArg Prod.fst heq,congrArg Prod.snd heq⟩

/-- The bounded fuel/descent bridge is explicit: fixedness alone is not used as
an unsupported greatest-fixed-point assertion. -/
theorem postfixed_subset_winning (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (W : Finset (Fin n))
    (hp : W ⊆ regionStep (I.kernel hI) I.menu I.priority B
      (winningRegion (I.kernel hI) I.menu I.priority) W) :
    W ⊆ winningRegion (I.kernel hI) I.menu I.priority B := by
  have hc : 0 < B.card := Finset.card_pos.mpr hB
  obtain ⟨t,ht⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hc)
  have he := regionStep_congr_lower (I.kernel hI) I.menu I.priority B
    (winningRegion (I.kernel hI) I.menu I.priority)
    (computedRegion (I.kernel hI) I.menu I.priority t) (by
      intro C hC
      have hcard := Finset.card_lt_card hC
      exact computedRegion_fuel_irrelevant _ _ _ C C.card t (le_refl _) (by omega))
  rw [he] at hp
  unfold winningRegion
  rw [ht, computedRegion, if_pos hB]
  exact postfixed_subset_descend _ (regionStep_mono _ _ _ _ _) hp (Finset.subset_univ _) _

/-- Query-independent soundness of every node in an accepted support DAG. -/
theorem body_sound {I : Input q n k} {c : Body q n k} (h : BodyValid I c) :
    ∀ N ∈ c, N.states ⊆ winningRegion (I.kernel h.1) I.menu I.priority N.support := by
  have all : ∀ B : Support q, ∀ N ∈ c, N.support = B →
      N.states ⊆ winningRegion (I.kernel h.1) I.menu I.priority B := by
    intro B
    induction B using Finset.strongInductionOn with
    | _ B ih =>
      intro N hNc hNB
      have hv := h.2.2 N hNc
      have hB : B.Nonempty := hNB ▸ hv.1
      have hA : N.pairs ⊆ regionAllowed (I.kernel h.1) I.menu B
          (winningRegion (I.kernel h.1) I.menu I.priority) N.states := by
        intro e he
        obtain ⟨hs,hm,hchildren⟩ := hv.2.2.1 e he
        apply (mem_regionAllowed _ _ _ _ _ _).mpr
        refine ⟨hs, by simpa only [hNB] using hm, ?_⟩
        intro y hC
        have hraw : (I.live N.support e y).Nonempty := by simpa [hNB] using hC
        have hchild := hchildren y hraw
        by_cases heq : I.live N.support e y = N.support
        · have hi : liveUpdate (I.kernel h.1) B e y = B := by simpa [hNB] using heq
          simpa only [heq,if_true,hi] using hchild
        · rw [if_neg heq] at hchild
          obtain ⟨hproper,C,hCc,hCB,hy⟩ := hchild
          have hcB : C.support ⊂ B := by simpa only [hCB,hNB] using hproper
          have hywin := ih C.support hcB C hCc rfl hy
          have hne : liveUpdate (I.kernel h.1) B e y ≠ B := by simpa [hNB] using heq
          rw [if_neg hne]
          simpa [hCB,hNB] using hywin
      apply postfixed_subset_winning I h.1 B hB N.states
      intro s hs
      apply (mem_regionStep _ _ _ _ _ _ _).mpr
      refine ⟨hs,?_⟩
      intro θ hθ
      obtain ⟨o,ho,hos,hoθ⟩ := Node.obligation_exists hv.2.1 hs (hNB.symm ▸ hθ)
      have hw := hv.2.2.2 o ho
      rw [hos,hoθ,hNB] at hw
      rcases Witness.valid_sound h.1 hθ hw with hx | ⟨t,ht,hpath⟩
      · exact Or.inl (reachableExit_mono _ _ _ hA hx)
      · exact Or.inr ⟨t,targetStates_mono _ _ _ _ hA ht,reach_mono hA hpath⟩
  intro N hN
  exact all N.support N hN rfl

/-- Acceptance entails the exact inherited common lawful almost-sure parity
policy existence claim. The checker never constructs or serializes that policy. -/
theorem check_sound [NeZero n] {I : Input q n k} {c : Body q n k} {B : Support q} {s : Fin n}
    (h : check I c B s = true) (d : Pair n k) :
    HiddenParity.Necessity.SemanticWinning (R := Unit)
      (I.kernel (check_iff I c B s |>.mp h).1.1) I.menu I.priority d B s := by
  obtain ⟨hv,_,N,hN,hB,hs⟩ := (check_iff I c B s).mp h
  have hwin := body_sound hv N hN hs
  rw [hB] at hwin
  exact (HiddenParity.Sufficiency.computed_region_iff_common_parity_policy _ _ _ B s d).mp hwin
end OrthemicCertificate
