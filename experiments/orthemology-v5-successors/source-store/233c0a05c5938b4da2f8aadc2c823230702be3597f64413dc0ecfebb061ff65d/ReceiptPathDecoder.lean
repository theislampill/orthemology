import LiteralSamplerExecution
import HistoryPathConsistency

/-! A total measurable accepted-receipt path, with its null fallback explicit.
Only a mathematical readout is totalized; execution never invents a receipt. -/
namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
variable {Y : Type*} [DecidableEq Y]

theorem first_report_unique {out : ℕ → Option Y} {r s : ℕ} {y z : Y}
    (hr : ∀ i < r, out i = none) (hy : out r = some y)
    (hs : ∀ i < s, out i = none) (hz : out s = some z) : r=s ∧ y=z := by
  have he : r=s := by
    by_contra h
    rcases lt_or_gt_of_ne h with h | h
    · rw [hs r h] at hy; contradiction
    · rw [hr s h] at hz; contradiction
  subst s
  exact ⟨rfl,Option.some.inj (hy.symm.trans hz)⟩

theorem reports_unique (n : ℕ) {ys zs : Fin n → Y} {out : ℕ → Option Y}
    (hy : reports n ys out) (hz : reports n zs out) : ys=zs := by
  induction n generalizing out with
  | zero => exact Subsingleton.elim _ _
  | succ n ih =>
      obtain ⟨r,hr,hy,ht⟩ := hy
      obtain ⟨s,hs,hz,hu⟩ := hz
      obtain ⟨hrs,hyz⟩ := first_report_unique hr hy hs hz
      subst s
      have hh := ih ht hu
      funext i
      exact Fin.cases hyz (fun j => congrFun hh j) i

theorem reports_take (m n : ℕ) (hmn : m ≤ n) (ys : Fin n → Y) (out : ℕ → Option Y)
    (h : reports n ys out) : reports m (fun i => ys (Fin.castLE hmn i)) out := by
  induction m generalizing n out with
  | zero => trivial
  | succ m ih =>
      cases n with
      | zero => omega
      | succ n =>
          obtain ⟨r,hr,hy,ht⟩ := h
          refine ⟨r,hr,hy, ?_⟩
          exact ih n (by omega) (fun i => ys i.succ) _ ht

section Measurability
variable [Fintype Y] [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable {Ω : Type*} [MeasurableSpace Ω]

theorem measurableSet_reports (n : ℕ) (ys : Fin n → Y) (out : Ω → ℕ → Option Y)
    (hout : ∀ k y, MeasurableSet {x | out x k = y}) : MeasurableSet {x | reports n ys (out x)} := by
  induction n generalizing out with
  | zero => simp only [reports]; exact MeasurableSet.univ
  | succ n ih =>
      have hnone (r : ℕ) : MeasurableSet {x | ∀ i < r, out x i = none} := by
        have hi (i : ℕ) : MeasurableSet {x | out x i = none} := hout i none
        simpa [Set.setOf_forall] using MeasurableSet.iInter (fun i => MeasurableSet.iInter (fun _hi : i < r => hi i))
      have hsome (r : ℕ) : MeasurableSet {x | out x r = some (ys 0)} :=
        hout r _
      have htail (r : ℕ) : MeasurableSet {x | reports n (fun i => ys i.succ) (fun i => out x (r+1+i))} :=
        ih _ _ (fun i => hout (r+1+i))
      simpa [reports,Set.setOf_exists,Set.setOf_and] using
        MeasurableSet.iUnion (fun r => (hnone r).inter ((hsome r).inter (htail r)))

variable [Inhabited Y]

/-- Pick the unique available accepted prefix and return its final coordinate.
If it does not exist, return `default` solely to totalize the mathematical map. -/
noncomputable def decodeReports (out : ℕ → Option Y) (n : ℕ) : Y := by
  classical
  exact if h : ∃ ys : Fin (n+1) → Y, reports (n+1) ys out
    then Classical.choose h (Fin.last n) else default

theorem decodeReports_of_reports (n : ℕ) (ys : Fin n → Y) (out : ℕ → Option Y)
    (h : reports n ys out) (i : Fin n) : decodeReports out i = ys i := by
  classical
  have hle : i.val+1 ≤ n := by omega
  let zs : Fin (i.val+1) → Y := fun j => ys (Fin.castLE hle j)
  have hz : reports (i.val+1) zs out := reports_take _ _ hle ys out h
  have hex : ∃ vs : Fin (i.val+1) → Y, reports (i.val+1) vs out := ⟨zs,hz⟩
  simp only [decodeReports,dif_pos hex]
  have he : Classical.choose hex = zs := reports_unique _ (Classical.choose_spec hex) hz
  rw [he]
  rfl

/-- Total decoder measurability is proved on all proposal streams, not just the
probability-one set where every receipt eventually exists. -/
theorem measurable_decodeReports (out : Ω → ℕ → Option Y)
    (hout : ∀ k y, MeasurableSet {x | out x k = y}) : Measurable (fun x => decodeReports (out x)) := by
  classical
  apply measurable_pi_lambda
  intro n
  apply measurable_to_countable
  intro x
  have hex : MeasurableSet {w | ∃ ys : Fin (n+1) → Y, reports (n+1) ys (out w)} := by
    simpa [Set.setOf_exists] using MeasurableSet.iUnion (fun ys => measurableSet_reports (n+1) ys out hout)
  have he : (fun w => decodeReports (out w) n) ⁻¹' {decodeReports (out x) n} =
      ({w | ¬∃ ys : Fin (n+1) → Y, reports (n+1) ys (out w)} ∩
        {w | (default : Y) = decodeReports (out x) n}) ∪
      ⋃ ys : Fin (n+1) → Y, {w | reports (n+1) ys (out w)} ∩
        {w | ys (Fin.last n) = decodeReports (out x) n} := by
    ext w
    simp only [Set.mem_preimage,Set.mem_singleton_iff,Set.mem_union,Set.mem_inter_iff,
      Set.mem_setOf_eq,Set.mem_iUnion]
    by_cases hw : ∃ ys : Fin (n+1) → Y, reports (n+1) ys (out w)
    · obtain ⟨ys,hy⟩ := hw
      have hh := decodeReports_of_reports (n+1) ys (out w) hy (Fin.last n)
      constructor
      · intro h
        exact Or.inr ⟨ys,hy,hh ▸ h⟩
      · rintro (⟨hn,_⟩ | ⟨zs,hz,he⟩)
        · exact False.elim (hn ⟨ys,hy⟩)
        · exact (decodeReports_of_reports (n+1) zs (out w) hz (Fin.last n)).trans he
    · simp only [decodeReports,dif_neg hw]
      simp only [hw,false_and,not_false_eq_true,true_and]
      constructor
      · exact Or.inl
      · rintro (h | ⟨ys,hy,_⟩)
        · exact h
        · exact False.elim (hw ⟨ys,hy⟩)
  rw [he]
  have hconst (p : Prop) : MeasurableSet {w : Ω | p} := by
    by_cases hp : p <;> simp [hp]
  exact (hex.compl.inter (hconst _)).union
    (MeasurableSet.iUnion (fun ys => (measurableSet_reports _ ys out hout).inter (hconst _)))

end Measurability
end Orthemology.RationalLaw

namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
variable {Y : Type*} [DecidableEq Y] [Fintype Y] [Inhabited Y]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable {Ω : Type*} [MeasurableSpace Ω]

def receiptCylinder (n : ℕ) (ys : Fin n → Y) : Set (ℕ → Y) :=
  {z | ∀ i : Fin n, z i = ys i}

theorem measurableSet_receiptCylinder (n : ℕ) (ys : Fin n → Y) :
    MeasurableSet (receiptCylinder n ys) := by
  unfold receiptCylinder
  simpa [Set.setOf_forall] using MeasurableSet.iInter (fun i : Fin n =>
    (measurable_pi_apply (i : ℕ) : Measurable (fun z : ℕ → Y => z i)) (measurableSet_singleton (ys i)))

theorem decodeReports_cylinder_iff (n : ℕ) (ys : Fin n → Y) (out : ℕ → Option Y)
    (h : ∃ zs : Fin n → Y, reports n zs out) :
    decodeReports out ∈ receiptCylinder n ys ↔ reports n ys out := by
  obtain ⟨zs,hz⟩ := h
  constructor
  · intro hx
    have he : zs = ys := by
      funext i
      exact (decodeReports_of_reports n zs out hz i).symm.trans (hx i)
    rwa [← he]
  · intro hy i
    exact decodeReports_of_reports n ys out hy i

/-- Fallbacks have no effect on any decoded cylinder when all finite receipts exist a.s. -/
theorem decoded_cylinder_eq_report_event (μ : Measure Ω) (out : Ω → ℕ → Option Y)
    (hout : ∀ k y, MeasurableSet {x | out x k = y})
    (hcomplete : ∀ᵐ x ∂μ, ∀ n, ∃ ys : Fin n → Y, reports n ys (out x))
    (n : ℕ) (ys : Fin n → Y) :
    (μ.map (fun x => decodeReports (out x))) (receiptCylinder n ys) =
      μ {x | reports n ys (out x)} := by
  rw [Measure.map_apply (measurable_decodeReports out hout) (measurableSet_receiptCylinder n ys)]
  apply measure_congr
  filter_upwards [hcomplete] with x hx
  exact propext (decodeReports_cylinder_iff n ys (out x) (hx n))

/-- Complete sequence laws are determined by the stated finite receipt cylinders. -/
theorem receipt_law_ext (μ ν : Measure (ℕ → Y)) [IsFiniteMeasure ν]
    (h : ∀ n ys, μ (receiptCylinder n ys) = ν (receiptCylinder n ys)) : μ=ν := by
  classical
  apply Orthemology.Tranche2.PolicyEmbedding.measure_eq_of_prefix_maps
  intro N
  apply Measure.ext_of_singleton
  intro y
  rw [Measure.map_apply (Preorder.measurable_frestrictLe N) (measurableSet_singleton _),
    Measure.map_apply (Preorder.measurable_frestrictLe N) (measurableSet_singleton _)]
  let ys : Fin (N+1) → Y := fun i => y ⟨i,Finset.mem_Iic.mpr (by omega)⟩
  have he : (Preorder.frestrictLe (π := fun _ : ℕ => Y) N) ⁻¹' {y} = receiptCylinder (N+1) ys := by
    ext z
    change (Preorder.frestrictLe N z = y) ↔ ∀ i : Fin (N+1), z i = ys i
    constructor
    · intro hh i
      exact congrFun hh ⟨i,Finset.mem_Iic.mpr (by omega)⟩
    · intro hh
      funext i
      exact hh ⟨i,by have := Finset.mem_Iic.mp i.property; omega⟩
  rw [he]
  exact h _ _

/-- Source-bound complete-law upgrade: supplying the actual finite report-event
probabilities and proving completion suffices; no whole-law adapter is assumed. -/
theorem decoded_law_eq_of_report_probabilities (μ : Measure Ω) (out : Ω → ℕ → Option Y)
    (hout : ∀ k y, MeasurableSet {x | out x k = y})
    (hcomplete : ∀ᵐ x ∂μ, ∀ n, ∃ ys : Fin n → Y, reports n ys (out x))
    (ν : Measure (ℕ → Y)) [IsFiniteMeasure ν]
    (hprob : ∀ n ys, μ {x | reports n ys (out x)} = ν (receiptCylinder n ys)) :
    μ.map (fun x => decodeReports (out x)) = ν := by
  apply receipt_law_ext
  intro n ys
  rw [decoded_cylinder_eq_report_event μ out hout hcomplete]
  exact hprob n ys

end Orthemology.RationalLaw
