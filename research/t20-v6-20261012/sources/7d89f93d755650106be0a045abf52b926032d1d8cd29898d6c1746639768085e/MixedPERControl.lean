import CaseOperational

/- A concrete excluded, proper, conversion-saturated mixed PER that rejects nu.
This is an adversarial control of the restriction, not a whole-source model. -/
namespace MixedPERControl
open CaseOperational
infixl:70 " @@ " => T.app

def j : T := .k @@ .a0

theorem a0_not_j : ¬ Conv .a0 j := by
  intro h
  exact atom_not_fun (t := T.a0) (Or.inl (.refl _)) ⟨j, .k1 _, h⟩

theorem i_not_j : ¬ Conv .i j := by
  intro h
  have h10 : Conv .a1 .a0 :=
    .trans (.symm (.i .a1)) (.trans (h.left .a1) (.k .a0 .a1))
  exact atom_distinct (.symm h10)

def C0 (t : T) : Prop := Conv t .a0 ∨ Conv t .i
def C1 (t : T) : Prop := Conv t j

theorem classes_disjoint {t} (h0 : C0 t) (h1 : C1 t) : False := by
  rcases h0 with h0 | hi
  · exact a0_not_j (.trans (.symm h0) h1)
  · exact i_not_j (.trans (.symm hi) h1)

def R (x y : T) : Prop := (C0 x ∧ C0 y) ∨ (C1 x ∧ C1 y)

theorem R_sym {x y} (h : R x y) : R y x := by
  rcases h with h | h
  · exact .inl ⟨h.2,h.1⟩
  · exact .inr ⟨h.2,h.1⟩

theorem R_trans {x y z} (h : R x y) (k : R y z) : R x z := by
  rcases h with h | h <;> rcases k with k | k
  · exact .inl ⟨h.1,k.2⟩
  · exact False.elim (classes_disjoint h.2 k.1)
  · exact False.elim (classes_disjoint k.1 h.2)
  · exact .inr ⟨h.1,k.2⟩

theorem C0_transport {t u} (h : Conv t u) (hc : C0 t) : C0 u := by
  rcases hc with ha | hi
  · exact .inl (.trans (.symm h) ha)
  · exact .inr (.trans (.symm h) hi)

theorem C1_transport {t u} (h : Conv t u) (hc : C1 t) : C1 u :=
  .trans (.symm h) hc

theorem R_saturated {x y x' y'} (hx : Conv x x') (hy : Conv y y')
    (h : R x y) : R x' y' := by
  rcases h with h | h
  · exact .inl ⟨C0_transport hx h.1,C0_transport hy h.2⟩
  · exact .inr ⟨C1_transport hx h.1,C1_transport hy h.2⟩

theorem mixed_related : R .a0 .i := .inl ⟨.inl (.refl _), .inr (.refl _)⟩
theorem j_related : R j j := .inr ⟨.refl _,.refl _⟩

theorem a0_not_related_j : ¬ R .a0 j := by
  intro h
  rcases h with h | h
  · exact classes_disjoint h.2 (.refl _)
  · exact a0_not_j h.1

def Arrow (A B : T → T → Prop) (f g : T) :=
  ∀ x y, A x y → B (f @@ x) (g @@ y)

def constantJ : T := .k @@ j

theorem constantJ_endomap : Arrow R R constantJ constantJ := by
  intro x y _
  exact R_saturated (.symm (.k j x)) (.symm (.k j y)) j_related

/-- A universe admitting this one ordinary saturated PER excludes the
    candidate nonparametric Church value. The restriction is substantive. -/
theorem nu_rejected_by_mixed_PER : ¬ Arrow (Arrow R R) (Arrow R R) .nu .nu := by
  intro h
  have outputs := h constantJ constantJ constantJ_endomap .a0 .i mixed_related
  have hl : Conv (.nu @@ constantJ @@ .a0) .a0 := nu_atom0 _
  have hr : Conv (.nu @@ constantJ @@ .i) j :=
    .trans (nu_fun constantJ (raw_fun_val .i)) (.k j .i)
  exact a0_not_related_j (R_saturated hl hr outputs)

/-- Both atom and function support occur; a proper nonhomogeneous universe
    element is doing the rejecting. -/
theorem support_mixes_tags : R .a0 .a0 ∧ R .i .i ∧ R j j :=
  ⟨.inl ⟨.inl (.refl _),.inl (.refl _)⟩,
   .inl ⟨.inr (.refl _),.inr (.refl _)⟩,j_related⟩

def HomogeneousOrUniversal (P : T → T → Prop) : Prop :=
  (∀ x y, P x y) ∨ (∀ x, P x x → AtomVal x) ∨ (∀ x, P x x → FunVal x)

/-- The actual rawAtom rule gives these two supports after the intended
    source embedding; within this universe it forces Raw to be universal. -/
theorem raw_support_forces_universal {P : T → T → Prop}
    (hP : HomogeneousOrUniversal P) (ha : P .a0 .a0) (hi : P .i .i) :
    ∀ x y, P x y := by
  rcases hP with ht | hat | hfn
  · exact ht
  · exact False.elim (atom_not_fun (hat _ hi) (raw_fun_val .i))
  · exact False.elim (atom_not_fun (t := T.a0) (.inl (.refl _)) (hfn _ ha))

theorem conversion_not_admissible : ¬ HomogeneousOrUniversal Conv := by
  intro h
  exact atom_distinct (raw_support_forces_universal h (.refl _) (.refl _) .a0 .a1)

#print axioms raw_support_forces_universal
#print axioms conversion_not_admissible
#print axioms R_sym
#print axioms R_trans
#print axioms R_saturated
#print axioms nu_rejected_by_mixed_PER
end MixedPERControl
