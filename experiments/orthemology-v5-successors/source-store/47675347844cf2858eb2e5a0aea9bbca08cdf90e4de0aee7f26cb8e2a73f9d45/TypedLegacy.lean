/- Restricted, literal-code legacy embedding into finite typed contexts. -/
import TypedStructural
import TypedSoundness
import P01DependentControls

namespace P01TC.Legacy
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Exactly the available raw-variable capability; every component is a derivation. -/
structure RawContext (Γ : Tel) : Prop where
  ctx : Ctx Γ
  vars : ∀ n, n < Γ.length → Has Γ (.var n) .raw

def rawTel : Nat → Tel
  | 0 => []
  | n+1 => .raw :: rawTel n

@[simp] theorem rawTel_length (n : Nat) : (rawTel n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => exact congrArg Nat.succ ih

theorem RawContext.ext {Γ : Tel} (h : RawContext Γ) : RawContext (.raw :: Γ) := by
  have hc : Ctx (.raw :: Γ) := .ext h.ctx (.raw h.ctx)
  refine ⟨hc, ?_⟩
  intro n hn
  cases n with
  | zero => exact .var (.raw hc) .zero
  | succ n => exact has_wk (h.vars n (Nat.lt_of_succ_lt_succ hn)) h.ctx (.raw h.ctx)

theorem rawTel_context (n : Nat) : RawContext (rawTel n) := by
  induction n with
  | zero => exact ⟨.nil, fun n hn => False.elim (Nat.not_lt_zero n hn)⟩
  | succ n ih => exact ih.ext

/-- Raw polynomials are derived from their finitely scoped variable occurrences. -/
theorem raw_term {Γ : Tel} {p : Poly} (hΓ : RawContext Γ) (hp : Scoped Γ.length p) :
    Has Γ p .raw := by
  induction p with
  | var n => exact hΓ.vars n hp
  | atom t => exact .rawAtom (.raw hΓ.ctx)
  | app f a hf ha => exact .rawApp (.raw hΓ.ctx) (hf hp.1) (ha hp.2)

/-- The newest J coordinate is made Raw by the explicit identity-proof erasure rule. -/
theorem RawContext.theta {Γ : Tel} {x : Poly} (h : RawContext Γ) (hx : Scoped Γ.length x) :
    RawContext (theta Γ .raw x) := by
  have hx' := raw_term h hx
  have hA : Form Γ .raw := .raw h.ctx
  have hhead := form_theta_head h.ctx hA hx'
  have hbase : Ctx (.raw :: Γ) := .ext h.ctx hA
  have hctx := ctx_theta h.ctx hA hx'
  refine ⟨hctx, ?_⟩
  intro n hn
  cases n with
  | zero =>
      exact .proofErase (.raw hctx) (form_wk hhead hbase hhead)
        (.var (form_wk hhead hbase hhead) .zero)
  | succ n =>
      exact has_wk (h.ext.vars n (Nat.lt_of_succ_lt_succ hn)) hbase hhead

theorem form_arr {Γ : Tel} {A B : Ty} (hΓ : Ctx Γ) (hA : Form Γ A) (hB : Form Γ B) :
    Form Γ (arr A B) := .pi hA (form_wk hB hΓ hA)

theorem form_fin (C : TypeCode) {Γ : Tel} (hΓ : Ctx Γ) : Form Γ (fin C) := by
  induction C with
  | var n => exact .param hΓ
  | bottom => exact .bottom hΓ
  | arrow A B ha hb => exact form_arr hΓ ha hb
  | all B ih => exact .allFinite hΓ

/-- A type translation also records finite support at its exact binder depth.
Old All occurs only inside an entire accepted embedFinite subtree. -/
inductive Translation : Nat → P01DF.Ty → Ty → Prop
  | finite (n : Nat) (C : TypeCode) : Translation n (P01DF.embedFinite C) (fin C)
  | raw (n : Nat) : Translation n .raw .raw
  | identity {n p q} : Scoped n p → Scoped n q → Translation n (.identity p q) (.identity .raw p q)
  | arrow {n A B A' B'} : Translation n A A' → Translation n B B' → Translation n (.arrow A B) (arr A' B')
  | pi {n B B'} : Translation (n+1) B B' → Translation n (.pi B) (.pi .raw B')
  | sigma {n B B'} : Translation (n+1) B B' → Translation n (.sigma B) (.sigma .raw B')

theorem Translation.form {n : Nat} {A : P01DF.Ty} {A' : Ty} (h : Translation n A A')
    {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n) : Form Γ A' := by
  induction h generalizing Γ with
  | finite n C => exact form_fin C hΓ.ctx
  | raw n => exact .raw hΓ.ctx
  | identity hp hq =>
      exact .identity (.raw hΓ.ctx)
        (raw_term hΓ (by simpa only [hlen] using hp))
        (raw_term hΓ (by simpa only [hlen] using hq))
  | arrow hA hB iA iB => exact form_arr hΓ.ctx (iA hΓ hlen) (iB hΓ hlen)
  | pi hB iB => exact .pi (.raw hΓ.ctx) (iB hΓ.ext (congrArg Nat.succ hlen))
  | sigma hB iB => exact .sigma (.raw hΓ.ctx) (iB hΓ.ext (congrArg Nat.succ hlen))

theorem Translation.subst {n : Nat} {A : P01DF.Ty} {A' : Ty} (h : Translation n A A')
    {m : Nat} (σ : Nat → Poly) (hs : ScopedSub n m σ) :
    Translation m (P01DF.substIndex σ A) (P01TC.subst σ A') := by
  induction h generalizing m σ with
  | finite n C =>
      simpa only [P01DF.Syntactic.index_embedFinite, subst_fin] using Translation.finite m C
  | raw n => exact .raw m
  | identity hp hq => exact .identity (scoped_subst hp hs) (scoped_subst hq hs)
  | arrow hA hB iA iB =>
      simpa only [P01DF.substIndex, subst_arr] using Translation.arrow (iA σ hs) (iB σ hs)
  | pi hB iB => exact .pi (iB (pup σ) (scopedSub_lift hs))
  | sigma hB iB => exact .sigma (iB (pup σ) (scopedSub_lift hs))

theorem Translation.inst {n : Nat} {B : P01DF.Ty} {B' : Ty} (h : Translation (n+1) B B')
    {a : Poly} (ha : Scoped n a) : Translation n (P01DF.instantiate B a) (inst B' a) :=
  h.subst (cons a Poly.var) (scopedSub_cons ha (scopedSub_id n))

theorem Translation.motiveAt {n : Nat} {B : P01DF.Ty} {B' : Ty} (h : Translation (n+2) B B')
    {y e : Poly} (hy : Scoped n y) (he : Scoped n e) :
    Translation n (P01DF.motiveAt B y e) (P01TC.motiveAt B' y e) :=
  h.subst (cons e (cons y Poly.var)) (scopedSub_cons he (scopedSub_cons hy (scopedSub_id n)))

/-- A constructor-faithful tree for the old Prop-valued judgment.
Keeping the tree in Type preserves derivation history before proof erasure. -/
inductive Derivation : Poly → P01DF.Ty → Type
  | raw (p : Poly) : Derivation p .raw
  | finite {t C} : FiniteDerives t C → Derivation (.atom t) (P01DF.embedFinite C)
  | i (A) : Derivation (.atom .i) (.arrow A A)
  | k (A B) : Derivation (.atom .k) (.arrow A (.arrow B A))
  | s (A B C) : Derivation (.atom .s) (.arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C)))
  | allIntro {p B} : Derivation p B → Derivation p (.all B)
  | allElim {p B A} : Derivation p (.all B) → Derivation p (P01DF.instantiateType B A)
  | app {f a A B} : Derivation f (.arrow A B) → Derivation a A → Derivation (.app f a) B
  | piIntro {b B} : Derivation b B → Derivation (abstract b) (.pi B)
  | piElim {f a B} : Derivation f (.pi B) → Derivation (.app f a) (P01DF.instantiate B a)
  | sigmaIntro {a b B} : Derivation b (P01DF.instantiate B a) → Derivation (pairPoly a b) (.sigma B)
  | sigmaSnd {z B} : Derivation z (.sigma B) → Derivation (sndPoly z) (P01DF.instantiate B (fstPoly z))
  | identityIntro {p q} : P01DF.PolyConv p q → Derivation (.atom .i) (.identity p q)
  | j {x y e d B} : Derivation e (.identity x y) →
      Derivation d (P01DF.motiveAt B x (.atom .i)) → Derivation (jPoly d y e) (P01DF.motiveAt B y e)
  | conv {p q A} : Derivation p A → P01DF.PolyConv p q → Derivation q A

/-- Every tree erases to exactly the corresponding accepted old judgment. -/
def Derivation.erase {p A} (h : Derivation p A) : P01DF.Has p A := by
  induction h with
  | raw p => exact .raw p
  | finite ht => exact .finite ht
  | i A => exact .i A
  | k A B => exact .k A B
  | s A B C => exact .s A B C
  | allIntro h ih => exact .allIntro ih
  | allElim h ih => exact .allElim ih
  | app hf ha ihf iha => exact .app ihf iha
  | piIntro hb ih => exact .piIntro ih
  | piElim hf ih => exact .piElim ih
  | sigmaIntro hb ih => exact .sigmaIntro ih
  | sigmaSnd hz ih => exact .sigmaSnd ih
  | identityIntro hc => exact .identityIntro hc
  | j he hd ihe ihd => exact .j ihe ihd
  | conv hp hc ih => exact .conv ih hc

/-- A restriction on the actual old derivation, rather than only its conclusion.
Each motive and implicit polynomial receives its own finite scope check. -/
inductive Restricted : (n : Nat) → {p : Poly} → {A : P01DF.Ty} → Derivation p A → Ty → Prop
  | raw {n p} : Scoped n p → Restricted n (.raw p) .raw
  | finite {n t C} (h : FiniteDerives t C) : Restricted n (.finite h) (fin C)
  | i {n A A'} : Translation n A A' → Restricted n (.i A) (arr A' A')
  | k {n A B A' B'} : Translation n A A' → Translation n B B' →
      Restricted n (.k A B) (arr A' (arr B' A'))
  | s {n A B C A' B' C'} : Translation n A A' → Translation n B B' → Translation n C C' →
      Restricted n (.s A B C) (arr (arr A' (arr B' C')) (arr (arr A' B') (arr A' C')))
  | app {n A B A' B' f a} {hf : Derivation f (.arrow A B)} {ha : Derivation a A} :
      Translation n A A' → Translation n B B' → Restricted n hf (arr A' B') → Restricted n ha A' →
      Restricted n (.app hf ha) B'
  | piIntro {n B B' b} {hb : Derivation b B} : Translation (n+1) B B' →
      Restricted (n+1) hb B' → Restricted n (.piIntro hb) (.pi .raw B')
  | piElim {n B B' f a} {hf : Derivation f (.pi B)} : Translation (n+1) B B' →
      Scoped n a → Restricted n hf (.pi .raw B') → Restricted n (.piElim (a := a) hf) (inst B' a)
  | sigmaIntro {n B B' a b} {hb : Derivation b (P01DF.instantiate B a)} :
      Translation (n+1) B B' → Scoped n a → Restricted n hb (inst B' a) →
      Restricted n (.sigmaIntro hb) (.sigma .raw B')
  | sigmaSnd {n B B' z} {hz : Derivation z (.sigma B)} : Translation (n+1) B B' →
      Restricted n hz (.sigma .raw B') → Restricted n (.sigmaSnd hz) (inst B' (fstPoly z))
  | identityIntro {n p q} (h : P01DF.PolyConv p q) : Scoped n p → Scoped n q →
      Restricted n (.identityIntro h) (.identity .raw p q)
  | j {n B B' x y e d} {he : Derivation e (.identity x y)}
      {hd : Derivation d (P01DF.motiveAt B x (.atom .i))} :
      Translation (n+2) B B' → Scoped n x → Scoped n y →
      Restricted n he (.identity .raw x y) → Restricted n hd (P01TC.motiveAt B' x (.atom .i)) →
      Restricted n (.j he hd) (P01TC.motiveAt B' y e)
  | conv {n A A' p q} {hp : Derivation p A} (h : P01DF.PolyConv p q) :
      Scoped n q → Restricted n hp A' → Restricted n (.conv hp h) A'

/-- The translated derivation has exactly the same source polynomial. -/
theorem Restricted.embed {n : Nat} {p : Poly} {A : P01DF.Ty} {h : Derivation p A} {A' : Ty}
    (hr : Restricted n h A') {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n) :
    Has Γ p A' := by
  induction hr generalizing Γ with
  | raw hp => exact raw_term hΓ (by simpa only [hlen] using hp)
  | finite ht => exact .finite (form_fin _ hΓ.ctx) ht
  | i hA =>
      have hA' := hA.form hΓ hlen
      exact .i hA' (form_arr hΓ.ctx hA' hA')
  | k hA hB =>
      have hA' := hA.form hΓ hlen
      have hB' := hB.form hΓ hlen
      exact .k hA' hB' (form_arr hΓ.ctx hA' (form_arr hΓ.ctx hB' hA'))
  | s hA hB hC =>
      have hA' := hA.form hΓ hlen
      have hB' := hB.form hΓ hlen
      have hC' := hC.form hΓ hlen
      exact .s hA' hB' hC'
        (form_arr hΓ.ctx (form_arr hΓ.ctx hA' (form_arr hΓ.ctx hB' hC'))
          (form_arr hΓ.ctx (form_arr hΓ.ctx hA' hB') (form_arr hΓ.ctx hA' hC')))
  | app hA hB hf ha iF iA =>
      have hA' := hA.form hΓ hlen
      have hB' := hB.form hΓ hlen
      simpa only [inst_wk] using
        Has.piElim (form_arr hΓ.ctx hA' hB')
          (by simpa only [inst_wk] using hB') (iF hΓ hlen) (iA hΓ hlen)
  | piIntro hB hb ib =>
      have hb' := ib hΓ.ext (congrArg Nat.succ hlen)
      exact .piIntro (.pi (.raw hΓ.ctx) (hB.form hΓ.ext (congrArg Nat.succ hlen)))
        hb' (scoped_abstract (has_scoped hb'))
  | piElim hB ha hf iF =>
      exact .piElim (.pi (.raw hΓ.ctx) (hB.form hΓ.ext (congrArg Nat.succ hlen)))
        ((hB.inst ha).form hΓ hlen) (iF hΓ hlen)
        (raw_term hΓ (by simpa only [hlen] using ha))
  | sigmaIntro hB ha hb ib =>
      exact .sigmaIntro (.sigma (.raw hΓ.ctx) (hB.form hΓ.ext (congrArg Nat.succ hlen)))
        ((hB.inst ha).form hΓ hlen)
        (raw_term hΓ (by simpa only [hlen] using ha)) (ib hΓ hlen)
  | sigmaSnd hB hz iz =>
      have hz' := iz hΓ hlen
      have hs := scoped_fst (has_scoped hz')
      exact .sigmaSnd (has_form hz')
        ((hB.inst (by simpa only [hlen] using hs)).form hΓ hlen) hz'
  | identityIntro hc hp hq =>
      have hp' := raw_term hΓ (by simpa only [hlen] using hp)
      have hq' := raw_term hΓ (by simpa only [hlen] using hq)
      exact .identityIntro (.identity (.raw hΓ.ctx) hp' hq') hp' hq' hc
  | @j n B B' x y e d he0 hd0 hB hx hy he hd ie id =>
      have hxscope : Scoped Γ.length x := by simpa only [hlen] using hx
      have hyscope : Scoped Γ.length y := by simpa only [hlen] using hy
      have hx' := raw_term hΓ hxscope
      have hy' := raw_term hΓ hyscope
      have he' := ie hΓ hlen
      have hd' := id hΓ hlen
      have hescope := has_scoped he'
      exact .j (.raw hΓ.ctx)
        (hB.form (hΓ.theta hxscope) (by simp only [theta, List.length_cons, hlen]))
        (.identity (.raw hΓ.ctx) hx' hy')
        ((hB.motiveAt hx (by trivial)).form hΓ hlen)
        ((hB.motiveAt hy (by simpa only [hlen] using hescope)).form hΓ hlen)
        hx' hy' he' hd'
  | conv hc hq hp ip =>
      have hp' := ip hΓ hlen
      exact .conv (has_form hp') hp' hc (by simpa only [hlen] using hq)

theorem Restricted.raw_embed {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A') :
    Has (rawTel n) p A' := hr.embed (rawTel_context n) (rawTel_length n)

theorem Restricted.scoped {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A') : Scoped n p := by
  simpa only [rawTel_length] using has_scoped hr.raw_embed

theorem Restricted.translation {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A') : Translation n A A' := by
  induction hr with
  | raw hp => exact .raw _
  | finite ht => exact .finite _ _
  | i hA => exact .arrow hA hA
  | k hA hB => exact .arrow hA (.arrow hB hA)
  | s hA hB hC => exact .arrow (.arrow hA (.arrow hB hC)) (.arrow (.arrow hA hB) (.arrow hA hC))
  | app hA hB hf ha iF iA => exact hB
  | piIntro hB hb ib => exact .pi hB
  | piElim hB ha hf iF => exact hB.inst ha
  | sigmaIntro hB ha hb ib => exact .sigma hB
  | sigmaSnd hB hz iz => exact hB.inst (scoped_fst hz.scoped)
  | identityIntro hc hp hq => exact .identity hp hq
  | j hB hx hy he hd ie id => exact hB.motiveAt hy he.scoped
  | conv hc hq hp ip => exact ip

theorem Restricted.formed {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A') : Form (rawTel n) A' :=
  has_form hr.raw_embed

/-- This test observes constructor history before erasure into the old proposition. -/
def Derivation.allFree {p A} : Derivation p A → Prop
  | .raw _ | .finite _ | .i _ | .k _ _ | .s _ _ _ | .identityIntro _ => True
  | .allIntro _ | .allElim _ => False
  | .app hf ha => hf.allFree ∧ ha.allFree
  | .piIntro hb | .piElim hb | .sigmaIntro hb | .sigmaSnd hb => hb.allFree
  | .j he hd => he.allFree ∧ hd.allFree
  | .conv hp _ => hp.allFree

theorem Restricted.allFree {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A') : h.allFree := by
  induction hr <;> simp_all only [Derivation.allFree, and_self]

theorem no_allIntro {n : Nat} {p : Poly} {B : P01DF.Ty} {h : Derivation p B} {A' : Ty} :
    ¬ Restricted n (.allIntro h) A' := by intro hr; exact hr.allFree

theorem no_allElim {n : Nat} {p : Poly} {B A : P01DF.Ty}
    {h : Derivation p (.all B)} {A' : Ty} :
    ¬ Restricted n (.allElim (A := A) h) A' := by intro hr; exact hr.allFree

/-- Unary interpretations agree at every valuation, before any context validity premise. -/
theorem Translation.F_agrees {n : Nat} {A : P01DF.Ty} {A' : Ty} (h : Translation n A A')
    (ρ : OEnv) (η : Env) (t u : Term) :
    F A' ρ η t u = (((P01DF.interpret A).run η).obj ρ).rel t u := by
  induction h generalizing ρ η t u with
  | finite n C => rw [F_fin, P01DF.interpret_embedFinite]
  | raw n => rfl
  | identity hp hq => rfl
  | arrow hA hB iA iB =>
      simp only [F_arr, P01DF.interpret, arrowModel, ArrPER, PiPER, iA, iB]
  | pi hB iB =>
      simp only [F, P01DF.interpret, P01DF.rawModel, P01DF.piModel, PiPER, rawPER, iB]
  | sigma hB iB =>
      simp only [F, P01DF.interpret, P01DF.rawModel, P01DF.sigmaModel, SigmaPER, rawPER, iB]

/-- Heterogeneous agreement uses the actual two pointwise-convertible valuations. -/
theorem Translation.G_agrees {n : Nat} {A : P01DF.Ty} {A' : Ty} (h : Translation n A A')
    (r : REnv) (η ξ : Env) (hc : P01DF.IndexRelated η ξ) (t u : Term) :
    G A' r η ξ t u = ((P01DF.interpret A).run η).rel r t u := by
  induction h generalizing r η ξ t u with
  | finite n C => rw [G_fin, P01DF.interpret_embedFinite]
  | raw n => rfl
  | @identity n p q hp hq =>
      apply propext
      change (Conv (eval p η) (eval q η) ∧ Conv (eval p ξ) (eval q ξ) ∧
        Conv t .i ∧ Conv u .i) ↔ (Conv (eval p η) (eval q η) ∧ Conv t .i ∧ Conv u .i)
      constructor
      · intro h; exact ⟨h.1, h.2.2⟩
      · intro h
        exact ⟨h.1, (P01DF.eval_index_related p hc).symm.trans
          (h.1.trans (P01DF.eval_index_related q hc)), h.2⟩
  | @arrow n A B A' B' hA hB iA iB =>
      simp only [G_arr, hA.F_agrees, hB.F_agrees, iA r η ξ hc, iB r η ξ hc,
        P01DF.interpret, arrowModel, arrowLink, Model.asLink, PER.dom, ArrPER, PiPER]
      rw [← P01DF.interpret_index_transport A hc, ← P01DF.interpret_index_transport B hc]
  | @pi n B B' hB iB =>
      simp only [G]
      rw [(Translation.pi hB).F_agrees, (Translation.pi hB).F_agrees]
      rw [← P01DF.interpret_index_transport (.pi B) hc]
      apply propext
      constructor
      · intro h
        refine ⟨h.1, h.2.1, ?_⟩
        intro a b hab
        exact (iB r (cons a η) (cons b ξ) (P01DF.index_cons hc hab) _ _) ▸ h.2.2 a b hab
      · intro h
        refine ⟨h.1, h.2.1, ?_⟩
        intro a b hab
        exact (iB r (cons a η) (cons b ξ) (P01DF.index_cons hc hab) _ _).symm ▸ h.2.2 a b hab
  | @sigma n B B' hB iB =>
      simp only [G]
      rw [(Translation.sigma hB).F_agrees, (Translation.sigma hB).F_agrees]
      rw [← P01DF.interpret_index_transport (.sigma B) hc]
      apply propext
      constructor
      · intro h
        refine ⟨h.2.2.1, h.2.2.2.1, h.2.2.2.2.1, ?_⟩
        exact (iB r (cons (firstTerm t) η) (cons (firstTerm u) ξ)
          (P01DF.index_cons hc h.2.2.2.2.1) _ _) ▸ h.2.2.2.2.2
      · intro h
        have he := ((P01DF.interpret (.sigma B)).run η).endpoints r h
        refine ⟨he.1, he.2, h.1, h.2.1, h.2.2.1, ?_⟩
        exact (iB r (cons (firstTerm t) η) (cons (firstTerm u) ξ)
          (P01DF.index_cons hc h.2.2.1) _ _).symm ▸ h.2.2.2

/-- Readback of the exact finite subgrammar, without term-indexed constructors. -/
def decodeFinite : P01DF.Ty → Option TypeCode
  | .param n => some (.var n)
  | .bottom => some .bottom
  | .arrow A B => match decodeFinite A, decodeFinite B with
      | some A', some B' => some (.arrow A' B')
      | _, _ => none
  | .all B => (decodeFinite B).map TypeCode.all
  | .raw | .identity _ _ | .pi _ | .sigma _ => none

/-- Deterministic translation; an old All is accepted only through finite readback. -/
def translate : P01DF.Ty → Option Ty
  | .param n => some (.param n)
  | .bottom => some .bottom
  | .raw => some .raw
  | .identity p q => some (.identity .raw p q)
  | .arrow A B => match translate A, translate B with
      | some A', some B' => some (arr A' B')
      | _, _ => none
  | .pi B => (translate B).map (Ty.pi .raw)
  | .sigma B => (translate B).map (Ty.sigma .raw)
  | .all B => (decodeFinite B).map Ty.allFinite

theorem decodeFinite_embed (C : TypeCode) : decodeFinite (P01DF.embedFinite C) = some C := by
  induction C with
  | var n => rfl
  | bottom => rfl
  | arrow A B iA iB => simp only [P01DF.embedFinite, decodeFinite, iA, iB]
  | all B iB => simp only [P01DF.embedFinite, decodeFinite, iB, Option.map]

theorem decodeFinite_sound {A : P01DF.Ty} {C : TypeCode} (h : decodeFinite A = some C) :
    A = P01DF.embedFinite C := by
  induction A generalizing C with
  | param n => cases h; rfl
  | bottom => cases h; rfl
  | raw => cases h
  | identity p q => cases h
  | pi B iB => cases h
  | sigma B iB => cases h
  | arrow A B iA iB =>
      cases hA : decodeFinite A with
      | none => simp only [decodeFinite, hA] at h; cases h
      | some A' =>
          cases hB : decodeFinite B with
          | none => simp only [decodeFinite, hA, hB] at h; cases h
          | some B' =>
              simp only [decodeFinite, hA, hB, Option.some.injEq] at h
              cases h
              exact congrArg₂ P01DF.Ty.arrow (iA hA) (iB hB)
  | all B iB =>
      cases hB : decodeFinite B with
      | none => simp only [decodeFinite, hB, Option.map] at h; cases h
      | some B' =>
          simp only [decodeFinite, hB, Option.map, Option.some.injEq] at h
          cases h
          exact congrArg P01DF.Ty.all (iB hB)

theorem translate_embedFinite (C : TypeCode) : translate (P01DF.embedFinite C) = some (fin C) := by
  induction C with
  | var n => rfl
  | bottom => rfl
  | arrow A B iA iB => simp only [P01DF.embedFinite, translate, iA, iB, fin]
  | all B iB => simp only [P01DF.embedFinite, translate, decodeFinite_embed, Option.map, fin]

theorem Translation.readback {n : Nat} {A : P01DF.Ty} {A' : Ty} (h : Translation n A A') :
    translate A = some A' := by
  induction h with
  | finite n C => exact translate_embedFinite C
  | raw n => rfl
  | identity hp hq => rfl
  | arrow hA hB iA iB => simp only [translate, iA, iB]
  | pi hB iB => simp only [translate, iB, Option.map]
  | sigma hB iB => simp only [translate, iB, Option.map]

theorem Translation.unique {n m : Nat} {A : P01DF.Ty} {A' B' : Ty}
    (h : Translation n A A') (k : Translation m A B') : A' = B' :=
  Option.some.inj (h.readback.symm.trans k.readback)

/-- Every accepted old All is exactly an entire finite-image subtree. -/
theorem Translation.all_image {n : Nat} {B : P01DF.Ty} {A' : Ty}
    (h : Translation n (.all B) A') : ∃ C, B = P01DF.embedFinite C ∧ A' = .allFinite C := by
  have he := h.readback
  change (decodeFinite B).map Ty.allFinite = some A' at he
  cases hb : decodeFinite B with
  | none => simp only [hb, Option.map] at he; cases he
  | some C =>
      simp only [hb, Option.map, Option.some.injEq] at he
      exact ⟨C, decodeFinite_sound hb, he.symm⟩

/-- Equality is of the interpreted PER records, not merely inclusion of carriers. -/
theorem Translation.object_agrees {n : Nat} {A : P01DF.Ty} {A' : Ty}
    (h : Translation n A A') {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n)
    {ρ : OEnv} {η : Env} (d : D Γ ρ η) :
    objectOf (form_sound (h.form hΓ hlen)).2.laws d = ((P01DF.interpret A).run η).obj ρ := by
  apply per_ext
  intro t u
  exact Iff.of_eq (h.F_agrees ρ η t u)

theorem Restricted.object_agrees {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A')
    {ρ : OEnv} {η : Env} (d : D (rawTel n) ρ η) :
    objectOf (form_sound hr.formed).2.laws d = ((P01DF.interpret A).run η).obj ρ := by
  apply per_ext
  intro t u
  exact Iff.of_eq (hr.translation.F_agrees ρ η t u)

/-- The accepted dependent All/Pi example lies outside the finite-All translation. -/
theorem no_dependentPolyType {n : Nat} {A' : Ty} :
    ¬ Translation n P01DF.dependentPolyType A' := by
  intro h
  have he := h.readback
  change none = some A' at he
  cases he

/-- Finite representability of the conclusion does not admit an All-introduction tree. -/
def excludedFiniteConclusion : Derivation (.atom .i)
    (.all (.arrow (.param 0) (.param 0))) := .allIntro (.i (.param 0))

theorem no_excludedFiniteConclusion {n : Nat} {A' : Ty} :
    ¬ Restricted n excludedFiniteConclusion A' := no_allIntro

/-- The source judgment is the constructor-preserving erasure of the retained tree. -/
theorem Restricted.old_judgment {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (_hr : Restricted n h A') : P01DF.Has p A := h.erase

theorem Restricted.heterogeneous_agrees {n : Nat} {p : Poly} {A : P01DF.Ty}
    {h : Derivation p A} {A' : Ty} (hr : Restricted n h A')
    (r : REnv) (η ξ : Env) (hc : P01DF.IndexRelated η ξ) (t u : Term) :
    G A' r η ξ t u = ((P01DF.interpret A).run η).rel r t u :=
  hr.translation.G_agrees r η ξ hc t u

/-- A nonempty open-variable control uses the derived Raw rule in an all-Raw telescope. -/
theorem raw_variable_embedding : Has (rawTel 1) (.var 0) .raw :=
  (Restricted.raw (n := 1) (p := .var 0) (Nat.zero_lt_succ 0)).raw_embed

end P01TC.Legacy
