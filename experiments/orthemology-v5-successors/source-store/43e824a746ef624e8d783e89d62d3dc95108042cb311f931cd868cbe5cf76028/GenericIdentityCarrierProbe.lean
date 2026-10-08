/-
Isolated T20 generic Church identity-carrier probe.
No inherited calculus, conversion, compiler or endpoint is changed.
This module does not prove the literal compiled x / x+0 identity.
-/
import EffectiveObserver
import ExtensionalRepairSyntax

namespace P01AC.ExtensionalRepair.GenericIdentityCarrierProbe
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness

def i : Poly := .atom .i
def R : Ty := .identity .raw i i
def probeBody : Poly := .app (.app (.var 0) i) i
def F : Poly := abstract probeBody
def G : Poly := abstract i
def C : Ty := arr N .raw

theorem ctxN : Ctx [N] := .ext .nil (N_form .nil)
theorem raw_form : Form [N] .raw := .raw ctxN
theorem i_raw : Has [N] i .raw := .rawAtom raw_form
theorem R_form : Form [N] R := .identity raw_form i_raw i_raw
theorem i_R : Has [N] i R := .identityIntro R_form i_raw i_raw (.refl i)
theorem n_has : Has [N] (.var 0) N := .var (N_form ctxN) .zero

theorem iteration_at_identity : Has [N] probeBody R := by
  have hRR := form_arr R_form R_form
  have hI : Has [N] i (arr R R) := .i R_form hRR
  have hN : Has [N] (.var 0) (arr (arr R R) (arr R R)) :=
    .allElim (N_form ctxN) R_form (form_arr hRR hRR) n_has
  exact app_has hRR R_form (app_has (form_arr hRR hRR) hRR hN hI) i_R

theorem probe_raw : Has [N] probeBody .raw :=
  .proofErase raw_form R_form iteration_at_identity
theorem target_form : Form [N] (.identity .raw probeBody i) :=
  .identity raw_form probe_raw i_raw

/-- The original J telescope: proof coordinate 0, varying endpoint coordinate 1. -/
def Θ : Tel := theta [N] .raw i
def M : Ty := .identity .raw (.var 0) i

theorem theta_ctx : Ctx Θ := ctx_theta ctxN raw_form i_raw
theorem theta_proof_form : Form Θ (.identity .raw i (.var 1)) :=
  .identity (.raw theta_ctx) (.rawAtom (.raw theta_ctx))
    (.var (.raw theta_ctx) (.succ .zero))
theorem theta_proof_has : Has Θ (.var 0) (.identity .raw i (.var 1)) :=
  .var theta_proof_form .zero
theorem theta_proof_raw : Has Θ (.var 0) .raw :=
  .proofErase (.raw theta_ctx) theta_proof_form theta_proof_has
theorem motive_form : Form Θ M :=
  .identity (.raw theta_ctx) theta_proof_raw (.rawAtom (.raw theta_ctx))

theorem motive_base_exact : motiveAt M i i = R := rfl
theorem motive_target_exact : motiveAt M i probeBody = .identity .raw probeBody i := rfl

theorem literal_probe_j :
    Has [N] (jPoly i i probeBody) (.identity .raw probeBody i) :=
  .j raw_form motive_form R_form R_form target_form
    i_raw i_raw iteration_at_identity i_R

theorem j_proof_conversion (d y e : Poly) : P01DF.PolyConv (jPoly d y e) d :=
  (P01DF.PolyConv.app (.k (.app (.atom .k) d) y) (.refl e)).trans (.k d e)

/-- Current Has proves the exact open Raw identity for a generic Church input. -/
theorem raw_unit_probe : Has [N] i (.identity .raw probeBody i) :=
  .conv target_form literal_probe_j (j_proof_conversion i i probeBody) trivial

theorem F_literal : F =
    .app (.app (.atom .s) (.app (.app (.atom .s) i) (.app (.atom .k) i)))
      (.app (.atom .k) i) := by
  simp [F, probeBody, i, abstract, freeZero, drop, pren, psub]
theorem G_literal : G = .app (.atom .k) i := by
  simp [G, i, abstract, freeZero, drop, pren, psub]

theorem F_beta (v : Poly) :
    P01DF.PolyConv (.app F v) (.app (.app v i) i) := by
  rw [F_literal]
  exact (P01DF.PolyConv.s (.app (.app (.atom .s) i) (.app (.atom .k) i))
      (.app (.atom .k) i) v).trans
    ((P01DF.PolyConv.app (.s i (.app (.atom .k) i) v) (.k i v)).trans
      (.app (.app (.i v) (.k i v)) (.refl i)))

theorem G_beta (v : Poly) : P01DF.PolyConv (.app G v) i := by
  rw [G_literal]
  exact .k i v

theorem C_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ C :=
  form_arr (N_form hΓ) (.raw hΓ)
theorem F_has : Has [] F C :=
  .piIntro (C_form .nil) probe_raw (scoped_abstract (has_scoped probe_raw))
theorem G_has : Has [] G C :=
  .piIntro (C_form .nil) i_raw (scoped_abstract (has_scoped i_raw))
theorem F_scoped : Scoped 0 F := has_scoped F_has
theorem G_scoped : Scoped 0 G := has_scoped G_has

def leftPoint : Poly := .app (pren Nat.succ F) (.var 0)
def rightPoint : Poly := .app (pren Nat.succ G) (.var 0)
def pointType : Ty := .identity .raw leftPoint rightPoint
def pointMotive : Ty := .identity .raw (.var 0) (.app G (.var 2))

theorem left_point_exact : leftPoint = .app F (.var 0) := by
  simp [leftPoint, F_literal, i, pren, psub]
theorem right_point_exact : rightPoint = .app G (.var 0) := by
  simp [rightPoint, G_literal, i, pren, psub]

theorem left_point_R : Has [N] leftPoint R := by
  rw [left_point_exact]
  exact .conv R_form iteration_at_identity (F_beta (.var 0)).symm
    ⟨scoped_mono F_scoped (by decide), Nat.zero_lt_succ 0⟩
theorem left_point_raw : Has [N] leftPoint .raw :=
  .proofErase raw_form R_form left_point_R
theorem right_point_raw : Has [N] rightPoint .raw := by
  rw [right_point_exact]
  exact .conv raw_form i_raw (G_beta (.var 0)).symm
    ⟨scoped_mono G_scoped (by decide), Nat.zero_lt_succ 0⟩
theorem point_form : Form [N] pointType :=
  .identity raw_form left_point_raw right_point_raw

theorem point_motive_form : Form Θ pointMotive := by
  have hG : Has Θ (.app G (.var 2)) .raw :=
    .conv (.raw theta_ctx) (.rawAtom (.raw theta_ctx)) (G_beta (.var 2)).symm
      ⟨scoped_mono G_scoped (by decide), Nat.lt_succ_self 2⟩
  exact .identity (.raw theta_ctx) theta_proof_raw hG

theorem point_motive_base_exact :
    motiveAt pointMotive i i = .identity .raw i rightPoint := by
  simp [motiveAt, pointMotive, subst, psub, rightPoint, G_literal, i, pren, P01F.cons]
theorem point_motive_target_exact :
    motiveAt pointMotive i leftPoint = pointType := by
  simp [motiveAt, pointMotive, pointType, subst, psub, rightPoint, G_literal, i, pren, P01F.cons]

theorem point_base_form : Form [N] (motiveAt pointMotive i i) := by
  rw [point_motive_base_exact]
  exact .identity raw_form i_raw right_point_raw
theorem point_base_has : Has [N] i (motiveAt pointMotive i i) := by
  rw [point_motive_base_exact]
  apply Has.identityIntro (.identity raw_form i_raw right_point_raw) i_raw right_point_raw
  rw [right_point_exact]
  exact (G_beta (.var 0)).symm

/-- Exact pointwise premise of the unchanged piExt rule, obtained with current J. -/
theorem point_identity : Has [N] i pointType := by
  have hj : Has [N] (jPoly i i leftPoint) (motiveAt pointMotive i leftPoint) :=
    .j raw_form point_motive_form R_form point_base_form
      (by rw [point_motive_target_exact]; exact point_form)
      i_raw i_raw left_point_R point_base_has
  rw [point_motive_target_exact] at hj
  exact .conv point_form hj (j_proof_conversion i i leftPoint) trivial

theorem point_family_form : Form [] (.pi N pointType) :=
  .pi (N_form .nil) point_form
theorem point_evidence : Has [] G (.pi N pointType) :=
  .piIntro point_family_form point_identity (scoped_abstract trivial)
theorem closed_identity_form : Form [] (.identity C F G) :=
  .identity (C_form .nil) F_has G_has

/-- The promised closed HasE equality at the inhabited N-to-Raw carrier. -/
theorem closed_probe_identity : HasE [] i (.identity C F G) :=
  .piExt
    (form_inclusion (N_form .nil))
    (form_inclusion raw_form)
    (form_inclusion (C_form .nil))
    (has_inclusion F_has)
    (has_inclusion G_has)
    (form_inclusion point_form)
    (form_inclusion point_family_form)
    (has_inclusion point_evidence)
    (form_inclusion closed_identity_form)
    F_scoped G_scoped G_scoped
    (form_scoped (N_form .nil)) trivial

theorem domain_inhabited : Has [] (inputNumeral 0) N := inputNumeral_has 0
theorem carrier_inhabited : Has [] G C := G_has

#print axioms raw_unit_probe
#print axioms point_identity
#print axioms F_has
#print axioms G_has
#print axioms closed_probe_identity

end P01AC.ExtensionalRepair.GenericIdentityCarrierProbe
