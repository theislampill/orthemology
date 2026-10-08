import Init

/-!
Conditional source-owned veracity boundary. No metaphysical predicate is
defined by truthfulness. `K` is only the epistemic fragment the proof uses.
The arbitrary occasion type does not certify an exhaustive possibility space.
-/
namespace VeracityBoundary

universe u v w x y

structure Model (Source : Type u) (Occasion : Type v) (Token : Type w)
    (Content : Type x) (Exercise : Type y) where
  asserts : Occasion → Source → Token → Content → Prop
  trueAt : Occasion → Content → Prop
  knowsFalse : Occasion → Source → Content → Prop
  aware : Occasion → Source → Token → Content → Prop
  deliberate : Occasion → Source → Token → Prop
  exercise : Token → Exercise
  actual : Occasion → Source → Exercise → Prop
  fitting : Occasion → Source → Exercise → Prop
  shortcoming : Occasion → Source → Exercise → Prop

variable {S : Type u} {O : Type v} {T : Type w} {Q : Type x} {E : Type y}
variable (m : Model S O T Q E) (g : S)

def Counterfeit (c : O) (t : T) (q : Q) : Prop :=
  m.asserts c g t q ∧ m.knowsFalse c g q ∧
    m.aware c g t q ∧ m.deliberate c g t

def K : Prop := ∀ c t q, m.asserts c g t q → ¬ m.trueAt c q → m.knowsFalse c g q
def A : Prop := ∀ c t q, m.asserts c g t q → m.aware c g t q
def C : Prop := ∀ c t q, m.asserts c g t q → m.deliberate c g t
def D : Prop := ∀ c t q, Counterfeit m g c t q → m.shortcoming c g (m.exercise t)
def N : Prop := ∀ c e, m.shortcoming c g e → ¬ m.fitting c g e
def P : Prop := ∀ c e, m.actual c g e → m.fitting c g e
def ExerciseBridge : Prop :=
  ∀ c t q, m.asserts c g t q → m.actual c g (m.exercise t)
def Factive : Prop := ∀ c q, m.knowsFalse c g q → ¬ m.trueAt c q
def Veracity : Prop := ∀ c t q, m.asserts c g t q → m.trueAt c q
def NoCounterfeit : Prop := ∀ c t q, ¬ Counterfeit m g c t q
def Package : Prop := K m g ∧ A m g ∧ C m g ∧ D m g ∧ N m g ∧ P m g ∧ ExerciseBridge m g

/-- The primary theorem is local in awareness/control and needs no truth
    factivity assumption beyond the knowledge coverage direction it uses. -/
theorem controlled_token_true
    (knowledge : K m g) (classification : D m g) (purity : N m g)
    (conformance : P m g) (exerciseBridge : ExerciseBridge m g)
    {c : O} {t : T} {q : Q} (owned : m.asserts c g t q)
    (awareness : m.aware c g t q) (control : m.deliberate c g t) :
    m.trueAt c q :=
  Classical.byContradiction fun falseContent =>
    purity c (m.exercise t)
      (classification c t q ⟨owned, knowledge c t q owned falseContent, awareness, control⟩)
      (conformance c (m.exercise t) (exerciseBridge c t q owned))

/-- The universal conclusion requires the stated full semantic coverage. -/
theorem veracity_of_coverage
    (knowledge : K m g) (awareness : A m g) (control : C m g)
    (classification : D m g) (purity : N m g) (conformance : P m g)
    (exerciseBridge : ExerciseBridge m g) : Veracity m g :=
  fun c t q owned => controlled_token_true m g knowledge classification purity conformance
    exerciseBridge owned (awareness c t q owned) (control c t q owned)

theorem counterfeit_iff_false_under_coverage
    (knowledge : K m g) (awareness : A m g) (control : C m g)
    (factivity : Factive m g) {c : O} {t : T} {q : Q}
    (owned : m.asserts c g t q) :
    Counterfeit m g c t q ↔ ¬ m.trueAt c q :=
  ⟨fun h => factivity c q h.2.1,
    fun h => ⟨owned, knowledge c t q owned h, awareness c t q owned, control c t q owned⟩⟩

/-- A no-counterfeit leaf is not an independently weaker warrant under
    this semantic coverage. The broader normative package is not equated to T0. -/
theorem veracity_iff_no_counterfeit
    (knowledge : K m g) (awareness : A m g) (control : C m g)
    (factivity : Factive m g) : Veracity m g ↔ NoCounterfeit m g := by
  constructor
  · intro truth c t q counterfeit
    exact factivity c q counterfeit.2.1 (truth c t q counterfeit.1)
  · intro integrity c t q owned
    exact Classical.byContradiction fun falseContent =>
      integrity c t q ⟨owned, knowledge c t q owned falseContent,
        awareness c t q owned, control c t q owned⟩

/-- Constructive incompatibility form: no classical failed-premise disjunction
    is hidden in this diagnostic. -/
theorem false_excludes_package {c : O} {t : T} {q : Q}
    (owned : m.asserts c g t q) (falseContent : ¬ m.trueAt c q) : ¬ Package m g := by
  intro h
  exact h.2.2.2.2.1 c (m.exercise t)
    (h.2.2.2.1 c t q ⟨owned, h.1 c t q owned falseContent,
      h.2.1 c t q owned, h.2.2.1 c t q owned⟩)
    (h.2.2.2.2.2.1 c (m.exercise t) (h.2.2.2.2.2.2 c t q owned))

/-- Stronger informed ownership interpretation. This changes the assertion
    extension; it does not derive coverage for the original weak signature. -/
def informedOwnership : Model S O T Q E :=
  { m with asserts := fun c s t q =>
      m.asserts c s t q ∧ m.aware c s t q ∧ m.deliberate c s t }

theorem strong_awareness : A (informedOwnership m) g := fun _ _ _ h => h.2.1
theorem strong_control : C (informedOwnership m) g := fun _ _ _ h => h.2.2

theorem strong_veracity
    (knowledge : K m g) (classification : D m g) (purity : N m g)
    (conformance : P m g) (exerciseBridge : ExerciseBridge m g) :
    Veracity (informedOwnership m) g :=
  fun _ _ _ h => controlled_token_true m g knowledge classification purity conformance
    exerciseBridge h.1 h.2.1 h.2.2

/-- Exact identification needed to carry strong-interpretation truth back to
    the weak signature; neither this coverage nor its warrant is manufactured. -/
theorem strong_equals_base_iff_coverage :
    (∀ c t q, (informedOwnership m).asserts c g t q ↔ m.asserts c g t q) ↔
      (A m g ∧ C m g) := by
  constructor
  · intro h
    exact ⟨fun c t q ha => ((h c t q).mpr ha).2.1,
      fun c t q ha => ((h c t q).mpr ha).2.2⟩
  · intro h c t q
    exact ⟨fun ha => ha.1, fun ha => ⟨ha, h.1 c t q ha, h.2 c t q ha⟩⟩

end VeracityBoundary
