import Lean

/-!
Conditional algebraic closure for homogeneous saturated partial equivalence relations.
This file does not construct an applicative algebra and does not assume universe closure.
The dependent Pi/Sigma relations have exactly the shape used by FullPER.F.
-/
namespace HomogeneousPER

universe u v

abbrev Rel (D : Type u) := D → D → Prop

structure Applicative (D : Type u) where
  app : D → D → D
  conv : Rel D
  conv_refl : ∀ x, conv x x
  conv_sym : ∀ {x y}, conv x y → conv y x
  conv_trans : ∀ {x y z}, conv x y → conv y z → conv x z
  app_congr : ∀ {f g x y}, conv f g → conv x y → conv (app f x) (app g y)
  K : D
  KI : D

structure Strata {D : Type u} (S : Applicative D) where
  Atom : D → Prop
  Fun : D → Prop
  disjoint : ∀ {x}, Atom x → Fun x → False
  strict : ∀ {f x}, Atom (S.app f x) ∨ Fun (S.app f x) → Fun f

structure IsPER {D : Type u} (S : Applicative D) (R : Rel D) : Prop where
  sym : ∀ {x y}, R x y → R y x
  trans : ∀ {x y z}, R x y → R y z → R x z
  saturated : ∀ {x y x' y'}, S.conv x x' → S.conv y y' → R x y → R x' y'

theorem IsPER.left {D : Type u} {S : Applicative D} {R : Rel D}
    (h : IsPER S R) {x y} (xy : R x y) : R x x := h.trans xy (h.sym xy)

theorem IsPER.right {D : Type u} {S : Applicative D} {R : Rel D}
    (h : IsPER S R) {x y} (xy : R x y) : R y y := h.trans (h.sym xy) xy

def Universal {D : Type u} (R : Rel D) : Prop := ∀ x y, R x y

def Supported {D : Type u} (P : D → Prop) (R : Rel D) : Prop := ∀ x, R x x → P x

def Eligible {D : Type u} {S : Applicative D} (H : Strata S) (R : Rel D) : Prop :=
  IsPER S R ∧ (Universal R ∨ Supported H.Atom R ∨ Supported H.Fun R)

def Extensional {D : Type u} (A : Rel D) (B : D → Rel D) : Prop :=
  ∀ x y, A x y → B x = B y

def Inter {D : Type u} {I : Sort v} (R : I → Rel D) : Rel D :=
  fun x y => ∀ i, R i x y

def Pi {D : Type u} (S : Applicative D) (A : Rel D) (B : D → Rel D) : Rel D :=
  fun f g => ∀ x y, A x y → B x (S.app f x) (S.app g y)

def first {D : Type u} (S : Applicative D) (z : D) : D := S.app z S.K

def second {D : Type u} (S : Applicative D) (z : D) : D := S.app z S.KI

def Sigma {D : Type u} (S : Applicative D) (A : Rel D) (B : D → Rel D) : Rel D :=
  fun z w => A (first S z) (first S w) ∧ B (first S z) (second S z) (second S w)

def Arrow {D : Type u} (S : Applicative D) (A B : Rel D) : Rel D :=
  Pi S A (fun _ => B)

section Closure
variable {D : Type u} {S : Applicative D} (H : Strata S)

 theorem eligible_empty : Eligible H (fun _ _ => False) :=
  ⟨⟨False.elim, fun h _ => h, fun _ _ h => h⟩,
    Or.inr (Or.inl (fun _ h => False.elim h))⟩

 theorem eligible_universal : Eligible H (fun _ _ => True) :=
  ⟨⟨fun _ => True.intro, fun _ _ => True.intro, fun _ _ _ => True.intro⟩,
    Or.inl (fun _ _ => True.intro)⟩

 /-- A proposition-guarded conversion class is eligible whenever that class is Fun-supported. -/
 theorem eligible_prop_class_fun (c : D) (p : Prop)
    (support : ∀ x, S.conv x c → H.Fun x) :
    Eligible H (fun x y => p ∧ S.conv x c ∧ S.conv y c) := by
  refine ⟨?_, Or.inr (Or.inr (fun x xx => support x xx.2.1))⟩
  exact {
    sym := fun h => ⟨h.1, h.2.2, h.2.1⟩
    trans := fun h k => ⟨h.1, h.2.1, k.2.2⟩
    saturated := fun cx cy h => ⟨h.1,
      S.conv_trans (S.conv_sym cx) h.2.1,
      S.conv_trans (S.conv_sym cy) h.2.2⟩ }

 theorem per_inter {I : Sort v} {R : I → Rel D} (h : ∀ i, IsPER S (R i)) :
    IsPER S (Inter R) where
  sym := fun xy i => (h i).sym (xy i)
  trans := fun xy yz i => (h i).trans (xy i) (yz i)
  saturated := fun cx cy xy i => (h i).saturated cx cy (xy i)

 theorem eligible_inter {I : Sort v} {R : I → Rel D} (h : ∀ i, Eligible H (R i)) :
    Eligible H (Inter R) := by
  classical
  refine ⟨per_inter (fun i => (h i).1), ?_⟩
  by_cases all : ∀ i, Universal (R i)
  · exact Or.inl (fun x y i => all i x y)
  · have exists_strict : ∃ i, ¬ Universal (R i) := Classical.not_forall.mp all
    obtain ⟨i, hi⟩ := exists_strict
    rcases (h i).2 with univ | atom | func
    · exact False.elim (hi univ)
    · exact Or.inr (Or.inl (fun x xx => atom x (xx i)))
    · exact Or.inr (Or.inr (fun x xx => func x (xx i)))

 theorem per_pi {A : Rel D} {B : D → Rel D} (a : IsPER S A)
    (b : ∀ x, A x x → IsPER S (B x)) (ext : Extensional A B) :
    IsPER S (Pi S A B) where
  sym := by
    intro f g fg x y xy
    have byx := fg y x (a.sym xy)
    rw [← ext x y xy] at byx
    exact (b x (a.left xy)).sym byx
  trans := by
    intro f g h fg gh x y xy
    exact (b x (a.left xy)).trans (fg x x (a.left xy)) (gh x y xy)
  saturated := by
    intro f g f' g' cf cg fg x y xy
    exact (b x (a.left xy)).saturated
      (S.app_congr cf (S.conv_refl x)) (S.app_congr cg (S.conv_refl y)) (fg x y xy)

 /-- A supported input with a nonuniversal fiber forces every Pi inhabitant to be Fun. -/
 theorem pi_supported_fun_of_strict_fiber {A : Rel D} {B : D → Rel D}
    (b : ∀ x, A x x → Eligible H (B x))
    {x : D} (xx : A x x) (strict : ¬ Universal (B x)) :
    Supported H.Fun (Pi S A B) := by
  intro f ff
  have out := ff x x xx
  rcases (b x xx).2 with univ | atom | func
  · exact False.elim (strict univ)
  · exact H.strict (Or.inl (atom _ out))
  · exact H.strict (Or.inr (func _ out))

 /-- The converse requires constant-function realizers; it is not a consequence of
     strictness alone. The candidate combinatory algebra provides this K law. -/
 theorem pi_universal_iff {A : Rel D} {B : D → Rel D} (a : IsPER S A)
    (b : ∀ x, A x x → IsPER S (B x))
    (k_rule : ∀ c x, S.conv (S.app (S.app S.K c) x) c) :
    Universal (Pi S A B) ↔ ∀ x, A x x → Universal (B x) := by
  constructor
  · intro all x xx c d
    have out := all (S.app S.K c) (S.app S.K d) x x xx
    exact (b x xx).saturated (k_rule c x) (k_rule d x) out
  · intro all f g x y xy
    exact all x (a.left xy) _ _

 theorem pi_nonuniversal_iff {A : Rel D} {B : D → Rel D} (a : IsPER S A)
    (b : ∀ x, A x x → IsPER S (B x))
    (k_rule : ∀ c x, S.conv (S.app (S.app S.K c) x) c) :
    ¬ Universal (Pi S A B) ↔ ∃ x, A x x ∧ ¬ Universal (B x) := by
  classical
  rw [pi_universal_iff a b k_rule]
  constructor
  · intro h
    obtain ⟨x, hx⟩ := Classical.not_forall.mp h
    by_cases xx : A x x
    · exact ⟨x, xx, fun hu => hx (fun _ => hu)⟩
    · exact False.elim (hx (fun hh => False.elim (xx hh)))
  · intro h all
    obtain ⟨x, xx, strict⟩ := h
    exact strict (all x xx)

 theorem eligible_pi {A : Rel D} {B : D → Rel D} (a : Eligible H A)
    (b : ∀ x, A x x → Eligible H (B x)) (ext : Extensional A B) :
    Eligible H (Pi S A B) := by
  classical
  refine ⟨per_pi a.1 (fun x xx => (b x xx).1) ext, ?_⟩
  by_cases all : ∀ x, A x x → Universal (B x)
  · exact Or.inl (fun f g x y xy => all x (a.1.left xy) (S.app f x) (S.app g y))
  · have witness : ∃ x, A x x ∧ ¬ Universal (B x) := by
      obtain ⟨x, hx⟩ := Classical.not_forall.mp all
      by_cases xx : A x x
      · exact ⟨x, xx, fun univ => hx (fun _ => univ)⟩
      · exact False.elim (hx (fun h => False.elim (xx h)))
    obtain ⟨x, xx, strict⟩ := witness
    exact Or.inr (Or.inr (pi_supported_fun_of_strict_fiber H b xx strict))

 theorem per_sigma {A : Rel D} {B : D → Rel D} (a : IsPER S A)
    (b : ∀ x, A x x → IsPER S (B x)) (ext : Extensional A B) :
    IsPER S (Sigma S A B) where
  sym := by
    intro z w zw
    refine ⟨a.sym zw.1, ?_⟩
    rw [← ext _ _ zw.1]
    exact (b _ (a.left zw.1)).sym zw.2
  trans := by
    intro z w v zw wv
    refine ⟨a.trans zw.1 wv.1, ?_⟩
    have second_wv := wv.2
    rw [← ext _ _ zw.1] at second_wv
    exact (b _ (a.left zw.1)).trans zw.2 second_wv
  saturated := by
    intro z w z' w' cz cw zw
    have fz := S.app_congr cz (S.conv_refl S.K)
    have fw := S.app_congr cw (S.conv_refl S.K)
    have sz := S.app_congr cz (S.conv_refl S.KI)
    have sw := S.app_congr cw (S.conv_refl S.KI)
    refine ⟨a.saturated fz fw zw.1, ?_⟩
    have axz : A (first S z) (first S z') :=
      a.saturated (S.conv_refl _) fz (a.left zw.1)
    rw [← ext _ _ axz]
    exact (b _ (a.left zw.1)).saturated sz sw zw.2

 /-- In the universal-base case, extensionality makes every fiber literally equal. -/
 theorem family_constant_of_universal {A : Rel D} {B : D → Rel D}
    (a : Universal A) (ext : Extensional A B) (x y : D) : B x = B y := ext x y (a x y)

 theorem eligible_sigma {A : Rel D} {B : D → Rel D} (a : Eligible H A)
    (b : ∀ x, A x x → Eligible H (B x)) (ext : Extensional A B) :
    Eligible H (Sigma S A B) := by
  refine ⟨per_sigma a.1 (fun x xx => (b x xx).1) ext, ?_⟩
  rcases a.2 with univ | atom | func
  · have center := b S.K (univ S.K S.K)
    rcases center.2 with buniv | batom | bfunc
    · left
      intro z w
      refine ⟨univ _ _, ?_⟩
      rw [family_constant_of_universal univ ext (first S z) S.K]
      exact buniv _ _
    · right; right
      intro z zz
      have out := zz.2
      rw [family_constant_of_universal univ ext (first S z) S.K] at out
      exact H.strict (Or.inl (batom _ out))
    · right; right
      intro z zz
      have out := zz.2
      rw [family_constant_of_universal univ ext (first S z) S.K] at out
      exact H.strict (Or.inr (bfunc _ out))
  · right; right
    intro z zz
    exact H.strict (Or.inl (atom _ zz.1))
  · right; right
    intro z zz
    exact H.strict (Or.inr (func _ zz.1))

 theorem eligible_arrow {A B : Rel D} (a : Eligible H A) (b : Eligible H B) :
    Eligible H (Arrow S A B) := eligible_pi H a (fun _ _ => b) (fun _ _ _ => rfl)

end Closure

/- The Church relation quantifies over exactly the eligible relations, not all PERs. -/
def Church {D : Type u} {S : Applicative D} (H : Strata S) : Rel D :=
  fun m n => ∀ R : Rel D, Eligible H R → Arrow S (Arrow S R R) (Arrow S R R) m n

section Numeral
variable {D : Type u} {S : Applicative D} (H : Strata S) (nu : D)
variable (nu_atom : ∀ f x, H.Atom x → S.conv (S.app (S.app nu f) x) x)
variable (nu_fun : ∀ f x, H.Fun x → S.conv (S.app (S.app nu f) x) (S.app f x))

include nu_atom nu_fun

 /-- The case operator respects every pair of related endomaps in the universe. -/
 theorem nu_respects {R : Rel D} (r : Eligible H R) {f g x y : D}
    (fg : Arrow S R R f g) (xy : R x y) :
    R (S.app (S.app nu f) x) (S.app (S.app nu g) y) := by
  rcases r.2 with univ | atom | func
  · exact univ _ _
  · exact r.1.saturated
      (S.conv_sym (nu_atom f x (atom x (r.1.left xy))))
      (S.conv_sym (nu_atom g y (atom y (r.1.right xy)))) xy
  · exact r.1.saturated
      (S.conv_sym (nu_fun f x (func x (r.1.left xy))))
      (S.conv_sym (nu_fun g y (func y (r.1.right xy)))) (fg x y xy)

 theorem nu_church : Church H nu nu := by
  intro R r f g fg x y xy
  exact nu_respects H nu nu_atom nu_fun r fg xy

omit nu_atom nu_fun

 theorem eligible_church : Eligible H (Church H) := by
  let R : { R : Rel D // Eligible H R } → Rel D :=
    fun r => Arrow S (Arrow S r.val r.val) (Arrow S r.val r.val)
  have closed : Eligible H (Inter R) := eligible_inter H (fun r =>
    eligible_arrow H (eligible_arrow H r.property r.property)
      (eligible_arrow H r.property r.property))
  have eq : Church H = Inter R := by
    funext m n
    apply propext
    constructor
    · intro h r; exact h r.val r.property
    · intro h r hr; exact h ⟨r, hr⟩
  rw [eq]
  exact closed

end Numeral

#print axioms eligible_inter
#print axioms eligible_pi
#print axioms eligible_sigma
#print axioms nu_church
#print axioms eligible_church
end HomogeneousPER
