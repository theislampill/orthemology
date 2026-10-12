import SourceUniqueness
import InternalRecursorPrinciple
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity InternalRecursorPrinciple
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def uniquePointProof : Poly :=
  sndPoly (.app (.app (.var 0) (totalStep (recTotalStep (.var 1)))) (totalSeed (.var 2)))

theorem rigidity_type_closed : twk Rigidity = Rigidity := by
  simp [twk, trename, Rigidity, ZeroAt, StepAt, ResultAt, NT, N, NBody, arr, wk, subst, liftRen]

theorem internal_unique_point :
    HasE [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] uniquePointProof
      (.identity A (.app (.var 3) (.var 0)) (.app (.app (.var 0) (.var 4)) (.var 5))) := by
  have cR := Ctx.ext Ctx.nil (rigidity_formed Ctx.nil)
  have cA := Ctx.ext cR (show Form [Rigidity] A from .param cR)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  have cZ := Ctx.ext cU (zero_law_formed cR)
  have cS := Ctx.ext cZ (step_law_formed cR)
  have cN := Ctx.ext cS (N_form cS)
  have hn : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 0) N :=
    .var (N_form cN) .zero
  have hu : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 3) (arr N A) :=
    .var (form_arr (N_form cN) (.param cN)) (.succ (.succ (.succ .zero)))
  have hf : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 4) End :=
    .var (form_arr (.param cN) (.param cN)) (.succ (.succ (.succ (.succ .zero))))
  have ha : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 5) A :=
    .var (.param cN) (.succ (.succ (.succ (.succ (.succ .zero)))))
  have rz : Lookup [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] 2 (wk (wk (wk ZeroLaw))) :=
    .succ (.succ .zero)
  have hz0 := Has.var (lookup_form cN rz) rz
  have hz : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 2)
      (RecZero (.var 5) (.var 3)) := by
    simpa [RecZero, ZeroLaw, wk, subst, A, pren, psub, zero,
      P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] using hz0
  have rs : Lookup [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] 1 (wk (wk StepLaw)) :=
    .succ .zero
  have hs0 := Has.var (lookup_form cN rs) rs
  have hs : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 1)
      (RecStep (.var 4) (.var 3)) := by
    simpa [RecStep, RecStepBody, StepLaw, wk, subst, A, pren, psub, pup, N, NBody, arr,
      P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)] using hs0
  have rr : Lookup [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] 6
      (wk (wk (wk (wk (wk (wk (wk Rigidity))))))) :=
    .succ (.succ (.succ (.succ (.succ (.succ .zero)))))
  have hr0 := Has.var (lookup_form cN rr) rr
  have hr : Has [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] (.var 6) Rigidity := by
    simpa only [wk, rigidity_subst] using hr0
  exact recursor_unique_source cN hf ha hu hz hs (has_inclusion hr) hn


theorem uniquePointProof_scoped : Scoped 7 uniquePointProof := by
  have hz : Scoped 7 zero := scoped_mono (has_scoped (inputNumeral_has 0)) (by simp [Scoped])
  have hs : Scoped 8 succPoly := scoped_mono (has_scoped succ_has) (by simp [Scoped])
  have hnext : Scoped 8 nextIndex := ⟨hs, scoped_fst (by simp [Scoped] : Scoped 8 (.var 0))⟩
  have hd : Scoped 8 (recTotalStep (.var 1)) := by
    change Scoped 8 (.app (.var 2) (fstPoly (.var 0)))
    exact ⟨by simp [Scoped], scoped_fst (by simp [Scoped])⟩
  have hstep : Scoped 7 (totalStep (recTotalStep (.var 1))) :=
    scoped_abstract (scoped_pair hnext hd)
  exact scoped_snd ⟨⟨by simp [Scoped], hstep⟩, scoped_pair hz (by simp [Scoped])⟩

def uniqueUniformProof : Poly :=
  abstract (abstract (abstract (abstract (abstract (abstract uniquePointProof)))))

theorem internal_uniqueness_under_rigidity : HasE [Rigidity] uniqueUniformProof Uniqueness := by
  have cR := Ctx.ext Ctx.nil (rigidity_formed Ctx.nil)
  have cA := Ctx.ext cR (show Form [Rigidity] A from .param cR)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  have hZ := zero_law_formed cR
  have hS := step_law_formed cR
  have hU := unique_conclusion_formed cR
  have h1 := HasE.piIntro (form_inclusion hU) internal_unique_point
    (scoped_abstract uniquePointProof_scoped)
  have h2 := HasE.piIntro (form_inclusion (.pi hS hU)) h1
    (scoped_abstract (scoped_abstract uniquePointProof_scoped))
  have h3 := HasE.piIntro (form_inclusion (.pi hZ (.pi hS hU))) h2
    (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped)))
  have h4 := HasE.piIntro
    (form_inclusion (.pi (form_arr (N_form cF) (.param cF)) (.pi hZ (.pi hS hU)))) h3
    (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped))))
  have h5 := HasE.piIntro
    (form_inclusion (.pi (form_arr (.param cA) (.param cA))
      (.pi (form_arr (N_form cF) (.param cF)) (.pi hZ (.pi hS hU))))) h4
    (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped)))))
  have h6 := HasE.piIntro
    (form_inclusion (.pi (.param cR) (.pi (form_arr (.param cA) (.param cA))
      (.pi (form_arr (N_form cF) (.param cF)) (.pi hZ (.pi hS hU)))))) h5
    (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped))))))
  apply HasE.allIntro (form_inclusion (uniqueness_formed cR))
  simpa only [twkTel, List.map_cons, List.map_nil, rigidity_type_closed] using h6

theorem uniqueness_term_closed (σ : Nat → Poly) : subst σ Uniqueness = Uniqueness := by
  simp [Uniqueness, ZeroLaw, StepLaw, UniqueConclusion, A, End, N, NBody,
    arr, wk, subst, psub, pup, pren,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))]

/-- The exact previously formed generic internal recursor-uniqueness
    proposition follows from explicit internal Rigidity in the unchanged
    original HasE calculus. This is a closed source implication, not a new rule. -/
theorem rigidity_implies_internal_uniqueness :
    HasE [] (abstract uniqueUniformProof) (arr Rigidity Uniqueness) := by
  apply HasE.piIntro (form_inclusion (form_arr (rigidity_formed Ctx.nil) (uniqueness_formed Ctx.nil)))
  · simpa only [wk, uniqueness_term_closed] using internal_uniqueness_under_rigidity
  · exact scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract
      (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped))))))

#print axioms internal_unique_point
#print axioms rigidity_implies_internal_uniqueness
end RigidityInitiality
