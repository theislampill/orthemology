/- Exact, conditional scalar-fusion reduction. The literal endpoint remains open. -/
import EffectiveObserver
import ExtensionalRepairSyntax

namespace P01AC.ExtensionalRepair.ExactScalarFusion
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

def i : Poly := .atom .i
def T : Ty := arr N N
def A : Ty := .param 0
def End : Ty := arr A A
def scalarL : Poly := .app (.app (.var 2) (.var 1)) (.var 0)
def scalarR (k : Poly) : Poly := .app (.app (.app k (.var 2)) (.var 1)) (.var 0)
def Leaf (k : Poly) : Ty := .identity A scalarL (scalarR k)
def W (k : Poly) : Ty := .pi N (.all (.pi End (.pi A (Leaf k))))
def c3 : Poly := abstract (abstract (abstract i))

theorem psub_closed {k : Poly} (hk : Scoped 0 k) (σ : Nat → Poly) : psub σ k = k := by
  induction k with
  | var n => exact False.elim (Nat.not_lt_zero n hk)
  | atom t => rfl
  | app f a ihf iha => exact congrArg₂ Poly.app (ihf hk.1) (iha hk.2)

theorem pren_closed {k : Poly} (hk : Scoped 0 k) (r : Nat → Nat) : pren r k = k :=
  psub_closed hk _

theorem closed_has_T {k : Poly} (hk : Has [] k T) {Γ : Tel} (hΓ : Ctx Γ) : Has Γ k T := by
  have hr : Renaming [] Γ id := ⟨by simp, by intro n A h; cases h⟩
  simpa only [psub_closed (has_scoped hk), T, N, NBody, arr, wk, subst] using has_rename hk hΓ hr

theorem T_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ T := form_arr (N_form hΓ) (N_form hΓ)
theorem A_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ A := .param hΓ
theorem End_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ End := form_arr (A_form hΓ) (A_form hΓ)
theorem i_T {Γ : Tel} (hΓ : Ctx Γ) : Has Γ i T := .i (N_form hΓ) (T_form hΓ)

theorem W_subst {k : Poly} (hk : Scoped 0 k) (σ : Nat → Poly) : subst σ (W k) = W k := by
  simp [W, Leaf, A, End, scalarL, scalarR, N, NBody, arr, wk, subst, psub,
    pup, P01F.cons, pren, psub_closed hk]

theorem W_twk (k : Poly) : twk (W k) = W k := rfl

theorem inst_NBody_A : tinst NBody A = arr End End := rfl

theorem scalar_n_has {Γ : Tel} (hΓ : Ctx Γ) {n : Poly} (hn : Has Γ n N)
    {f a : Poly} (hf : Has Γ f End) (ha : Has Γ a A) :
    Has Γ (.app (.app n f) a) A := by
  have he := End_form hΓ
  have hn' : Has Γ n (arr End End) := .allElim (N_form hΓ) (A_form hΓ)
    (form_arr he he) hn
  exact app_has he (A_form hΓ) (app_has (form_arr he he) he hn' hf) ha

/-- The only variable context shape needed to form the scalar family. -/
theorem scalar_context {Γ : Tel} (hΓ : Ctx Γ) : Ctx (A :: End :: N :: twkTel Γ) := by
  have h0 := ctx_twk hΓ
  have h1 := Ctx.ext h0 (N_form h0)
  exact .ext (.ext h1 (End_form h1)) (A_form (.ext h1 (End_form h1)))

theorem scalar_leaf_form {Γ : Tel} (hΓ : Ctx Γ) {k : Poly}
    (hk : Has (A :: End :: N :: twkTel Γ) k T) :
    Form (A :: End :: N :: twkTel Γ) (Leaf k) := by
  let Δ := A :: End :: N :: twkTel Γ
  have hc : Ctx Δ := scalar_context hΓ
  have hn : Has Δ (.var 2) N := .var (N_form hc) (.succ (.succ .zero))
  have hf : Has Δ (.var 1) End := .var (End_form hc) (.succ .zero)
  have ha : Has Δ (.var 0) A := .var (A_form hc) .zero
  have hkn := app_has (T_form hc) (N_form hc) hk hn
  exact .identity (A_form hc) (scalar_n_has hc hn hf ha) (scalar_n_has hc hkn hf ha)

theorem W_form {k : Poly} (hk : Has [] k T) {Γ : Tel} (hΓ : Ctx Γ) : Form Γ (W k) := by
  apply Form.pi (N_form hΓ)
  apply Form.all (.ext hΓ (N_form hΓ))
  change Form (N :: twkTel Γ) (.pi End (.pi A (Leaf k)))
  have hn := Ctx.ext (ctx_twk hΓ) (N_form (ctx_twk hΓ))
  exact .pi (End_form hn) (.pi (A_form (.ext hn (End_form hn)))
    (scalar_leaf_form hΓ (closed_has_T hk (scalar_context hΓ))))

theorem c3_scoped (n : Nat) : Scoped n c3 := by
  exact scoped_abstract (scoped_abstract (scoped_abstract trivial))

theorem W_base : Has [] c3 (W i) := by
  have hw := W_form (i_T Ctx.nil) Ctx.nil
  have h0 : Ctx [N] := .ext .nil (N_form .nil)
  have h1 : Ctx [End, N] := .ext h0 (End_form h0)
  have hc : Ctx [A, End, N] := .ext h1 (A_form h1)
  have hn : Has [A, End, N] (.var 2) N := .var (N_form hc) (.succ (.succ .zero))
  have hf : Has [A, End, N] (.var 1) End := .var (End_form hc) (.succ .zero)
  have ha : Has [A, End, N] (.var 0) A := .var (A_form hc) .zero
  have hl := scalar_n_has hc hn hf ha
  have hr := scalar_n_has hc (app_has (T_form hc) (N_form hc) (i_T hc) hn) hf ha
  have leaf : Has [A, End, N] i (Leaf i) :=
    .identityIntro (.identity (A_form hc) hl hr) hl hr
      (P01DF.PolyConv.app (.app (.i (.var 2)) (.refl (.var 1))) (.refl (.var 0))).symm
  have hleaf := has_form leaf
  have hfam := Form.pi (A_form h1) hleaf
  have hffam := Form.pi (End_form h0) hfam
  exact .piIntro hw (.allIntro (.all h0 hffam)
    (.piIntro hffam (.piIntro hfam leaf (scoped_abstract trivial))
      (scoped_abstract (scoped_abstract trivial)))) (c3_scoped 0)

theorem j_conversion (d y e : Poly) : PolyConvPlus (jPoly d y e) d :=
  (PolyConvPlus.app (.k (.app (.atom .k) d) y) (.refl e)).trans (.k d e)

/-- The endpoint coordinate is 1 before the three term binders, hence 4 here. -/
def M : Ty := W (.var 4)

theorem M_form : Form (theta [] T i) M := by
  let Γ := theta [] T i
  have hc : Ctx Γ := ctx_theta .nil (T_form .nil) (i_T .nil)
  apply Form.pi (N_form hc)
  apply Form.all (.ext hc (N_form hc))
  change Form (N :: twkTel Γ) (.pi End (.pi A (Leaf (.var 4))))
  have hn := Ctx.ext (ctx_twk hc) (N_form (ctx_twk hc))
  apply Form.pi (End_form hn)
  apply Form.pi (A_form (.ext hn (End_form hn)))
  apply scalar_leaf_form hc
  exact .var (T_form (scalar_context hc)) (.succ (.succ (.succ (.succ .zero))))

theorem M_at {k : Poly} (hk : Scoped 0 k) (e : Poly) : motiveAt M k e = W k := by
  simp [motiveAt, M, W, Leaf, A, End, scalarL, scalarR, N, NBody, arr, wk,
    subst, psub, pup, P01F.cons, pren, psub_closed hk]

theorem forward_fixed {k e : Poly} (hk : Has [] k T)
    (he : HasE [] e (.identity T i k)) : HasE [] c3 (W k) := by
  have hbase : Form [] (motiveAt M i i) := by
    rw [M_at (show Scoped 0 i from trivial)]
    exact W_form (i_T .nil) .nil
  have htarget : Form [] (motiveAt M k e) := by
    rw [M_at (has_scoped hk)]
    exact W_form hk .nil
  have hd : Has [] c3 (motiveAt M i i) := by
    rw [M_at (show Scoped 0 i from trivial)]
    exact W_base
  have hj := HasE.j (form_inclusion (T_form .nil)) (form_inclusion M_form)
    (form_inclusion (.identity (T_form .nil) (i_T .nil) hk))
    (form_inclusion hbase) (form_inclusion htarget)
    (has_inclusion (i_T .nil)) (has_inclusion hk) he (has_inclusion hd)
  rw [M_at (has_scoped hk)] at hj
  exact .conv (form_inclusion (W_form hk .nil)) hj (j_conversion c3 k e) (c3_scoped 0)

end P01AC.ExtensionalRepair.ExactScalarFusion
