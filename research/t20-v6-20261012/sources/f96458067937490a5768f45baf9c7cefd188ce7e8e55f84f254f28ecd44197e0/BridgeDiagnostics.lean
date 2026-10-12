import Std

/-!
T20 independent deep-dive: optional Lean candidates.

STATUS: NOT COMPILED IN THE PRODUCING SESSION. These are fully written proof
candidates, not a claimed Lean/kernel result. The verified replay for this
archive runs Python only. Compile this file separately with Lean 4.19.0 and
inspect its declarations and axiom output before assigning kernel credit.

No actual-world existence, divine uniqueness, causal interpretation, or
cognitive warrant follows merely from these predicate-level statements.
-/

namespace T20IndependentDeepDive

universe u v z

def Necessary {W : Type u} (p : W → Prop) : Prop := ∀ w, p w

theorem common_requisite
    {W : Type u} (P N R : W → Prop)
    (cover : ∀ w, P w ∨ N w)
    (p_requires : ∀ w, P w → R w)
    (n_requires : ∀ w, N w → R w) : Necessary R := by
  intro w
  rcases cover w with hp | hn
  · exact p_requires w hp
  · exact n_requires w hn

theorem all_witnesses_common_requisite
    {W : Type u} {I : Type v} (P R : W → Prop) (N : I → W → Prop)
    (cover : ∀ w, P w ∨ ∃ i, N i w)
    (p_requires : ∀ w, P w → R w)
    (all_require : ∀ i w, N i w → R w) : Necessary R := by
  intro w
  rcases cover w with hp | ⟨i, hi⟩
  · exact p_requires w hp
  · exact all_require i w hi

theorem no_deletion_of_common_requisite
    {W : Type u} (P N R : W → Prop)
    (cover : ∀ w, P w ∨ N w)
    (p_requires : ∀ w, P w → R w)
    (n_requires : ∀ w, N w → R w) : ¬ ∃ w, ¬ R w := by
  rintro ⟨w, absent⟩
  exact absent (common_requisite P N R cover p_requires n_requires w)

inductive World where
  | first | second | third
  deriving DecidableEq, Repr

def Positive : World → Prop
  | .first => True
  | _ => False

def Required : World → Prop
  | .third => False
  | _ => True

def NegativeWitness : Bool → World → Prop
  | false, .second => True
  | true, .third => True
  | _, _ => False

theorem rotating_cover : ∀ w, Positive w ∨ ∃ i, NegativeWitness i w := by
  intro w
  cases w with
  | first => exact Or.inl True.intro
  | second => exact Or.inr ⟨false, True.intro⟩
  | third => exact Or.inr ⟨true, True.intro⟩

theorem negative_implies_absence :
    ∀ i w, NegativeWitness i w → ¬ Positive w := by
  intro i w
  cases i <;> cases w <;> simp [NegativeWitness, Positive]

theorem positive_requires : ∀ w, Positive w → Required w := by
  intro w
  cases w <;> simp [Positive, Required]

theorem selected_negative_requires :
    ∀ w, NegativeWitness false w → Required w := by
  intro w
  cases w <;> simp [NegativeWitness, Required]

theorem no_uniform_negative_witness :
    ¬ ∃ i, ∀ w, Positive w ∨ NegativeWitness i w := by
  rintro ⟨i, h⟩
  cases i with
  | false => simpa [Positive, NegativeWitness] using h World.third
  | true => simpa [Positive, NegativeWitness] using h World.second

theorem requirement_is_not_necessary : ¬ Necessary Required := by
  intro h
  exact h World.third

/-- Simple rectangular special case of the compatibility-component theorem.
    Full modal recombination is an explicit hypothesis, not derived from aseity. -/
theorem rectangular_common_output
    {X : Type u} {Y : Type v} {Z : Type z}
    (f : X → Z) (g : Y → Z) (x0 : X) (y0 : Y)
    (equal_at_every_pair : ∀ x y, f x = g y) :
    (∀ x, f x = f x0) ∧ (∀ y, g y = f x0) := by
  constructor
  · intro x
    exact (equal_at_every_pair x y0).trans (equal_at_every_pair x0 y0).symm
  · intro y
    exact (equal_at_every_pair x0 y).symm

/-- Abstract mutual-partial-explanation lemma, at the singleton interface. -/
theorem mutual_partial_identity
    {F : Type u} (Part PE : F → F → Prop)
    (anti : ∀ x y, Part x y → Part y x → x = y)
    (nec : ∀ x y, PE x y → y ≠ x → ¬ Part y x → ¬ PE y x)
    (q r : F) (qr : PE q r) (rq : PE r q) : q = r := by
  classical
  by_contra hne
  have hne' : r ≠ q := fun h => hne h.symm
  have rp : Part r q := by
    by_contra h
    exact (nec q r qr hne' h) rq
  have qp : Part q r := by
    by_contra h
    exact (nec r q rq hne h) qr
  exact hne (anti q r qp rp)

/-- Total-explainer uniqueness and source weakening exclude any larger source. -/
theorem no_total_source_padding
    {F : Type u} (Part : F → F → Prop) (Total : F → Prop)
    (q r : F) (q_total : Total q)
    (unique : ∀ x, Total x → x = q)
    (weakening : ∀ x y, Total x → Part x y → Total y)
    (qr : Part q r) : r = q := by
  exact unique r (weakening q r q_total qr)

/-- Necessity of a bearer is not used to make a particular determination necessary. -/
theorem necessary_determination_transmits
    {W : Type u} (D E : W → Prop)
    (det : Necessary D) (law : ∀ w, D w → E w) : Necessary E := by
  intro w
  exact law w (det w)

#print axioms common_requisite
#print axioms all_witnesses_common_requisite
#print axioms no_deletion_of_common_requisite
#print axioms rotating_cover
#print axioms negative_implies_absence
#print axioms positive_requires
#print axioms selected_negative_requires
#print axioms no_uniform_negative_witness
#print axioms requirement_is_not_necessary
#print axioms rectangular_common_output
#print axioms mutual_partial_identity
#print axioms no_total_source_padding
#print axioms necessary_determination_transmits

end T20IndependentDeepDive
