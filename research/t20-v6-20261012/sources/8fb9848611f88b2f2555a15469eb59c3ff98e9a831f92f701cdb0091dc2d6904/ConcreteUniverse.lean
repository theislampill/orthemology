import HomogeneousPER
import CaseOperational

/-! Instantiation of the conditional closure results in the checked SKI + case term algebra.
This establishes the concrete eligible universe and Church inhabitant, not source soundness. -/
namespace ConcreteUniverse
open CaseOperational HomogeneousPER

 def S : Applicative T where
  app := T.app
  conv := Conv
  conv_refl := Conv.refl
  conv_sym := Conv.symm
  conv_trans := Conv.trans
  app_congr := Conv.app
  K := .k
  KI := .app .k .i

 def H : Strata S where
  Atom := AtomVal
  Fun := FunVal
  disjoint := atom_not_fun
  strict := head_origin

 abbrev U := Eligible H

 theorem bottom_eligible : U (fun _ _ => False) := eligible_empty H
 theorem top_eligible : U (fun _ _ => True) := eligible_universal H

 theorem i_class_support (x : T) (h : Conv x .i) : FunVal x := ⟨.i, .i, h⟩

 theorem i_eligible : U (fun x y => Conv x .i ∧ Conv y .i) := by
  refine ⟨?_, Or.inr (Or.inr (fun x xx => i_class_support x xx.1))⟩
  exact {
    sym := fun h => ⟨h.2, h.1⟩
    trans := fun h k => ⟨h.1, k.2⟩
    saturated := fun cx cy h => ⟨.trans (.symm cx) h.1, .trans (.symm cy) h.2⟩ }

 theorem identity_eligible (p : Prop) : U (fun x y => p ∧ Conv x .i ∧ Conv y .i) :=
  eligible_prop_class_fun H .i p i_class_support

 theorem nu_atom (f x : T) (hx : AtomVal x) : Conv (.app (.app .nu f) x) x := by
  rcases hx with h0 | h1
  · exact .trans (h0.right (.app .nu f)) (.trans (nu_atom0 f) (.symm h0))
  · exact .trans (h1.right (.app .nu f)) (.trans (nu_atom1 f) (.symm h1))

 theorem concrete_nu_church : Church H .nu .nu :=
  nu_church H .nu nu_atom (fun f _ hv => CaseOperational.nu_fun f hv)

 theorem concrete_church_eligible : U (Church H) := eligible_church H

 theorem concrete_inter_closed {I : Sort _} {R : I → Rel T} (h : ∀ i, U (R i)) :
    U (Inter R) := eligible_inter H h

 theorem concrete_pi_closed {A : Rel T} {B : T → Rel T} (a : U A)
    (b : ∀ x, A x x → U (B x)) (ext : Extensional A B) :
    U (Pi S A B) := eligible_pi H a b ext

 theorem concrete_sigma_closed {A : Rel T} {B : T → Rel T} (a : U A)
    (b : ∀ x, A x x → U (B x)) (ext : Extensional A B) :
    U (Sigma S A B) := eligible_sigma H a b ext

 theorem concrete_pi_nonuniversal_iff {A : Rel T} {B : T → Rel T} (a : U A)
    (b : ∀ x, A x x → U (B x)) :
    ¬ Universal (Pi S A B) ↔ ∃ x, A x x ∧ ¬ Universal (B x) :=
  pi_nonuniversal_iff a.1 (fun x xx => (b x xx).1) Conv.k

#print axioms concrete_nu_church
#print axioms concrete_church_eligible
#print axioms concrete_pi_closed
#print axioms concrete_sigma_closed
#print axioms identity_eligible
end ConcreteUniverse
