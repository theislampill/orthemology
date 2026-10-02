import IndependentProductFamilies

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Set Finset
open scoped BigOperators
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
variable {Y : Type*} [MeasurableSpace Y]

def consOracle (z : Y × (ℕ → Y)) : ℕ → Y
  | 0 => z.1
  | n+1 => z.2 n

lemma consOracle_measurable : Measurable (consOracle (Y := Y)) := by
  apply measurable_pi_lambda
  intro n
  cases n with
  | zero => exact measurable_fst
  | succ n => exact (measurable_pi_apply n).comp measurable_snd

def headTailIndex : ℕ → Unit ⊕ ℕ
  | 0 => Sum.inl ()
  | n+1 => Sum.inr n

lemma headTailIndex_injective : Function.Injective headTailIndex := by
  intro n m h
  cases n <;> cases m <;> simp_all [headTailIndex]

/-- Head plus fresh iid tail is again the declared infinite iid experiment.
This identity supplies one-step continuation without conditioning on tails. -/
theorem iid_cons_law (q : Measure Y) [IsProbabilityMeasure q] :
    (q.prod (Measure.infinitePi (fun _ : ℕ => q))).map consOracle =
      Measure.infinitePi (fun _ : ℕ => q) := by
  classical
  let X : Unit → Y → Y := fun _ => id
  let Z : ℕ → (ℕ → Y) → Y := fun n ω => ω n
  have hi := independent_product_families q (Measure.infinitePi (fun _ : ℕ => q)) X Z
    (iIndepFun.of_subsingleton) (infinite_product_coordinates_independent (fun _ : ℕ => q))
  let untag : (k : Unit ⊕ ℕ) → FamilyValue (I := Unit) (J := ℕ) Y Y k → Y :=
    fun k => match k with | .inl _ => id | .inr _ => id
  have hm : ∀ k, Measurable (untag k) := by intro k; cases k <;> exact measurable_id
  have hj := (hi.comp untag hm).precomp headTailIndex_injective
  have hh : iIndepFun (fun n (z : Y × (ℕ → Y)) => consOracle z n)
      (q.prod (Measure.infinitePi (fun _ : ℕ => q))) := by
    convert hj using 1
    funext n z
    cases n <;> rfl
  have hcoord : ∀ n, (q.prod (Measure.infinitePi (fun _ : ℕ => q))).map
      (fun z => consOracle z n) = q := by
    intro n
    cases n with
    | zero => simp only [consOracle,Measure.map_fst_prod,measure_univ,one_smul]
    | succ n =>
      change (q.prod (Measure.infinitePi (fun _ : ℕ => q))).map ((fun ω => ω n) ∘ Prod.snd) = _
      rw [← Measure.map_map (measurable_pi_apply n) measurable_snd,Measure.map_snd_prod,
        measure_univ,one_smul,infinite_product_coordinate_law]
  apply Measure.eq_infinitePi
  intro I sets hsets
  rw [Measure.map_apply consOracle_measurable (MeasurableSet.pi I.countable_toSet hsets)]
  have he : consOracle ⁻¹' Set.pi (I : Set ℕ) sets =
      ⋂ n ∈ I, (fun z : Y × (ℕ → Y) => consOracle z n) ⁻¹' sets n := by
    ext z
    simp
  rw [he,hh.measure_inter_preimage_eq_mul I hsets]
  apply Finset.prod_congr rfl
  intro n hn
  rw [← Measure.map_apply (show Measurable (fun z : Y × (ℕ → Y) => consOracle z n) from
    (measurable_pi_apply n).comp consOracle_measurable) (hsets n hn),hcoord]
end Orthemology.Tranche3
