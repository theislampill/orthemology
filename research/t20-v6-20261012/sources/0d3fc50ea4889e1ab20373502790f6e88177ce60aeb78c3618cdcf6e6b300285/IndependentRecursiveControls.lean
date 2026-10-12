import P01RecursiveModel
namespace IndependentRecursiveControls
open OrthemologyV2 OrthemologyV3 P01D P01R

def arbitraryLinks (ρ τ : OEnv) (rs : ∀ n, Link (ρ n) (τ n)) : REnv where
  left := ρ
  right := τ
  rel := fun n => (rs n).rel
  endpoints := fun n => (rs n).endpoints
  respect := fun n => (rs n).respect

theorem arbitrary_link_environment_represented (ρ τ : OEnv)
    (rs : ∀ n, Link (ρ n) (τ n)) (n : Nat) :
    (arbitraryLinks ρ τ rs).at n = rs n := by
  apply P01R.link_ext
  intro t u
  rfl

def universalPER : PER where
  rel := fun _ _ => True
  sym := fun _ => True.intro
  trans := fun _ _ => True.intro
  raw := fun _ _ _ => True.intro

def crossLink : Link rawPER universalPER where
  rel := fun _ _ => True
  endpoints := fun _ => ⟨Conv.refl _, True.intro⟩
  respect := fun _ _ _ => True.intro

theorem nonempty_heterogeneous_link : crossLink.rel Term.i Term.k := True.intro

theorem polymorphic_identity_derivable : FiniteDerives .i identityCode :=
  .allI (.i (.var 0))

theorem recursive_all_identity_nonempty (ρ : OEnv) :
    ((P01R.interpret identityCode).obj ρ).dom .i :=
  finite_new_model_member polymorphic_identity_derivable ρ

theorem recursive_all_identity_heterogeneous (r : REnv) :
    (P01R.interpret identityCode).rel r .i .i :=
  finite_fundamental polymorphic_identity_derivable r

theorem bottom_has_no_finite_inhabitant (t : Term) : ¬ FiniteDerives t .bottom := by
  intro h
  have hmem := finite_new_model_member h (fun _ => rawPER)
  change False at hmem
  exact hmem

#print axioms arbitrary_link_environment_represented
#print axioms nonempty_heterogeneous_link
#print axioms recursive_all_identity_nonempty
#print axioms recursive_all_identity_heterogeneous
#print axioms bottom_has_no_finite_inhabitant
end IndependentRecursiveControls
