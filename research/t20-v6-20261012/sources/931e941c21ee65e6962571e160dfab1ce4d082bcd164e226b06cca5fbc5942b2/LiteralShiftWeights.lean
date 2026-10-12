import LiteralShiftPersistence
import Q8Measure

/-! Exact fair-Cantor stopping weights for the literal compiler classifier.
The proof counts the actual finite payload fibres, passes their floor dyadics
to the rational limit, and bounds the unresolved event by one cylinder at
every positive depth. No alternate sampler or probability assumption is used. -/

namespace P02.LiteralShift
open Set MeasureTheory Filter P02A2.Q8Measure
open scoped ENNReal Topology BigOperators

private theorem wordPayload_injective_length (u v : List Bool)
    (hl : u.length = v.length) (hp : wordPayload u = wordPayload v) : u = v := by
  induction u generalizing v with
  | nil => simpa using hl.symm
  | cons b u ih =>
      cases v with
      | nil => simp at hl
      | cons c v =>
          have hl' : u.length = v.length := by simpa using hl
          have hu := wordPayload_lt u
          have hv := wordPayload_lt v
          rw [hl'] at hu
          cases b <;> cases c <;> simp only [wordPayload, Bool.false_eq_true,
            ↓reduceIte, zero_mul, one_mul, zero_add] at hp
          · exact congrArg (false :: ·) (ih v hl' hp)
          · omega
          · rw [hl'] at hp; omega
          · rw [hl'] at hp
            exact congrArg (true :: ·) (ih v hl' (by omega))

private def payloadFin (k : ℕ) (w : Fin k → Bool) : Fin (2^k) :=
  ⟨wordPayload (List.ofFn w), by simpa using wordPayload_lt (List.ofFn w)⟩

private theorem payloadFin_bijective (k : ℕ) : Function.Bijective (payloadFin k) := by
  apply (Fintype.bijective_iff_injective_and_card _).mpr
  constructor
  · intro u v h
    apply List.ofFn_injective
    apply wordPayload_injective_length
    · simp
    · exact congrArg Fin.val h
  · simp

private noncomputable def payloadEquiv (k : ℕ) : (Fin k → Bool) ≃ Fin (2^k) :=
  Equiv.ofBijective _ (payloadFin_bijective k)

theorem streamPayload_measurable (k : ℕ) :
    Measurable (fun x : Cantor => wordPayload (streamPrefix x k)) := by
  exact (measurable_of_countable (fun w : Fin k → Bool => wordPayload (List.ofFn w))).comp
    (measurable_pi_lambda _ (fun i => measurable_pi_apply i.val))

private theorem fair_prefix (k : ℕ) (w : Fin k → Bool) :
    fairCantor {x | (fun i : Fin k => x i.val) = w} = (1/2 : ℝ≥0∞)^k := by
  let y : Cantor := fun n => if h : n < k then w ⟨n,h⟩ else false
  have he : {x : Cantor | (fun i : Fin k => x i.val) = w} =
      Set.pi (↑(Finset.range k) : Set ℕ) (fun n => {y n}) := by
    ext x
    constructor
    · intro hx n hn
      have hn' := Finset.mem_range.mp hn
      simpa [y, hn'] using congrFun hx ⟨n,hn'⟩
    · intro hx
      funext i
      simpa [y, i.isLt] using hx i.val (Finset.mem_range.mpr i.isLt)
  rw [he, fairCantor_cylinder, Finset.card_range]

theorem fair_payload_singleton (k v : ℕ) (hv : v < 2^k) :
    fairCantor {x | wordPayload (streamPrefix x k) = v} = (1/2 : ℝ≥0∞)^k := by
  let w := (payloadEquiv k).symm ⟨v,hv⟩
  have hw : wordPayload (List.ofFn w) = v :=
    congrArg Fin.val ((payloadEquiv k).apply_symm_apply ⟨v,hv⟩)
  have he : {x : Cantor | wordPayload (streamPrefix x k) = v} =
      {x | (fun i : Fin k => x i.val) = w} := by
    ext x
    constructor
    · intro hx
      apply List.ofFn_injective
      apply wordPayload_injective_length
      · simp
      · exact hx.trans hw.symm
    · intro hx
      change wordPayload (List.ofFn (fun i : Fin k => x i.val)) = v
      rw [hx]
      exact hw
  rw [he, fair_prefix]

theorem fair_payload_lt (k t : ℕ) (ht : t ≤ 2^k) :
    fairCantor {x | wordPayload (streamPrefix x k) < t} =
      t * (1/2 : ℝ≥0∞)^k := by
  have he : {x : Cantor | wordPayload (streamPrefix x k) < t} =
      ⋃ i : Fin t, {x | wordPayload (streamPrefix x k) = i.val} := by
    ext x
    simp only [Set.mem_setOf_eq, Set.mem_iUnion]
    constructor
    · intro hx; exact ⟨⟨_,hx⟩,rfl⟩
    · rintro ⟨i,hi⟩; rw [hi]; exact i.isLt
  rw [he, measure_iUnion]
  · simp only [fair_payload_singleton k _ (lt_of_lt_of_le (Fin.isLt _) ht)]
    simp
  · intro i j hij
    apply Set.disjoint_left.mpr
    intro x hi hj
    exact hij (Fin.ext (hi.symm.trans hj))
  · intro i
    exact (streamPayload_measurable k) (measurableSet_singleton i.val)

private theorem classify_false_iff (a b k : ℕ) (hb : 0 < b) (x : Cantor) :
    streamClassify a b x k = some false ↔
      wordPayload (streamPrefix x k) < a*2^k/b := by
  rw [streamClassify]
  split_ifs with h1 h2
  · simp only [true_iff]
    exact Nat.lt_of_succ_le ((Nat.le_div_iff_mul_le hb).mpr (by simpa [Nat.mul_comm] using h1))
  · simp only [Option.some.injEq, Bool.true_eq_false, false_iff, not_lt]
    by_contra h
    have hn : wordPayload (streamPrefix x k)+1 ≤ a*2^k/b := by omega
    exact h1 (by simpa [Nat.mul_comm] using (Nat.le_div_iff_mul_le hb).mp hn)
  · simp only [reduceCtorEq, false_iff, not_lt]
    by_contra h
    have hn : wordPayload (streamPrefix x k)+1 ≤ a*2^k/b := by omega
    exact h1 (by simpa [Nat.mul_comm] using (Nat.le_div_iff_mul_le hb).mp hn)

theorem fair_classify_false (a b k : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    fairCantor {x | streamClassify a b x k = some false} =
      (a*2^k/b : ℕ) * (1/2 : ℝ≥0∞)^k := by
  simp_rw [classify_false_iff a b k hb]
  apply fair_payload_lt
  apply (Nat.div_le_iff_le_mul_add_pred hb).mpr
  nlinarith [Nat.mul_le_mul_right (2^k) hab]

private theorem dyadic_floor_bounds (a b k : ℕ) (hb : 0 < b) :
    (a:ℝ)/b - (1/2:ℝ)^k ≤ (a*2^k/b : ℕ)/(2:ℝ)^k ∧
    (a*2^k/b : ℕ)/(2:ℝ)^k ≤ (a:ℝ)/b := by
  have hbR : (0:ℝ) < b := by exact_mod_cast hb
  have hpR : (0:ℝ) < (2:ℝ)^k := by positivity
  have hlo : ((a*2^k/b : ℕ):ℝ) * b ≤ (a:ℝ)*(2:ℝ)^k := by
    exact_mod_cast Nat.div_mul_le_self (a*2^k) b
  have hhi : (a:ℝ)*(2:ℝ)^k < (((a*2^k/b : ℕ):ℝ)+1)*b := by
    exact_mod_cast (by simpa [Nat.mul_comm] using Nat.lt_mul_div_succ (a*2^k) hb : a*2^k < (a*2^k/b+1)*b)
  constructor
  · rw [sub_le_iff_le_add]
    apply (div_le_iff₀ hbR).mpr
    rw [one_div_pow, ← add_div, div_mul_eq_mul_div]
    apply (le_div_iff₀ hpR).mpr
    nlinarith
  · rw [div_le_div_iff₀ hpR hbR]
    exact hlo

private theorem tendsto_dyadic_floor_real (a b : ℕ) (hb : 0 < b) :
    Tendsto (fun k : ℕ => (a*2^k/b : ℕ)/(2:ℝ)^k) atTop (𝓝 ((a:ℝ)/b)) := by
  have hpow : Tendsto (fun k : ℕ => (1/2:ℝ)^k) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num) (by norm_num)
  have hlow : Tendsto (fun k : ℕ => (a:ℝ)/b - (1/2:ℝ)^k) atTop (𝓝 ((a:ℝ)/b)) := by
    simpa using tendsto_const_nhds.sub hpow
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le hlow tendsto_const_nhds
    (fun k => (dyadic_floor_bounds a b k hb).1)
    (fun k => (dyadic_floor_bounds a b k hb).2)

private theorem tendsto_dyadic_floor (a b : ℕ) (hb : 0 < b) :
    Tendsto (fun k : ℕ => (a*2^k/b : ℕ) * (1/2 : ℝ≥0∞)^k) atTop
      (𝓝 ((a:ℝ≥0∞)/b)) := by
  have h := ENNReal.tendsto_ofReal (tendsto_dyadic_floor_real a b hb)
  have hbR : (0:ℝ) < b := by exact_mod_cast hb
  simp only [ENNReal.ofReal_div_of_pos hbR, ENNReal.ofReal_natCast] at h
  convert h using 1
  funext k
  rw [ENNReal.ofReal_div_of_pos (by positivity), ENNReal.ofReal_natCast,
    ENNReal.ofReal_pow (by norm_num), ENNReal.ofReal_ofNat]
  simp [div_eq_mul_inv, ENNReal.inv_pow]

def eventualSide (a b : ℕ) (side : Bool) : Set Cantor :=
  {x | ∃ k, 1 ≤ k ∧ streamClassify a b x k = some side}

theorem streamClassify_fibre_measurable (a b k : ℕ) (side : Bool) :
    MeasurableSet {x | streamClassify a b x k = some side} := by
  exact (streamPayload_measurable k) (Set.to_countable {v : ℕ |
    (if b*(v+1) ≤ a*2^k then some false else if a*2^k ≤ b*v then some true else none) = some side}).measurableSet

theorem eventualSide_eq_iUnion (a b : ℕ) (side : Bool) :
    eventualSide a b side = ⋃ k : ℕ, {x | streamClassify a b x (k+1) = some side} := by
  ext x
  simp only [eventualSide, Set.mem_setOf_eq, Set.mem_iUnion]
  constructor
  · rintro ⟨k,hk,h⟩
    obtain ⟨j,rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
    exact ⟨j,h⟩
  · rintro ⟨k,h⟩
    exact ⟨k+1,by omega,h⟩

theorem eventualSide_measurable (a b : ℕ) (side : Bool) : MeasurableSet (eventualSide a b side) := by
  rw [eventualSide_eq_iUnion]
  exact MeasurableSet.iUnion (fun k => streamClassify_fibre_measurable a b (k+1) side)

theorem fair_eventual_below (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    fairCantor (eventualSide a b false) = (a:ℝ≥0∞)/b := by
  rw [eventualSide_eq_iUnion]
  have hm : Monotone (fun k : ℕ => {x | streamClassify a b x (k+1) = some false}) := by
    intro k m hkm x hx
    exact streamClassify_persistent a b (k+1) (m+1) x false hb (by omega) hx
  have hμ := tendsto_measure_iUnion_atTop (μ := fairCantor) hm
  simp only [Function.comp_def, fair_classify_false a b _ hb hab] at hμ
  exact tendsto_nhds_unique hμ ((tendsto_dyadic_floor a b hb).comp (tendsto_add_atTop_nat 1))

def unresolvedSet (a b : ℕ) : Set Cantor :=
  {x | ∀ k, 1 ≤ k → streamClassify a b x k = none}

private theorem unresolved_payload_unique (a b k : ℕ)
    (x y : Cantor) (hx : streamClassify a b x k = none)
    (hy : streamClassify a b y k = none) :
    wordPayload (streamPrefix x k) = wordPayload (streamPrefix y k) := by
  simp only [streamClassify] at hx hy
  split_ifs at hx with hx1 hx2; try contradiction
  split_ifs at hy with hy1 hy2; try contradiction
  have hx1' : a*2^k < b*(wordPayload (streamPrefix x k)+1) := by omega
  have hy1' : a*2^k < b*(wordPayload (streamPrefix y k)+1) := by omega
  have hx2' : b*wordPayload (streamPrefix x k) < a*2^k := by omega
  have hy2' : b*wordPayload (streamPrefix y k) < a*2^k := by omega
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hmul := Nat.mul_le_mul_left b (Nat.succ_le_of_lt hlt)
    nlinarith
  · have hmul := Nat.mul_le_mul_left b (Nat.succ_le_of_lt hgt)
    nlinarith

theorem fair_unresolved_zero (a b : ℕ) (_hb : 0 < b) :
    fairCantor (unresolvedSet a b) = 0 := by
  by_cases h : (unresolvedSet a b).Nonempty
  · obtain ⟨y,hy⟩ := h
    apply le_antisymm _ (zero_le _)
    apply ge_of_tendsto' ((ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one
      (by norm_num : (1/2 : ℝ≥0∞) < 1)).comp (tendsto_add_atTop_nat 1))
    intro k
    calc
      fairCantor (unresolvedSet a b) ≤
          fairCantor {x | wordPayload (streamPrefix x (k+1)) = wordPayload (streamPrefix y (k+1))} := by
        apply measure_mono
        intro x hx
        exact unresolved_payload_unique a b (k+1) x y (hx _ (by omega)) (hy _ (by omega))
      _ = (1/2 : ℝ≥0∞)^(k+1) := fair_payload_singleton _ _ (by simpa using wordPayload_lt (streamPrefix y (k+1)))
  · rw [Set.not_nonempty_iff_eq_empty.mp h]
    exact measure_empty

theorem eventualSides_disjoint (a b : ℕ) (hb : 0 < b) :
    Disjoint (eventualSide a b false) (eventualSide a b true) := by
  apply Set.disjoint_left.mpr
  rintro x ⟨k,hk,hkc⟩ ⟨m,hm,hmc⟩
  have hl := streamClassify_persistent a b k (max k m) x false hb (le_max_left _ _) hkc
  have hu := streamClassify_persistent a b m (max k m) x true hb (le_max_right _ _) hmc
  rw [hl] at hu
  cases hu

theorem eventualSides_union (a b : ℕ) :
    eventualSide a b false ∪ eventualSide a b true = (unresolvedSet a b)ᶜ := by
  ext x
  simp only [Set.mem_union, eventualSide, unresolvedSet, Set.mem_setOf_eq, Set.mem_compl_iff]
  constructor
  · rintro (⟨k,hk,h⟩ | ⟨k,hk,h⟩) hu <;> have he := hu k hk <;> rw [h] at he <;> cases he
  · intro hu
    push_neg at hu
    obtain ⟨k,hk,h⟩ := hu
    cases hc : streamClassify a b x k with
    | none => exact (h hc).elim
    | some side => cases side with
      | false => exact Or.inl ⟨k,hk,hc⟩
      | true => exact Or.inr ⟨k,hk,hc⟩

theorem unresolvedSet_measurable (a b : ℕ) : MeasurableSet (unresolvedSet a b) := by
  have h := ((eventualSide_measurable a b false).union (eventualSide_measurable a b true)).compl
  rw [eventualSides_union, compl_compl] at h
  exact h

theorem fair_eventual_above (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    fairCantor (eventualSide a b true) = 1 - (a:ℝ≥0∞)/b := by
  have h : fairCantor (eventualSide a b false) + fairCantor (eventualSide a b true) = 1 := by
    rw [← measure_union (eventualSides_disjoint a b hb) (eventualSide_measurable a b true),
      eventualSides_union, measure_compl (unresolvedSet_measurable a b) (measure_ne_top _ _),
      fair_unresolved_zero a b hb, measure_univ, tsub_zero]
  rw [fair_eventual_below a b hb hab, add_comm] at h
  exact ENNReal.eq_sub_of_add_eq' (by norm_num) h

theorem fair_firstCut_below (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    fairCantor {x | ∃ k, FirstCut a b x k false} = (a:ℝ≥0∞)/b := by
  simp_rw [exists_firstCut_iff_classified a b _ false hb]
  exact fair_eventual_below a b hb hab

theorem fair_firstCut_above (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    fairCantor {x | ∃ k, FirstCut a b x k true} = 1 - (a:ℝ≥0∞)/b := by
  simp_rw [exists_firstCut_iff_classified a b _ true hb]
  exact fair_eventual_above a b hb hab

/-- The literal compiler's indefinitely unresolved boundary has probability zero. -/
theorem fair_unresolved (a b : ℕ) (hb : 0 < b) :
    fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0 :=
  fair_unresolved_zero a b hb

#print axioms fair_classify_false
#print axioms fair_unresolved_zero
#print axioms fair_unresolved
#print axioms fair_firstCut_below
#print axioms fair_firstCut_above

end P02.LiteralShift
