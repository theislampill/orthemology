/- Isolated finite-certificate extension. All original rules and their
   syntactic premises are retained; current Has/HasPlus/HasE are untouched. -/
import UnaryNormalForm
namespace P01AC.UnaryCertificate
open OrthemologyV2 OrthemologyV3 P01D P01R

mutual
  inductive CtxC : Tel → Prop
    | nil : CtxC []
    | ext : CtxC Γ → FormC Γ A → CtxC (A :: Γ)
  inductive FormC : Tel → Ty → Prop
    | param : CtxC Γ → FormC Γ (.param n)
    | bottom : CtxC Γ → FormC Γ .bottom
    | all : CtxC Γ → FormC (twkTel Γ) B → FormC Γ (.all B)
    | raw : CtxC Γ → FormC Γ .raw
    | pi : FormC Γ A → FormC (A :: Γ) B → FormC Γ (.pi A B)
    | sigma : FormC Γ A → FormC (A :: Γ) B → FormC Γ (.sigma A B)
    | identity : FormC Γ A → HasC Γ p A → HasC Γ q A → FormC Γ (.identity A p q)
  inductive HasC : Tel → Poly → Ty → Prop
    | var : FormC Γ A → Lookup Γ n A → HasC Γ (.var n) A
    | i : FormC Γ A → FormC Γ (arr A A) → HasC Γ (.atom .i) (arr A A)
    | k : FormC Γ A → FormC Γ B → FormC Γ (arr A (arr B A)) →
        HasC Γ (.atom .k) (arr A (arr B A))
    | s : FormC Γ A → FormC Γ B → FormC Γ C →
        FormC Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        HasC Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : (τ : List Ty) → finSupport C ≤ τ.length →
        (∀ n, n < τ.length → FormC Γ (typeImages τ n)) →
        FormC Γ (tsubst (typeImages τ) (fin C)) → FiniteDerives t C →
        HasC Γ (.atom t) (tsubst (typeImages τ) (fin C))
    | allIntro : FormC Γ (.all B) → HasC (twkTel Γ) p B → HasC Γ p (.all B)
    | allElim : FormC Γ (.all B) → FormC Γ A → FormC Γ (tinst B A) →
        HasC Γ p (.all B) → HasC Γ p (tinst B A)
    | rawAtom : FormC Γ .raw → HasC Γ (.atom t) .raw
    | rawApp : FormC Γ .raw → HasC Γ f .raw → HasC Γ a .raw → HasC Γ (.app f a) .raw
    | piIntro : FormC Γ (.pi A B) → HasC (A :: Γ) b B → Scoped Γ.length (abstract b) →
        HasC Γ (abstract b) (.pi A B)
    | piElim : FormC Γ (.pi A B) → FormC Γ (inst B a) →
        HasC Γ f (.pi A B) → HasC Γ a A → HasC Γ (.app f a) (inst B a)
    | sigmaIntro : FormC Γ (.sigma A B) → FormC Γ (inst B a) →
        HasC Γ a A → HasC Γ b (inst B a) → HasC Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : FormC Γ A → FormC Γ (.sigma A B) → HasC Γ z (.sigma A B) →
        HasC Γ (fstPoly z) A
    | sigmaSnd : FormC Γ (.sigma A B) → FormC Γ (inst B (fstPoly z)) →
        HasC Γ z (.sigma A B) → HasC Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : FormC Γ (.identity A p q) → HasC Γ p A → HasC Γ q A →
        P01DF.PolyConv p q → HasC Γ (.atom .i) (.identity A p q)
    | proofErase : FormC Γ .raw → FormC Γ (.identity A x y) →
        HasC Γ p (.identity A x y) → HasC Γ p .raw
    | j : FormC Γ A → FormC (theta Γ A x) B →
        FormC Γ (.identity A x y) → FormC Γ (motiveAt B x (.atom .i)) →
        FormC Γ (motiveAt B y e) → HasC Γ x A → HasC Γ y A →
        HasC Γ e (.identity A x y) → HasC Γ d (motiveAt B x (.atom .i)) →
        HasC Γ (jPoly d y e) (motiveAt B y e)
    | conv : FormC Γ A → HasC Γ p A → P01DF.PolyConv p q → Scoped Γ.length q → HasC Γ q A
    /-- Finite computational evidence; no semantic relation is a rule premise. -/
    | certified (e f : P01AC.UnaryIdentity.Expr) (c : P01AC.UnaryIdentity.Certificate) :
        FormC Γ (.identity (arr P01AC.EffectiveCompleteness.N P01AC.EffectiveCompleteness.N)
          e.closed f.closed) →
        P01AC.UnaryIdentity.verifyCertificate e f c = true →
        HasC Γ (.atom .i) (.identity (arr P01AC.EffectiveCompleteness.N P01AC.EffectiveCompleteness.N)
          e.closed f.closed)
end

theorem has_inclusion {Γ p A} (h : P01AC.Has Γ p A) : HasC Γ p A := by
  induction h using P01AC.Has.rec
    (motive_1 := fun Γ _ => CtxC Γ)
    (motive_2 := fun Γ A _ => FormC Γ A) with
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

theorem form_inclusion {Γ A} (h : P01AC.Form Γ A) : FormC Γ A := by
  induction h using P01AC.Form.rec
    (motive_1 := fun Γ _ => CtxC Γ)
    (motive_3 := fun Γ p A _ => HasC Γ p A) with
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

theorem ctx_inclusion {Γ} (h : P01AC.Ctx Γ) : CtxC Γ := by
  induction h using P01AC.Ctx.rec
    (motive_3 := fun Γ p A _ => HasC Γ p A)
    (motive_2 := fun Γ A _ => FormC Γ A) with
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

end P01AC.UnaryCertificate
