import SourceControls
import FamilyObstructions
import StructuredObserver

namespace IndependentTypeFamilyControls
open P01AC P01D P01AC.ExtensionalRepair
open TypeIndexedSourceControls TypeIndexedFamilyObstructions

-- Literal source equalities make both weakening and self-instantiation explicit.
theorem constant_telescope_unchanged : twkTel [ConstantAll] = [ConstantAll] := rfl
theorem observer_telescope_unchanged :
    twkTel TypeIndexedStructuredObserver.Γ = TypeIndexedStructuredObserver.Γ := rfl
theorem actual_self_instance :
    tinst DiscriminatorBody Discriminator = arr Discriminator .raw := rfl

-- Actual typed source values used by the Raw falsification control.
theorem seed_raw_source : HasE [] (.atom .i) .raw := .rawAtom (.raw .nil)
theorem update_raw_source : HasE [] (.app (.atom .k) (.atom .k)) .raw :=
  .rawApp (.raw .nil) (.rawAtom (.raw .nil)) (.rawAtom (.raw .nil))
theorem numerals_source (k : Nat) :
    HasE [] (P01AC.EffectiveCompleteness.inputNumeral k) P01AC.EffectiveCompleteness.N :=
  has_inclusion (P01AC.EffectiveCompleteness.inputNumeral_has k)

-- The retained atom/application bridge cannot erase the raw distinction either.
theorem raw_observations_plus_distinct :
    ¬ Intensional.Plus.PolyConvPlus
      (.atom (eval TypeIndexedStructuredObserver.observe
        (TypeIndexedStructuredObserver.probeEnv 0)))
      (.atom (eval TypeIndexedStructuredObserver.observe
        (TypeIndexedStructuredObserver.probeEnv 1))) := by
  intro h
  exact TypeIndexedStructuredObserver.raw_observations_distinct
    (Intensional.Plus.polyConvPlus_sound h zeroEnv)

-- A singleton index avoids the full-family obstruction even with two Raw values.
theorem singleton_index_full_families_coherent (f : Unit → Bool) :
    f = reabstract () f := by
  funext i
  cases i
  rfl

-- A singleton result avoids the diagonal obstruction: its nontriviality premise matters.
def trivial_full_self_product : Unit ≃ ((i : Unit) → Unit → Unit) where
  toFun _ := fun _ _ => ()
  invFun _ := ()
  left_inv x := by cases x; rfl
  right_inv f := by
    funext i x
    cases f i x
    rfl

-- Two independently supplied Church-style families; only local set calculations.
-- In particular Bool below is NOT interpreted as the complete source Raw algebra.
def testCarrier : Bool → Type
  | false => Unit
  | true => Bool

def zeroFamily (i : Bool) (_ : (Bool × (testCarrier i → testCarrier i)) →
    (Bool × (testCarrier i → testCarrier i)))
    (s : Bool × (testCarrier i → testCarrier i)) := s

def oneFamily (i : Bool) (step : (Bool × (testCarrier i → testCarrier i)) →
    (Bool × (testCarrier i → testCarrier i)))
    (s : Bool × (testCarrier i → testCarrier i)) := step s

def varyingFamily (i : Bool) (step : (Bool × (testCarrier i → testCarrier i)) →
    (Bool × (testCarrier i → testCarrier i)))
    (s : Bool × (testCarrier i → testCarrier i)) :=
  if i then step s else s

theorem zero_family_uniform (f : Bool → Bool) (a : Bool) (i j : Bool) :
    structuredObservation testCarrier zeroFamily f a i =
      structuredObservation testCarrier zeroFamily f a j := rfl

theorem one_family_uniform (f : Bool → Bool) (a : Bool) (i j : Bool) :
    structuredObservation testCarrier oneFamily f a i =
      structuredObservation testCarrier oneFamily f a j := rfl

theorem varying_family_separates :
    structuredObservation testCarrier varyingFamily Bool.not false false ≠
      structuredObservation testCarrier varyingFamily Bool.not false true := by
  decide

-- Constancy of the output family alone is insufficient without body assembly.
theorem coherent_result_exists_despite_varying_family :
    ∃ result : ConstantFamilies Bool Bool false,
      result.val = reabstract false result.val ∧
      structuredObservation testCarrier varyingFamily Bool.not false false ≠
        structuredObservation testCarrier varyingFamily Bool.not false true := by
  exact ⟨⟨fun _ => false, fun _ => rfl⟩, rfl, varying_family_separates⟩

-- Adding exactly the advertised assembly equations rejects that same local family.
theorem varying_family_has_no_coherent_assembly :
    ¬ ∃ result : ConstantFamilies Bool Bool false,
      ∀ i, result.val i =
        structuredObservation testCarrier varyingFamily Bool.not false i := by
  rintro ⟨result, assembly⟩
  exact varying_family_separates
    (structured_observer_uniform false testCarrier varyingFamily Bool.not false
      result assembly false true)

#print axioms constant_telescope_unchanged
#print axioms observer_telescope_unchanged
#print axioms actual_self_instance
#print axioms seed_raw_source
#print axioms update_raw_source
#print axioms numerals_source
#print axioms raw_observations_plus_distinct
#print axioms singleton_index_full_families_coherent
#print axioms trivial_full_self_product
#print axioms zero_family_uniform
#print axioms one_family_uniform
#print axioms varying_family_separates
#print axioms coherent_result_exists_despite_varying_family
#print axioms varying_family_has_no_coherent_assembly
end IndependentTypeFamilyControls
