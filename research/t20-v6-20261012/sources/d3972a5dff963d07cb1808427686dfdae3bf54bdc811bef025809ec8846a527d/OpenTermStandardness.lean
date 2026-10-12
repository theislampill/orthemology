import Init

/- New isolated metatheorem. This does not import or prove a HasE judgement.
   The carrier consists of finite OPEN SKI terms. Polymorphic membership below
   ranges over ALL conversion-saturated PERs on that carrier. -/
namespace OpenTermStandardness

inductive T where
  | var : Nat → T
  | i : T
  | k : T
  | s : T
  | zero : T
  | one : T
  | app : T → T → T
  deriving DecidableEq, Repr

infixl:70 " ⬝ " => T.app

inductive Conv : T → T → Prop where
  | refl (t) : Conv t t
  | symm : Conv x y → Conv y x
  | trans : Conv x y → Conv y z → Conv x z
  | app : Conv f g → Conv x y → Conv (f ⬝ x) (g ⬝ y)
  | i (x) : Conv (T.i ⬝ x) x
  | k (x y) : Conv (T.k ⬝ x ⬝ y) x
  | s (f g x) : Conv (T.s ⬝ f ⬝ g ⬝ x) (f ⬝ x ⬝ (g ⬝ x))

def subst (σ : Nat → T) : T → T
  | .var n => σ n
  | .i => .i
  | .k => .k
  | .s => .s
  | .zero => .zero
  | .one => .one
  | .app f x => subst σ f ⬝ subst σ x

theorem Conv.subst {x y : T} (h : Conv x y) (σ : Nat → T) :
    Conv (subst σ x) (subst σ y) := by
  induction h with
  | refl x => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact .app ih ih'
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _

def bound : T → Nat
  | .var n => n + 1
  | .i | .k | .s | .zero | .one => 0
  | .app f x => max (bound f) (bound x)

theorem subst_fixed (t : T) (σ : Nat → T)
    (h : ∀ j, j < bound t → σ j = .var j) : subst σ t = t := by
  induction t with
  | var j => exact h j (Nat.lt_succ_self j)
  | i => rfl
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app f x ihf ihx =>
      change (subst σ f).app (subst σ x) = f.app x
      rw [ihf (fun j hj => h j (Nat.lt_of_lt_of_le hj (Nat.le_max_left _ _))),
          ihx (fun j hj => h j (Nat.lt_of_lt_of_le hj (Nat.le_max_right _ _)))]

def freshSubst (n f a : T) (j : Nat) : T :=
  if j = bound n then f else if j = bound n + 1 then a else .var j

theorem freshSubst_fixed (n f a : T) : subst (freshSubst n f a) n = n := by
  apply subst_fixed
  intro j hj
  have h₁ : j ≠ bound n := Nat.ne_of_lt hj
  have h₂ : j ≠ bound n + 1 := Nat.ne_of_lt (Nat.lt_trans hj (Nat.lt_succ_self _))
  simp [freshSubst, h₁, h₂]

def iter (f a : T) : Nat → T
  | 0 => a
  | n + 1 => f ⬝ iter f a n

theorem subst_iter (σ : Nat → T) (f a : T) (k : Nat) :
    subst σ (iter f a k) = iter (subst σ f) (subst σ a) k := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg (T.app (subst σ f)) ih

structure SatPER where
  rel : T → T → Prop
  symm : ∀ {x y}, rel x y → rel y x
  trans : ∀ {x y z}, rel x y → rel y z → rel x z
  saturated : ∀ {x y x' y'}, Conv x x' → Conv y y' → rel x y → rel x' y'

def Arrow (R S : T → T → Prop) (f g : T) : Prop :=
  ∀ x y, R x y → S (f ⬝ x) (g ⬝ y)

def ChurchAt (R : SatPER) (n : T) : Prop :=
  Arrow (Arrow R.rel R.rel) (Arrow R.rel R.rel) n n

def Church (n : T) : Prop := ∀ R : SatPER, ChurchAt R n

/- Equality restricted to the conversion-saturated f-orbit of a. The definition
   deliberately does not assume that distinct iteration counts are distinct. -/
def orbit (f a : T) : SatPER where
  rel x y := Conv x y ∧ ∃ k, Conv x (iter f a k)
  symm := by
    rintro x y ⟨hxy, k, hxk⟩
    exact ⟨hxy.symm, k, hxy.symm.trans hxk⟩
  trans := by
    rintro x y z ⟨hxy, k, hxk⟩ ⟨hyz, _⟩
    exact ⟨hxy.trans hyz, k, hxk⟩
  saturated := by
    rintro x y x' y' hx hy ⟨hxy, k, hxk⟩
    exact ⟨hx.symm.trans (hxy.trans hy), k, hx.symm.trans hxk⟩

theorem orbit_seed (f a : T) : (orbit f a).rel a a :=
  ⟨.refl _, 0, .refl _⟩

theorem orbit_step (f a : T) : Arrow (orbit f a).rel (orbit f a).rel f f := by
  rintro x y ⟨hxy, k, hxk⟩
  exact ⟨.app (.refl f) hxy, k + 1, .app (.refl f) hxk⟩

def UniformIter (n : T) : Prop :=
  ∃ k, ∀ f a, Conv (n ⬝ f ⬝ a) (iter f a k)

/-- A single fresh orbit test yields one count valid at EVERY erased application.
    Full PER membership is the premise, not derivability or parametricity. -/
theorem church_standard (n : T) (hn : Church n) : UniformIter n := by
  let u := T.var (bound n)
  let v := T.var (bound n + 1)
  have h := hn (orbit u v) u u (orbit_step u v) v v (orbit_seed u v)
  obtain ⟨k, hk⟩ := h.2
  refine ⟨k, ?_⟩
  intro f a
  have hs := hk.subst (freshSubst n f a)
  simpa only [subst, freshSubst_fixed, subst_iter, u, v, freshSubst,
    if_pos rfl, Nat.add_one_ne_self, if_false] using hs

/-- The proof in fact needs only this ONE PER instance for each n. -/
theorem one_fresh_orbit_suffices (n : T)
    (h : ChurchAt (orbit (.var (bound n)) (.var (bound n + 1))) n) :
    UniformIter n := by
  have hx := h (.var (bound n)) (.var (bound n)) (orbit_step _ _)
    (.var (bound n + 1)) (.var (bound n + 1)) (orbit_seed _ _)
  obtain ⟨k, hk⟩ := hx.2
  refine ⟨k, ?_⟩
  intro f a
  have hs := hk.subst (freshSubst n f a)
  simpa only [subst, freshSubst_fixed, subst_iter, freshSubst,
    if_pos rfl, Nat.add_one_ne_self, if_false] using hs

#print axioms church_standard
#print axioms one_fresh_orbit_suffices
end OpenTermStandardness
