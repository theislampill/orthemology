import FiniteK
import ExtensionalRepairSyntax

/- Exact source bridge. The conditional semantic contract covers only Raw,
not the other carriers of a type-indexed interpretation or all of HasE. -/
namespace FiniteRawObstruction.Source
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.Intensional.Plus (PolyConvPlus)
universe u

/-- The literal two-Raw-variable context suffices for the obstruction. -/
def rawContext : Tel := [.raw, .raw]

theorem raw_context : CtxE rawContext :=
  .ext (.ext .nil (.raw .nil)) (.raw (.ext .nil (.raw .nil)))

theorem x_raw : HasE rawContext (.var 0) .raw :=
  .var (.raw raw_context) .zero

theorem y_raw : HasE rawContext (.var 1) .raw :=
  .var (.raw raw_context) (.succ .zero)

theorem k_application_raw :
    HasE rawContext (.app (.app (.atom .k) (.var 0)) (.var 1)) .raw :=
  .rawApp (.raw raw_context)
    (.rawApp (.raw raw_context) (.rawAtom (.raw raw_context)) x_raw) y_raw

/-- This is an original conversion generator, before the atom/app bridge. -/
theorem original_k_conversion :
    P01DF.PolyConv (.app (.app (.atom .k) (.var 0)) (.var 1)) (.var 0) :=
  .k _ _

theorem k_conversion :
    PolyConvPlus (.app (.app (.atom .k) (.var 0)) (.var 1)) (.var 0) :=
  .k _ _

/-- Its equality also occurs in actual source identity syntax, with witness I. -/
theorem k_identity : HasE rawContext (.atom .i)
    (.identity .raw (.app (.app (.atom .k) (.var 0)) (.var 1)) (.var 0)) :=
  .identityIntro (.identity (.raw raw_context) k_application_raw x_raw)
    k_application_raw x_raw k_conversion

/-- Compositional interpretation of the actual Poly constructors. All variables
range over A; application is total and remains inside A. -/
structure RawDenotation (A : Type u) where
  atom : Term → A
  app : A → A → A

def RawDenotation.interp {A : Type u} (D : RawDenotation A)
    (ρ : Nat → A) : Poly → A
  | .var n => ρ n
  | .atom t => D.atom t
  | .app f x => D.app (D.interp ρ f) (D.interp ρ x)

/-- A small required fragment of ordinary equality-valued Raw soundness. No
claim that mere unary membership soundness implies this equality contract. -/
def RawDenotation.Sound {A : Type u} (D : RawDenotation A) : Prop :=
  ∀ {p q : Poly}, HasE rawContext p .raw → HasE rawContext q .raw →
    PolyConvPlus p q → ∀ ρ : Nat → A, D.interp ρ p = D.interp ρ q

def RawDenotation.toTotalK {A : Type u} (D : RawDenotation A) (h : D.Sound) :
    TotalK A where
  app := D.app
  k := D.atom .k
  k_law := by
    intro x y
    let ρ : Nat → A := fun n => if n = 0 then x else y
    have e := h k_application_raw x_raw k_conversion ρ
    simpa only [RawDenotation.interp, ρ, ↓reduceIte, Nat.one_ne_zero] using e

theorem finite_raw_subsingleton {A : Type u} [Finite A]
    (D : RawDenotation A) (h : D.Sound) : Subsingleton A :=
  (D.toTotalK h).finite_subsingleton

theorem nontrivial_raw_infinite {A : Type u} [Nontrivial A]
    (D : RawDenotation A) (h : D.Sound) : Infinite A :=
  (D.toTotalK h).nontrivial_infinite

/-- In particular Bool cannot be the WHOLE equality-valued total Raw carrier.
This says nothing against a Bool typed carrier inside an infinite Raw model. -/
theorem no_bool_raw (D : RawDenotation Bool) : ¬ D.Sound := by
  intro h
  have hs := finite_raw_subsingleton D h
  have e : false = true := hs.elim _ _
  cases e

/-- Raw alone may validly collapse. This is not a whole-HasE model. -/
def singletonRaw : RawDenotation Unit where
  atom := fun _ => ()
  app := fun _ _ => ()

theorem singleton_raw_sound : singletonRaw.Sound :=
  fun _ _ _ _ => Subsingleton.elim _ _

#print axioms original_k_conversion
#print axioms k_application_raw
#print axioms k_identity
#print axioms RawDenotation.toTotalK
#print axioms finite_raw_subsingleton
#print axioms nontrivial_raw_infinite
#print axioms no_bool_raw
#print axioms singleton_raw_sound
end FiniteRawObstruction.Source
