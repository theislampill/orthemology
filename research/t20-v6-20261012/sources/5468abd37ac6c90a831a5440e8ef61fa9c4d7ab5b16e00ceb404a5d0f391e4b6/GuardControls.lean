import HomogeneousPER

/-! Counterexamples and positive controls for the hypotheses of homogeneous closure.
All finite checks use kernel-reduced `decide`, never native_decide. -/
namespace HomogeneousPER.GuardControls

abbrev D := Fin 3

namespace MissingExtensionality
 def S : Applicative D where
  app f x := if f = 1 then (if x = 0 then 1 else 0) else 2
  conv := Eq
  conv_refl := Eq.refl
  conv_sym := Eq.symm
  conv_trans := Eq.trans
  app_congr := by intros; subst_vars; rfl
  K := 0
  KI := 1

 def H : Strata S where
  Atom x := x = 0
  Fun x := x = 1
  disjoint := by decide
  strict := by decide

 def A : Rel D := fun _ _ => True
 def B (x : D) : Rel D := if x = 1 then (fun _ _ => True) else (fun _ _ => False)

 theorem base_eligible : Eligible H A := eligible_universal H
 theorem fibers_eligible (x : D) : Eligible H (B x) := by
  by_cases h : x = 1
  · simpa only [B, if_pos h] using eligible_universal H
  · simpa only [B, if_neg h] using eligible_empty H

 theorem family_not_extensional : ¬ Extensional A B := by
  intro h
  have eq := h 1 2 True.intro
  have yes : B 1 0 0 := by simp [B]
  rw [eq] at yes
  exact yes

 /-- Dropping extensionality is a real failure: even symmetry of Sigma is lost. -/
 theorem sigma_not_per : ¬ IsPER S (Sigma S A B) := by
  intro per
  have forward : Sigma S A B 1 0 := by simp [Sigma, A, B, first, second, S]
  have backward : ¬ Sigma S A B 0 1 := by simp [Sigma, A, B, first, second, S]
  exact backward (per.sym forward)
end MissingExtensionality

namespace MissingStrictness
 def S : Applicative D where
  app f _ := if f = 2 then 2 else 0
  conv := Eq
  conv_refl := Eq.refl
  conv_sym := Eq.symm
  conv_trans := Eq.trans
  app_congr := by intros; subst_vars; rfl
  K := 0
  KI := 1

 def Atom (x : D) := x = 0
 def Fun (x : D) := x = 1
 def A : Rel D := fun x y => x = 0 ∧ y = 0
 def Shape (R : Rel D) := Universal R ∨ Supported Atom R ∨ Supported Fun R

 theorem atom_fun_disjoint : ∀ x, Atom x → Fun x → False := by unfold Atom Fun; decide
 theorem base_shape : Shape A := Or.inr (Or.inl (fun _ h => h.1))
 theorem base_per : IsPER S A where
  sym := fun h => ⟨h.2, h.1⟩
  trans := fun h k => ⟨h.1, k.2⟩
  saturated := by intros; subst_vars; assumption

 theorem strictness_fails : ¬ (∀ f x, Atom (S.app f x) ∨ Fun (S.app f x) → Fun f) := by
  intro h
  have hf := h 0 0 (Or.inl rfl)
  exact (by unfold Fun; decide : ¬ Fun 0) hf

 /-- Both arguments 0 and 1 enter the Pi support, but 2 does not. -/
 theorem pi_not_homogeneous : ¬ Shape (Pi S A (fun _ => A)) := by
  intro h
  rcases h with all | atom | func
  · have bad := all 2 2 0 0 ⟨rfl, rfl⟩
    exact (by simp [A, S] : ¬ A (S.app 2 0) (S.app 2 0)) bad
  · have one : Pi S A (fun _ => A) 1 1 := by simp [Pi, A, S]
    exact (by unfold Atom; decide : ¬ Atom 1) (atom 1 one)
  · have zero : Pi S A (fun _ => A) 0 0 := by simp [Pi, A, S]
    exact (by unfold Fun; decide : ¬ Fun 0) (func 0 zero)
end MissingStrictness

namespace EmptyDomain
 /-- An empty domain makes every Pi universal even when every fiber is empty.
     A missing strict-fiber witness must not be invented off the domain support. -/
 theorem empty_pi_universal {D : Type} (S : Applicative D) (B : D → Rel D) :
    Universal (Pi S (fun _ _ => False) B) := by
  intro f g x y h
  exact False.elim h
end EmptyDomain

#print axioms MissingExtensionality.sigma_not_per
#print axioms MissingStrictness.pi_not_homogeneous
#print axioms EmptyDomain.empty_pi_universal
end HomogeneousPER.GuardControls
