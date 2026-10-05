import Mathlib

set_option autoImplicit false

namespace LawCompletion

open Set Filter
open scoped Topology

variable {X : Type*}

/-- The state survives every finite backward depth; witnesses can differ by depth. -/
def Survives (f : X → X) (x : X) : Prop := ∀ n : ℕ, ∃ y : X, f^[n] y = x

/-- Compatibility is required along one entire infinite backward sequence. -/
def Backward (f : X → X) (b : ℕ → X) : Prop := ∀ i : ℕ, b i = f (b (i + 1))

def SingletonSurvival (f : X → X) (e : X) : Prop := ∀ x, Survives f x ↔ x = e

def UniqueBackward (f : X → X) : Prop := ∃! b : ℕ → X, Backward f b

theorem backward_iterate (f : X → X) (b : ℕ → X) (hb : Backward f b)
    (i n : ℕ) : f^[n] (b (i + n)) = b i := by
  induction n generalizing i with
  | zero => simp
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      rw [show i + (n + 1) = (i + 1) + n by omega, ih]
      exact (hb i).symm

theorem backward_survives (f : X → X) (b : ℕ → X) (hb : Backward f b)
    (i : ℕ) : Survives f (b i) := by
  intro n
  exact ⟨b (i + n), backward_iterate f b hb i n⟩

theorem fixed_survives (f : X → X) (e : X) (he : f e = e) : Survives f e := by
  intro n
  refine ⟨e, ?_⟩
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, he]

theorem survives_forward (f : X → X) (x : X) (hx : Survives f x) :
    Survives f (f x) := by
  intro n
  obtain ⟨y, hy⟩ := hx n
  refine ⟨f y, ?_⟩
  rw [← Function.iterate_succ_apply, Function.iterate_succ_apply', hy]

theorem singleton_fixed (f : X → X) (e : X) (h : SingletonSurvival f e) : f e = e :=
  (h (f e)).mp (survives_forward f e ((h e).mpr rfl))

theorem singleton_unique_fixed (f : X → X) (e : X) (h : SingletonSurvival f e) :
    ∀ x, f x = x ↔ x = e := by
  intro x
  constructor
  · intro hx
    exact (h x).mp (fixed_survives f x hx)
  · intro hxe
    subst x
    exact singleton_fixed f e h

theorem singleton_unique_backward (f : X → X) (e : X) (h : SingletonSurvival f e) :
    UniqueBackward f := by
  refine ⟨fun _ => e, ?_, ?_⟩
  · intro i
    exact (singleton_fixed f e h).symm
  · intro b hb
    funext i
    exact (h (b i)).mp (backward_survives f b hb i)

theorem unique_backward_constant (f : X → X) (h : UniqueBackward f) :
    ∃ e, f e = e ∧ ∀ b, Backward f b → b = fun _ => e := by
  obtain ⟨b, hb, huniq⟩ := h
  have htail : (fun i => b (i + 1)) = b := huniq _ (fun i => hb (i + 1))
  have hstep (i : ℕ) : b (i + 1) = b i := congrFun htail i
  have hconst (i : ℕ) : b i = b 0 := by
    induction i with
    | zero => rfl
    | succ i ih => exact (hstep i).trans ih
  refine ⟨b 0, ?_, ?_⟩
  · calc
      f (b 0) = f (b (0 + 1)) := congrArg f (hstep 0).symm
      _ = b 0 := (hb 0).symm
  · intro c hc
    rw [huniq c hc]
    funext i
    exact hconst i

section Metric
variable [MetricSpace X]

/-- The epsilon formulation includes all starting states under one common bound. -/
def UniformAttraction (f : X → X) (e : X) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ n ≥ N, ∀ x : X, dist (f^[n] x) e < ε

def PointwiseAttraction (f : X → X) (e : X) : Prop :=
  ∀ x : X, Tendsto (fun n : ℕ => f^[n] x) atTop (𝓝 e)

theorem uniform_iff_tendstoUniformly (f : X → X) (e : X) :
    UniformAttraction f e ↔ TendstoUniformly (fun n : ℕ => f^[n]) (fun _ => e) atTop := by
  simp only [UniformAttraction, Metric.tendstoUniformly_iff, eventually_atTop, dist_comm]

theorem uniform_pointwise (f : X → X) (e : X) (h : UniformAttraction f e) :
    PointwiseAttraction f e := by
  intro x
  apply Metric.tendsto_atTop.mpr
  intro ε hε
  obtain ⟨N, hN⟩ := h ε hε
  exact ⟨N, fun n hn => hN n hn x⟩

theorem uniform_fixed_singleton (f : X → X) (e : X) (he : f e = e)
    (hu : UniformAttraction f e) : SingletonSurvival f e := by
  intro x
  constructor
  · intro hx
    apply eq_of_forall_dist_le
    intro ε hε
    obtain ⟨N, hN⟩ := hu ε hε
    obtain ⟨y, hy⟩ := hx N
    rw [← hy]
    exact (hN N le_rfl y).le
  · intro hxe
    subst x
    exact fixed_survives f e he

end Metric
end LawCompletion
