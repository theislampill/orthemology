import FiniteCorrectionTable

namespace FiniteSidecar
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.IdentityComplexity (canonical)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def Evidence : Ty := .identity .raw (.atom .i) (.atom .i)
def Labelled : Ty := .sigma N Evidence
def State : Ty := .sigma N Labelled
def Reply : Ty := .sigma N State

def pack (coarse tag evidence : Poly) : Poly := pairPoly coarse (pairPoly tag evidence)
def encodeState (coarse tag : Nat) : Poly := pack (inputNumeral coarse) (inputNumeral tag) (.atom .i)

theorem evidence_form {Γ} (hc : Ctx Γ) : Form Γ Evidence :=
  .identity (.raw hc) (.rawAtom (.raw hc)) (.rawAtom (.raw hc))
theorem labelled_form {Γ} (hc : Ctx Γ) : Form Γ Labelled :=
  .sigma (N_form hc) (evidence_form (.ext hc (N_form hc)))
theorem state_form {Γ} (hc : Ctx Γ) : Form Γ State :=
  .sigma (N_form hc) (labelled_form (.ext hc (N_form hc)))
theorem reply_form {Γ} (hc : Ctx Γ) : Form Γ Reply :=
  .sigma (N_form hc) (state_form (.ext hc (N_form hc)))
theorem evidence_has {Γ} (hc : Ctx Γ) : Has Γ (.atom .i) Evidence :=
  .identityIntro (evidence_form hc) (.rawAtom (.raw hc)) (.rawAtom (.raw hc)) (.refl _)
theorem pack_has {Γ z k e} (hc : Ctx Γ) (hz : Has Γ z N) (hk : Has Γ k N)
    (he : Has Γ e Evidence) : Has Γ (pack z k e) State :=
  .sigmaIntro (state_form hc) (labelled_form hc) hz
    (.sigmaIntro (labelled_form hc) (evidence_form hc) hk he)
theorem encodeState_has (z k : Nat) : Has [] (encodeState z k) State :=
  pack_has .nil (inputNumeral_has z) (inputNumeral_has k) (evidence_has .nil)

def coarsePoly (p : Poly) : Poly := fstPoly p
def tagPoly (p : Poly) : Poly := fstPoly (sndPoly p)

theorem coarse_has {Γ p} (hc : Ctx Γ) (hp : Has Γ p State) : Has Γ (coarsePoly p) N :=
  .sigmaFst (N_form hc) (state_form hc) hp
theorem tag_has {Γ p} (hc : Ctx Γ) (hp : Has Γ p State) : Has Γ (tagPoly p) N :=
  .sigmaFst (N_form hc) (labelled_form hc) (.sigmaSnd (state_form hc) (labelled_form hc) hp)

def tableInputs : Nat → Poly
  | 0 => coarsePoly (.var 0)
  | 1 => tagPoly (.var 0)
  | _+2 => inputNumeral 0

def tableBody (rows : List (List Nat)) (fallback : Nat := 0) : Poly :=
  psub tableInputs (tablePR rows fallback).compile

theorem tableBody_has (rows : List (List Nat)) (fallback : Nat) :
    Has [State] (tableBody rows fallback) N := by
  have hc : Ctx [State] := .ext .nil (state_form .nil)
  have hp : Has [State] (.var 0) State := .var (state_form hc) .zero
  have hm : MixedSubstitution (NatCtx 2) [State] tableInputs Ty.param := by
    refine ⟨fun _ => .param hc, ?_⟩
    intro i A hi
    have he := nat_lookup_eq hi
    cases he
    change Has [State] (tableInputs i) N
    cases i with
    | zero => exact coarse_has hc hp
    | succ i => cases i with
      | zero => exact tag_has hc hp
      | succ i => exact closed_has (inputNumeral_has 0) N_subst hc
  simpa only [tableBody, mixed_param, N_subst] using
    has_mixed (table_typed rows fallback) hc hm

def tableObserver (rows : List (List Nat)) (fallback : Nat := 0) : Poly :=
  abstract (tableBody rows fallback)
theorem tableObserver_has (rows : List (List Nat)) (fallback : Nat) :
    Has [] (tableObserver rows fallback) (arr State N) :=
  .piIntro (form_arr (state_form .nil) (N_form .nil)) (tableBody_has rows fallback)
    (scoped_abstract (has_scoped (tableBody_has rows fallback)))

/-- The entire branch/next-coarse/next-tag row is read from the same source state. -/
structure Tables where
  branch : List (List Nat)
  nextCoarse : List (List Nat)
  nextTag : List (List Nat)

def controllerBody (tables : Tables) : Poly :=
  pairPoly (tableBody tables.branch) (pack (tableBody tables.nextCoarse)
    (tableBody tables.nextTag) (.atom .i))
def controller (tables : Tables) : Poly := abstract (controllerBody tables)

theorem controllerBody_has (tables : Tables) : Has [State] (controllerBody tables) Reply := by
  have hc : Ctx [State] := .ext .nil (state_form .nil)
  exact .sigmaIntro (reply_form hc) (state_form hc) (tableBody_has tables.branch 0)
    (pack_has hc (tableBody_has tables.nextCoarse 0) (tableBody_has tables.nextTag 0)
      (evidence_has hc))
theorem controller_has (tables : Tables) : Has [] (controller tables) (arr State Reply) :=
  .piIntro (form_arr (state_form .nil) (reply_form .nil)) (controllerBody_has tables)
    (scoped_abstract (has_scoped (controllerBody_has tables)))
theorem controller_hasE (tables : Tables) :
    P01AC.ExtensionalRepair.HasE [] (controller tables) (arr State Reply) :=
  P01AC.ExtensionalRepair.has_inclusion (controller_has tables)
theorem controller_hasJ (tables : Tables) :
    JointCompletion.HasJ [] (controller tables) (arr State Reply) := .hasBase (controller_hasE tables)

/-- Count fidelity concerns ordinary data projections, not proof-realizer identities. -/
def Represents (p : Term) (z k : Nat) : Prop :=
  NatObs (firstTerm p) z ∧ NatObs (firstTerm (secondTerm p)) k

theorem encoded_represents (z k : Nat) : Represents (eval (encodeState z k) zeroEnv) z k := by
  change Represents (pairTerm (canonical z) (pairTerm (canonical k) .i)) z k
  exact ⟨NatObs.of_conv (pair_first _ _) (canonical_obs z),
    NatObs.of_conv (((pair_second _ _).left .k).trans (pair_first _ _)) (canonical_obs k)⟩

theorem tableBody_observes (rows : List (List Nat)) (fallback : Nat)
    {p : Term} {z k : Nat} (hp : Represents p z k) :
    NatObs (eval (tableBody rows fallback) (cons p zeroEnv))
      (tableValue rows fallback z k) := by
  simp only [tableBody, eval_sub]
  apply table_observes rows fallback _ (cons z (cons k (fun _ => 0)))
  intro i hi
  cases i with
  | zero => exact hp.1
  | succ i => cases i with
    | zero => exact hp.2
    | succ i => omega

theorem tableObserver_observes (rows : List (List Nat)) (fallback : Nat)
    {p : Term} {z k : Nat} (hp : Represents p z k) :
    NatObs (.app (eval (tableObserver rows fallback) zeroEnv) p)
      (tableValue rows fallback z k) :=
  NatObs.of_conv (P01Source.red_conv (abstraction_beta (tableBody rows fallback) zeroEnv p))
    (tableBody_observes rows fallback hp)

/-- A deterministic correction returns the exact joint branch and next state. -/
theorem controller_observes (tables : Tables) {p : Term} {z k : Nat}
    (hp : Represents p z k) :
    NatObs (firstTerm (.app (eval (controller tables) zeroEnv) p))
      (tableValue tables.branch 0 z k) ∧
    Represents (secondTerm (.app (eval (controller tables) zeroEnv) p))
      (tableValue tables.nextCoarse 0 z k) (tableValue tables.nextTag 0 z k) := by
  let b := eval (tableBody tables.branch) (cons p zeroEnv)
  let z' := eval (tableBody tables.nextCoarse) (cons p zeroEnv)
  let k' := eval (tableBody tables.nextTag) (cons p zeroEnv)
  have run : Conv (.app (eval (controller tables) zeroEnv) p)
      (pairTerm b (pairTerm z' (pairTerm k' .i))) :=
    P01Source.red_conv (abstraction_beta (controllerBody tables) zeroEnv p)
  have hb := tableBody_observes tables.branch 0 hp
  have hz := tableBody_observes tables.nextCoarse 0 hp
  have hk := tableBody_observes tables.nextTag 0 hp
  refine ⟨NatObs.of_conv ((run.left .k).trans (pair_first _ _)) hb, ?_⟩
  have hs := (run.left (.app .k .i)).trans (pair_second _ _)
  exact ⟨NatObs.of_conv ((hs.left .k).trans (pair_first _ _)) hz,
    NatObs.of_conv ((((hs.left (.app .k .i)).trans (pair_second _ _)).left .k).trans
      (pair_first _ _)) hk⟩

/-- Arbitrary finite correction rows, with default 0 outside the represented rectangle. -/
def finiteTables (Z M : Nat) (branch nextCoarse nextTag : Nat → Nat → Nat) : Tables :=
  ⟨tabulate Z M branch, tabulate Z M nextCoarse, tabulate Z M nextTag⟩

theorem finite_controller_observes {Z M z k : Nat}
    (branch nextCoarse nextTag : Nat → Nat → Nat) (hz : z < Z) (hk : k < M)
    {p : Term} (hp : Represents p z k) :
    NatObs (firstTerm (.app (eval (controller (finiteTables Z M branch nextCoarse nextTag)) zeroEnv) p))
      (branch z k) ∧
    Represents (secondTerm (.app (eval (controller (finiteTables Z M branch nextCoarse nextTag)) zeroEnv) p))
      (nextCoarse z k) (nextTag z k) := by
  simpa only [finiteTables, tabulate_value _ hz hk] using
    controller_observes (finiteTables Z M branch nextCoarse nextTag) hp

#print axioms controller_hasE
#print axioms controller_hasJ
#print axioms finite_controller_observes
end FiniteSidecar
