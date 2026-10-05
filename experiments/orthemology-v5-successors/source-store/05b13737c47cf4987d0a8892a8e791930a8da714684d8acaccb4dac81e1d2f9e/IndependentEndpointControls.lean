import P01DependentControls
import P01ContextualJ
namespace TypedNucleusIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01DF

/-- Both endpoint domains are nonempty; this relation is intentionally
    nonfunctional and supplies no equality reflection. -/
def totalRawLink : Link totalPER rawPER where
  rel := fun _ _ => True
  endpoints := fun _ => ⟨True.intro, Conv.refl _⟩
  respect := fun _ _ _ => True.intro

def rawTotalLink : Link rawPER totalPER where
  rel := fun _ _ => True
  endpoints := fun _ => ⟨Conv.refl _, True.intro⟩
  respect := fun _ _ _ => True.intro

theorem cross_links_do_not_reflect_right_equality :
    totalRawLink.rel .i .i ∧ totalRawLink.rel .i P01DF.skk ∧
    totalPER.rel .i .i ∧ ¬ rawPER.rel .i P01DF.skk := by
  exact ⟨True.intro,True.intro,True.intro,P01Source.I_SKK_not_convertible⟩

theorem cross_links_do_not_reflect_left_equality :
    rawTotalLink.rel .i .i ∧ rawTotalLink.rel P01DF.skk .i ∧
    totalPER.rel .i .i ∧ ¬ rawPER.rel .i P01DF.skk := by
  exact ⟨True.intro,True.intro,True.intro,P01Source.I_SKK_not_convertible⟩

/-- A one-sided Id predicate has a witness outside its claimed right PER. -/
theorem one_sided_id_endpoint_restriction_fails :
    (totalPER.rel .i .i ∧ Conv Term.i .i ∧ Conv Term.i .i) ∧
    ¬ (IdPER rawPER .i P01DF.skk).dom .i := by
  refine ⟨⟨True.intro,.refl _,.refl _⟩,?_⟩
  intro h
  exact P01Source.I_SKK_not_convertible h.1

/-- Unformed syntax cannot have the candidate's lawful transport theorem. -/
theorem untyped_raw_family_transport_fails (ρ : OEnv) :
    ∃ (P : PER) (x y : Term), P.rel x y ∧
      (IdPER rawPER x .i).dom .i ∧ ¬ (IdPER rawPER y .i).dom .i := by
  refine ⟨(P01R.interpret identityCode).obj ρ,.i,P01DF.skk,?_,
    ⟨.refl _,.refl _,.refl _⟩,?_⟩
  · exact ((P01R.interpret identityCode).identity ρ _ _).mp
      (recursive_polymorphic_I_skk (diagEnv ρ))
  · intro h
    exact P01Source.I_SKK_not_convertible h.1.symm

theorem proof_coordinate_invariance_is_not_optional :
    ¬ (∀p q, Conv p q → inspectProof p = inspectProof q) :=
  proof_inspection_not_coherent

/-- Open conversion can erase an otherwise out-of-scope argument. -/
def PolyScoped (n : Nat) : Poly → Prop
  | .var k => k < n
  | .atom _ => True
  | .app f a => PolyScoped n f ∧ PolyScoped n a

theorem raw_conversion_does_not_preserve_scope :
    ∃ p q : Poly, P01DF.PolyConv p q ∧ PolyScoped 0 p ∧ ¬ PolyScoped 0 q := by
  refine ⟨.atom .i,.app (.app (.atom .k) (.atom .i)) (.var 0),
    .symm (.k _ _),True.intro,?_⟩
  intro h
  exact Nat.not_lt_zero 0 h.2

#print axioms raw_conversion_does_not_preserve_scope
#print axioms cross_links_do_not_reflect_right_equality
#print axioms cross_links_do_not_reflect_left_equality
#print axioms one_sided_id_endpoint_restriction_fails
#print axioms untyped_raw_family_transport_fails
#print axioms proof_coordinate_invariance_is_not_optional
end TypedNucleusIndependentReview
