import PositiveRigidity

namespace CompletionIndependence
open P01AC P01D
open JointCompletion (CtxJ FormJ HasJ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Literal syntactic inclusion, not semantic reflection. Both selected rule
constructors are available in the unchanged frozen joint candidate. -/
theorem into_joint {σ ι Γ p A} (h : HasX σ ι Γ p A) : HasJ Γ p A := by
  induction h using HasX.rec
    (motive_1 := fun Γ _ => CtxJ Γ)
    (motive_2 := fun Γ A _ => FormJ Γ A) with
    | ctxBase h => exact .ctxBase h
    | formBase h => exact .formBase h
    | hasBase h => exact .hasBase h
    | nil => exact .nil
    | ext hΓ hA c a => exact .ext c a
    | param hΓ c => exact .param c
    | bottom hΓ c => exact .bottom c
    | all hΓ hB c b => exact .all c b
    | raw hΓ c => exact .raw c
    | pi hA hB a b => exact .pi a b
    | sigma hA hB a b => exact .sigma a b
    | identity hA hp hq a p q => exact .identity a p q
    | var hA hv a => exact .var a hv
    | i hA ht a t => exact .i a t
    | k hA hB ht a b t => exact .k a b t
    | s hA hB hC ht a b c t => exact .s a b c t
    | finite τ bound hτ hA hf a t => exact .finite τ bound a t hf
    | allIntro hAll hp a p => exact .allIntro a p
    | allElim hAll hA hTarget hp a x t p => exact .allElim a x t p
    | rawAtom hA a => exact .rawAtom a
    | rawApp hA hf hx a f x => exact .rawApp a f x
    | piIntro hA hb hs a b => exact .piIntro a b hs
    | piElim hPi ht hf ha pi t f a => exact .piElim pi t f a
    | sigmaIntro hSigma ht ha hb s t a b => exact .sigmaIntro s t a b
    | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
    | sigmaSnd hSigma ht hz s t z => exact .sigmaSnd s t z
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p pq hs
    | piExt hA hB hPi hp hq hM hPiM hh hTarget sp sq sh sA sB a b pi p q m pim h t =>
        exact .piExt a b pi p q m pim h t sp sq sh sA sB
    | allExt hB hAll hp hq hN hh hTarget sp sq sh sB b all p q n h t =>
        exact .allExt b all p q n h t sp sq sh sB
    | sigmaElim enabled hΓ hA hB hP hd hz c a b p d z => exact .sigmaElim c a b p d z
    | natInduction enabled hΓ hP hp hs c p seed step => exact .natInduction c p seed step

end CompletionIndependence

namespace P01AC.ExtensionalRepair.ExactScalarFusion.SelectiveCompletion
open OrthemologyV2 OrthemologyV3 P01D P01R
open CompletionIndependence

/-- Explicit transport of the retained forward_fixed construction to the
selective syntax: J uses its actual source motive M and proof erasure. -/
theorem forward_fixedX {σ ι : Bool} {k e : Poly} (hk : Has [] k T)
    (he : HasX σ ι [] e (.identity T i k)) : HasX σ ι [] c3 (W k) := by
  have hbase : Form [] (motiveAt M i i) := by
    rw [M_at (show Scoped 0 i from trivial)]
    exact W_form (i_T .nil) .nil
  have htarget : Form [] (motiveAt M k e) := by
    rw [M_at (P01AC.has_scoped hk)]
    exact W_form hk .nil
  have hd : Has [] c3 (motiveAt M i i) := by
    rw [M_at (show Scoped 0 i from trivial)]
    exact W_base
  have hj := HasX.j (.formBase (form_inclusion (T_form .nil))) (.formBase (form_inclusion M_form))
    (.formBase (form_inclusion (.identity (T_form .nil) (i_T .nil) hk)))
    (.formBase (form_inclusion hbase)) (.formBase (form_inclusion htarget))
    (.hasBase (has_inclusion (i_T .nil))) (.hasBase (has_inclusion hk)) he (.hasBase (has_inclusion hd))
  rw [M_at (P01AC.has_scoped hk)] at hj
  exact .conv (.formBase (form_inclusion (W_form hk .nil))) hj (j_conversion c3 k e) (c3_scoped 0)

theorem induction_only_fixed_scalar : HasX false true [] c3 (W FullPER.Application.originalQ) := by
  obtain ⟨p,hp⟩ := RigidityInitiality.FullE.PositiveCompletion.induction_only_compiler_identity
  have h : HasX false true [] p (.identity T i FullPER.Application.originalQ) := by
    rw [← SourceRigidity.result_exact] at hp
    exact hp
  exact forward_fixedX InternalGraph.BridgeAssembly.original_q_has h

end P01AC.ExtensionalRepair.ExactScalarFusion.SelectiveCompletion

namespace RigidityInitiality.FullE.PositiveCompletion
open P01AC P01D P01AC.ExtensionalRepair
open CompletionIndependence

theorem joint_rigidity : JointCompletion.HasJ []
    (abstract (abstract (abstract SourceRigidity.ident))) SourceRigidity.Rigidity :=
  into_joint induction_only_rigidity

theorem joint_compiler_identity : ∃ p, JointCompletion.HasJ [] p FullPER.Application.originalIdentity := by
  obtain ⟨p,hp⟩ := induction_only_compiler_identity
  exact ⟨p,into_joint hp⟩

theorem joint_fixed_scalar : JointCompletion.HasJ [] ExactScalarFusion.c3
    (ExactScalarFusion.W FullPER.Application.originalQ) :=
  into_joint ExactScalarFusion.SelectiveCompletion.induction_only_fixed_scalar

theorem original_rigidity_still_absent (p : Poly) : ¬ HasE [] p SourceRigidity.Rigidity :=
  RigidityDiscriminator.rigidity_uninhabited p

theorem original_identity_still_absent (p : Poly) : ¬ HasE [] p FullPER.Application.originalIdentity :=
  HomogeneousOriginalIdentity.original_identity_uninhabited p

theorem original_fixed_scalar_still_absent : ¬ HasE [] ExactScalarFusion.c3
    (ExactScalarFusion.W FullPER.Application.originalQ) :=
  HomogeneousOriginalW.original_c3_not_W

theorem induction_only_raw_identity_absent (p : Poly) :
    ¬ HasX false true [] p (.identity .raw FullPER.Application.originalP FullPER.Application.originalQ) := by
  intro h
  have v := CompletionIndependence.InductionModel.fundamental h SigmaTagBoundary.emptyEnv
    TaggedPER.zeroEnv TaggedPER.zeroEnv SigmaTagBoundary.empty_admissible ⟨rfl,rfl⟩
  exact FullPER.Application.original_raw_distinct _ v.1

theorem joint_raw_identity_absent (p : Poly) :
    ¬ JointCompletion.HasJ [] p (.identity .raw FullPER.Application.originalP FullPER.Application.originalQ) := by
  intro h
  have v := JointCompletion.fundamental h FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  exact FullPER.Application.original_raw_distinct _ v.1

#print axioms original_fixed_scalar_still_absent
#print axioms induction_only_raw_identity_absent
#print axioms joint_raw_identity_absent
#print axioms CompletionIndependence.into_joint
#print axioms ExactScalarFusion.SelectiveCompletion.forward_fixedX
#print axioms ExactScalarFusion.SelectiveCompletion.induction_only_fixed_scalar
#print axioms joint_rigidity
#print axioms joint_compiler_identity
#print axioms joint_fixed_scalar
#print axioms original_rigidity_still_absent
#print axioms original_identity_still_absent
end RigidityInitiality.FullE.PositiveCompletion
