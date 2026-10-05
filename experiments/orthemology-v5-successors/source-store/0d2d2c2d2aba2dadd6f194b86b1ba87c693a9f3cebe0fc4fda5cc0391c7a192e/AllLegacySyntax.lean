/- Recursive, source-code-preserving translation of the entire old type grammar. -/
import AllNucleusSyntax
import AllStructural
import TypedLegacy
namespace P01AC.Legacy
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- The accepted constructor-faithful tree is reused literally, before Prop erasure. -/
abbrev Derivation := P01TC.Legacy.Derivation

def erase {p A} (h : Derivation p A) : P01DF.Has p A := h.erase

/-- Unlike the accepted nucleus comparison, All is recursively translated everywhere. -/
def translate : P01DF.Ty → Ty
  | .param n => .param n
  | .bottom => .bottom
  | .raw => .raw
  | .identity p q => .identity .raw p q
  | .arrow A B => arr (translate A) (translate B)
  | .pi B => .pi .raw (translate B)
  | .sigma B => .sigma .raw (translate B)
  | .all B => .all (translate B)

/-- Exact finite term support, including both displayed identity endpoints. -/
def TypeSupported (n : Nat) : P01DF.Ty → Prop
  | .param _ | .bottom | .raw => True
  | .identity p q => Scoped n p ∧ Scoped n q
  | .arrow A B => TypeSupported n A ∧ TypeSupported n B
  | .pi B | .sigma B => TypeSupported (n+1) B
  | .all B => TypeSupported n B

theorem translate_index (A : P01DF.Ty) (σ : Nat → Poly) :
    translate (P01DF.substIndex σ A) = subst σ (translate A) := by
  induction A generalizing σ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [P01DF.substIndex, translate, subst_arr, ha, hb]
  | pi B ih => simp only [P01DF.substIndex, translate, subst, ih]
  | sigma B ih => simp only [P01DF.substIndex, translate, subst, ih]
  | all B ih => simp only [P01DF.substIndex, translate, subst, ih]

theorem translate_inst (B : P01DF.Ty) (a : Poly) :
    translate (P01DF.instantiate B a) = inst (translate B) a := translate_index B _

theorem translate_motiveAt (B : P01DF.Ty) (y e : Poly) :
    translate (P01DF.motiveAt B y e) = motiveAt (translate B) y e := translate_index B _

theorem translate_rename (A : P01DF.Ty) (r : Nat → Nat) :
    translate (P01DF.renameType r A) = trename r (translate A) := by
  induction A generalizing r with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [P01DF.renameType, translate, trename_arr, ha, hb]
  | pi B ih => simp only [P01DF.renameType, translate, trename, ih]
  | sigma B ih => simp only [P01DF.renameType, translate, trename, ih]
  | all B ih => simp only [P01DF.renameType, translate, trename, ih]

theorem translate_liftTypes (τ : Nat → P01DF.Ty) :
    (fun n => translate (P01DF.liftTypes τ n)) = tup (fun n => translate (τ n)) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact translate_rename (τ n) Nat.succ

theorem translate_liftIndices (τ : Nat → P01DF.Ty) :
    (fun n => translate (P01DF.liftIndices τ n)) = fun n => wk (translate (τ n)) := by
  funext n
  exact translate_index (τ n) _

theorem translate_typeSubst (A : P01DF.Ty) (τ : Nat → P01DF.Ty) :
    translate (P01DF.substType τ A) = tsubst (fun n => translate (τ n)) (translate A) := by
  have hp : pup Poly.var = Poly.var := by funext n; cases n <;> rfl
  induction A generalizing τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => simp only [P01DF.substType, translate, tsubst, mixed, psub_id]
  | arrow A B ha hb => simp only [P01DF.substType, translate, tsubst_arr, ha, hb]
  | pi B ih =>
      simp only [P01DF.substType, translate, ih, translate_liftIndices, tsubst, mixed, hp]
  | sigma B ih =>
      simp only [P01DF.substType, translate, ih, translate_liftIndices, tsubst, mixed, hp]
  | all B ih =>
      simp only [P01DF.substType, translate, ih, translate_liftTypes, tsubst, mixed]

theorem translate_tinst (B A : P01DF.Ty) :
    translate (P01DF.instantiateType B A) = tinst (translate B) (translate A) := by
  rw [P01DF.instantiateType, translate_typeSubst]
  unfold tinst
  congr 1
  funext n
  cases n <;> rfl

theorem translate_finite (C : TypeCode) : translate (P01DF.embedFinite C) = fin C := by
  induction C with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [P01DF.embedFinite, translate, ha, hb, fin]
  | all B ih => simp only [P01DF.embedFinite, translate, ih, fin]

/-- Every variable is available at Raw through an actual syntactic derivation. -/
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

@[simp] theorem rawTel_twk (n : Nat) : twkTel (rawTel n) = rawTel n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [rawTel,twkTel,List.map_cons,twk,trename] using congrArg (Ty.raw :: ·) ih

theorem RawContext.ext {Γ : Tel} (h : RawContext Γ) : RawContext (.raw :: Γ) := by
  have hc : Ctx (.raw :: Γ) := .ext h.ctx (.raw h.ctx)
  refine ⟨hc, ?_⟩
  intro n hn
  cases n with
  | zero => exact .var (.raw hc) .zero
  | succ n => exact has_wk (h.vars n (Nat.lt_of_succ_lt_succ hn)) h.ctx (.raw h.ctx)

theorem RawContext.twk {Γ : Tel} (h : RawContext Γ) : RawContext (twkTel Γ) := by
  refine ⟨ctx_twk h.ctx, ?_⟩
  intro n hn
  exact has_twk (h.vars n (by simpa only [twkTel,List.length_map] using hn))

theorem rawTel_context (n : Nat) : RawContext (rawTel n) := by
  induction n with
  | zero => exact ⟨.nil, fun n hn => False.elim (Nat.not_lt_zero n hn)⟩
  | succ n ih => exact ih.ext

theorem raw_term {Γ : Tel} {p : Poly} (hΓ : RawContext Γ) (hp : Scoped Γ.length p) : Has Γ p .raw := by
  induction p with
  | var n => exact hΓ.vars n hp
  | atom t => exact .rawAtom (.raw hΓ.ctx)
  | app f a hf ha => exact .rawApp (.raw hΓ.ctx) (hf hp.1) (ha hp.2)

/-- Theta's newest declaration is Id, not Raw. Only proofErase grants Raw access. -/
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
  | succ n => exact has_wk (h.ext.vars n (Nat.lt_of_succ_lt_succ hn)) hbase hhead

theorem TypeSupported.form {n : Nat} {A : P01DF.Ty} (h : TypeSupported n A)
    {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n) : Form Γ (translate A) := by
  induction A generalizing n Γ with
  | param k => exact .param hΓ.ctx
  | bottom => exact .bottom hΓ.ctx
  | raw => exact .raw hΓ.ctx
  | identity p q =>
      exact .identity (.raw hΓ.ctx)
        (raw_term hΓ (by simpa only [hlen] using h.1))
        (raw_term hΓ (by simpa only [hlen] using h.2))
  | arrow A B ha hb => exact form_arr (ha h.1 hΓ hlen) (hb h.2 hΓ hlen)
  | pi B ih => exact .pi (.raw hΓ.ctx) (ih h hΓ.ext (congrArg Nat.succ hlen))
  | sigma B ih => exact .sigma (.raw hΓ.ctx) (ih h hΓ.ext (congrArg Nat.succ hlen))
  | all B ih => exact .all hΓ.ctx (ih h hΓ.twk (by simpa only [twkTel,List.length_map] using hlen))

theorem rawTel_lookup_type {n k A} (h : Lookup (rawTel n) k A) : A = .raw := by
  induction n generalizing k A with
  | zero => cases h
  | succ n ih =>
      cases h with
      | zero => rfl
      | succ h => rw [ih h]; rfl

/-- Literal identity-polynomial typed transport from an all-Raw source.
This total interface is used only for scoped syntax, not as a zero-padded semantic map. -/
theorem RawContext.identitySubstitution {Γ : Tel} (hΓ : RawContext Γ) :
    MixedSubstitution (rawTel Γ.length) Γ Poly.var Ty.param := by
  refine ⟨fun _ => .param hΓ.ctx, ?_⟩
  intro n A hn
  have ht := rawTel_lookup_type hn
  subst A
  exact hΓ.vars n (by simpa only [rawTel_length] using lookup_lt hn)

/-- Finite identity components retain atom-zero term padding and Bottom type padding. -/
theorem RawContext.finiteIdentitySubstitution {Γ : Tel} (hΓ : RawContext Γ) (n : Nat) :
    MixedSub Γ (rawTel Γ.length) (identityImages Γ.length) (parameterImages n) := by
  constructor
  · apply MixedTerms.ofLookup hΓ.ctx (rawTel_context Γ.length).ctx
      (by simp only [identityImages_length,rawTel_length])
    intro k A hk
    have hbound : k < Γ.length := by simpa only [rawTel_length] using lookup_lt hk
    rw [identityImages_get hbound,rawTel_lookup_type hk]
    exact hΓ.vars k hbound
  · intro k hk
    rw [parameterImages_get (by simpa only [parameterImages_length] using hk)]
    exact .param hΓ.ctx

/-- Only the scoped action of the finite identity is equated with literal syntax.
No global equality between the zero-padded component function and Poly.var is used. -/
theorem RawContext.transport_form {Γ : Tel} {A : Ty} (hΓ : RawContext Γ)
    (hA : Form (rawTel Γ.length) A) : Form Γ A := by
  have hs := hΓ.finiteIdentitySubstitution (typeSupport A)
  have he : mixed (images (identityImages Γ.length))
      (typeImages (parameterImages (typeSupport A))) A = A :=
    mixed_finite_identity (by simpa only [rawTel_length] using form_scoped hA) (Nat.le_refl _)
  simpa only [he] using hs.form hA

/-- The J motive is formed first in all-Raw, then transported unchanged into Theta. -/
theorem TypeSupported.theta_form {n : Nat} {B : P01DF.Ty} (hB : TypeSupported (n+2) B)
    {Γ : Tel} {x : Poly} (hΓ : RawContext Γ) (hlen : Γ.length = n) (hx : Scoped Γ.length x) :
    Form (theta Γ .raw x) (translate B) := by
  have hθ := hΓ.theta hx
  apply hθ.transport_form
  apply hB.form (rawTel_context _) 
  simp only [rawTel_length,theta,List.length_cons,hlen]

end P01AC.Legacy
