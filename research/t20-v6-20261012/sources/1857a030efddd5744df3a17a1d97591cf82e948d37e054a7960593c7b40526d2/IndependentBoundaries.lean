import SeededSourceHistories
namespace SeededSource.IndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC FiniteSidecar
example : cubeValue [[[7]], [[8]]] 0 0 0 = 7 := by decide
example : cubeValue [[[7]], [[8]]] 0 0 1 = 8 := by decide
example : cubeValue [[[7]], [[8]]] 0 0 2 = 0 := by decide
example : cubeValue [[[7]], [[8]]] 1 0 0 = 0 := by decide
example : cubeValue [[[7]], [[8]]] 0 1 0 = 0 := by decide
example : cubeValue [] 0 0 0 = 0 := by decide
-- Typing neither enforces a positive seed space nor row normalization.
example : Has [] (sampler ⟨[], [], []⟩) (arr Input Reply) := sampler_has _
example (c : Cubes) : Closed 1 1 1 0 c := by
  intro z k u hz hk hu
  omega
-- Incompatible coordinate shapes are accepted source data; joint-kernel assembly
-- must align them externally rather than deriving that from source typing.
def misaligned : Cubes := ⟨[[[1]], [[2]]], [[[0]]], [[[0]], [[4]]]⟩
example : cubeValue misaligned.branch 0 0 1 = 2 ∧
    cubeValue misaligned.nextCoarse 0 0 1 = 0 ∧
    cubeValue misaligned.nextTag 0 0 1 = 4 := by decide
example : ¬ Closed 1 1 3 2 misaligned := by
  intro h
  have hh := h 0 0 1 (by decide) (by decide) (by decide)
  have : cubeValue misaligned.nextTag 0 0 1 = 4 := by decide
  omega
example (p : Poly) : SeededSource.runSource [] p = ([],p) := rfl
end SeededSource.IndependentReview
