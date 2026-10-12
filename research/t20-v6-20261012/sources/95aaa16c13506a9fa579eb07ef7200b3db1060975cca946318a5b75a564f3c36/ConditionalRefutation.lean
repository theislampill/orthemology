import FullPERHalting
import Initiality
import JointSyntax
import HasEStructuralBase

namespace PRConditionalRefutation
open P01AC P01D OrthemologyV2 OrthemologyV3
open P01AC.ExtensionalRepair
open P01AC.Intensional.Plus
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.BooleanIdentity
open FullPERTests JointCompletion
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def RawClash : Ty := .identity .raw (.atom .zero) (.atom .one)
def NoConfusion : Ty := arr RawClash .bottom

theorem clash_form {Γ : Tel} (hc : Ctx Γ) : Form Γ RawClash :=
  .identity (.raw hc) (.rawAtom (.raw hc)) (.rawAtom (.raw hc))
theorem noConfusion_form {Γ : Tel} (hc : Ctx Γ) : Form Γ NoConfusion :=
  form_arr (clash_form hc) (.bottom hc)

theorem form_closed {A : Ty} (h : Form [] A) {Γ : Tel} (hc : Ctx Γ) : Form Γ A := by
  have hs : MixedSubstitution [] Γ Poly.var Ty.param :=
    ⟨fun _ => .param hc, fun h => nomatch h⟩
  simpa only [mixed_param, subst_id] using form_mixed h hc hs

def observationPoly (f : PR 2) (e k : Nat) : Poly :=
  .app (.app (.app (simFamily f e) (inputNumeral k)) (.atom .zero)) (.atom .one)

theorem observation_has (f : PR 2) (e k : Nat) : Has [] (observationPoly f e k) .raw := by
  have hr : Form [] .raw := .raw .nil
  have hB : Form [] B := B_form .nil
  have pn := app_has (form_arr (N_form .nil) hB) hB (simFamily_has f e) (inputNumeral_has k)
  have br : Has [] (.app (simFamily f e) (inputNumeral k)) (arr .raw (arr .raw .raw)) :=
    .allElim hB hr (form_arr hr (form_arr hr hr)) pn
  exact app_has (form_arr hr hr) hr
    (app_has (form_arr hr (form_arr hr hr)) (form_arr hr hr) br (.rawAtom hr)) (.rawAtom hr)

theorem program_subst (f : PR 2) (e : Nat) (σ : Nat → Poly) :
    subst σ (programType f e) = programType f e := by
  simp only [programType, testType, subst, N_subst, testBody, psub,
    psub_closed (has_scoped (simFamily_has f e)), pup, P01F.cons]

theorem body_inst (f : PR 2) (e k : Nat) :
    inst (.identity .raw (testBody (simFamily f e)) (.atom .zero)) (inputNumeral k) =
      .identity .raw (observationPoly f e k) (.atom .zero) := by
  simp only [inst,subst,testBody,observationPoly,psub,P01F.cons,
    psub_closed (has_scoped (simFamily_has f e))]

theorem observation_conversion (f : PR 2) (e k : Nat)
    (bad : f.denote (inputs k e) ≠ 0) :
    PolyConvPlus (observationPoly f e k) (.atom .one) := by
  apply (closed_conversion_iff (has_scoped (observation_has f e k)) (show Scoped 0 (.atom .one) from trivial)).mpr
  simpa [observationPoly,eval,observationAt,observe,P01AC.IdentityComplexity.canonical,
    bad,decide_true,pick,↓reduceIte] using simFamily_obs f e k

/-- Actual J transports the finite failed test into Raw zero/one equality.
    Every formation/type premise here is old source syntax. -/
theorem clash_of_test {Γ : Tel} (hc : Ctx Γ) (f : PR 2) (e k : Nat)
    (bad : f.denote (inputs k e) ≠ 0) {r : Poly}
    (hr : HasE Γ r (.identity .raw (observationPoly f e k) (.atom .zero))) :
    HasE Γ (jPoly (.atom .i) (.atom .zero) r) RawClash := by
  have raw : Form Γ .raw := .raw hc
  have obs : Has Γ (observationPoly f e k) .raw :=
    closed_has (observation_has f e k) (fun _ => rfl) hc
  have z : Has Γ (.atom .zero) .raw := .rawAtom raw
  have o : Has Γ (.atom .one) .raw := .rawAtom raw
  let P : Ty := .identity .raw (.var 0) (.atom .one)
  have cr : Ctx (.raw :: Γ) := .ext hc raw
  have hP : Form (.raw :: Γ) P := .identity (.raw cr) (.var (.raw cr) .zero) (.rawAtom (.raw cr))
  have hb : HasE Γ (.atom .i) (.identity .raw (observationPoly f e k) (.atom .one)) :=
    .identityIntro (form_inclusion (.identity raw obs o)) (has_inclusion obs) (has_inclusion o)
      (observation_conversion f e k bad)
  exact RigidityInitiality.transport_source hc raw hP obs z hr hb

/-- Finite computation constructs an old-E implication. It does not introduce
    no-confusion as a rule or assert that its antecedent is derivable. -/
theorem refutation_template (f : PR 2) (e k : Nat)
    (bad : f.denote (inputs k e) ≠ 0) :
    ∃ t : Poly, HasE [] t (arr NoConfusion (arr (programType f e) .bottom)) := by
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
  refine ⟨abstract (abstract b), .piIntro
    (form_inclusion (form_arr (noConfusion_form .nil)
      (form_arr (programType_form f e) (.bottom .nil)))) ?_
    (scoped_abstract (P01AC.ExtensionalRepair.Structural.has_scoped inner))⟩
  simpa only [wk,subst_arr,program_subst,subst] using inner

/-- The supplied no-confusion proof remains an explicit actual HasJ premise. -/
theorem refute_failed_test (f : PR 2) (e k : Nat)
    (bad : f.denote (inputs k e) ≠ 0) {c : Poly}
    (hc : HasJ [] c NoConfusion) :
    ∃ r : Poly, HasJ [] r (arr (programType f e) .bottom) := by
  obtain ⟨t, ht⟩ := refutation_template f e k bad
  refine ⟨.app t c, ?_⟩
  have h := HasJ.piElim (.formBase (form_inclusion
      (form_arr (noConfusion_form .nil) (form_arr (programType_form f e) (.bottom .nil)))))
    (show FormJ [] (inst (wk (arr (programType f e) .bottom)) c) from by
      simpa only [inst_wk] using FormJ.formBase (form_inclusion (form_arr (programType_form f e) (.bottom .nil))))
    (.hasBase ht) hc
  simpa only [inst_wk] using h

#print axioms refutation_template
#print axioms refute_failed_test
end PRConditionalRefutation
