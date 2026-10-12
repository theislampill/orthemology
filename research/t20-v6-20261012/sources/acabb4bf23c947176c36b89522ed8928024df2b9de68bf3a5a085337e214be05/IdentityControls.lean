import EffectiveChurchIdentity

namespace ClosedChurchIdentity.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedScalarInstances (scalarLeft)

def numeralTyping (k : Nat) : HasE [] (inputNumeral k) N :=
  has_inclusion (EffectiveCompleteness.inputNumeral_has k)

theorem numeral_identity_iff (j k : Nat) :
    HasE [] i (.identity N (inputNumeral j) (inputNumeral k)) ↔ j = k :=
  identity_iff_count_eq (numeralTyping j) (numeralTyping k)
    (numeral_observation j) (numeral_observation k)

theorem different_numerals_no_witness :
    ¬ ∃ r, HasE [] r (.identity N (inputNumeral 2) (inputNumeral 3)) := by
  intro h
  have e := (identity_exists_iff_count_eq (numeralTyping 2) (numeralTyping 3)
    (numeral_observation 2) (numeral_observation 3)).mp h
  contradiction

def iTyping : HasE [] (.atom .i) N :=
  has_inclusion (.allIntro (EffectiveCompleteness.N_form .nil)
    (.i (ExactScalarFusion.End_form .nil)
      (form_arr (ExactScalarFusion.End_form .nil) (ExactScalarFusion.End_form .nil))))

def skkTyping : HasE [] (.atom P01R.skk) N :=
  has_inclusion (.allIntro (EffectiveCompleteness.N_form .nil)
    (finite_import .nil (finite_skk_identity (.arrow (.var 0) (.var 0)))))

theorem i_observation : PolyConvPlus (scalarLeft (.atom .i)) (iterationPoly 1) :=
  .app (.i (.var 1)) (.refl (.var 0))

theorem skk_observation : PolyConvPlus (scalarLeft (.atom P01R.skk)) (iterationPoly 1) := by
  have h : PolyConvPlus (.app (.atom P01R.skk) (.var 1)) (.var 1) :=
    (PolyConvPlus.app skk_head_exposure (.refl (.var 1))).trans
      ((PolyConvPlus.s (.atom .k) (.atom .k) (.var 1)).trans
        (.k (.var 1) (.app (.atom .k) (.var 1))))
  exact .app h (.refl (.var 0))

/-- Positive source identity, while the unchanged raw conversion stays false. -/
theorem source_equal_raw_distinct :
    HasE [] i (.identity N (.atom .i) (.atom P01R.skk)) ∧
      ¬ PolyConvPlus (.atom .i) (.atom P01R.skk) := by
  refine ⟨(identity_iff_count_eq iTyping skkTyping i_observation skk_observation).mpr rfl, ?_⟩
  intro h
  exact P01Source.I_SKK_not_convertible (Intensional.Plus.polyConvPlus_sound h zeroEnv)

#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentity iTyping skkTyping)
#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentity (numeralTyping 2) (numeralTyping 2))
#guard !(@decide _ (EffectiveChurchIdentity.decideTypedIdentity (numeralTyping 2) (numeralTyping 3)))
#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentityExists iTyping skkTyping)
#guard !(@decide _ (EffectiveChurchIdentity.decideTypedIdentityExists (numeralTyping 0) (numeralTyping 1)))

#print axioms different_numerals_no_witness
#print axioms source_equal_raw_distinct
end ClosedChurchIdentity.Controls
