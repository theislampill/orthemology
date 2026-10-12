/- Actual unchanged-HasE conditional refutation of the original faithful-Raw
   identity. NoConfusion remains the explicit antecedent, not a new rule. -/
import SourceRawSeparator
import Initiality
import HasEStructuralBase

namespace OriginalRawSeparator.Conditional
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.ExtensionalRepair
open P01AC.Intensional.Plus (PolyConvPlus)
open P01AC.BooleanPrimitive (psub_closed)
open FullPER.Application (originalP originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The same literal conditional antecedent used by the finite-test templates. -/
def RawClash : Ty := .identity .raw (.atom .zero) (.atom .one)
def NoConfusion : Ty := arr RawClash .bottom

theorem clash_form {Γ : Tel} (hc : Ctx Γ) : Form Γ RawClash :=
  .identity (.raw hc) (.rawAtom (.raw hc)) (.rawAtom (.raw hc))
theorem noConfusion_form {Γ : Tel} (hc : Ctx Γ) : Form Γ NoConfusion :=
  P01AC.form_arr (clash_form hc) (.bottom hc)

theorem closed_raw {Γ : Tel} (hc : Ctx Γ) {p : Poly} (hp : Scoped 0 p) : Has Γ p .raw := by
  induction p with
  | var n => exact False.elim (Nat.not_lt_zero n hp)
  | atom t => exact .rawAtom (.raw hc)
  | app f a ihf iha => exact .rawApp (.raw hc) (ihf hp.1) (iha hp.2)

theorem originalP_closed : Scoped 0 originalP :=
  P01AC.has_scoped P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed_has

theorem originalQ_closed : Scoped 0 originalQ :=
  P01AC.has_scoped P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has

-- The finite probe contains no term variables.
theorem probe_closed : Scoped 0 probeP := by
  simp [probeP, tailP, pairPoly, Scoped]

theorem context_subst (t : Poly) (σ : Nat → Poly) :
    psub σ (contextPoly t) = contextPoly (psub σ t) := by
  simp only [contextPoly, psub, psub_closed probe_closed]

theorem context_raw {Γ : Tel} (hc : Ctx Γ) {p : Poly} (hp : Has Γ p .raw) :
    Has Γ (contextPoly p) .raw := by
  have raw : Form Γ .raw := .raw hc
  exact .rawApp raw (.rawApp raw (.rawApp raw (.rawApp raw hp
    (closed_raw hc probe_closed)) (.rawAtom raw)) (.rawAtom raw)) (.rawAtom raw)

def RawIdentity : Ty := .identity .raw originalP originalQ

theorem rawIdentity_subst (σ : Nat → Poly) : subst σ RawIdentity = RawIdentity := by
  simp only [RawIdentity, subst, psub_closed originalP_closed, psub_closed originalQ_closed]

theorem rawIdentity_form {Γ : Tel} (hc : Ctx Γ) : Form Γ RawIdentity :=
  .identity (.raw hc) (closed_raw hc originalP_closed) (closed_raw hc originalQ_closed)

/-- Two old J applications; both conversion leaves use the literal finite separator. -/
def clashWitness (e : Poly) : Poly :=
  jPoly (jPoly (.atom .i) originalQ e) (.atom .one) (.atom .i)

theorem clash_of_original {Γ : Tel} (hc : Ctx Γ) {e : Poly}
    (he : HasE Γ e RawIdentity) : HasE Γ (clashWitness e) RawClash := by
  have raw : Form Γ .raw := .raw hc
  have hp : Has Γ originalP .raw := closed_raw hc originalP_closed
  have hq : Has Γ originalQ .raw := closed_raw hc originalQ_closed
  have hz : Has Γ (.atom .zero) .raw := .rawAtom raw
  have ho : Has Γ (.atom .one) .raw := .rawAtom raw
  have cr : Ctx (.raw :: Γ) := .ext hc raw
  let P : Ty := .identity .raw (.atom .zero) (contextPoly (.var 0))
  have hP : Form (.raw :: Γ) P := .identity (.raw cr) (.rawAtom (.raw cr))
    (context_raw cr (.var (.raw cr) .zero))
  have atP (p : Poly) : inst P p = .identity .raw (.atom .zero) (contextPoly p) := by
    simp only [P, inst, subst, context_subst, psub, P01F.cons]
  have start : HasE Γ (.atom .i) (inst P originalP) := by
    rw [atP]
    exact .identityIntro (form_inclusion (.identity raw hz (context_raw hc hp)))
      (has_inclusion hz) (has_inclusion (context_raw hc hp)) source_left.symm
  have moved := RigidityInitiality.transport_source hc raw hP hp hq he start
  rw [atP] at moved
  let Q : Ty := .identity .raw (.atom .zero) (.var 0)
  have hQ : Form (.raw :: Γ) Q := .identity (.raw cr) (.rawAtom (.raw cr))
    (.var (.raw cr) .zero)
  have finish : HasE Γ (.atom .i) (.identity .raw (contextPoly originalQ) (.atom .one)) :=
    .identityIntro (form_inclusion (.identity raw (context_raw hc hq) ho))
      (has_inclusion (context_raw hc hq)) (has_inclusion ho) source_right
  exact RigidityInitiality.transport_source hc raw hQ (context_raw hc hq) ho finish moved

def refutationBody : Poly := .app (.var 1) (clashWitness (.var 0))
def witness : Poly := abstract (abstract refutationBody)

/-- A closed, actual old-E proof of NoConfusion → (Id_Raw(P,Q) → Bottom). -/
theorem witness_has : HasE [] witness (arr NoConfusion (arr RawIdentity .bottom)) := by
  have c1 : Ctx [NoConfusion] := .ext .nil (noConfusion_form .nil)
  have p1 : Form [NoConfusion] RawIdentity := rawIdentity_form c1
  have c2 : Ctx [RawIdentity, NoConfusion] := .ext c1 p1
  have hp : HasE [RawIdentity, NoConfusion] (.var 0) RawIdentity := by
    have h := HasE.var (form_inclusion (P01AC.form_wk p1 c1 p1))
      (Lookup.zero (A := RawIdentity) (Γ := [NoConfusion]))
    simpa only [wk, rawIdentity_subst] using h
  have clash := clash_of_original c2 hp
  have hnc : HasE [RawIdentity, NoConfusion] (.var 1) NoConfusion :=
    .var (form_inclusion (noConfusion_form c2)) (.succ .zero)
  have hb : HasE [RawIdentity, NoConfusion] refutationBody .bottom :=
    .piElim (form_inclusion (noConfusion_form c2)) (form_inclusion (.bottom c2)) hnc clash
  have inner : HasE [NoConfusion] (abstract refutationBody) (arr RawIdentity .bottom) :=
    .piIntro (form_inclusion (P01AC.form_arr p1 (.bottom c1))) hb
      (scoped_abstract (P01AC.ExtensionalRepair.Structural.has_scoped hb))
  apply HasE.piIntro
    (form_inclusion (P01AC.form_arr (noConfusion_form .nil)
      (P01AC.form_arr (rawIdentity_form .nil) (.bottom .nil))))
    (show HasE [NoConfusion] (abstract refutationBody) (wk (arr RawIdentity .bottom)) from by
      simpa only [wk, subst_arr, rawIdentity_subst, subst] using inner)
    (scoped_abstract (P01AC.ExtensionalRepair.Structural.has_scoped inner))

theorem witness_closed : Scoped 0 witness :=
  P01AC.ExtensionalRepair.Structural.has_scoped witness_has

/-- The full literal formula, without local type abbreviations. -/
theorem literal_witness_has : HasE [] witness
    (arr (arr (.identity .raw (.atom .zero) (.atom .one)) .bottom)
      (arr (.identity .raw originalP originalQ) .bottom)) := witness_has

/-- Supplied old-E no-confusion evidence specializes the conditional proof. -/
theorem refute_with_noConfusion {nc : Poly} (hn : HasE [] nc NoConfusion) :
    HasE [] (.app witness nc) (arr RawIdentity .bottom) := by
  have h := HasE.piElim (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed witness_has)
    (show FormE [] (inst (wk (arr RawIdentity .bottom)) nc) by
      simpa only [inst_wk] using form_inclusion
        (P01AC.form_arr (rawIdentity_form Ctx.nil) (.bottom .nil))) witness_has hn
  simpa only [inst_wk] using h

#print axioms clash_of_original
#print axioms witness_has
#print axioms refute_with_noConfusion
#print axioms literal_witness_has
#print axioms witness_closed
end OriginalRawSeparator.Conditional
