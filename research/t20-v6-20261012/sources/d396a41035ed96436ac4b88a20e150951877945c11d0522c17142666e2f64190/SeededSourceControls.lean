import SeededSourceHistories
namespace SeededSource.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC FiniteSidecar
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
-- Exact fixture constructed in rational_kernel.py and cross-checked against FIXTURE.json.
def fixture : Cubes := ⟨[[[0], [1]], [[0], [1]], [[0], [1]], [[0], [1]], [[1], [1]], [[1], [1]]], [[[0], [1]], [[0], [1]], [[0], [1]], [[1], [1]], [[1], [1]], [[1], [1]]], [[[0], [0]], [[0], [0]], [[0], [0]], [[0], [0]], [[0], [0]], [[0], [0]]]⟩
def joint (u : Nat) : Nat × Nat × Nat :=
  (cubeValue fixture.branch 0 0 u, cubeValue fixture.nextCoarse 0 0 u,
    cubeValue fixture.nextTag 0 0 u)
theorem joint_counts :
    ((List.range 6).map joint).count (0,0,0) = 3 ∧
    ((List.range 6).map joint).count (0,1,0) = 1 ∧
    ((List.range 6).map joint).count (1,1,0) = 2 := by decide
theorem joint_range : ∀ u ∈ List.range 6,
    joint u ∈ [(0,0,0),(0,1,0),(1,1,0)] := by decide
-- Actual unchanged Has typing, with seed supplied as an ordinary argument.
theorem fixture_typed : Has [] (sampler fixture) (arr Input Reply) := sampler_has _
theorem fixture_source_joint (u : Nat) :
    ReplyRepresents
      (eval (.app (sampler fixture) (seeded (inputNumeral u) (encodeState 0 0))) zeroEnv)
      (joint u) :=
  sampler_observes fixture (seeded_represents (canonical_obs u) (encoded_represents 0 0))
def actions : List (Cubes × Nat) := [(fixture,0),(fixture,5),(fixture,1)]
theorem history_codes : runCodes actions 0 0 = ([(0,0,0),(1,1,0),(1,1,0)],(1,0)) := by decide
theorem fixture_source_history :
    List.Forall₂ (fun r t => ReplyRepresents (eval r zeroEnv) t)
      (runSource (actions.map (fun cu => (cu.1,inputNumeral cu.2))) (encodeState 0 0)).1
      [(0,0,0),(1,1,0),(1,1,0)] := by
  have h := (SeededSource.runSource_observes actions (encoded_represents 0 0)).1
  rw [history_codes] at h
  exact h
-- Fallback does not enforce seed bounds or enabled menus.
theorem out_of_range_seed_falls_back : joint 6 = (0,0,0) := by decide
theorem fixture_closed : Closed 2 1 2 6 fixture := by
  intro z k u hz hk hu
  have hk0 : k = 0 := by omega
  subst k
  have hz01 : z = 0 ∨ z = 1 := by omega
  have hu6 : u = 0 ∨ u = 1 ∨ u = 2 ∨ u = 3 ∨ u = 4 ∨ u = 5 := by omega
  rcases hz01 with rfl | rfl <;> rcases hu6 with rfl | rfl | rfl | rfl | rfl | rfl <;> decide
#print axioms fixture_source_joint
#print axioms fixture_source_history
#print axioms joint_counts
end SeededSource.Controls
