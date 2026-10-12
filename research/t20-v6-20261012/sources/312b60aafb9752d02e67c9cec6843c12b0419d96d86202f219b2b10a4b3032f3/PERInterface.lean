import FrozenCompilerMirror

/- A precise reduct-level endpoint result. This is not a HasE soundness proof. -/
namespace OpenTermStandardness

def arrowPER (R S : SatPER) : SatPER where
  rel := Arrow R.rel S.rel
  symm := by
    intro f g h x y hxy
    exact S.symm (h y x (R.symm hxy))
  trans := by
    intro f g h hfg hgh x y hxy
    have hyy := R.trans (R.symm hxy) hxy
    exact S.trans (hfg x y hxy) (hgh y y hyy)
  saturated := by
    intro f g f' g' hf hg h x y hxy
    exact S.saturated (.app hf (.refl x)) (.app hg (.refl y)) (h x y hxy)

def churchPER : SatPER where
  rel n m := ∀ R : SatPER, (arrowPER (arrowPER R R) (arrowPER R R)).rel n m
  symm := by
    intro n m h R
    exact (arrowPER (arrowPER R R) (arrowPER R R)).symm (h R)
  trans := by
    intro n m l hnm hml R
    exact (arrowPER (arrowPER R R) (arrowPER R R)).trans (hnm R) (hml R)
  saturated := by
    intro n m n' m' hn hm h R
    exact (arrowPER (arrowPER R R) (arrowPER R R)).saturated hn hm (h R)

theorem churchPER_dom (n : T) : churchPER.rel n n ↔ Church n := Iff.rfl

theorem iter_related (R : SatPER) {f g a b : T}
    (hfg : Arrow R.rel R.rel f g) (hab : R.rel a b) (k : Nat) :
    R.rel (iter f a k) (iter g b k) := by
  induction k with
  | zero => exact hab
  | succ k ih => exact hfg _ _ ih

/-- Converse direction: no global parametricity axiom is needed here either. -/
theorem uniformIter_church (n : T) (hn : UniformIter n) : Church n := by
  obtain ⟨k, hk⟩ := hn
  intro R f g hfg a b hab
  exact R.saturated (hk f a).symm (hk g b).symm (iter_related R hfg hab k)

/-- Exact domain characterization for this full-PER open-term interpretation. -/
theorem church_iff_uniformIter (n : T) : Church n ↔ UniformIter n :=
  ⟨church_standard n, uniformIter_church n⟩

/-- The tested Church interpretation is inhabited by every finite successor numeral. -/
theorem successorNumeral_church (k : Nat) : Church (successorNumeral k) := by
  intro R f g hfg a b hab
  exact R.saturated (successorNumeral_application k f a).symm
    (successorNumeral_application k g b).symm (iter_related R hfg hab k)

/-- Typed endpoint equality in this reduct, including heterogeneous related
    Church inputs. This is stronger than pointwise agreement on identical n. -/
theorem identity_q_related : (arrowPER churchPER churchPER).rel .i q := by
  intro n m hnm
  have hm : Church m := churchPER.trans (churchPER.symm hnm) hnm
  intro R f g hfg a b hab
  have h := hnm R f g hfg a b hab
  exact R.saturated
    (Conv.app (Conv.app (.i n) (.refl f)) (.refl a)).symm
    (church_scalar_fusion m hm g b) h

/-- Consequently this full-PER reduct cannot separate I and the compiler mirror q. -/
theorem no_reduct_separator : ¬ ¬ (arrowPER churchPER churchPER).rel .i q :=
  fun h => h identity_q_related

#print axioms church_iff_uniformIter
#print axioms successorNumeral_church
#print axioms identity_q_related
#print axioms no_reduct_separator
end OpenTermStandardness
