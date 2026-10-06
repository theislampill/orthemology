import DynamicInterlock

/-! Semantic complement/portfolio bridge, singleton incidence bound, and the
finite four-edge lemma used by the ordinary C(9,4,2) lower proof.  This does not
claim to formalize the whole repetition-incidence argument or all binomial
covering numbers. -/

namespace ChargedInterlock

def Contained (n : Nat) (c a : Nat → Bool) : Prop :=
  ∀ i, i < n → c i = true → a i = true

def IntactPath (n : Nat) (l c : Nat → Bool) : Prop :=
  ∀ i, i < n → l i = true → c i = false

theorem complement_path_iff (n : Nat) (a c : Nat → Bool) :
    IntactPath n (fun i => !a i) c ↔ Contained n c a := by
  constructor
  · intro intact i hi hc
    have h := intact i hi
    cases ha : a i <;> simp_all
  · intro contained i hi hl
    have h := contained i hi
    cases ha : a i <;> cases hc : c i <;> simp_all

def CoversMaximalFaults (n b : Nat) (blocks : List (Nat → Bool)) : Prop :=
  ∀ c, card n c = b → ∃ a, a ∈ blocks ∧ Contained n c a

def HasIntactPath (n b : Nat) (paths : List (Nat → Bool)) : Prop :=
  ∀ c, card n c = b → ∃ l, l ∈ paths ∧ IntactPath n l c

theorem covering_portfolio_equivalence (n b : Nat) (blocks : List (Nat → Bool)) :
    CoversMaximalFaults n b blocks ↔
      HasIntactPath n b (blocks.map (fun a i => !a i)) := by
  constructor
  · intro covering c hc
    obtain ⟨a, ha, hca⟩ := covering c hc
    refine ⟨(fun i => !a i), ?_, (complement_path_iff n a c).mpr hca⟩
    exact List.mem_map.mpr ⟨a, ha, rfl⟩
  · intro paths c hc
    obtain ⟨l, hl, intact⟩ := paths c hc
    obtain ⟨a, ha, heq⟩ := List.mem_map.mp hl
    subst l
    exact ⟨a, ha, (complement_path_iff n a c).mp intact⟩

theorem card_union_le (n : Nat) (a d : Nat → Bool) :
    card n (fun i => a i || d i) ≤ card n a + card n d := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    cases ha : a n <;> cases hd : d n <;> simp_all [card] <;> omega

def unionBlocks (blocks : List (Nat → Bool)) (i : Nat) : Bool :=
  blocks.any (fun a => a i)

def sumCards (n : Nat) : List (Nat → Bool) → Nat
  | [] => 0
  | a :: rest => card n a + sumCards n rest

theorem union_card_le_sum (n : Nat) (blocks : List (Nat → Bool)) :
    card n (unionBlocks blocks) ≤ sumCards n blocks := by
  induction blocks with
  | nil =>
    have empty : card n (fun _ => false) = 0 := by
      induction n with
      | zero => rfl
      | succ n ih => simpa [card] using ih
    change card n (fun _ => false) ≤ 0
    omega
  | cons a rest ih =>
    have step := card_union_le n a (unionBlocks rest)
    have funEq : unionBlocks (a :: rest) = (fun i => a i || unionBlocks rest i) := by
      funext i
      simp [unionBlocks]
    rw [funEq]
    simp only [sumCards]
    omega

theorem sum_cards_bound (n k : Nat) (blocks : List (Nat → Bool))
    (bounded : ∀ a, a ∈ blocks → card n a ≤ k) :
    sumCards n blocks ≤ blocks.length * k := by
  induction blocks with
  | nil => simp [sumCards]
  | cons a rest ih =>
    have ha := bounded a (by simp)
    have restBound : ∀ d, d ∈ rest → card n d ≤ k := by
      intro d hd
      exact bounded d (by simp [hd])
    have hr := ih restBound
    simp only [sumCards, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

theorem singleton_cover_incidence (n k : Nat) (blocks : List (Nat → Bool))
    (covers : ∀ i, i < n → ∃ a, a ∈ blocks ∧ a i = true)
    (bounded : ∀ a, a ∈ blocks → card n a ≤ k) :
    n ≤ blocks.length * k := by
  have full : ∀ i, i < n → unionBlocks blocks i = true := by
    intro i hi
    obtain ⟨a, ha, hit⟩ := covers i hi
    exact List.any_eq_true.mpr ⟨a, ha, hit⟩
  have hc := pointwise_full_card n (unionBlocks blocks) full
  have hu := union_card_le_sum n blocks
  have hs := sum_cards_bound n k blocks bounded
  omega

def fourVertexEdge : Nat → Nat × Nat
  | 0 => (0, 1)
  | 1 => (0, 2)
  | 2 => (0, 3)
  | 3 => (1, 2)
  | 4 => (1, 3)
  | _ => (2, 3)

def disjointEdges (a b : Nat × Nat) : Bool :=
  a.1 != b.1 && a.1 != b.2 && a.2 != b.1 && a.2 != b.2

def hasDisjointEdgePair (mask : Nat) : Bool :=
  (List.range 6).any fun i =>
    mask.testBit i && (List.range 6).any fun j =>
      mask.testBit j && disjointEdges (fourVertexEdge i) (fourVertexEdge j)

set_option maxRecDepth 8192 in
theorem four_distinct_edges_have_disjoint_pair :
    ∀ mask : Fin 64,
      card 6 (fun i => mask.val.testBit i) = 4 →
      hasDisjointEdgePair mask.val = true := by decide

#print axioms covering_portfolio_equivalence
#print axioms singleton_cover_incidence
#print axioms four_distinct_edges_have_disjoint_pair

end ChargedInterlock
