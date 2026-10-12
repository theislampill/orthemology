/- P01 U11 proposal. UNVERIFIED at Lean 4.19.0.
   Coherence in the proof coordinate is an explicit new hypothesis.
   This semantic lemma is NOT a contextual syntactic calculus or checker. -/
import EffectsAndDependence

namespace P01CoherentJ
open OrthemologyV2 OrthemologyV3

structure BasedMotive (A : Code) (x : Term) where
  fibre : Term → Term → Code
  coherent : ∀ {y z p q : Term},
    (equalityCode A x y).accepts p →
    (equalityCode A x z).accepts q →
    Conv y z → Conv p q → ∀ t,
    (fibre y p).accepts t ↔ (fibre z q).accepts t

theorem based_J {A : Code} {x y p d : Term}
    (C : BasedMotive A x)
    (h : (equalityCode A x y).accepts p)
    (hd : (C.fibre x .i).accepts d) :
    (C.fibre y p).accepts d := by
  have hr : (equalityCode A x x).accepts .i := equality_reflexive h.1
  exact (C.coherent hr h h.2.2.1 (.symm h.2.2.2) d).mp hd

def jTerm (d y p : Term) : Term :=
  .app (.app (.app .k (.app .k d)) y) p

theorem j_reduces (d y p : Term) : Red (jTerm d y p) d := by
  exact .tail (.left (.k (.app .k d) y) p)
    (.tail (.k d p) (.refl d))

theorem tracked_based_J {A : Code} {x y p d : Term}
    (C : BasedMotive A x)
    (h : (equalityCode A x y).accepts p)
    (hd : (C.fibre x .i).accepts d) :
    (C.fibre y p).accepts (jTerm d y p) := by
  exact (code_conversion (C.fibre y p) (red_conv (j_reduces d y p))).mpr
    (based_J C h hd)

theorem j_beta (d x : Term) : Conv (jTerm d x .i) d :=
  red_conv (j_reduces d x .i)

end P01CoherentJ

namespace P01CoherentJ
open OrthemologyV2 OrthemologyV3

theorem app_congr {f g x y : Term} (hf : Conv f g) (hx : Conv x y) :
    Conv (.app f x) (.app g y) :=
  .trans (Conv.left hf x) (Conv.right g hx)

theorem pair_congr {x x' y y' : Term} (hx : Conv x x') (hy : Conv y y') :
    Conv (pairTerm x y) (pairTerm x' y') := by
  unfold pairTerm
  exact app_congr
    (app_congr (.refl .s)
      (app_congr (.refl (.app .s .i)) (app_congr (.refl .k) hx)))
    (app_congr (.refl .k) hy)

/-- Sigma eta is valid on actual encoded Sigma inhabitants; it is NOT Pi eta. -/
theorem sigma_eta {A : Code} {B : CoherentFamily} {z : Term}
    (hz : (dependentSigma A B).accepts z) :
    Conv (pairTerm (firstTerm z) (secondTerm z)) z := by
  obtain ⟨x,y,hx,hy,hz⟩ := hz
  have hf : Conv (firstTerm z) x := .trans (Conv.left hz .k) (pair_first x y)
  have hs : Conv (secondTerm z) y :=
    .trans (Conv.left hz (.app .k .i)) (pair_second x y)
  exact .trans (pair_congr hf hs) (.symm hz)

end P01CoherentJ
