import HenkinSelectiveSoundness
import TaggedSelectiveSoundness
import JointControls
import CompletionSeparation
import InductionRigidityConverse

namespace CompletionIndependence
open P01AC P01D
open P01AC.ExtensionalRepair (CtxE FormE HasE has_inclusion form_inclusion ctx_inclusion)
open P01AC.EffectiveCompleteness (N)
open RigidityInitiality (dependentStepType sectionPoly)
open RigidityInitiality.FullE.InductionConverse (EqFamily family_form family_step family_at)
open SourceRigidity (zero)
open FullPER.Application (originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def WeakSigmaSchema (s i : Bool) : Prop :=
  ∀ (Γ : Tel) (A B P : Ty) (d z : Poly),
    CtxX s i Γ → FormX s i Γ A → FormX s i (A :: Γ) B →
    FormX s i (.sigma A B :: Γ) P →
    HasX s i (B :: A :: Γ) d (SigmaCompletion.branchType P) →
    HasX s i Γ z (.sigma A B) → ∃ t, HasX s i Γ t (inst P z)

def WeakInductionSchema (s i : Bool) : Prop :=
  ∀ (Γ : Tel) (P : Ty) (p step : Poly), CtxX s i Γ →
    FormX s i (N :: Γ) P → HasX s i Γ p (inst P zero) →
    HasX s i Γ step (dependentStepType P) → ∃ t, HasX s i Γ t (.pi N P)

/-- Active full rule, including recursively extended premises. -/
theorem sigma_schema_admitted : WeakSigmaSchema true false := by
  intro Γ A B P d z hc ha hb hP hd hz
  exact ⟨_,.sigmaElim rfl hc ha hb hP hd hz⟩

/-- Active full rule, including recursively extended premises. -/
theorem induction_schema_admitted : WeakInductionSchema false true := by
  intro Γ P p step hc hP hp hs
  exact ⟨_,.natInduction rfl hc hP hp hs⟩

theorem induction_extension_no_eta_at (p : Poly) :
    ¬ HasX false true [SigmaTagBoundary.SigmaRaw] p SigmaTagBoundary.etaBody := by
  intro h
  let η := TaggedPER.cons OpenTermStandardness.T.i TaggedPER.zeroEnv
  have ev : TaggedPER.E [SigmaTagBoundary.SigmaRaw] SigmaTagBoundary.emptyEnv η η :=
    ⟨⟨rfl,rfl⟩,SigmaTagBoundary.ghost_member _ _⟩
  exact SigmaTagBoundary.eta_at_ghost_empty _ _ _ _
    (InductionModel.fundamental h SigmaTagBoundary.emptyEnv η η SigmaTagBoundary.empty_admissible ev)

/-- Not even the weak full Sigma rule is admissible after full induction. -/
theorem induction_does_not_admit_sigma : ¬ WeakSigmaSchema false true := by
  intro rule
  let S := SigmaTagBoundary.SigmaRaw
  have c : Ctx [S] := .ext .nil (JointCompletion.Controls.sigma_form .nil)
  have a : Form [S] .raw := .raw c
  have b : Form (.raw :: [S]) .raw := .raw (.ext c a)
  have hP := SigmaCompletion.eta_motive_formed c a b
  have hd := SigmaCompletion.canonical_eta_branch c a b
  have hz : Has [S] (.var 0) S := .var (JointCompletion.Controls.sigma_form c) .zero
  obtain ⟨t,ht⟩ := rule [S] .raw .raw _ (.atom .i) (.var 0)
    (.ctxBase (ctx_inclusion c)) (.formBase (form_inclusion a)) (.formBase (form_inclusion b))
    (.formBase (form_inclusion hP)) (.hasBase (has_inclusion hd)) (.hasBase (has_inclusion hz))
  exact induction_extension_no_eta_at t (by simpa only [SigmaCompletion.eta_motive_at] using ht)

/-- The old compiler's equality family has no section in the Sigma-only
extension: the retained nonstandard Church element separates its endpoints. -/
theorem sigma_extension_no_compiler_section (p : Poly) :
    ¬ HasX true false [] p (.pi N (EqFamily originalQ)) := by
  intro h
  have v := SigmaModel.fundamental h HomogeneousOriginalW.emptyTypes
    HenkinSoundness.zeroEnv HenkinSoundness.zeroEnv HomogeneousOriginalW.emptyTypes_admissible ⟨rfl,rfl⟩
  have point := v CaseOperational.T.nu CaseOperational.T.nu
    (HomogeneousOriginalW.nu_N _ _)
  have pair := point.1 HomogeneousOriginalW.atomPER HomogeneousCounterexample.scalarStep
    HomogeneousCounterexample.scalarStep HomogeneousOriginalW.scalarStep_related
    CaseOperational.T.a0 CaseOperational.T.a0 HomogeneousOriginalW.atom0_related
  have bad := pair.1
  simp only [HenkinSoundness.interp_app,HenkinSoundness.interp_ren,HenkinSoundness.interp_var,
    HenkinSoundness.cons] at bad
  change CaseOperational.Conv
    (HenkinSourceTransport.interp originalQ HenkinSoundness.zeroEnv ⬝ CaseOperational.T.nu ⬝
      HomogeneousCounterexample.scalarStep ⬝ CaseOperational.T.a0)
    (CaseOperational.T.nu ⬝ HomogeneousCounterexample.scalarStep ⬝ CaseOperational.T.a0) at bad
  unfold FullPER.Application.originalQ at bad
  rw [HomogeneousCounterexample.original_q_eval] at bad
  exact HomogeneousCounterexample.scalar_not_convertible bad.symm

/-- Full induction fails already at an actual old-formed closed family with
old-typed zero and step data, even after all full Sigma rules are admitted. -/
theorem sigma_does_not_admit_induction : ¬ WeakInductionSchema true false := by
  intro rule
  have hq : HasE [] originalQ SourceRigidity.NT :=
    has_inclusion P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.original_q_has
  have hP := family_form CtxE.nil hq
  have hp : HasE [] SourceRigidity.ident (inst (EqFamily originalQ) zero) :=
    (family_at originalQ zero).symm ▸ has_inclusion (SourceRigidity.q_zero_evidence Ctx.nil)
  obtain ⟨step,hs⟩ := family_step CtxE.nil hq
    (has_inclusion (SourceRigidity.q_step_evidence Ctx.nil))
  obtain ⟨t,ht⟩ := rule [] (EqFamily originalQ) SourceRigidity.ident step .nil
    (.formBase hP) (.hasBase hp) (.hasBase hs)
  exact sigma_extension_no_compiler_section t ht

theorem full_rule_independence :
    (WeakSigmaSchema true false ∧ ¬ WeakInductionSchema true false) ∧
    (WeakInductionSchema false true ∧ ¬ WeakSigmaSchema false true) :=
  ⟨⟨sigma_schema_admitted,sigma_does_not_admit_induction⟩,
    ⟨induction_schema_admitted,induction_does_not_admit_sigma⟩⟩

theorem sigma_extension_no_bottom (p : Poly) : ¬ HasX true false [] p .bottom := by
  intro h
  exact SigmaModel.fundamental h HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv
    HenkinSoundness.zeroEnv HomogeneousOriginalW.emptyTypes_admissible ⟨rfl,rfl⟩

theorem induction_extension_no_bottom (p : Poly) : ¬ HasX false true [] p .bottom := by
  intro h
  exact InductionModel.fundamental h SigmaTagBoundary.emptyEnv TaggedPER.zeroEnv
    TaggedPER.zeroEnv SigmaTagBoundary.empty_admissible ⟨rfl,rfl⟩

/-- Explicitly different Raw interpretations. -/
theorem sigma_model_raw_top (ρ : HenkinSoundness.REnv) (η : HenkinSoundness.Env)
    (p q : CaseOperational.T) : HenkinSoundness.F .raw ρ η p q := trivial

theorem induction_model_raw_faithful (ρ : TaggedPER.REnv) (η : TaggedPER.Env) :
    TaggedPER.F .raw ρ η = OpenTermStandardness.Conv := rfl

#print axioms sigma_extension_no_compiler_section
#print axioms induction_extension_no_eta_at
#print axioms full_rule_independence
#print axioms sigma_extension_no_bottom
#print axioms induction_extension_no_bottom
end CompletionIndependence
