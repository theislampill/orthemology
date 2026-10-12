import JointSyntax

/- Selective rule extensions. Each Boolean enables exactly one full external
completion constructor. Original Has, HasE, HasC and HasX sigmaRule inductionRule remain unchanged. -/
namespace CompletionIndependence
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.Intensional.Plus (PolyConvPlus)
mutual
  inductive CtxX (sigmaRule inductionRule : Bool) : Tel → Prop
    | ctxBase : P01AC.ExtensionalRepair.CtxE Γ → CtxX sigmaRule inductionRule Γ
    | nil : CtxX sigmaRule inductionRule []
    | ext : CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule Γ A → CtxX sigmaRule inductionRule (A :: Γ)
  inductive FormX (sigmaRule inductionRule : Bool) : Tel → Ty → Prop
    | formBase : P01AC.ExtensionalRepair.FormE Γ A → FormX sigmaRule inductionRule Γ A
    | param : CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule Γ (.param n)
    | bottom : CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule Γ .bottom
    | all : CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule (twkTel Γ) B → FormX sigmaRule inductionRule Γ (.all B)
    | raw : CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule Γ .raw
    | pi : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule (A :: Γ) B → FormX sigmaRule inductionRule Γ (.pi A B)
    | sigma : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule (A :: Γ) B → FormX sigmaRule inductionRule Γ (.sigma A B)
    | identity : FormX sigmaRule inductionRule Γ A → HasX sigmaRule inductionRule Γ p A → HasX sigmaRule inductionRule Γ q A → FormX sigmaRule inductionRule Γ (.identity A p q)
  inductive HasX (sigmaRule inductionRule : Bool) : Tel → Poly → Ty → Prop
    | hasBase : P01AC.ExtensionalRepair.HasE Γ p A → HasX sigmaRule inductionRule Γ p A
    | var : FormX sigmaRule inductionRule Γ A → Lookup Γ n A → HasX sigmaRule inductionRule Γ (.var n) A
    | i : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule Γ (arr A A) → HasX sigmaRule inductionRule Γ (.atom .i) (arr A A)
    | k : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule Γ B → FormX sigmaRule inductionRule Γ (arr A (arr B A)) →
        HasX sigmaRule inductionRule Γ (.atom .k) (arr A (arr B A))
    | s : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule Γ B → FormX sigmaRule inductionRule Γ C →
        FormX sigmaRule inductionRule Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        HasX sigmaRule inductionRule Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : (τ : List Ty) → finSupport C ≤ τ.length →
        (∀ n, n < τ.length → FormX sigmaRule inductionRule Γ (typeImages τ n)) →
        FormX sigmaRule inductionRule Γ (tsubst (typeImages τ) (fin C)) → FiniteDerives t C →
        HasX sigmaRule inductionRule Γ (.atom t) (tsubst (typeImages τ) (fin C))
    | allIntro : FormX sigmaRule inductionRule Γ (.all B) → HasX sigmaRule inductionRule (twkTel Γ) p B → HasX sigmaRule inductionRule Γ p (.all B)
    | allElim : FormX sigmaRule inductionRule Γ (.all B) → FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule Γ (tinst B A) →
        HasX sigmaRule inductionRule Γ p (.all B) → HasX sigmaRule inductionRule Γ p (tinst B A)
    | rawAtom : FormX sigmaRule inductionRule Γ .raw → HasX sigmaRule inductionRule Γ (.atom t) .raw
    | rawApp : FormX sigmaRule inductionRule Γ .raw → HasX sigmaRule inductionRule Γ f .raw → HasX sigmaRule inductionRule Γ a .raw → HasX sigmaRule inductionRule Γ (.app f a) .raw
    | piIntro : FormX sigmaRule inductionRule Γ (.pi A B) → HasX sigmaRule inductionRule (A :: Γ) b B → Scoped Γ.length (abstract b) →
        HasX sigmaRule inductionRule Γ (abstract b) (.pi A B)
    | piElim : FormX sigmaRule inductionRule Γ (.pi A B) → FormX sigmaRule inductionRule Γ (inst B a) →
        HasX sigmaRule inductionRule Γ f (.pi A B) → HasX sigmaRule inductionRule Γ a A → HasX sigmaRule inductionRule Γ (.app f a) (inst B a)
    | sigmaIntro : FormX sigmaRule inductionRule Γ (.sigma A B) → FormX sigmaRule inductionRule Γ (inst B a) →
        HasX sigmaRule inductionRule Γ a A → HasX sigmaRule inductionRule Γ b (inst B a) → HasX sigmaRule inductionRule Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule Γ (.sigma A B) → HasX sigmaRule inductionRule Γ z (.sigma A B) →
        HasX sigmaRule inductionRule Γ (fstPoly z) A
    | sigmaSnd : FormX sigmaRule inductionRule Γ (.sigma A B) → FormX sigmaRule inductionRule Γ (inst B (fstPoly z)) →
        HasX sigmaRule inductionRule Γ z (.sigma A B) → HasX sigmaRule inductionRule Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : FormX sigmaRule inductionRule Γ (.identity A p q) → HasX sigmaRule inductionRule Γ p A → HasX sigmaRule inductionRule Γ q A →
        PolyConvPlus p q → HasX sigmaRule inductionRule Γ (.atom .i) (.identity A p q)
    | proofErase : FormX sigmaRule inductionRule Γ .raw → FormX sigmaRule inductionRule Γ (.identity A x y) →
        HasX sigmaRule inductionRule Γ p (.identity A x y) → HasX sigmaRule inductionRule Γ p .raw
    | j : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule (theta Γ A x) B →
        FormX sigmaRule inductionRule Γ (.identity A x y) → FormX sigmaRule inductionRule Γ (motiveAt B x (.atom .i)) →
        FormX sigmaRule inductionRule Γ (motiveAt B y e) → HasX sigmaRule inductionRule Γ x A → HasX sigmaRule inductionRule Γ y A →
        HasX sigmaRule inductionRule Γ e (.identity A x y) → HasX sigmaRule inductionRule Γ d (motiveAt B x (.atom .i)) →
        HasX sigmaRule inductionRule Γ (jPoly d y e) (motiveAt B y e)
    | conv : FormX sigmaRule inductionRule Γ A → HasX sigmaRule inductionRule Γ p A → PolyConvPlus p q → Scoped Γ.length q → HasX sigmaRule inductionRule Γ q A
    /-- Exactly §3.1: all explicit formation and scope premises are retained. -/
    | piExt : FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule (A :: Γ) B → FormX sigmaRule inductionRule Γ (.pi A B) →
        HasX sigmaRule inductionRule Γ p (.pi A B) → HasX sigmaRule inductionRule Γ q (.pi A B) →
        FormX sigmaRule inductionRule (A :: Γ) (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0))) →
        FormX sigmaRule inductionRule Γ (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        HasX sigmaRule inductionRule Γ h (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
          (.app (pren Nat.succ q) (.var 0)))) →
        FormX sigmaRule inductionRule Γ (.identity (.pi A B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length A → TyScoped (Γ.length + 1) B →
        HasX sigmaRule inductionRule Γ (.atom .i) (.identity (.pi A B) p q)
    /-- Exactly §3.2: one finite body proof under the type-weakened telescope. -/
    | allExt : FormX sigmaRule inductionRule (twkTel Γ) B → FormX sigmaRule inductionRule Γ (.all B) →
        HasX sigmaRule inductionRule Γ p (.all B) → HasX sigmaRule inductionRule Γ q (.all B) →
        FormX sigmaRule inductionRule (twkTel Γ) (.identity B p q) →
        HasX sigmaRule inductionRule (twkTel Γ) h (.identity B p q) →
        FormX sigmaRule inductionRule Γ (.identity (.all B) p q) →
        Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
        TyScoped Γ.length B → HasX sigmaRule inductionRule Γ (.atom .i) (.identity (.all B) p q)
    /-- All actual recursively formed motives and newly typed inputs are allowed. -/
    | sigmaElim : sigmaRule = true → CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule Γ A → FormX sigmaRule inductionRule (A :: Γ) B →
        FormX sigmaRule inductionRule (.sigma A B :: Γ) P →
        HasX sigmaRule inductionRule (B :: A :: Γ) d (SigmaCompletion.branchType P) → HasX sigmaRule inductionRule Γ z (.sigma A B) →
        HasX sigmaRule inductionRule Γ (SigmaCompletion.branchAt d (fstPoly z) (sndPoly z)) (inst P z)
    /-- Full dependent induction; the witness is the retained uniform polynomial. -/
    | natInduction : inductionRule = true → CtxX sigmaRule inductionRule Γ → FormX sigmaRule inductionRule (P01AC.EffectiveCompleteness.N :: Γ) P →
        HasX sigmaRule inductionRule Γ p (inst P SourceRigidity.zero) → HasX sigmaRule inductionRule Γ s (RigidityInitiality.dependentStepType P) →
        HasX sigmaRule inductionRule Γ (RigidityInitiality.sectionPoly p s) (.pi P01AC.EffectiveCompleteness.N P)
end

end CompletionIndependence
