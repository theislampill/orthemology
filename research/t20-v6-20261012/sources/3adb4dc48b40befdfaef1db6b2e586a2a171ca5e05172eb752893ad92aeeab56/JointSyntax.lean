import JointSubstitution

/- A separate, unadopted joint-completion syntax. Has, HasE and HasC are imported
unchanged. The original HasE constructor block is reproduced exactly under fresh
names, and neither completion rule has a semantic-validity premise. -/
namespace JointCompletion
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.Intensional.Plus (PolyConvPlus)
mutual
  inductive CtxJ : Tel → Prop
    | ctxBase : P01AC.ExtensionalRepair.CtxE Γ → CtxJ Γ
    | nil : CtxJ []
    | ext : CtxJ Γ → FormJ Γ A → CtxJ (A :: Γ)
  inductive FormJ : Tel → Ty → Prop
    | formBase : P01AC.ExtensionalRepair.FormE Γ A → FormJ Γ A
    | param : CtxJ Γ → FormJ Γ (.param n)
    | bottom : CtxJ Γ → FormJ Γ .bottom
    | all : CtxJ Γ → FormJ (twkTel Γ) B → FormJ Γ (.all B)
    | raw : CtxJ Γ → FormJ Γ .raw
    | pi : FormJ Γ A → FormJ (A :: Γ) B → FormJ Γ (.pi A B)
    | sigma : FormJ Γ A → FormJ (A :: Γ) B → FormJ Γ (.sigma A B)
    | identity : FormJ Γ A → HasJ Γ p A → HasJ Γ q A → FormJ Γ (.identity A p q)
  inductive HasJ : Tel → Poly → Ty → Prop
    | hasBase : P01AC.ExtensionalRepair.HasE Γ p A → HasJ Γ p A
    | var : FormJ Γ A → Lookup Γ n A → HasJ Γ (.var n) A
    | i : FormJ Γ A → FormJ Γ (arr A A) → HasJ Γ (.atom .i) (arr A A)
    | k : FormJ Γ A → FormJ Γ B → FormJ Γ (arr A (arr B A)) →
        HasJ Γ (.atom .k) (arr A (arr B A))
    | s : FormJ Γ A → FormJ Γ B → FormJ Γ C →
        FormJ Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        HasJ Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : (τ : List Ty) → finSupport C ≤ τ.length →
        (∀ n, n < τ.length → FormJ Γ (typeImages τ n)) →
        FormJ Γ (tsubst (typeImages τ) (fin C)) → FiniteDerives t C →
        HasJ Γ (.atom t) (tsubst (typeImages τ) (fin C))
    | allIntro : FormJ Γ (.all B) → HasJ (twkTel Γ) p B → HasJ Γ p (.all B)
    | allElim : FormJ Γ (.all B) → FormJ Γ A → FormJ Γ (tinst B A) →
        HasJ Γ p (.all B) → HasJ Γ p (tinst B A)
    | rawAtom : FormJ Γ .raw → HasJ Γ (.atom t) .raw
    | rawApp : FormJ Γ .raw → HasJ Γ f .raw → HasJ Γ a .raw → HasJ Γ (.app f a) .raw
    | piIntro : FormJ Γ (.pi A B) → HasJ (A :: Γ) b B → Scoped Γ.length (abstract b) →
        HasJ Γ (abstract b) (.pi A B)
    | piElim : FormJ Γ (.pi A B) → FormJ Γ (inst B a) →
        HasJ Γ f (.pi A B) → HasJ Γ a A → HasJ Γ (.app f a) (inst B a)
    | sigmaIntro : FormJ Γ (.sigma A B) → FormJ Γ (inst B a) →
        HasJ Γ a A → HasJ Γ b (inst B a) → HasJ Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : FormJ Γ A → FormJ Γ (.sigma A B) → HasJ Γ z (.sigma A B) →
        HasJ Γ (fstPoly z) A
    | sigmaSnd : FormJ Γ (.sigma A B) → FormJ Γ (inst B (fstPoly z)) →
        HasJ Γ z (.sigma A B) → HasJ Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : FormJ Γ (.identity A p q) → HasJ Γ p A → HasJ Γ q A →
        PolyConvPlus p q → HasJ Γ (.atom .i) (.identity A p q)
    | proofErase : FormJ Γ .raw → FormJ Γ (.identity A x y) →
        HasJ Γ p (.identity A x y) → HasJ Γ p .raw
    | j : FormJ Γ A → FormJ (theta Γ A x) B →
        FormJ Γ (.identity A x y) → FormJ Γ (motiveAt B x (.atom .i)) →
        FormJ Γ (motiveAt B y e) → HasJ Γ x A → HasJ Γ y A →
        HasJ Γ e (.identity A x y) → HasJ Γ d (motiveAt B x (.atom .i)) →
        HasJ Γ (jPoly d y e) (motiveAt B y e)
    | conv : FormJ Γ A → HasJ Γ p A → PolyConvPlus p q → Scoped Γ.length q → HasJ Γ q A
    /-- Exactly §3.1: all explicit formation and scope premises are retained. -/
    | piExt : FormJ Γ A → FormJ (A :: Γ) B → FormJ Γ (.pi A B) →
        HasJ Γ p (.pi A B) → HasJ Γ q (.pi A B) →
        FormJ (A :: Γ) (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0))) →
        FormJ Γ (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        HasJ Γ h (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        FormJ Γ (.identity (.pi A B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length A → TyScoped (Γ.length + 1) B →
        HasJ Γ (.atom .i) (.identity (.pi A B) p q)
    /-- Exactly §3.2: one finite body proof under the type-weakened telescope. -/
    | allExt : FormJ (twkTel Γ) B → FormJ Γ (.all B) →
        HasJ Γ p (.all B) → HasJ Γ q (.all B) →
        FormJ (twkTel Γ) (.identity B p q) →
        HasJ (twkTel Γ) h (.identity B p q) →
        FormJ Γ (.identity (.all B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length B → HasJ Γ (.atom .i) (.identity (.all B) p q)
    /-- All actual recursively formed motives and newly typed inputs are allowed. -/
    | sigmaElim : CtxJ Γ → FormJ Γ A → FormJ (A :: Γ) B →
        FormJ (.sigma A B :: Γ) P →
        HasJ (B :: A :: Γ) d (SigmaCompletion.branchType P) → HasJ Γ z (.sigma A B) →
        HasJ Γ (SigmaCompletion.branchAt d (fstPoly z) (sndPoly z)) (inst P z)
    /-- Full dependent induction; the witness is the retained uniform polynomial. -/
    | natInduction : CtxJ Γ → FormJ (P01AC.EffectiveCompleteness.N :: Γ) P →
        HasJ Γ p (inst P SourceRigidity.zero) → HasJ Γ s (RigidityInitiality.dependentStepType P) →
        HasJ Γ (RigidityInitiality.sectionPoly p s) (.pi P01AC.EffectiveCompleteness.N P)
end

end JointCompletion
