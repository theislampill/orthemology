import Mathlib

set_option autoImplicit false

namespace IndexedCompletion

open Set Filter
open scoped Topology

universe u
variable {X : ℕ → Type u}

/-- A genuinely nonstationary family of bonding maps between possibly different spaces. -/
abbrev Bonding (X : ℕ → Type u) := ∀ i : ℕ, X (i + 1) → X i

/-- Finite composition from remote coordinate j down to coordinate i. -/
def transport (f : Bonding X) (i j : ℕ) (h : i ≤ j) : X j → X i :=
  Nat.leRecOn (C := fun j => X j → X i) h (fun {k} g => g ∘ f k) id

@[simp] theorem transport_self (f : Bonding X) (i : ℕ) (x : X i) :
    transport f i i le_rfl x = x := by
  rw [transport, Nat.leRecOn_self]
  rfl

theorem transport_succ (f : Bonding X) (i j : ℕ) (h : i ≤ j) (x : X (j + 1)) :
    transport f i (j + 1) (by omega) x = transport f i j h (f j x) := by
  rw [transport, Nat.leRecOn_succ h]
  rfl

@[simp] theorem transport_one (f : Bonding X) (i : ℕ) (x : X (i + 1)) :
    transport f i (i + 1) (Nat.le_succ i) x = f i x := by
  rw [transport_succ f i i le_rfl, transport_self]

/-- Associativity of finite composites, without identifying any coordinate spaces. -/
theorem transport_comp (f : Bonding X) (i j k : ℕ) (hij : i ≤ j) (hjk : j ≤ k) (x : X k) :
    transport f i k (hij.trans hjk) x =
      transport f i j hij (transport f j k hjk x) := by
  induction k, hjk using Nat.le_induction with
  | base => simp
  | succ k hjk ih =>
      rw [transport_succ f i k (hij.trans hjk), transport_succ f j k hjk]
      exact ih (f k x)

/-- Leftmost bonding map of a finite composite. -/
theorem transport_left (f : Bonding X) (i j : ℕ) (h : i + 1 ≤ j) (x : X j) :
    transport f i j (by omega) x = f i (transport f (i + 1) j h x) := by
  rw [transport_comp f i (i + 1) j (Nat.le_succ i) h, transport_one]

def Compatible (f : Bonding X) (b : ∀ i, X i) : Prop := ∀ i, b i = f i (b (i + 1))

def Survives (f : Bonding X) (i : ℕ) (x : X i) : Prop :=
  ∀ j (h : i ≤ j), ∃ z : X j, transport f i j h z = x

def AllSingleton (f : Bonding X) : Prop :=
  ∀ i, ∃ e : X i, ∀ x, Survives f i x ↔ x = e

def UniqueRealization (f : Bonding X) : Prop := ∃! b : ∀ i, X i, Compatible f b

theorem compatible_transport (f : Bonding X) (b : ∀ i, X i) (hb : Compatible f b)
    (i j : ℕ) (h : i ≤ j) : transport f i j h (b j) = b i := by
  induction j, h using Nat.le_induction with
  | base => simp
  | succ j h ih => rw [transport_succ f i j h, ← hb j, ih]

theorem compatible_survives (f : Bonding X) (b : ∀ i, X i) (hb : Compatible f b)
    (i : ℕ) : Survives f i (b i) := fun j h => ⟨b j, compatible_transport f b hb i j h⟩

/-- Finite path chosen from one remote boundary; arbitrary later values are irrelevant. -/
noncomputable def finitePath [∀ i, Nonempty (X i)] (f : Bonding X) (j : ℕ) (z : X j) :
    ∀ i, X i := fun i => if h : i ≤ j then transport f i j h z else Classical.choice inferInstance

@[simp] theorem finitePath_at [∀ i, Nonempty (X i)] (f : Bonding X) (j : ℕ) (z : X j)
    (i : ℕ) (h : i ≤ j) : finitePath f j z i = transport f i j h z := by
  simp [finitePath, h]

theorem finitePath_compatible [∀ i, Nonempty (X i)] (f : Bonding X) (j : ℕ) (z : X j)
    (i : ℕ) (h : i < j) : finitePath f j z i = f i (finitePath f j z (i + 1)) := by
  rw [finitePath_at f j z i (by omega), finitePath_at f j z (i + 1) (by omega)]
  exact transport_left f i j (by omega) z

section Topology
variable [∀ i, TopologicalSpace (X i)]

theorem transport_continuous (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (i j : ℕ) (h : i ≤ j) : Continuous (transport f i j h) := by
  induction j, h using Nat.le_induction with
  | base => simpa [transport, Nat.leRecOn_self] using (continuous_id : Continuous (fun x : X i => x))
  | succ j h ih =>
      have heq : transport f i (j + 1) (by omega) = (transport f i j h) ∘ f j := by
        funext x
        exact transport_succ f i j h x
      rw [heq]
      exact ih.comp (hf j)

end Topology
end IndexedCompletion
