/- New qualification-only boundary tests. These are not claimed as recovered
   attempt-0003 declarations and do not mechanize its full recursive U10 model. -/
import P01Examples
namespace P01Qualification
open OrthemologyV2 OrthemologyV3 P01D

def skk : Term := .app (.app .s .k) .k

theorem skk_application (x : Term) : Red (.app skk x) x :=
  .tail (.s .k .k x) (.tail (.k x (.app .k x)) (.refl _))

theorem identity_skk_function_relation (P : PER) : (ArrPER P P).rel .i skk := by
  intro x y hxy
  exact P.raw (.symm (.step (.i x)))
    (P01Source.red_conv (skk_application y)).symm hxy

theorem typed_equality_strictly_coarser :
    (¬ Conv .i skk) ∧ ∀ P : PER, (ArrPER P P).rel .i skk :=
  ⟨P01Source.I_SKK_not_convertible, identity_skk_function_relation⟩

theorem omega_empty_arrow_membership : (ArrPER botPER botPER).dom omega := by
  intro x y hxy
  exact False.elim hxy

theorem omega_not_source_SN : ¬ StronglyNormalising omega :=
  three_cycle_not_SN omega_step1 omega_step2 omega_step3

theorem new_PER_membership_does_not_imply_SN :
    ∃ P : PER, P.dom omega ∧ ¬ StronglyNormalising omega :=
  ⟨ArrPER botPER botPER, omega_empty_arrow_membership, omega_not_source_SN⟩

def omegaIntrinsic : Tm nilContext (constantTy nilContext (ArrPER botPER botPER)) where
  code := .atom omega
  valid := fun _ => omega_empty_arrow_membership

theorem tracked_dependent_core_does_not_imply_SN :
    ¬ StronglyNormalising (omegaIntrinsic.at ()) := omega_not_source_SN

theorem all_identity_nonempty : (AllPER idParamFamily).dom .i :=
  (all_domain idParamFamily .i).mpr (fun _ _ R => identity_link R)

theorem all_identity_legal_self_instance :
    (ArrPER (AllPER idParamFamily) (AllPER idParamFamily)).dom .i :=
  all_self_eliminate all_identity_nonempty

theorem join_rejects_distinct_normal_forms :
    P01Certificate.checkJoin .i .k [] [] = none := rfl

theorem join_returns_actual_conversion :
    ∃ p : PLift (Conv (.app .i .i) .i),
      P01Certificate.checkJoin (.app .i .i) .i [[]] [] = some p :=
  ⟨⟨.step (.i .i)⟩, rfl⟩
end P01Qualification
