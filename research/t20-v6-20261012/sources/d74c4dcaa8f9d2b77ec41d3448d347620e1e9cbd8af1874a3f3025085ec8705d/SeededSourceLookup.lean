import SourceCorrectionHistories

namespace SeededSource
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC FiniteSidecar
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- An externally supplied natural seed, followed by the unchanged sidecar state. -/
def Input : Ty := .sigma N State
theorem input_form {Γ} (hc : Ctx Γ) : Form Γ Input :=
  .sigma (N_form hc) (state_form (.ext hc (N_form hc)))
def seeded (u p : Poly) : Poly := pairPoly u p
theorem seeded_has {u p : Poly} (hu : Has [] u N) (hp : Has [] p State) :
    Has [] (seeded u p) Input := .sigmaIntro (input_form .nil) (state_form .nil) hu hp

def liftTable (rows : List (List Nat)) : PR 3 :=
  .comp (tablePR rows 0) (fun i => .proj ⟨i.val, by omega⟩)
def cubePR (cube : List (List (List Nat))) : PR 3 :=
  lookupPR (.proj ⟨2, by decide⟩) (cube.map liftTable) (constantPR 3 0)
def cubeValue (cube : List (List (List Nat))) (z k u : Nat) : Nat :=
  tableValue (cube[u]?.getD []) 0 z k

theorem liftTable_denote (rows : List (List Nat)) (v : Nat → Nat) :
    (liftTable rows).denote v = tableValue rows 0 (v 0) (v 1) := by
  simp [liftTable, PR.denote, tablePR_denote]
theorem cubePR_denote (cube : List (List (List Nat))) (v : Nat → Nat) :
    (cubePR cube).denote v = cubeValue cube (v 0) (v 1) (v 2) := by
  simp only [cubePR, lookupPR_denote, List.map_map, Function.comp_def,
    liftTable_denote, constantPR_denote, PR.denote]
  generalize v 2 = u
  induction cube generalizing u with
  | nil => simp [lookupValue, cubeValue, tableValue]
  | cons row rows ih => cases u <;> simp [lookupValue, cubeValue] at *; exact ih _

def inputs : Nat → Poly
  | 0 => coarsePoly (sndPoly (.var 0))
  | 1 => tagPoly (sndPoly (.var 0))
  | 2 => fstPoly (.var 0)
  | _+3 => inputNumeral 0
def body (cube : List (List (List Nat))) : Poly := psub inputs (cubePR cube).compile

theorem body_has (cube : List (List (List Nat))) : Has [Input] (body cube) N := by
  have hc : Ctx [Input] := .ext .nil (input_form .nil)
  have hp : Has [Input] (.var 0) Input := .var (input_form hc) .zero
  have hs : Has [Input] (sndPoly (.var 0)) State :=
    .sigmaSnd (input_form hc) (state_form hc) hp
  have hm : MixedSubstitution (NatCtx 3) [Input] inputs Ty.param := by
    refine ⟨fun _ => .param hc, ?_⟩
    intro i A hi
    have he := nat_lookup_eq hi
    cases he
    change Has [Input] (inputs i) N
    cases i with
    | zero => exact coarse_has hc hs
    | succ i => cases i with
      | zero => exact tag_has hc hs
      | succ i => cases i with
        | zero => exact .sigmaFst (N_form hc) (input_form hc) hp
        | succ i => exact closed_has (inputNumeral_has 0) N_subst hc
  simpa only [body, mixed_param, N_subst] using has_mixed (cubePR cube).compile_has hc hm

structure Cubes where
  branch : List (List (List Nat))
  nextCoarse : List (List (List Nat))
  nextTag : List (List (List Nat))
def samplerBody (c : Cubes) : Poly :=
  pairPoly (body c.branch) (pack (body c.nextCoarse) (body c.nextTag) (.atom .i))
def sampler (c : Cubes) : Poly := abstract (samplerBody c)
theorem samplerBody_has (c : Cubes) : Has [Input] (samplerBody c) Reply := by
  have hc : Ctx [Input] := .ext .nil (input_form .nil)
  exact .sigmaIntro (reply_form hc) (state_form hc) (body_has c.branch)
    (pack_has hc (body_has c.nextCoarse) (body_has c.nextTag) (evidence_has hc))
theorem sampler_has (c : Cubes) : Has [] (sampler c) (arr Input Reply) :=
  .piIntro (form_arr (input_form .nil) (reply_form .nil)) (samplerBody_has c)
    (scoped_abstract (has_scoped (samplerBody_has c)))
theorem sampler_hasE (c : Cubes) :
    ExtensionalRepair.HasE [] (sampler c) (arr Input Reply) :=
  ExtensionalRepair.has_inclusion (sampler_has c)
theorem sampler_hasJ (c : Cubes) :
    JointCompletion.HasJ [] (sampler c) (arr Input Reply) := .hasBase (sampler_hasE c)

def RepresentsInput (p : Term) (z k u : Nat) : Prop :=
  Represents (secondTerm p) z k ∧ NatObs (firstTerm p) u

theorem seeded_represents {u p : Poly} {z k n : Nat}
    (hu : NatObs (eval u zeroEnv) n) (hp : Represents (eval p zeroEnv) z k) :
    RepresentsInput (eval (seeded u p) zeroEnv) z k n := by
  change RepresentsInput (pairTerm (eval u zeroEnv) (eval p zeroEnv)) z k n
  have hs := pair_second (eval u zeroEnv) (eval p zeroEnv)
  exact ⟨⟨NatObs.of_conv (hs.left .k) hp.1,
    NatObs.of_conv ((hs.left (.app .k .i)).left .k) hp.2⟩,
    NatObs.of_conv (pair_first _ _) hu⟩

theorem body_observes (cube : List (List (List Nat))) {p : Term} {z k u : Nat}
    (hp : RepresentsInput p z k u) :
    NatObs (eval (body cube) (cons p zeroEnv)) (cubeValue cube z k u) := by
  simp only [body, eval_sub]
  have ho := (cubePR cube).compile_obs (fun i => eval (inputs i) (cons p zeroEnv))
    (cons z (cons k (cons u (fun _ => 0))))
  apply (show (cubePR cube).denote (cons z (cons k (cons u (fun _ => 0)))) =
    cubeValue cube z k u from cubePR_denote _ _ ▸ rfl) ▸ ho
  intro i hi
  cases i with
  | zero => exact hp.1.1
  | succ i => cases i with
    | zero => exact hp.1.2
    | succ i => cases i with
      | zero => exact hp.2
      | succ i => omega

theorem sampler_observes (c : Cubes) {p : Term} {z k u : Nat}
    (hp : RepresentsInput p z k u) :
    NatObs (firstTerm (.app (eval (sampler c) zeroEnv) p)) (cubeValue c.branch z k u) ∧
    Represents (secondTerm (.app (eval (sampler c) zeroEnv) p))
      (cubeValue c.nextCoarse z k u) (cubeValue c.nextTag z k u) := by
  let b := eval (body c.branch) (cons p zeroEnv)
  let z' := eval (body c.nextCoarse) (cons p zeroEnv)
  let k' := eval (body c.nextTag) (cons p zeroEnv)
  have run : Conv (.app (eval (sampler c) zeroEnv) p)
      (pairTerm b (pairTerm z' (pairTerm k' .i))) :=
    P01Source.red_conv (abstraction_beta (samplerBody c) zeroEnv p)
  have hb := body_observes c.branch hp
  have hz := body_observes c.nextCoarse hp
  have hk := body_observes c.nextTag hp
  refine ⟨NatObs.of_conv ((run.left .k).trans (pair_first _ _)) hb, ?_⟩
  have hs := (run.left (.app .k .i)).trans (pair_second _ _)
  exact ⟨NatObs.of_conv ((hs.left .k).trans (pair_first _ _)) hz,
    NatObs.of_conv ((((hs.left (.app .k .i)).trans (pair_second _ _)).left .k).trans
      (pair_first _ _)) hk⟩

#print axioms sampler_has
#print axioms sampler_hasJ
#print axioms sampler_observes
end SeededSource
