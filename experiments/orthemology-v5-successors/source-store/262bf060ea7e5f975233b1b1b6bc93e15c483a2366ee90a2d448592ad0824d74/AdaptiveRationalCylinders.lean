import RationalRejectionLaw

/-! History-adaptive common-policy laws, directly as events of the original bit tape. -/
namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

variable {H Y : Type*} [DecidableEq Y]

/-- Only accepted values update the history. The row may depend on that history,
while the rejection set is shared across every row and model. -/
def historyConstraints (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) : (n : ℕ) → H → (Fin n → Y) → (Fin n → ℕ) → List (Finset (Mealy.Block L))
  | 0, _, _, _ => []
  | n+1, h, ys, rs =>
      (List.replicate (rs 0) (rejectedBlocks L D hDB) ++ [receiptBlocks L D hDB (row h) (ys 0)]) ++
        historyConstraints L D hDB row update n (update h (ys 0)) (fun i => ys i.succ) (fun i => rs i.succ)

def historyJoint (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) (rs : Fin n → ℕ) : Set Cantor :=
  constraintEvent (historyConstraints L D hDB row update n h ys rs)

noncomputable def historyMass (D : ℕ) (row : H → Fin D → Y) (update : H → Y → H) :
    (n : ℕ) → H → (Fin n → Y) → ℝ≥0∞
  | 0, _, _ => 1
  | n+1, h, ys => (weight D (row h) (ys 0) : ℝ≥0∞)/D *
      historyMass D row update n (update h (ys 0)) (fun i => ys i.succ)

noncomputable def clockMass (L D n : ℕ) (rs : Fin n → ℕ) : ℝ≥0∞ :=
  ∏ i, ((1-(D : ℝ≥0∞)/(2^L : ℕ))^(rs i) * ((D : ℝ≥0∞)/(2^L : ℕ)))

theorem historyJoint_succ (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin (n+1) → Y) (rs : Fin (n+1) → ℕ) (x : Cantor) :
    x ∈ historyJoint L D hDB row update (n+1) h ys rs ↔
      x ∈ firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB (row h) (ys 0)) (rs 0) ∧
      shift ((rs 0+1)*L) x ∈ historyJoint L D hDB row update n (update h (ys 0))
        (fun i => ys i.succ) (fun i => rs i.succ) := by
  simp only [historyJoint, historyConstraints, constraintEvent_append, List.length_append,
    List.length_replicate, List.length_singleton, firstEvent]

theorem historyJoint_disjoint (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) :
    Pairwise (fun rs ss => Disjoint (historyJoint L D hDB row update n h ys rs)
      (historyJoint L D hDB row update n h ys ss)) := by
  induction n generalizing h with
  | zero => intro rs ss hne; exact False.elim (hne (Subsingleton.elim _ _))
  | succ n ih =>
      intro rs ss hne
      apply Set.disjoint_left.mpr
      intro x hr hs
      rw [historyJoint_succ] at hr hs
      by_cases he : rs 0 = ss 0
      · have ht : (fun i : Fin n => rs i.succ) ≠ (fun i => ss i.succ) := by
          intro ht
          apply hne
          funext i
          refine Fin.cases he (fun j => congrFun ht j) i
        exact Set.disjoint_left.mp (ih _ _ ht) hr.2 (by simpa only [he] using hs.2)
      · exact Set.disjoint_left.mp
          (firstEvent_disjoint _ _ (rejection_receipt_disjoint L D hDB (row h) (ys 0)) he) hr.1 hs.1

/-- Exact cylinder mass with specified chronological receipts and all rejection counts.
The row at each receipt is evaluated at the preceding accepted history. -/
theorem history_joint_probability (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H)
    (ys : Fin n → Y) (rs : Fin n → ℕ) :
    fairCantor (historyJoint L D hDB row update n h ys rs) =
      historyMass D row update n h ys * clockMass L D n rs := by
  induction n generalizing h with
  | zero => simp [historyJoint, historyConstraints, constraintEvent, historyMass, clockMass]
  | succ n ih =>
      have hsplit : fairCantor (historyJoint L D hDB row update (n+1) h ys rs) =
          fairCantor (firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB (row h) (ys 0)) (rs 0)) *
          fairCantor (historyJoint L D hDB row update n (update h (ys 0))
            (fun i => ys i.succ) (fun i => rs i.succ)) := by
        simp only [historyJoint, historyConstraints, firstEvent, measure_constraintEvent_product,
          List.map_append, List.prod_append]
      rw [hsplit, receipt_clock_factorization L D hD hDB, receipt_probability,
        rejection_count_probability, ih]
      simp only [historyMass, clockMass, Fin.prod_univ_succ]
      ac_rfl

theorem tsum_fin_product (n : ℕ) (f : Fin n → ℕ → ℝ≥0∞) :
    (∑' rs : Fin n → ℕ, ∏ i, f i (rs i)) = ∏ i, ∑' r, f i r := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [← (Fin.consEquiv (fun _ : Fin (n+1) => ℕ)).tsum_eq]
      simp only [Fin.consEquiv, Equiv.coe_fn_mk, Fin.prod_univ_succ, Fin.cons_zero, Fin.cons_succ]
      rw [ENNReal.tsum_prod']
      simp only [ENNReal.tsum_mul_left, ih, ENNReal.tsum_mul_right]

theorem clockMass_total (L D n : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L) :
    (∑' rs : Fin n → ℕ, clockMass L D n rs) = 1 := by
  unfold clockMass
  rw [tsum_fin_product n (fun _ r => (1-(D : ℝ≥0∞)/(2^L : ℕ))^r * ((D : ℝ≥0∞)/(2^L : ℕ)))]
  have hgeom : (∑' r : ℕ, (1-(D : ℝ≥0∞)/(2^L : ℕ))^r * ((D : ℝ≥0∞)/(2^L : ℕ))) = 1 := by
    rw [ENNReal.tsum_mul_right, ENNReal.tsum_geometric,
      ENNReal.sub_sub_cancel (by simp) (accepted_fraction_le_one L D hDB), ENNReal.inv_mul_cancel]
    · simp [ne_of_gt hD]
    · exact ENNReal.mul_ne_top (by simp) (ENNReal.inv_ne_top.mpr (by positivity))
  simp only [hgeom, Finset.prod_const_one]

/-- The complete finite accepted-receipt cylinder law, after summing all waiting counts. -/
theorem accepted_history_probability (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) :
    fairCantor (⋃ rs : Fin n → ℕ, historyJoint L D hDB row update n h ys rs) =
      historyMass D row update n h ys := by
  rw [measure_iUnion (historyJoint_disjoint L D hDB row update n h ys)
    (fun _ => measurableSet_constraintEvent _)]
  simp only [history_joint_probability L D hD hDB, ENNReal.tsum_mul_left,
    clockMass_total L D n hD hDB, mul_one]


theorem historyJoint_unique (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) {ys zs : Fin n → Y} {rs ss : Fin n → ℕ} {x : Cantor}
    (hy : x ∈ historyJoint L D hDB row update n h ys rs)
    (hz : x ∈ historyJoint L D hDB row update n h zs ss) : ys = zs ∧ rs = ss := by
  induction n generalizing h x with
  | zero => exact ⟨Subsingleton.elim _ _, Subsingleton.elim _ _⟩
  | succ n ih =>
      rw [historyJoint_succ] at hy hz
      obtain ⟨hr,hyz⟩ := first_receipt_unique L D hDB (row h) hy.1 hz.1
      have hz' : shift ((rs 0+1)*L) x ∈ historyJoint L D hDB row update n (update h (ys 0))
          (fun i => zs i.succ) (fun i => ss i.succ) := by simpa only [hr,hyz] using hz.2
      obtain ⟨hys,hrs⟩ := ih _ hy.2 hz'
      constructor
      · funext i; exact Fin.cases hyz (fun j => congrFun hys j) i
      · funext i; exact Fin.cases hr (fun j => congrFun hrs j) i

def acceptedHistory (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) : Set Cantor :=
  ⋃ rs : Fin n → ℕ, historyJoint L D hDB row update n h ys rs

theorem measurableSet_acceptedHistory (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) :
    MeasurableSet (acceptedHistory L D hDB row update n h ys) :=
  MeasurableSet.iUnion (fun _ => measurableSet_constraintEvent _)

theorem acceptedHistory_disjoint (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) :
    Pairwise (fun ys zs => Disjoint (acceptedHistory L D hDB row update n h ys)
      (acceptedHistory L D hDB row update n h zs)) := by
  intro ys zs hne
  apply Set.disjoint_left.mpr
  rintro x hy hz
  obtain ⟨rs,hrs⟩ := Set.mem_iUnion.mp hy
  obtain ⟨ss,hss⟩ := Set.mem_iUnion.mp hz
  exact hne (historyJoint_unique L D hDB row update n h hrs hss).1

theorem weight_sum [Fintype Y] (D : ℕ) (decode : Fin D → Y) : ∑ y, weight D decode y = D := by
  simpa [weight] using
    Finset.sum_card_fiberwise_eq_card_filter (Finset.univ : Finset (Fin D)) Finset.univ decode

theorem row_fraction_sum [Fintype Y] (D : ℕ) (hD : 0 < D) (decode : Fin D → Y) :
    (∑ y, (weight D decode y : ℝ≥0∞)/D) = 1 := by
  simp only [div_eq_mul_inv]
  rw [← Finset.sum_mul]
  have hh : (∑ y, (weight D decode y : ℝ≥0∞)) = D := by exact_mod_cast weight_sum D decode
  rw [hh, ENNReal.mul_inv_cancel (by exact_mod_cast ne_of_gt hD) (by simp)]

theorem historyMass_total [Fintype Y] (D : ℕ) (hD : 0 < D)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H) :
    ∑ ys : Fin n → Y, historyMass D row update n h ys = 1 := by
  induction n generalizing h with
  | zero => simp [historyMass]
  | succ n ih =>
      rw [← (Fin.consEquiv (fun _ : Fin (n+1) => Y)).sum_comp]
      simp only [Fin.consEquiv, Equiv.coe_fn_mk, historyMass, Fin.cons_zero, Fin.cons_succ]
      rw [Fintype.sum_prod_type]
      simp only [← Finset.mul_sum, ih, mul_one, row_fraction_sum D hD]

/-- At least n actual acceptances occur with probability one, for every n. -/
theorem n_receipts_probability [Fintype Y] (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H) :
    fairCantor (⋃ ys : Fin n → Y, acceptedHistory L D hDB row update n h ys) = 1 := by
  rw [measure_iUnion (acceptedHistory_disjoint L D hDB row update n h)
    (measurableSet_acceptedHistory L D hDB row update n h), tsum_fintype]
  simp only [acceptedHistory, accepted_history_probability L D hD hDB]
  exact historyMass_total D hD row update n h

/-- All finite accepted prefixes exist almost surely on the original bit tape. -/
theorem infinitely_many_receipts [Fintype Y] (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (h : H) :
    ∀ᵐ x ∂fairCantor, ∀ n, ∃ ys : Fin n → Y, x ∈ acceptedHistory L D hDB row update n h ys := by
  rw [ae_all_iff]
  intro n
  rw [ae_iff]
  have he : {x : Cantor | ¬∃ ys : Fin n → Y, x ∈ acceptedHistory L D hDB row update n h ys} =
      (⋃ ys : Fin n → Y, acceptedHistory L D hDB row update n h ys)ᶜ := by ext x; simp
  rw [he, measure_compl (MeasurableSet.iUnion (measurableSet_acceptedHistory L D hDB row update n h))
    (measure_ne_top _ _), n_receipts_probability L D hD hDB, measure_univ, tsub_self]


/-- Literal sequential execution predicate. Read successive width-L proposals until
sample returns some value, update only then, and continue on the unused suffix. -/
def delivers (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H) :
    (n : ℕ) → H → (Fin n → Y) → Cantor → Prop
  | 0, _, _, _ => True
  | n+1, h, ys, x => ∃ r : ℕ,
      (∀ i < r, sample L D (row h) (block L i x) = none) ∧
      sample L D (row h) (block L r x) = some (ys 0) ∧
      delivers L D row update n (update h (ys 0)) (fun i => ys i.succ) (shift ((r+1)*L) x)

/-- The probability events above are exactly the sequential sampler's accepted prefixes. -/
theorem delivers_iff_acceptedHistory (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) (x : Cantor) :
    delivers L D row update n h ys x ↔ x ∈ acceptedHistory L D hDB row update n h ys := by
  induction n generalizing h x with
  | zero => simp [delivers, acceptedHistory, historyJoint, historyConstraints, constraintEvent]
  | succ n ih =>
      constructor
      · rintro ⟨r,hr,hy,ht⟩
        obtain ⟨rs,hrs⟩ := Set.mem_iUnion.mp ((ih _ _ _).mp ht)
        apply Set.mem_iUnion.mpr
        refine ⟨Fin.cons r rs, ?_⟩
        rw [historyJoint_succ]
        simp only [Fin.cons_zero, Fin.cons_succ]
        refine ⟨?_,hrs⟩
        rw [firstEvent_iff]
        exact ⟨fun i hi => (sample_none_iff L D hDB (row h) _).mp (hr i hi),
          (sample_some_iff L D hDB (row h) _ _).mp hy⟩
      · intro hx
        obtain ⟨rs,hrs⟩ := Set.mem_iUnion.mp hx
        rw [historyJoint_succ,firstEvent_iff] at hrs
        refine ⟨rs 0, ?_, ?_, ?_⟩
        · intro i hi
          exact (sample_none_iff L D hDB (row h) _).mpr (hrs.1.1 i hi)
        · exact (sample_some_iff L D hDB (row h) _ _).mpr hrs.1.2
        · exact (ih _ _ _).mpr (Set.mem_iUnion.mpr ⟨_,hrs.2⟩)

theorem literal_sampler_history_law (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) :
    fairCantor {x | delivers L D row update n h ys x} = historyMass D row update n h ys := by
  have he : {x | delivers L D row update n h ys x} = acceptedHistory L D hDB row update n h ys := by
    ext x
    exact delivers_iff_acceptedHistory L D hDB row update n h ys x
  rw [he]
  exact accepted_history_probability L D hD hDB row update n h ys

end Orthemology.RationalLaw
