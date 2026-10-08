/- Conditional semantic mixed substitution. Lawful source environments are frozen
   at base valuations; no law of the raw target type is assumed. -/
import AllRawRenaming
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Exact image interpretation, including the two necessary diagonal clauses.
    This is a metatheorem hypothesis, never a formation or typing premise. -/
structure ImageMatch (τ : Nat → Ty) (r : REnv) (η ξ : Env) (s : REnv) : Prop where
  left : ∀ n t u, F (τ n) r.left η t u = (s.left n).rel t u
  right : ∀ n t u, F (τ n) r.right ξ t u = (s.right n).rel t u
  cross : ∀ n t u, G (τ n) r η ξ t u = s.rel n t u
  diagLeft : ∀ n t u, G (τ n) (diagEnv r.left) η η t u = (s.left n).rel t u
  diagRight : ∀ n t u, G (τ n) (diagEnv r.right) ξ ξ t u = (s.right n).rel t u

theorem ImageMatch.diagonalLeft {τ r η ξ s} (h : ImageMatch τ r η ξ s) :
    ImageMatch τ (diagEnv r.left) η η (diagEnv s.left) :=
  ⟨h.left,h.left,h.diagLeft,h.diagLeft,h.diagLeft⟩

theorem ImageMatch.diagonalRight {τ r η ξ s} (h : ImageMatch τ r η ξ s) :
    ImageMatch τ (diagEnv r.right) ξ ξ (diagEnv s.right) :=
  ⟨h.right,h.right,h.diagRight,h.diagRight,h.diagRight⟩

theorem ImageMatch.termLift {τ r η ξ s} (h : ImageMatch τ r η ξ s) (a b : Term) :
    ImageMatch (fun n => wk (τ n)) r (cons a η) (cons b ξ) s where
  left := by intro n t u; rw [F_wk]; exact h.left n t u
  right := by intro n t u; rw [F_wk]; exact h.right n t u
  cross := by intro n t u; rw [G_wk]; exact h.cross n t u
  diagLeft := by intro n t u; rw [G_wk]; exact h.diagLeft n t u
  diagRight := by intro n t u; rw [G_wk]; exact h.diagRight n t u

theorem ImageMatch.typeLift {τ r η ξ s} (h : ImageMatch τ r η ξ s)
    {P Q : PER} (R : Link P Q) : ImageMatch (tup τ) (extendEnv R r) η ξ (extendEnv R s) where
  left := by intro n t u; cases n with
    | zero => rfl
    | succ n => exact (F_twk (τ n) P r.left η t u).trans (h.left n t u)
  right := by intro n t u; cases n with
    | zero => rfl
    | succ n => exact (F_twk (τ n) Q r.right ξ t u).trans (h.right n t u)
  cross := by intro n t u; cases n with
    | zero => rfl
    | succ n => exact (G_twk (τ n) R r η ξ t u).trans (h.cross n t u)
  diagLeft := by
    intro n t u; cases n with
    | zero => rfl
    | succ n =>
        change G (twk (τ n)) (diagEnv (cons P r.left)) η η t u = _
        rw [← extend_diag, G_twk]; exact h.diagLeft n t u
  diagRight := by
    intro n t u; cases n with
    | zero => rfl
    | succ n =>
        change G (twk (τ n)) (diagEnv (cons Q r.right)) ξ ξ t u = _
        rw [← extend_diag, G_twk]; exact h.diagRight n t u

abbrev EvalImages (σ : Nat → Poly) (η : Env) : Env := fun n => eval (σ n) η

theorem evalImages_pup (σ : Nat → Poly) (η : Env) (a : Term) :
    EvalImages (pup σ) (cons a η) = cons a (EvalImages σ η) := eval_pup_env σ η a

/-- Paired structural induction; replacement images stay frozen through both binders. -/
theorem FG_mixed (A : Ty) : ∀ σ τ r η ξ s, ImageMatch τ r η ξ s →
    (∀ t u, F (mixed σ τ A) r.left η t u = F A s.left (EvalImages σ η) t u) ∧
    (∀ t u, F (mixed σ τ A) r.right ξ t u = F A s.right (EvalImages σ ξ) t u) ∧
    (∀ t u, G (mixed σ τ A) r η ξ t u = G A s (EvalImages σ η) (EvalImages σ ξ) t u) := by
  induction A with
  | param n => intro σ τ r η ξ s h; exact ⟨h.left n,h.right n,h.cross n⟩
  | bottom => intros; exact ⟨fun _ _ => rfl,fun _ _ => rfl,fun _ _ => rfl⟩
  | raw => intros; exact ⟨fun _ _ => rfl,fun _ _ => rfl,fun _ _ => rfl⟩
  | identity A p q ih =>
      intro σ τ r η ξ s h
      have a := ih σ τ r η ξ s h
      constructor
      · intros; simp only [mixed,F_identity,a.1,eval_sub,EvalImages]
      constructor
      · intros; simp only [mixed,F_identity,a.2.1,eval_sub,EvalImages]
      · intros; simp only [mixed,G_identity,a.1,a.2.1,eval_sub,EvalImages]
  | pi A B ha hb =>
      intro σ τ r η ξ s h
      have a := ha σ τ r η ξ s h
      have bl := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).1
      have br := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).2.1
      have bg := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).2.2
      have fl : ∀ t u, F (mixed σ τ (.pi A B)) r.left η t u = F (.pi A B) s.left (EvalImages σ η) t u := by
        intros; simp only [mixed,F_pi,a.1,bl _ (.i),evalImages_pup]
      have fr : ∀ t u, F (mixed σ τ (.pi A B)) r.right ξ t u = F (.pi A B) s.right (EvalImages σ ξ) t u := by
        intros; simp only [mixed,F_pi,a.2.1,br (.i),evalImages_pup]
      refine ⟨fl,fr,?_⟩
      intro t u
      simp only [mixed,G_pi,F_pi,a.1,a.2.1,a.2.2,bl _ (.i),br (.i),bg,evalImages_pup]

  | sigma A B ha hb =>
      intro σ τ r η ξ s h
      have a := ha σ τ r η ξ s h
      have bl := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).1
      have br := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).2.1
      have bg := fun x y => (hb (pup σ) _ r (cons x η) (cons y ξ) s (h.termLift x y)).2.2
      have fl : ∀ t u, F (mixed σ τ (.sigma A B)) r.left η t u = F (.sigma A B) s.left (EvalImages σ η) t u := by
        intros; simp only [mixed,F_sigma,a.1,bl _ (.i),evalImages_pup]
      have fr : ∀ t u, F (mixed σ τ (.sigma A B)) r.right ξ t u = F (.sigma A B) s.right (EvalImages σ ξ) t u := by
        intros; simp only [mixed,F_sigma,a.2.1,br (.i),evalImages_pup]
      refine ⟨fl,fr,?_⟩
      intro t u
      simp only [mixed,G_sigma,F_sigma,a.1,a.2.1,a.2.2,bl _ (.i),br (.i),bg,evalImages_pup]

  | all B ih =>
      intro σ τ r η ξ s h
      have fl : ∀ t u, F (mixed σ τ (.all B)) r.left η t u = F (.all B) s.left (EvalImages σ η) t u := by
        intro t u
        have un := fun P Q (R : Link P Q) => (ih σ (tup τ) _ η η _ (h.diagonalLeft.typeLift R)).2.2
        have ob : ∀ P t u, F (mixed σ (tup τ) B) (cons P r.left) η t u = F B (cons P s.left) (EvalImages σ η) t u := fun P => (ih σ (tup τ) _ η η _ (h.diagonalLeft.typeLift (diagonal P))).1
        simp only [mixed,F_all,un,ob]
      have fr : ∀ t u, F (mixed σ τ (.all B)) r.right ξ t u = F (.all B) s.right (EvalImages σ ξ) t u := by
        intro t u
        have un := fun P Q (R : Link P Q) => (ih σ (tup τ) _ ξ ξ _ (h.diagonalRight.typeLift R)).2.2
        have ob : ∀ P t u, F (mixed σ (tup τ) B) (cons P r.right) ξ t u = F B (cons P s.right) (EvalImages σ ξ) t u := fun P => (ih σ (tup τ) _ ξ ξ _ (h.diagonalRight.typeLift (diagonal P))).1
        simp only [mixed,F_all,un,ob]
      refine ⟨fl,fr,?_⟩
      intro t u
      have cr := fun P Q (R : Link P Q) => (ih σ (tup τ) _ η ξ _ (h.typeLift R)).2.2
      rw [mixed,G_all,G_all]
      change (F (mixed σ τ (.all B)) r.left η t t ∧ F (mixed σ τ (.all B)) r.right ξ u u ∧
        ∀ (P Q : PER) (R : Link P Q), G (mixed σ (tup τ) B) (extendEnv R r) η ξ t u) = _
      simp only [fl,fr,cr]

end P01AC
