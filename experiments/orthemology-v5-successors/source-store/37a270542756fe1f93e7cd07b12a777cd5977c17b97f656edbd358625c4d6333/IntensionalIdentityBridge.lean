/- The single atom/application bridge, its closed conversion theorem, and the
   exact mutually inductive 2/7/18-rule hypothetical extension of AllSyntax.
   The delivered source syntax and all baseline files remain unchanged. -/
import AllPredicates

namespace P01AC.Intensional.Plus
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- The original seven conversion generators, plus exactly one bridge. -/
inductive PolyConvPlus : Poly → Poly → Prop
  | refl (p) : PolyConvPlus p p
  | symm : PolyConvPlus p q → PolyConvPlus q p
  | trans : PolyConvPlus p q → PolyConvPlus q r → PolyConvPlus p r
  | app : PolyConvPlus f g → PolyConvPlus p q → PolyConvPlus (.app f p) (.app g q)
  | i (p) : PolyConvPlus (.app (.atom .i) p) p
  | k (p q) : PolyConvPlus (.app (.app (.atom .k) p) q) p
  | s (p q r) : PolyConvPlus (.app (.app (.app (.atom .s) p) q) r)
      (.app (.app p r) (.app q r))
  | bridge (r t : Term) : PolyConvPlus (.atom (.app r t)) (.app (.atom r) (.atom t))

/-- Inclusion preserves every old conversion derivation. -/
theorem polyConv_inclusion {p q : Poly} (h : P01DF.PolyConv p q) :
    PolyConvPlus p q := by
  induction h with
  | refl => exact .refl _
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | app h k ih ik => exact .app ih ik
  | i p => exact .i p
  | k p q => exact .k p q
  | s p q r => exact .s p q r

/-- Every generator preserves the unchanged raw conversion under every valuation. -/
theorem polyConvPlus_sound {p q : Poly} (h : PolyConvPlus p q) (η : Env) :
    Conv (eval p η) (eval q η) := by
  induction h with
  | refl => exact .refl _
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | app h k ih ik => exact conv_app ih ik
  | i p => exact .step (.i _)
  | k p q => exact .step (.k _ _)
  | s p q r => exact .step (.s _ _ _)
  | bridge r t => exact .refl _

/-- Raw compatible application can be exposed and repacked with the bridge. -/
theorem atom_app_congr {f g a b : Term}
    (hf : PolyConvPlus (.atom f) (.atom g))
    (ha : PolyConvPlus (.atom a) (.atom b)) :
    PolyConvPlus (.atom (.app f a)) (.atom (.app g b)) :=
  (PolyConvPlus.bridge f a).trans
    ((PolyConvPlus.app hf ha).trans (PolyConvPlus.bridge g b).symm)

/-- All five source Step constructors lift, including both compatible contexts. -/
theorem raw_step_atom {t u : Term} (h : Step t u) :
    PolyConvPlus (.atom t) (.atom u) := by
  induction h with
  | i x => exact (PolyConvPlus.bridge .i x).trans (.i (.atom x))
  | k x y =>
      exact (PolyConvPlus.bridge (.app .k x) y).trans
        ((PolyConvPlus.app (.bridge .k x) (.refl (.atom y))).trans
          (.k (.atom x) (.atom y)))
  | s f g x =>
      exact (PolyConvPlus.bridge (.app (.app .s f) g) x).trans
        ((PolyConvPlus.app (.bridge (.app .s f) g) (.refl (.atom x))).trans
          ((PolyConvPlus.app (.app (.bridge .s f) (.refl (.atom g)))
            (.refl (.atom x))).trans
            ((PolyConvPlus.s (.atom f) (.atom g) (.atom x)).trans
              ((PolyConvPlus.app (PolyConvPlus.bridge f x).symm (PolyConvPlus.bridge g x).symm).trans
                (PolyConvPlus.bridge (.app f x) (.app g x)).symm))))
  | left h x ih => exact atom_app_congr ih (.refl (.atom x))
  | right f h ih => exact atom_app_congr (.refl (.atom f)) ih

/-- Raw Conv lifts on atoms by induction over its exact four constructors. -/
theorem raw_conv_atom {t u : Term} (h : Conv t u) :
    PolyConvPlus (.atom t) (.atom u) := by
  induction h with
  | refl => exact .refl _
  | step h => exact raw_step_atom h
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik

/-- A closed polynomial packs into the atom of its literal evaluation. -/
theorem closed_pack (p : Poly) (hp : Scoped 0 p) (η : Env) :
    PolyConvPlus p (.atom (eval p η)) := by
  induction p with
  | var n => exact False.elim (Nat.not_lt_zero n hp)
  | atom t => exact .refl _
  | app f a ihf iha =>
      exact (PolyConvPlus.app (ihf hp.1) (iha hp.2)).trans
        (PolyConvPlus.bridge (eval f η) (eval a η)).symm

/-- Closed conversion is exactly raw conversion of the zero-environment evaluations.
    The two explicit scope premises are essential to this converse. -/
theorem closed_conversion_iff {p q : Poly} (hp : Scoped 0 p) (hq : Scoped 0 q) :
    PolyConvPlus p q ↔ Conv (eval p zeroEnv) (eval q zeroEnv) := by
  constructor
  · intro h
    exact polyConvPlus_sound h zeroEnv
  · intro h
    exact (closed_pack p hp zeroEnv).trans
      ((raw_conv_atom h).trans (closed_pack q hq zeroEnv).symm)

/- This is a literal copy of the baseline mutual declarations, with only the
   judgement names freshened and the two PolyConv premises replaced. -/
mutual
  inductive CtxPlus : Tel → Prop
    | nil : CtxPlus []
    | ext : CtxPlus Γ → FormPlus Γ A → CtxPlus (A :: Γ)
  inductive FormPlus : Tel → Ty → Prop
    | param : CtxPlus Γ → FormPlus Γ (.param n)
    | bottom : CtxPlus Γ → FormPlus Γ .bottom
    | all : CtxPlus Γ → FormPlus (twkTel Γ) B → FormPlus Γ (.all B)
    | raw : CtxPlus Γ → FormPlus Γ .raw
    | pi : FormPlus Γ A → FormPlus (A :: Γ) B → FormPlus Γ (.pi A B)
    | sigma : FormPlus Γ A → FormPlus (A :: Γ) B → FormPlus Γ (.sigma A B)
    | identity : FormPlus Γ A → HasPlus Γ p A → HasPlus Γ q A → FormPlus Γ (.identity A p q)
  inductive HasPlus : Tel → Poly → Ty → Prop
    | var : FormPlus Γ A → Lookup Γ n A → HasPlus Γ (.var n) A
    | i : FormPlus Γ A → FormPlus Γ (arr A A) → HasPlus Γ (.atom .i) (arr A A)
    | k : FormPlus Γ A → FormPlus Γ B → FormPlus Γ (arr A (arr B A)) →
        HasPlus Γ (.atom .k) (arr A (arr B A))
    | s : FormPlus Γ A → FormPlus Γ B → FormPlus Γ C →
        FormPlus Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        HasPlus Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : (τ : List Ty) → finSupport C ≤ τ.length →
        (∀ n, n < τ.length → FormPlus Γ (typeImages τ n)) →
        FormPlus Γ (tsubst (typeImages τ) (fin C)) → FiniteDerives t C →
        HasPlus Γ (.atom t) (tsubst (typeImages τ) (fin C))
    | allIntro : FormPlus Γ (.all B) → HasPlus (twkTel Γ) p B → HasPlus Γ p (.all B)
    | allElim : FormPlus Γ (.all B) → FormPlus Γ A → FormPlus Γ (tinst B A) →
        HasPlus Γ p (.all B) → HasPlus Γ p (tinst B A)
    | rawAtom : FormPlus Γ .raw → HasPlus Γ (.atom t) .raw
    | rawApp : FormPlus Γ .raw → HasPlus Γ f .raw → HasPlus Γ a .raw → HasPlus Γ (.app f a) .raw
    | piIntro : FormPlus Γ (.pi A B) → HasPlus (A :: Γ) b B → Scoped Γ.length (abstract b) →
        HasPlus Γ (abstract b) (.pi A B)
    | piElim : FormPlus Γ (.pi A B) → FormPlus Γ (inst B a) →
        HasPlus Γ f (.pi A B) → HasPlus Γ a A → HasPlus Γ (.app f a) (inst B a)
    | sigmaIntro : FormPlus Γ (.sigma A B) → FormPlus Γ (inst B a) →
        HasPlus Γ a A → HasPlus Γ b (inst B a) → HasPlus Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : FormPlus Γ A → FormPlus Γ (.sigma A B) → HasPlus Γ z (.sigma A B) →
        HasPlus Γ (fstPoly z) A
    | sigmaSnd : FormPlus Γ (.sigma A B) → FormPlus Γ (inst B (fstPoly z)) →
        HasPlus Γ z (.sigma A B) → HasPlus Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : FormPlus Γ (.identity A p q) → HasPlus Γ p A → HasPlus Γ q A →
        PolyConvPlus p q → HasPlus Γ (.atom .i) (.identity A p q)
    | proofErase : FormPlus Γ .raw → FormPlus Γ (.identity A x y) →
        HasPlus Γ p (.identity A x y) → HasPlus Γ p .raw
    | j : FormPlus Γ A → FormPlus (theta Γ A x) B →
        FormPlus Γ (.identity A x y) → FormPlus Γ (motiveAt B x (.atom .i)) →
        FormPlus Γ (motiveAt B y e) → HasPlus Γ x A → HasPlus Γ y A →
        HasPlus Γ e (.identity A x y) → HasPlus Γ d (motiveAt B x (.atom .i)) →
        HasPlus Γ (jPoly d y e) (motiveAt B y e)
    | conv : FormPlus Γ A → HasPlus Γ p A → PolyConvPlus p q → Scoped Γ.length q → HasPlus Γ q A
end


/-- The old mutual typing grammar embeds without removing any premise. -/
theorem has_inclusion {Γ p A} (h : P01AC.Has Γ p A) : HasPlus Γ p A := by
  induction h using P01AC.Has.rec
    (motive_1 := fun Γ _ => CtxPlus Γ)
    (motive_2 := fun Γ A _ => FormPlus Γ A) with
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
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q (polyConv_inclusion pq)
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p (polyConv_inclusion pq) hs

/-- The old mutual typing grammar embeds without removing any premise. -/
theorem form_inclusion {Γ A} (h : P01AC.Form Γ A) : FormPlus Γ A := by
  induction h using P01AC.Form.rec
    (motive_1 := fun Γ _ => CtxPlus Γ)
    (motive_3 := fun Γ p A _ => HasPlus Γ p A) with
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
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q (polyConv_inclusion pq)
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p (polyConv_inclusion pq) hs

/-- The old mutual typing grammar embeds without removing any premise. -/
theorem ctx_inclusion {Γ} (h : P01AC.Ctx Γ) : CtxPlus Γ := by
  induction h using P01AC.Ctx.rec
    (motive_3 := fun Γ p A _ => HasPlus Γ p A)
    (motive_2 := fun Γ A _ => FormPlus Γ A) with
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
    | identityIntro hId hp hq pq a p q => exact .identityIntro a p q (polyConv_inclusion pq)
    | proofErase hRaw hId hp a i p => exact .proofErase a i p
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact .j a b i base t x y e d
    | conv hA hp pq hs a p => exact .conv a p (polyConv_inclusion pq) hs

end P01AC.Intensional.Plus
