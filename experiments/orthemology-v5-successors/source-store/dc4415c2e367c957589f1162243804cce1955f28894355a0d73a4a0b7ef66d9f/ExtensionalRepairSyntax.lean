/- Isolated, unadopted finite typed-extensional candidate. Baseline files are exact copies.
    The conversion relation is IMPORTED unchanged; it is not freshly extended. -/
import IntensionalIdentityBridge

namespace P01AC.ExtensionalRepair
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open Intensional
open Intensional.Plus (PolyConvPlus)

mutual
  inductive CtxE : Tel → Prop
    | nil : CtxE []
    | ext : CtxE Γ → FormE Γ A → CtxE (A :: Γ)
  inductive FormE : Tel → Ty → Prop
    | param : CtxE Γ → FormE Γ (.param n)
    | bottom : CtxE Γ → FormE Γ .bottom
    | all : CtxE Γ → FormE (twkTel Γ) B → FormE Γ (.all B)
    | raw : CtxE Γ → FormE Γ .raw
    | pi : FormE Γ A → FormE (A :: Γ) B → FormE Γ (.pi A B)
    | sigma : FormE Γ A → FormE (A :: Γ) B → FormE Γ (.sigma A B)
    | identity : FormE Γ A → HasE Γ p A → HasE Γ q A → FormE Γ (.identity A p q)
  inductive HasE : Tel → Poly → Ty → Prop
    | var : FormE Γ A → Lookup Γ n A → HasE Γ (.var n) A
    | i : FormE Γ A → FormE Γ (arr A A) → HasE Γ (.atom .i) (arr A A)
    | k : FormE Γ A → FormE Γ B → FormE Γ (arr A (arr B A)) →
        HasE Γ (.atom .k) (arr A (arr B A))
    | s : FormE Γ A → FormE Γ B → FormE Γ C →
        FormE Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        HasE Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : (τ : List Ty) → finSupport C ≤ τ.length →
        (∀ n, n < τ.length → FormE Γ (typeImages τ n)) →
        FormE Γ (tsubst (typeImages τ) (fin C)) → FiniteDerives t C →
        HasE Γ (.atom t) (tsubst (typeImages τ) (fin C))
    | allIntro : FormE Γ (.all B) → HasE (twkTel Γ) p B → HasE Γ p (.all B)
    | allElim : FormE Γ (.all B) → FormE Γ A → FormE Γ (tinst B A) →
        HasE Γ p (.all B) → HasE Γ p (tinst B A)
    | rawAtom : FormE Γ .raw → HasE Γ (.atom t) .raw
    | rawApp : FormE Γ .raw → HasE Γ f .raw → HasE Γ a .raw → HasE Γ (.app f a) .raw
    | piIntro : FormE Γ (.pi A B) → HasE (A :: Γ) b B → Scoped Γ.length (abstract b) →
        HasE Γ (abstract b) (.pi A B)
    | piElim : FormE Γ (.pi A B) → FormE Γ (inst B a) →
        HasE Γ f (.pi A B) → HasE Γ a A → HasE Γ (.app f a) (inst B a)
    | sigmaIntro : FormE Γ (.sigma A B) → FormE Γ (inst B a) →
        HasE Γ a A → HasE Γ b (inst B a) → HasE Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : FormE Γ A → FormE Γ (.sigma A B) → HasE Γ z (.sigma A B) →
        HasE Γ (fstPoly z) A
    | sigmaSnd : FormE Γ (.sigma A B) → FormE Γ (inst B (fstPoly z)) →
        HasE Γ z (.sigma A B) → HasE Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : FormE Γ (.identity A p q) → HasE Γ p A → HasE Γ q A →
        PolyConvPlus p q → HasE Γ (.atom .i) (.identity A p q)
    | proofErase : FormE Γ .raw → FormE Γ (.identity A x y) →
        HasE Γ p (.identity A x y) → HasE Γ p .raw
    | j : FormE Γ A → FormE (theta Γ A x) B →
        FormE Γ (.identity A x y) → FormE Γ (motiveAt B x (.atom .i)) →
        FormE Γ (motiveAt B y e) → HasE Γ x A → HasE Γ y A →
        HasE Γ e (.identity A x y) → HasE Γ d (motiveAt B x (.atom .i)) →
        HasE Γ (jPoly d y e) (motiveAt B y e)
    | conv : FormE Γ A → HasE Γ p A → PolyConvPlus p q → Scoped Γ.length q → HasE Γ q A
    /-- Exactly §3.1: all explicit formation and scope premises are retained. -/
    | piExt : FormE Γ A → FormE (A :: Γ) B → FormE Γ (.pi A B) →
        HasE Γ p (.pi A B) → HasE Γ q (.pi A B) →
        FormE (A :: Γ) (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0))) →
        FormE Γ (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        HasE Γ h (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        FormE Γ (.identity (.pi A B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length A → TyScoped (Γ.length + 1) B →
        HasE Γ (.atom .i) (.identity (.pi A B) p q)
    /-- Exactly §3.2: one finite body proof under the type-weakened telescope. -/
    | allExt : FormE (twkTel Γ) B → FormE Γ (.all B) →
        HasE Γ p (.all B) → HasE Γ q (.all B) →
        FormE (twkTel Γ) (.identity B p q) →
        HasE (twkTel Γ) h (.identity B p q) →
        FormE Γ (.identity (.all B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length B → HasE Γ (.atom .i) (.identity (.all B) p q)
end

/-- The old mutual typing grammar embeds without removing any premise. -/
theorem plus_has_inclusion {Γ p A} (h : Plus.HasPlus Γ p A) : HasE Γ p A := by
  induction h using Plus.HasPlus.rec
    (motive_1 := fun Γ _ => CtxE Γ)
    (motive_2 := fun Γ A _ => FormE Γ A) with
    | nil => exact .nil
    | ext hΓ hA c a => exact .ext c a
    | param hΓ c => exact .param c
    | bottom hΓ c => exact .bottom c
    | all hΓ hB c b => exact .all c b
    | raw hΓ c => exact .raw c
    | pi hA hB a b => exact .pi a b
    | sigma hA hB a b => exact .sigma a b
    | identity hA hp hq a p q => exact .identity a p q
    | var hA hv a => exact .var a hv
    | i hA ht a t => exact .i a t
    | k hA hB ht a b t => exact .k a b t
    | s hA hB hC ht a b c t => exact .s a b c t
    | finite τ bound hτ hA hf a t => exact .finite τ bound a t hf
    | allIntro hAll hp a p => exact .allIntro a p
    | allElim hAll hA hTarget hp a x t p => exact .allElim a x t p
    | rawAtom hA a => exact .rawAtom a
    | rawApp hA hf hx a f x => exact .rawApp a f x
    | piIntro hA hb hs a b => exact .piIntro a b hs
    | piElim hPi ht hf ha pi t f a => exact .piElim pi t f a
    | sigmaIntro hSigma ht ha hb s t a b => exact .sigmaIntro s t a b
    | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
    | sigmaSnd hSigma ht hz s t z => exact .sigmaSnd s t z
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p pq hs

/-- The old mutual typing grammar embeds without removing any premise. -/
theorem plus_form_inclusion {Γ A} (h : Plus.FormPlus Γ A) : FormE Γ A := by
  induction h using Plus.FormPlus.rec
    (motive_1 := fun Γ _ => CtxE Γ)
    (motive_3 := fun Γ p A _ => HasE Γ p A) with
    | nil => exact .nil
    | ext hΓ hA c a => exact .ext c a
    | param hΓ c => exact .param c
    | bottom hΓ c => exact .bottom c
    | all hΓ hB c b => exact .all c b
    | raw hΓ c => exact .raw c
    | pi hA hB a b => exact .pi a b
    | sigma hA hB a b => exact .sigma a b
    | identity hA hp hq a p q => exact .identity a p q
    | var hA hv a => exact .var a hv
    | i hA ht a t => exact .i a t
    | k hA hB ht a b t => exact .k a b t
    | s hA hB hC ht a b c t => exact .s a b c t
    | finite τ bound hτ hA hf a t => exact .finite τ bound a t hf
    | allIntro hAll hp a p => exact .allIntro a p
    | allElim hAll hA hTarget hp a x t p => exact .allElim a x t p
    | rawAtom hA a => exact .rawAtom a
    | rawApp hA hf hx a f x => exact .rawApp a f x
    | piIntro hA hb hs a b => exact .piIntro a b hs
    | piElim hPi ht hf ha pi t f a => exact .piElim pi t f a
    | sigmaIntro hSigma ht ha hb s t a b => exact .sigmaIntro s t a b
    | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
    | sigmaSnd hSigma ht hz s t z => exact .sigmaSnd s t z
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p pq hs

/-- The old mutual typing grammar embeds without removing any premise. -/
theorem plus_ctx_inclusion {Γ} (h : Plus.CtxPlus Γ) : CtxE Γ := by
  induction h using Plus.CtxPlus.rec
    (motive_3 := fun Γ p A _ => HasE Γ p A)
    (motive_2 := fun Γ A _ => FormE Γ A) with
    | nil => exact .nil
    | ext hΓ hA c a => exact .ext c a
    | param hΓ c => exact .param c
    | bottom hΓ c => exact .bottom c
    | all hΓ hB c b => exact .all c b
    | raw hΓ c => exact .raw c
    | pi hA hB a b => exact .pi a b
    | sigma hA hB a b => exact .sigma a b
    | identity hA hp hq a p q => exact .identity a p q
    | var hA hv a => exact .var a hv
    | i hA ht a t => exact .i a t
    | k hA hB ht a b t => exact .k a b t
    | s hA hB hC ht a b c t => exact .s a b c t
    | finite τ bound hτ hA hf a t => exact .finite τ bound a t hf
    | allIntro hAll hp a p => exact .allIntro a p
    | allElim hAll hA hTarget hp a x t p => exact .allElim a x t p
    | rawAtom hA a => exact .rawAtom a
    | rawApp hA hf hx a f x => exact .rawApp a f x
    | piIntro hA hb hs a b => exact .piIntro a b hs
    | piElim hPi ht hf ha pi t f a => exact .piElim pi t f a
    | sigmaIntro hSigma ht ha hb s t a b => exact .sigmaIntro s t a b
    | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
    | sigmaSnd hSigma ht hz s t z => exact .sigmaSnd s t z
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p pq hs


/-- Current derivations embed via the separately named exact bridge-only grammar. -/
theorem has_inclusion {Γ p A} (h : P01AC.Has Γ p A) : HasE Γ p A :=
  plus_has_inclusion (Plus.has_inclusion h)
theorem form_inclusion {Γ A} (h : P01AC.Form Γ A) : FormE Γ A :=
  plus_form_inclusion (Plus.form_inclusion h)
theorem ctx_inclusion {Γ} (h : P01AC.Ctx Γ) : CtxE Γ :=
  plus_ctx_inclusion (Plus.ctx_inclusion h)

end P01AC.ExtensionalRepair
