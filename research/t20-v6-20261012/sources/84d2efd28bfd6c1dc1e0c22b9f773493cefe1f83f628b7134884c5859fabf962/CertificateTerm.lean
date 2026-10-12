import RefutationCompleteness

namespace PRNegativeSearch
open P01AC P01D OrthemologyV2 OrthemologyV3
open P01AC.ExtensionalRepair P01AC.Intensional.Plus
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.BooleanIdentity
open FullPERTests JointCompletion PRConditionalRefutation
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Literal erased source certificate template, depending only on the failing index. -/
def certificateTerm (k : Nat) : Poly :=
  abstract (abstract (.app (.var 1)
    (jPoly (.atom .i) (.atom .zero) (.app (.var 0) (inputNumeral k)))))

/-- Named refinement of the literal witness constructed in the frozen
    existential refutation_template proof. The source rules are unchanged. -/
theorem certificateTerm_has (f : PR 2) (e k : Nat)
    (bad : f.denote (inputs k e) ≠ 0) :
    HasE [] (certificateTerm k) (arr NoConfusion (arr (programType f e) .bottom)) := by
  have c1 : Ctx [NoConfusion] := .ext .nil (noConfusion_form .nil)
  have p1 : Form [NoConfusion] (programType f e) := form_closed (programType_form f e) c1
  have c2 : Ctx [programType f e,NoConfusion] := .ext c1 p1
  have p2 : Form [programType f e,NoConfusion] (programType f e) := form_closed (programType_form f e) c2
  have hp : HasE [programType f e,NoConfusion] (.var 0) (programType f e) := by
    have v := HasE.var (form_inclusion (form_wk p1 c1 p1)) (Lookup.zero (A := programType f e) (Γ := [NoConfusion]))
    simpa only [wk,program_subst] using v
  have hn : HasE [programType f e,NoConfusion] (inputNumeral k) N :=
    has_inclusion (closed_has (inputNumeral_has k) N_subst c2)
  have ho := closed_has (observation_has f e k) (fun _ => rfl) c2
  have hi : Form [programType f e,NoConfusion]
      (.identity .raw (observationPoly f e k) (.atom .zero)) :=
    .identity (.raw c2) ho (.rawAtom (.raw c2))
  have htest : HasE [programType f e,NoConfusion] (.app (.var 0) (inputNumeral k))
      (.identity .raw (observationPoly f e k) (.atom .zero)) := by
    have h := HasE.piElim (form_inclusion p2)
      (show FormE _ (inst _ (inputNumeral k)) from (body_inst f e k).symm ▸ form_inclusion hi) hp hn
    simpa only [body_inst] using h
  have clash := clash_of_test c2 f e k bad htest
  have hnc : HasE [programType f e,NoConfusion] (.var 1) NoConfusion :=
    .var (form_inclusion (noConfusion_form c2)) (.succ .zero)
  have bot := HasE.piElim (form_inclusion (noConfusion_form c2))
    (show FormE _ (inst (wk .bottom) _) from form_inclusion (.bottom c2)) hnc clash
  let b : Poly := .app (.var 1) (jPoly (.atom .i) (.atom .zero) (.app (.var 0) (inputNumeral k)))
  have hb : HasE [programType f e,NoConfusion] b .bottom := bot
  have inner : HasE [NoConfusion] (abstract b) (arr (programType f e) .bottom) :=
    .piIntro (form_inclusion (form_arr p1 (.bottom c1))) hb
      (scoped_abstract (P01AC.ExtensionalRepair.Structural.has_scoped hb))
  change HasE [] (abstract (abstract b)) _
  refine .piIntro
    (form_inclusion (form_arr (noConfusion_form .nil)
      (form_arr (programType_form f e) (.bottom .nil)))) ?_
    (scoped_abstract (P01AC.ExtensionalRepair.Structural.has_scoped inner))
  simpa only [wk,subst_arr,program_subst,subst] using inner


#print axioms certificateTerm_has
end PRNegativeSearch
