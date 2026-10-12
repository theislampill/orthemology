import OriginalWNoninhabitation
import NoInternalNegation
import MixedPERControl
import GuardControls

/- Independent reviewer controls. The two models are deliberately kept in
   distinct namespaces; both conclusions use the same original source objects. -/
namespace ReviewHenkinSourceModel
open P01AC P01D
open P01AC.ExtensionalRepair (HasE FormE)
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3)
open CaseOperational (T Conv)

abbrev literalQ : Poly := P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed

theorem same_literal_q : HomogeneousOriginalW.originalQ = FullPER.Application.originalQ := rfl

theorem original_q_typed : HasE [] literalQ (arr P01AC.EffectiveCompleteness.N P01AC.EffectiveCompleteness.N) :=
  P01AC.ExtensionalRepair.has_inclusion P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has

theorem original_W_formed : FormE [] (W literalQ) :=
  P01AC.ExtensionalRepair.form_inclusion
    (P01AC.ExtensionalRepair.ExactScalarFusion.W_form
      P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has P01AC.Ctx.nil)

theorem literal_syntactic_independence :
    (∀ p : Poly, ¬ HasE [] p (W literalQ)) ∧
    (∀ p : Poly, ¬ HasE [] p (arr (W literalQ) .bottom)) :=
  ⟨HomogeneousOriginalW.original_W_uninhabited,
   T20SourceIndependence.no_internal_negation⟩

theorem literal_fixed_c3_failure : ¬ HasE [] c3 (W literalQ) :=
  literal_syntactic_independence.1 c3

theorem empty_context_and_church_nonvacuous :
    ∃ (ρ : HenkinSoundness.REnv) (η : HenkinSoundness.Env),
      HenkinSoundness.admissible ρ ∧ HenkinSoundness.D [] ρ η ∧
      HenkinSoundness.F P01AC.EffectiveCompleteness.N ρ η T.nu T.nu :=
  ⟨HomogeneousOriginalW.emptyTypes,HenkinSoundness.zeroEnv,
    HomogeneousOriginalW.emptyTypes_admissible,rfl,HomogeneousOriginalW.nu_N _ _⟩

theorem rejected_target_is_eligible :
    ConcreteUniverse.U (HenkinSoundness.F (W literalQ)
      HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv) :=
  HenkinSoundness.formation_eligible original_W_formed
    HomogeneousOriginalW.emptyTypes_admissible rfl

theorem identity_compiler_positive_source_control :
    HasE [] c3 (W P01AC.ExtensionalRepair.ExactScalarFusion.i) :=
  P01AC.ExtensionalRepair.has_inclusion P01AC.ExtensionalRepair.ExactScalarFusion.W_base

theorem identity_compiler_positive_model_control :
    HenkinSoundness.F (W P01AC.ExtensionalRepair.ExactScalarFusion.i)
      HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv
      (HenkinSourceTransport.interp c3 HenkinSoundness.zeroEnv)
      (HenkinSourceTransport.interp c3 HenkinSoundness.zeroEnv) :=
  HenkinSoundness.fundamental identity_compiler_positive_source_control
    HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv HenkinSoundness.zeroEnv
    HomogeneousOriginalW.emptyTypes_admissible ⟨rfl,rfl⟩

theorem literal_positive_full_PER_control (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F (W literalQ) ρ η (ImportedOpenTermTransport.interp c3 η)
      (ImportedOpenTermTransport.interp c3 η) := FullPER.Application.scalar_target_valid ρ η

theorem all_ranges_over_every_eligible_relation (B : Ty)
    (ρ : HenkinSoundness.REnv) (η : HenkinSoundness.Env) (u v : T) :
    HenkinSoundness.F (.all B) ρ η u v ↔
      ∀ (R : T → T → Prop), ConcreteUniverse.U R →
        HenkinSoundness.F B (HenkinSoundness.cons R ρ) η u v := by
  constructor
  · intro h R hr; exact h ⟨R,hr⟩
  · intro h R; exact h R.val R.property

theorem mixed_PER_saturated : HomogeneousPER.IsPER ConcreteUniverse.S MixedPERControl.R :=
  ⟨MixedPERControl.R_sym,MixedPERControl.R_trans,MixedPERControl.R_saturated⟩

theorem mixed_PER_excluded : ¬ConcreteUniverse.U MixedPERControl.R := by
  intro h
  have all := MixedPERControl.raw_support_forces_universal h.2
    MixedPERControl.support_mixes_tags.1 MixedPERControl.support_mixes_tags.2.1
  exact MixedPERControl.a0_not_related_j (all _ _)

theorem conversion_excluded : ¬ConcreteUniverse.U Conv :=
  fun h => MixedPERControl.conversion_not_admissible h.2

theorem Raw_is_strictly_coarser (ρ : HenkinSoundness.REnv) (η : HenkinSoundness.Env) :
    HenkinSoundness.F .raw ρ η T.a0 T.a1 ∧ ¬Conv T.a0 T.a1 :=
  ⟨True.intro,CaseOperational.atom_distinct⟩

def noNu : T → Prop
  | .nu => False
  | .app f a => noNu f ∧ noNu a
  | _ => True

theorem original_term_embedding_has_no_nu (t : OrthemologyV2.Term) :
    noNu (HenkinSourceTransport.embed t) := by
  induction t with
  | i | k | s | zero | one => trivial
  | app f a hf ha => exact ⟨hf,ha⟩

theorem nu_is_not_a_source_constant_image :
    ¬∃ t : OrthemologyV2.Term, HenkinSourceTransport.embed t = T.nu := by
  rintro ⟨t,ht⟩
  have h := original_term_embedding_has_no_nu t
  rw [ht] at h
  exact h

theorem original_poly_default_interpretation_has_no_nu (p : Poly) :
    noNu (HenkinSourceTransport.interp p HenkinSoundness.zeroEnv) := by
  induction p with
  | var n => trivial
  | atom t => exact original_term_embedding_has_no_nu t
  | app f a hf ha => exact ⟨hf,ha⟩

theorem nu_is_not_default_interpretation_of_any_original_poly :
    ¬∃ p : Poly, HenkinSourceTransport.interp p HenkinSoundness.zeroEnv = T.nu := by
  rintro ⟨p,hp⟩
  have h := original_poly_default_interpretation_has_no_nu p
  rw [hp] at h
  exact h

#print axioms nu_is_not_default_interpretation_of_any_original_poly
#print axioms original_q_typed
#print axioms original_W_formed
#print axioms literal_syntactic_independence
#print axioms empty_context_and_church_nonvacuous
#print axioms rejected_target_is_eligible
#print axioms identity_compiler_positive_source_control
#print axioms identity_compiler_positive_model_control
#print axioms literal_positive_full_PER_control
#print axioms all_ranges_over_every_eligible_relation
#print axioms mixed_PER_saturated
#print axioms mixed_PER_excluded
#print axioms conversion_excluded
#print axioms Raw_is_strictly_coarser
#print axioms nu_is_not_a_source_constant_image
end ReviewHenkinSourceModel
