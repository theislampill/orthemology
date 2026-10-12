import JointProofUniqueness
import OriginalProofUniqueness
import JointRecursorCongruence
import SourceTransport

namespace JointCompletion.ProofUniqueness.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.Intensional.Plus (PolyConvPlus)
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open JointCompletion.Controls (newMotive newMotive_subst)
open JointCompletion.InductionComputation
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def oldProofType : Ty := .identity .raw (.atom .i) (.atom .i)
theorem oldProofType_form {Γ} (hc : P01AC.ExtensionalRepair.CtxE Γ) :
    P01AC.ExtensionalRepair.FormE Γ oldProofType :=
  .identity (.raw hc) (.rawAtom (.raw hc)) (.rawAtom (.raw hc))

theorem original_bound_proofs_identical : P01AC.ExtensionalRepair.HasE
    [oldProofType,oldProofType] (.atom .i) (.identity oldProofType (.var 0) (.var 1)) := by
  have hc1 := P01AC.ExtensionalRepair.CtxE.ext .nil (oldProofType_form .nil)
  have hc := P01AC.ExtensionalRepair.CtxE.ext hc1 (oldProofType_form hc1)
  have h0 : P01AC.ExtensionalRepair.HasE [oldProofType,oldProofType] (.var 0) oldProofType :=
    .var (oldProofType_form hc) .zero
  have h1 : P01AC.ExtensionalRepair.HasE [oldProofType,oldProofType] (.var 1) oldProofType :=
    .var (oldProofType_form hc) (.succ .zero)
  exact P01AC.ExtensionalRepair.ProofUniqueness.identity_proof_unique hc h0 h1

/-- Same literal variable endpoints remain different in unrestricted raw syntax. -/
theorem bound_proofs_not_raw : ¬ PolyConvPlus (.var 0) (.var 1) := by
  intro h
  have hs := HenkinSourceTransport.source_plus_sound h
    (fun n => if n = 0 then CaseOperational.T.a0 else .a1)
  exact CaseOperational.atom_distinct (by simpa [HenkinSourceTransport.interp] using hs)

theorem new_bound_proofs_identical : HasJ [newMotive,newMotive] (.atom .i)
    (.identity newMotive (.var 0) (.var 1)) := by
  have h0F := JointCompletion.Controls.new_motive_form Ctx.nil
  have hc1 := CtxJ.ext .nil h0F
  have h1F : FormJ [newMotive] newMotive := by
    simpa only [wk,newMotive_subst] using Structural.form_wk h0F .nil h0F
  have hc := CtxJ.ext hc1 h1F
  have h2F : FormJ [newMotive,newMotive] newMotive := by
    simpa only [wk,newMotive_subst] using Structural.form_wk h1F hc1 h1F
  have h0 : HasJ [newMotive,newMotive] (.var 0) newMotive := by
    simpa only [wk,newMotive_subst] using HasJ.var (Structural.form_wk h1F hc1 h1F)
      (Lookup.zero (A := newMotive) (Γ := [newMotive]))
  have h1 : HasJ [newMotive,newMotive] (.var 1) newMotive := by
    apply HasJ.var h2F
    simpa only [wk,newMotive_subst] using Lookup.succ
      (Lookup.zero (A := newMotive) (Γ := [])) (B := newMotive)
  exact identity_proof_unique hc h0 h1

theorem new_carrier_not_old : ¬ P01AC.ExtensionalRepair.FormE [] newMotive :=
  JointCompletion.Controls.new_motive_not_old

/-- Any typed observation into a fixed carrier identifies identity proofs. -/
theorem typed_observer_constant {Γ A B x y e f observer}
    (hc : CtxJ Γ) (hB : FormJ Γ B)
    (he : HasJ Γ e (.identity A x y)) (hf : HasJ Γ f (.identity A x y))
    (ho : HasJ Γ observer (arr (.identity A x y) B)) :
    HasJ Γ (.atom .i) (.identity B (.app observer e) (.app observer f)) :=
  RecursorUniqueness.arrow_congr hc (Structural.has_form he) hB ho he hf
    (identity_proof_unique hc he hf)

/-- A numerical provenance observation of the same proof type has one count. -/
theorem numeric_observer_same_count {A x y e f observer j k}
    (he : HasJ [] e (.identity A x y)) (hf : HasJ [] f (.identity A x y))
    (ho : HasJ [] observer (arr (.identity A x y) N))
    (ce : PolyConvPlus (ClosedScalarInstances.scalarLeft (.app observer e)) (iterationPoly j))
    (cf : PolyConvPlus (ClosedScalarInstances.scalarLeft (.app observer f)) (iterationPoly k)) :
    j = k := by
  have hN := Structural.form_nat CtxJ.nil
  have hO := Structural.has_form ho
  exact DependentExtraction.identity_implies_count_eq
    (app_has hO hN ho he) (app_has hO hN ho hf) ce cf
    (typed_observer_constant .nil hN he hf ho)


/-- Provenance may instead be retained as an explicit natural label paired with evidence. -/
def labelledType : Ty := .sigma N oldProofType
def labelled (k : Nat) : Poly := pairPoly (inputNumeral k) (.atom .i)
theorem labelled_form {Γ} (hc : CtxJ Γ) : FormJ Γ labelledType :=
  .sigma (N_form hc) (.identity (.raw (.ext hc (N_form hc)))
    (.rawAtom (.raw (.ext hc (N_form hc)))) (.rawAtom (.raw (.ext hc (N_form hc)))))
theorem labelled_has (k : Nat) : HasJ [] (labelled k) labelledType := by
  have hH : FormJ [] oldProofType := .formBase (oldProofType_form .nil)
  have hr := HasJ.rawAtom (t := OrthemologyV2.Term.i) (FormJ.raw CtxJ.nil)
  have hi := HasJ.identityIntro hH hr hr (PolyConvPlus.refl _)
  exact .sigmaIntro (labelled_form .nil) hH (.hasBase (EffectiveNumerals.old_numeral_has k)) hi

/-- A source identity of labelled packages would force equal label observations. -/
theorem labels_equal_of_identity {j k r}
    (h : HasJ [] r (.identity labelledType (labelled j) (labelled k))) : j = k := by
  let P : Ty := .identity N (pren Nat.succ (fstPoly (labelled j))) (fstPoly (.var 0))
  have hS := labelled_form CtxJ.nil
  have hc := CtxJ.ext .nil hS
  have hSw : FormJ [labelledType] labelledType := labelled_form hc
  have hv : HasJ [labelledType] (.var 0) labelledType := .var hSw .zero
  have hj : HasJ [] (fstPoly (labelled j)) N := .sigmaFst (N_form .nil) hS (labelled_has j)
  have hk : HasJ [] (fstPoly (labelled k)) N := .sigmaFst (N_form .nil) hS (labelled_has k)
  have hP : FormJ [labelledType] P := .identity (N_form hc)
    (by simpa only [P01AC.BooleanPrimitive.N_subst, wk] using Structural.has_wk hj .nil hS)
    (.sigmaFst (N_form hc) hSw hv)
  have at_eq (z : Poly) : inst P z = .identity N (fstPoly (labelled j)) (fstPoly z) := by
    simp only [P,inst,subst,P01AC.BooleanPrimitive.N_subst,psub,P01F.cons,fstPoly]
    congr 2
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel (fstPoly (labelled j)) z Poly.var
  have hi := HasJ.identityIntro (.identity (N_form .nil) hj hj) hj hj (PolyConvPlus.refl _)
  have he := DependentExtraction.transport_erased .nil hS hP (labelled_has j) (labelled_has k) h
    ((at_eq (labelled j)).symm ▸ hi)
  have obs (n : Nat) : PolyConvPlus (ClosedScalarInstances.scalarLeft (fstPoly (labelled n))) (iterationPoly n) :=
    (PolyConvPlus.app (PolyConvPlus.app
      (P01AC.Intensional.Plus.polyConv_inclusion (P01AC.ExtensionalRepair.InternalGraph.pair_first _ _))
      (.refl _)) (.refl _)).trans (ClosedChurchIdentity.numeral_observation n)
  exact DependentExtraction.identity_implies_count_eq hj hk (obs j) (obs k)
    (by simpa only [at_eq] using he)

theorem distinct_labels_not_identical (r : Poly) :
    ¬ HasJ [] r (.identity labelledType (labelled 0) (labelled 1)) := by
  intro h
  have bad := labels_equal_of_identity h
  omega

#print axioms labelled_has
#print axioms distinct_labels_not_identical
#print axioms original_bound_proofs_identical
#print axioms bound_proofs_not_raw
#print axioms new_bound_proofs_identical
#print axioms typed_observer_constant
#print axioms numeric_observer_same_count
end JointCompletion.ProofUniqueness.Controls
