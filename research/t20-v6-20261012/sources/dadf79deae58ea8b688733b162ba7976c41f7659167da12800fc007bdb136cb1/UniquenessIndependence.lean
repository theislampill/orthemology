import UniquenessConverse
import RigidityDiscriminator

namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open SourceRigidity InternalRecursorPrinciple
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Source arrow application with arbitrary HasE function and argument proofs. -/
theorem appE_arrow {Γ : Tel} {X Y : Ty} {f a : Poly}
    (hX : Form Γ X) (hY : Form Γ Y)
    (hf : HasE Γ f (arr X Y)) (ha : HasE Γ a X) : HasE Γ (.app f a) Y := by
  have h := HasE.piElim (form_inclusion (form_arr hX hY))
    (form_inclusion (show Form Γ (inst (wk Y) a) from by simpa only [inst_wk] using hY)) hf ha
  simpa only [inst_wk] using h

/-- Composition is built from the actual source S/K constructors. It does not
    assume weakening or substitution for arbitrary HasE derivations. -/
theorem composeE {Γ : Tel} {X Y Z : Ty} {f g : Poly}
    (hX : Form Γ X) (hY : Form Γ Y) (hZ : Form Γ Z)
    (hf : HasE Γ f (arr Y Z)) (hg : HasE Γ g (arr X Y)) :
    HasE Γ (.app (.app (.atom .s) (.app (.atom .k) f)) g) (arr X Z) := by
  have hYZ := form_arr hY hZ
  have hXYZ := form_arr hX hYZ
  have hXY := form_arr hX hY
  have hXZ := form_arr hX hZ
  have hk : HasE Γ (.atom .k) (arr (arr Y Z) (arr X (arr Y Z))) :=
    .k (form_inclusion hYZ) (form_inclusion hX) (form_inclusion (form_arr hYZ hXYZ))
  have hKf := appE_arrow hYZ hXYZ hk hf
  have hs : HasE Γ (.atom .s) (arr (arr X (arr Y Z)) (arr (arr X Y) (arr X Z))) :=
    .s (form_inclusion hX) (form_inclusion hY) (form_inclusion hZ)
      (form_inclusion (form_arr hXYZ (form_arr hXY hXZ)))
  exact appE_arrow hXY hXZ (appE_arrow hXYZ (form_arr hXY hXZ) hs hKf) hg

/-- Exact generic internal uniqueness has no closed proof polynomial. -/
theorem internal_uniqueness_uninhabited (p : Poly) : ¬ HasE [] p Uniqueness := by
  intro hp
  have hr := appE_arrow (uniqueness_formed Ctx.nil) (rigidity_formed Ctx.nil)
    internal_uniqueness_implies_rigidity hp
  exact RigidityDiscriminator.rigidity_uninhabited _ hr

/-- Its internal negation also has no closed proof polynomial. The transfer
    uses an actual source composition with Rigidity→Uniqueness. -/
theorem internal_uniqueness_negation_uninhabited (p : Poly) :
    ¬ HasE [] p (arr Uniqueness .bottom) := by
  intro hp
  have hn := composeE (rigidity_formed Ctx.nil) (uniqueness_formed Ctx.nil)
    (Form.bottom Ctx.nil) hp rigidity_implies_internal_uniqueness
  exact RigidityDiscriminator.no_internal_negation _ hn

theorem internal_uniqueness_independence :
    (¬ ∃ p, HasE [] p Uniqueness) ∧
    (¬ ∃ p, HasE [] p (arr Uniqueness .bottom)) :=
  ⟨fun ⟨p, hp⟩ => internal_uniqueness_uninhabited p hp,
   fun ⟨p, hp⟩ => internal_uniqueness_negation_uninhabited p hp⟩

theorem internal_uniqueness_independence_Has :
    (¬ ∃ p, Has [] p Uniqueness) ∧
    (¬ ∃ p, Has [] p (arr Uniqueness .bottom)) :=
  ⟨fun ⟨p, hp⟩ => internal_uniqueness_uninhabited p (has_inclusion hp),
   fun ⟨p, hp⟩ => internal_uniqueness_negation_uninhabited p (has_inclusion hp)⟩

#print axioms composeE
#print axioms internal_uniqueness_independence
#print axioms internal_uniqueness_independence_Has
end RigidityInitiality
