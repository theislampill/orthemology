/- Retained typing-tree support, hidden conversion provenance, and both J coordinates. -/
import AllLegacyComparison

namespace P01AC.IndependentLegacy
open OrthemologyV2 OrthemologyV3 P01D P01R
open Legacy

def hiddenOpenConversion : P01DF.PolyConv (.atom .i) (.atom .i) :=
  .trans (.symm (.k (.atom .i) (.var 7))) (.k (.atom .i) (.var 7))

def hiddenOpenTree : Derivation (.atom .i) .raw :=
  .conv (.raw (.atom .i)) hiddenOpenConversion

/-- Only displayed typing-tree support is required, not proof-internal history. -/
theorem hidden_conversion_history_allowed : Supported 0 hiddenOpenTree := by
  simp [hiddenOpenTree,Supported,TypeSupported,Scoped]

def closedConclusionOpenPremise : Derivation (.atom .i) .raw :=
  .conv (.raw (.app (.app (.atom .k) (.atom .i)) (.var 0))) (.k _ _)

theorem closed_conclusion_does_not_hide_open_premise :
    ¬ Supported 0 closedConclusionOpenPremise := by
  intro h
  exact Nat.not_lt_zero 0 h.2.2.1.2

theorem all_intro_old_judgment :
    P01DF.Has (.atom .i) (.all (.arrow (.param 0) (.param 0))) := erase identityTree

theorem dependent_all_recovered :
    Has [] (abstract (.atom .k))
      (.all (.pi .raw (arr (.param 0)
        (arr (.identity .raw (.var 0) (.atom .i)) (.param 0))))) :=
  dependent_polymorphic_typed

def twoCoordinateMotive : P01DF.Ty := .identity (.var 1) (.var 0)
def nonliteralProof : Poly := .app (.atom .i) (.atom .i)

def twoCoordinateTree : Derivation (jPoly (.atom .i) (.atom .i) nonliteralProof)
    (P01DF.motiveAt twoCoordinateMotive (.atom .i) nonliteralProof) :=
  .j (B := twoCoordinateMotive)
    (.conv (.identityIntro (.refl (.atom .i))) (.symm (.i (.atom .i))))
    (.identityIntro (.refl (.atom .i)))

theorem two_coordinate_tree_supported : Supported 0 twoCoordinateTree := by
  simp [twoCoordinateTree,twoCoordinateMotive,nonliteralProof,Supported,TypeSupported,
    Scoped,P01DF.motiveAt,P01DF.substIndex,psub,P01F.cons,jPoly]

theorem proof_coordinate_legacy_J_translates :
    Has [] (jPoly (.atom .i) (.atom .i) nonliteralProof)
      (translate (P01DF.motiveAt twoCoordinateMotive (.atom .i) nonliteralProof)) :=
  two_coordinate_tree_supported.raw_embed

theorem theta_is_not_all_raw : theta [] .raw (.atom .i) ≠ rawTel 2 := by
  intro h
  cases h

end P01AC.IndependentLegacy
