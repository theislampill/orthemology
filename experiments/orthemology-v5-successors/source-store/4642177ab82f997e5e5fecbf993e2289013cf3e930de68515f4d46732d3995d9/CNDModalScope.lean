/-
T20 analytical premise audit. No metaphysical possibility claim is made.
`Original` describes complete original production of a contribution in a
specified respect. It does not define the source's whole-existence nonreceipt.
`Received` is whole-existence reception, not reception of a token state.
-/
namespace CNDModalScope

universe u v x y

def CND {W : Type u} {A : Type v} {E : Type x} {R : Type y}
    (Original : W → A → E → R → Prop) : Prop :=
  ∀ w a b e r, Original w a e r → Original w b e r → a = b

def Role {W : Type u} {A : Type v} {E : Type x} {R : Type y}
    (Original : W → A → E → R → Prop) (w : W) (g : A) : Prop :=
  ∃ e r, Original w g e r

/-- Production-only positive bridge, with world-local contribution witnesses.
    `overlap` is an additional complete-provision premise, not mere ancestry. -/
theorem original_role_excludes_reception
    {W : Type u} {A : Type v} {E : Type x} {R : Type y}
    (Original : W → A → E → R → Prop) (Received : W → A → Prop)
    (Relevant : W → Prop) (g : A)
    (nondup : CND Original)
    (role : ∀ w, Relevant w → Role Original w g)
    (overlap : ∀ w e r, Relevant w → Received w g →
      Original w g e r → ∃ h, h ≠ g ∧ Original w h e r) :
    ∀ w, Relevant w → ¬ Received w g := by
  intro w hw hr
  obtain ⟨e, r, hg⟩ := role w hw
  obtain ⟨h, hne, hh⟩ := overlap w e r hw hr hg
  exact hne (nondup w h g e r hh hg)

/-- A hypothetical received state must give up original-role retention if
    CND and the complete-overlap bridge apply. This is the exact diagnostic. -/
theorem receipt_excludes_original_role
    {W : Type u} {A : Type v} {E : Type x} {R : Type y}
    (Original : W → A → E → R → Prop) (Received : W → A → Prop)
    (nondup : CND Original) (w : W) (g : A)
    (overlap : ∀ e r, Received w g → Original w g e r →
      ∃ h, h ≠ g ∧ Original w h e r)
    (hr : Received w g) : ¬ Role Original w g := by
  intro hrole
  obtain ⟨e, r, hg⟩ := hrole
  obtain ⟨h, hne, hh⟩ := overlap e r hr hg
  exact hne (nondup w h g e r hh hg)

/- Two worlds, two rigid agents, two effect labels, two causal respects.
   Every world is relevant (hence no accessibility-frame loophole).
   g=false and h=true exist and have standing power in both worlds.
   In actual world false, g originally produces effect false and h effect true.
   In alternative true, h is original for both effects; g's agency is derived.
   Effects are held fixed here only to strengthen the separation example.
-/
def existsAt (_w _a : Bool) : Prop := True
def standingPower (_w _a : Bool) : Prop := True
def production (w a e r : Bool) : Prop :=
  r = false ∧ ((e = false ∧ a = w) ∨ (e = true ∧ a = true))
def wholeReceived (w a : Bool) : Prop := w = true ∧ a = false
def derivedExercise (w a e r : Bool) : Prop :=
  w = true ∧ a = false ∧ e = false ∧ r = false

theorem switch_cnd : CND production := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_nonvacuous : ∀ w : Bool, ∃ a e r, production w a e r := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_necessary_bearer : ∀ w : Bool, existsAt w false := by intro; trivial
theorem switch_standing_power : ∀ w : Bool, standingPower w false := by intro; trivial
theorem switch_actual_original_role : Role production false false := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_actual_nonreceipt : ¬ wholeReceived false false := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_possible_receipt_assignment : ∃ w : Bool, wholeReceived w false := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_derived_agency : derivedExercise true false false false := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide
theorem switch_exercised_efficacy_in_both_worlds : ∀ w : Bool,
    production w false false false ∨ derivedExercise w false false false := by
  simp only [production, derivedExercise]
  decide
theorem switch_lacks_role_invariance : ¬ (∀ w : Bool, Role production w false) := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide

/-- Even the complete-overlap bridge can hold in the separation. Its
    antecedent includes retained original production, which the switch lacks. -/
theorem switch_overlap : ∀ (w e r : Bool), wholeReceived w false →
    production w false e r → ∃ h : Bool, h ≠ false ∧ production w h e r := by
  simp only [CND, Role, production, wholeReceived, derivedExercise]
  decide

/-- A genuine supplied token state does not entail whole-existence receipt.
    The same original producer persists; different causal respects remain typed. -/
def tokenOriginal (_w a _e : Bool) (r : Bool) : Prop := a = false ∧ r = false
def tokenReceived (_w a : Bool) : Prop := a = false
def noWholeReceipt (_w _a : Bool) : Prop := False
theorem token_cnd : CND tokenOriginal := by
  simp only [CND, Role, tokenOriginal, tokenReceived, noWholeReceipt]
  decide
theorem token_original_role : ∀ w : Bool, Role tokenOriginal w false := by
  simp only [CND, Role, tokenOriginal, tokenReceived, noWholeReceipt]
  decide
theorem token_reception_without_whole :
    tokenReceived true false ∧ ¬ noWholeReceipt true false := by
  simp only [CND, Role, tokenOriginal, tokenReceived, noWholeReceipt]
  decide

/- These type and quantifier checks require no classical choice, S5 axiom,
   fixed transworld effect, fixed token history or causal self-production. -/
#print axioms original_role_excludes_reception
#print axioms receipt_excludes_original_role
#print axioms switch_cnd
#print axioms switch_overlap
end CNDModalScope
