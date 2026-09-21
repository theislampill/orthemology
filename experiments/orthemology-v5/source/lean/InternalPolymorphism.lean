/-
Internal polymorphism with a genuinely internal universal code.
Self-contained: imports Init only. No additional logical axioms.

STATUS: authored formalisation; this session has no Lean executable. See
VERIFICATION.json. Source inspection is not kernel verification.

The semantics is a concrete uniform realisability model, not the full ambient
function-space interpretation of v1. No novelty is claimed for this method.
-/
import Init

namespace OrthemologyV2

/-- Actual program syntax, independent of the types and typing relation. -/
inductive Term where
  | i | k | s | zero | one
  | app : Term → Term → Term
  deriving DecidableEq, Repr

/-- Compatible combinatory computation. The reference evaluator chooses the
    weak-head strategy within this relation. Type instantiation is erased. -/
inductive Step : Term → Term → Prop where
  | i (x : Term) : Step (.app .i x) x
  | k (x y : Term) : Step (.app (.app .k x) y) x
  | s (f g x : Term) :
      Step (.app (.app (.app .s f) g) x) (.app (.app f x) (.app g x))
  | left {f g : Term} (h : Step f g) (x : Term) :
      Step (.app f x) (.app g x)
  | right (f : Term) {x y : Term} (h : Step x y) :
      Step (.app f x) (.app f y)

inductive Red : Term → Term → Prop where
  | refl (t : Term) : Red t t
  | tail {t u v : Term} : Step t u → Red u v → Red t v

def Red.one {t u : Term} (h : Step t u) : Red t u :=
  .tail h (.refl u)

theorem Red.left {t u : Term} (h : Red t u) (x : Term) :
    Red (.app t x) (.app u x) := by
  induction h with
  | refl => exact .refl _
  | tail h _ ih => exact .tail (.left h x) ih

/-- Semantic type codes. Stability, not derivability, defines membership. -/
structure Code where
  accepts : Term → Prop
  stable : ∀ {t u : Term}, Step t u → (accepts t ↔ accepts u)

/-- Decoding retains an actual program, not just a proof-irrelevant truth value. -/
def El (A : Code) : Type := {t : Term // A.accepts t}

namespace Code

def bottom : Code where
  accepts := fun _ => False
  stable := fun _ => Iff.rfl

def top : Code where
  accepts := fun _ => True
  stable := fun _ => Iff.rfl

theorem along (A : Code) {t u : Term} (h : Red t u) :
    A.accepts t ↔ A.accepts u := by
  induction h with
  | refl => exact Iff.rfl
  | tail h _ ih => exact (A.stable h).trans ih

def arrow (A B : Code) : Code where
  accepts := fun f => ∀ x : Term, A.accepts x → B.accepts (.app f x)
  stable := by
    intro f g h
    constructor
    · intro hf x hx
      exact (B.stable (.left h x)).mp (hf x hx)
    · intro hg x hx
      exact (B.stable (.left h x)).mpr (hg x hx)

/-- There is NO restriction of the quantifier domain to previously formed codes.
    In particular `all B` is itself one of the arguments ranged over. -/
def all (B : Code → Code) : Code where
  accepts := fun t => ∀ A : Code, (B A).accepts t
  stable := by
    intro t u h
    constructor
    · intro ht A
      exact ((B A).stable h).mp (ht A)
    · intro hu A
      exact ((B A).stable h).mpr (hu A)

/-- Term-indexed dependent products are also internally coded. Their function
    values are programs; they are not arbitrary ambient functions. -/
def pi (A : Code) (B : El A → Code) : Code where
  accepts := fun f => ∀ x : El A, (B x).accepts (.app f x.val)
  stable := by
    intro f g h
    constructor
    · intro hf x
      exact ((B x).stable (.left h x.val)).mp (hf x)
    · intro hg x
      exact ((B x).stable (.left h x.val)).mpr (hg x)

end Code

def instantiate {B : Code → Code} (t : El (Code.all B)) (A : Code) : El (B A) :=
  ⟨t.val, t.property A⟩

/-- A family is admissible for erased polymorphic abstraction precisely when
    ONE underlying program serves every instance. The condition is explicit. -/
structure UniformSection (B : Code → Code) where
  valueAt : (A : Code) → El (B A)
  uniform : ∀ A : Code, (valueAt A).val = (valueAt Code.top).val

def abstractPoly {B : Code → Code} (f : UniformSection B) : El (Code.all B) :=
  ⟨(f.valueAt Code.top).val, fun A => by
    have h := (f.valueAt A).property
    rw [f.uniform A] at h
    exact h⟩

def unpack {B : Code → Code} (t : El (Code.all B)) : UniformSection B where
  valueAt := instantiate t
  uniform := fun _ => rfl

theorem polymorphic_beta {B : Code → Code} (f : UniformSection B) (A : Code) :
    instantiate (abstractPoly f) A = f.valueAt A :=
  Subtype.ext (f.uniform A).symm

theorem polymorphic_eta {B : Code → Code} (t : El (Code.all B)) :
    abstractPoly (unpack t) = t := Subtype.ext rfl

/-- The exact internal self-instantiation demanded in the design contract. -/
def selfInstantiate {B : Code → Code} (t : El (Code.all B)) :
    El (B (Code.all B)) := instantiate t (Code.all B)

theorem selfInstantiate_same_program {B : Code → Code} (t : El (Code.all B)) :
    (selfInstantiate t).val = t.val := rfl

structure TrackedSection (A : Code) (B : El A → Code) where
  valueAt : (x : El A) → El (B x)
  tracker : Term
  computes : ∀ x : El A, Red (.app tracker x.val) (valueAt x).val

def abstractPi {A : Code} {B : El A → Code} (f : TrackedSection A B) :
    El (Code.pi A B) :=
  ⟨f.tracker, fun x => ((B x).along (f.computes x)).mpr (f.valueAt x).property⟩

def applyPi {A : Code} {B : El A → Code} (f : El (Code.pi A B)) (x : El A) :
    El (B x) := ⟨.app f.val x.val, f.property x⟩

theorem dependent_beta {A : Code} {B : El A → Code}
    (f : TrackedSection A B) (x : El A) :
    Red (applyPi (abstractPi f) x).val (f.valueAt x).val := f.computes x

/-- Explicit uniform realisers for the ordinary combinatory typing rules. -/
theorem i_realises (A : Code) : (Code.arrow A A).accepts .i :=
  fun x hx => (A.stable (.i x)).mpr hx

theorem k_realises (A B : Code) :
    (Code.arrow A (Code.arrow B A)).accepts .k :=
  fun x hx y _ => (A.stable (.k x y)).mpr hx

theorem s_realises (A B C : Code) :
    (Code.arrow (Code.arrow A (Code.arrow B C))
      (Code.arrow (Code.arrow A B) (Code.arrow A C))).accepts .s :=
  fun f hf g hg x hx =>
    (C.stable (.s f g x)).mpr (hf x hx (.app g x) (hg x hx))

/-- A separately defined derivation system. There is no rule accepting an
    arbitrary semantic assertion, equilibrium, or self-issued certificate. -/
inductive Derives : Term → Code → Prop where
  | i (A : Code) : Derives .i (Code.arrow A A)
  | k (A B : Code) : Derives .k (Code.arrow A (Code.arrow B A))
  | s (A B C : Code) :
      Derives .s (Code.arrow (Code.arrow A (Code.arrow B C))
        (Code.arrow (Code.arrow A B) (Code.arrow A C)))
  | app {f x : Term} {A B : Code} :
      Derives f (Code.arrow A B) → Derives x A → Derives (.app f x) B
  | allIntro {t : Term} {B : Code → Code} :
      (∀ A : Code, Derives t (B A)) → Derives t (Code.all B)
  | allElim {t : Term} {B : Code → Code} :
      Derives t (Code.all B) → (A : Code) → Derives t (B A)
  | reduce {t u : Term} {A : Code} : Derives t A → Red t u → Derives u A

/-- Structural soundness: a proof over arbitrary derivation height, not a test
    over a finite catalogue of programs. -/
theorem sound {t : Term} {A : Code} (h : Derives t A) : A.accepts t := by
  induction h with
  | i A => exact i_realises A
  | k A B => exact k_realises A B
  | s A B C => exact s_realises A B C
  | app hf hx ihf ihx => exact ihf _ ihx
  | allIntro h ih => exact ih
  | allElim h A ih => exact ih A
  | reduce h r ih => exact (Code.along _ r).mp ih

theorem no_empty_derivation {t : Term} (h : Derives t Code.bottom) : False :=
  sound h

def emptyPoly : Code := Code.all (fun A => A)

theorem no_empty_polymorphic_value (x : El emptyPoly) : False :=
  x.property Code.bottom

theorem no_empty_polymorphic_derivation {t : Term} (h : Derives t emptyPoly) :
    False := sound h Code.bottom

/-- Nontrivial example: polymorphic identity and actual self-application. -/
def polyId : Code := Code.all (fun A => Code.arrow A A)

def identity : El polyId := ⟨.i, i_realises⟩

def apply {A B : Code} (f : El (Code.arrow A B)) (x : El A) : El B :=
  ⟨.app f.val x.val, f.property x.val x.property⟩

def identityAtOwnType : El (Code.arrow polyId polyId) := selfInstantiate identity

def identitySelfApplied : El polyId := apply identityAtOwnType identity

theorem identity_self_beta : Red identitySelfApplied.val identity.val :=
  Red.one (.i .i)

theorem identity_derives : Derives .i polyId := .allIntro (fun A => .i A)

theorem identity_self_derives : Derives (.app .i .i) polyId :=
  .app (.allElim identity_derives polyId) identity_derives

/-- Real program data, not merely the singleton proof semantics of Prop. -/
def polyBool : Code :=
  Code.all (fun A => Code.arrow A (Code.arrow A A))

def trueTerm : Term := .k

def falseTerm : Term := .app .k .i

theorem true_derives : Derives trueTerm polyBool :=
  .allIntro (fun A => .k A A)

theorem false_derives : Derives falseTerm polyBool :=
  .allIntro (fun A => .app (.k (Code.arrow A A) A) (.i A))

def trueValue : El polyBool := ⟨trueTerm, sound true_derives⟩

def falseValue : El polyBool := ⟨falseTerm, sound false_derives⟩

theorem bool_values_distinct : trueValue ≠ falseValue := by
  intro h
  have e : Term.k = Term.app Term.k Term.i := congrArg Subtype.val h
  cases e

theorem true_selects (x y : Term) : Red (.app (.app trueTerm x) y) x :=
  Red.one (.k x y)

theorem false_selects (x y : Term) : Red (.app (.app falseTerm x) y) y :=
  .tail (.left (.k .i x) y) (Red.one (.i y))

theorem true_selects_zero :
    Red (.app (.app trueTerm .zero) .one) .zero := true_selects _ _

theorem false_selects_one :
    Red (.app (.app falseTerm .zero) .one) .one := false_selects _ _

def zeroValue : El Code.top := ⟨.zero, trivial⟩
def oneValue : El Code.top := ⟨.one, trivial⟩

def observeTrue : El Code.top :=
  apply (apply (instantiate trueValue Code.top) zeroValue) oneValue

def observeFalse : El Code.top :=
  apply (apply (instantiate falseValue Code.top) zeroValue) oneValue

theorem typed_true_observation : Red observeTrue.val zeroValue.val := true_selects _ _
theorem typed_false_observation : Red observeFalse.val oneValue.val := false_selects _ _

theorem observed_outputs_distinct : Term.zero ≠ Term.one := by
  intro h
  cases h

def boolAtOwnType : El (Code.arrow polyBool (Code.arrow polyBool polyBool)) :=
  selfInstantiate trueValue

def trueSelfChoice : El polyBool := apply (apply boolAtOwnType trueValue) falseValue

theorem boolean_self_beta : Red trueSelfChoice.val trueValue.val :=
  true_selects trueTerm falseTerm

/-- Syntactic (finite) type descriptions, separate from semantic predicates.
    `all` is an actual constructor, not an external-only phantom name. -/
inductive TypeCode where
  | var : Nat → TypeCode
  | arrow : TypeCode → TypeCode → TypeCode
  | all : TypeCode → TypeCode
  | bottom
  deriving DecidableEq, Repr

def extend (A : Code) (ρ : Nat → Code) : Nat → Code
  | 0 => A
  | n + 1 => ρ n

def interpret : TypeCode → (Nat → Code) → Code
  | .var n, ρ => ρ n
  | .arrow A B, ρ => Code.arrow (interpret A ρ) (interpret B ρ)
  | .all B, ρ => Code.all (fun A => interpret B (extend A ρ))
  | .bottom, _ => Code.bottom

def identityCode : TypeCode := .all (.arrow (.var 0) (.var 0))
def booleanCode : TypeCode :=
  .all (.arrow (.var 0) (.arrow (.var 0) (.var 0)))

theorem identity_code_decodes (ρ : Nat → Code) : interpret identityCode ρ = polyId := rfl

theorem boolean_code_decodes (ρ : Nat → Code) : interpret booleanCode ρ = polyBool := rfl

/-- An internally coded diagonal SHAPE using realised predicates. This is not
    identified with full ambient powersets; that false identification is exactly
    what the model declines. Its universal code stays inside Code. -/
def predCode (A : Code) : Code := Code.arrow A polyBool

def doublePred (A : Code) : Code := predCode (predCode A)

def diagonalFamily (A : Code) : Code :=
  Code.arrow (Code.arrow (doublePred A) A) (doublePred A)

def diagonalPoly : Code := Code.all diagonalFamily

def diagonalWitnessTerm : Term := .app .k (.app .k falseTerm)

theorem diagonal_derives : Derives diagonalWitnessTerm diagonalPoly :=
  .allIntro (fun A =>
    .app (.k (doublePred A) (Code.arrow (doublePred A) A))
      (.app (.k polyBool (predCode A)) false_derives))

def diagonalWitness : El diagonalPoly := ⟨diagonalWitnessTerm, sound diagonal_derives⟩

def diagonalAtOwnType : El (diagonalFamily diagonalPoly) :=
  selfInstantiate diagonalWitness

theorem diagonal_internal_self_instantiation :
    diagonalAtOwnType.val = diagonalWitness.val := rfl

/-- A concrete ambient family with no uniform erased realiser. It is a legitimate
    external mathematical family, but not a term of this polymorphic calculus. -/
noncomputable def nonuniformFamily (A : Code) : El Code.top := by
  classical
  exact ⟨if A.accepts .i then .zero else .one, trivial⟩

theorem nonuniform_at_top : (nonuniformFamily Code.top).val = .zero := by
  simp [nonuniformFamily, Code.top]

theorem nonuniform_at_bottom : (nonuniformFamily Code.bottom).val = .one := by
  simp [nonuniformFamily, Code.bottom]

theorem no_nonuniform_abstraction
    (t : El (Code.all (fun _ => Code.top)))
    (h : ∀ A : Code, instantiate t A = nonuniformFamily A) : False := by
  have hz : t.val = Term.zero :=
    (congrArg Subtype.val (h Code.top)).trans nonuniform_at_top
  have ho : t.val = Term.one :=
    (congrArg Subtype.val (h Code.bottom)).trans nonuniform_at_bottom
  exact observed_outputs_distinct (hz.symm.trans ho)

/-- Hence no abstraction of ALL ambient families can obey beta with the actual
    instantiation operation. Admissibility is a proved restriction, not a label. -/
theorem no_full_ambient_abstraction
    (lam : ((A : Code) → El Code.top) → El (Code.all (fun _ => Code.top)))
    (beta : ∀ f A, instantiate (lam f) A = f A) : False :=
  no_nonuniform_abstraction (lam nonuniformFamily) (beta nonuniformFamily)

/-- A support specification, with no probability or equilibrium axiom. -/
structure SafeSupport (A : Code) where
  supported : Term → Prop
  safe : ∀ t : Term, supported t → A.accepts t

def SafeSupport.instantiate {B : Code → Code}
    (p : SafeSupport (Code.all B)) (A : Code) : SafeSupport (B A) where
  supported := p.supported
  safe := fun t ht => p.safe t ht A

theorem support_cannot_realise_empty (p : SafeSupport Code.bottom)
    (t : Term) (ht : p.supported t) : False := p.safe t ht

/-- All inhabitation and soundness theorems remain relative to the ambient
    foundational system; none claims to prove Lean's own consistency. -/
theorem resolution :
    Nonempty (El polyId) ∧
    Nonempty (El (Code.arrow polyId polyId)) ∧
    Nonempty (El diagonalPoly) ∧
    Nonempty (El (diagonalFamily diagonalPoly)) ∧
    (∀ t, ¬ Derives t Code.bottom) :=
  ⟨⟨identity⟩, ⟨identityAtOwnType⟩, ⟨diagonalWitness⟩,
   ⟨diagonalAtOwnType⟩, fun _ h => no_empty_derivation h⟩

end OrthemologyV2

#print axioms OrthemologyV2.resolution
#print axioms OrthemologyV2.sound
#print axioms OrthemologyV2.polymorphic_beta
#print axioms OrthemologyV2.polymorphic_eta
#print axioms OrthemologyV2.dependent_beta
#print axioms OrthemologyV2.identity_self_derives
#print axioms OrthemologyV2.diagonal_derives
#print axioms OrthemologyV2.no_full_ambient_abstraction
#print axioms OrthemologyV2.no_empty_polymorphic_value
