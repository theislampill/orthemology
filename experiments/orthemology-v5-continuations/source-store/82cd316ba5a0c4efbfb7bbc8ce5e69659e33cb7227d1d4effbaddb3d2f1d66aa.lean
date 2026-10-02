/- Syntax-directed first-order dependent typing. Every term is a finite SKI
   polynomial; there is no constructor taking a semantic validity theorem. -/
import P01DependentSubstitution
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Explicit open raw conversion. Bracket abstraction congruence is
    intentionally absent: canonical Conv does not validate that rule. -/
inductive PolyConv : Poly → Poly → Prop
  | refl (p) : PolyConv p p
  | symm : PolyConv p q → PolyConv q p
  | trans : PolyConv p q → PolyConv q r → PolyConv p r
  | app : PolyConv f g → PolyConv p q → PolyConv (.app f p) (.app g q)
  | i (p) : PolyConv (.app (.atom .i) p) p
  | k (p q) : PolyConv (.app (.app (.atom .k) p) q) p
  | s (p q r) : PolyConv (.app (.app (.app (.atom .s) p) q) r)
      (.app (.app p r) (.app q r))

theorem polyConv_sound {p q : Poly} (h : PolyConv p q) (η : Env) :
    Conv (eval p η) (eval q η) := by
  induction h with
  | refl => exact .refl _
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | app h k ih ik => exact conv_app ih ik
  | i p => exact .step (.i _)
  | k p q => exact .step (.k _ _)
  | s p q r => exact .step (.s _ _ _)

def motiveAt (B : Ty) (y p : Poly) : Ty := substIndex (cons p (cons y Poly.var)) B

theorem interpret_motiveAt (B : Ty) (y p : Poly) (η : Env) :
    (interpret (motiveAt B y p)).run η =
      (interpret B).run (cons (eval p η) (cons (eval y η) η)) := by
  rw [motiveAt,interpret_index_substitution]
  congr 1
  funext n; cases n with
  | zero => rfl
  | succ n => cases n <;> rfl

inductive Has : Poly → Ty → Prop
  | raw (p) : Has p .raw
  | finite {t A} : FiniteDerives t A → Has (.atom t) (embedFinite A)
  | i (A) : Has (.atom .i) (.arrow A A)
  | k (A B) : Has (.atom .k) (.arrow A (.arrow B A))
  | s (A B C) : Has (.atom .s)
      (.arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C)))
  | allIntro : Has p B → Has p (.all B)
  | allElim : Has p (.all B) → Has p (instantiateType B A)
  | app : Has f (.arrow A B) → Has a A → Has (.app f a) B
  | piIntro : Has b B → Has (abstract b) (.pi B)
  | piElim : Has f (.pi B) → Has (.app f a) (instantiate B a)
  | sigmaIntro : Has b (instantiate B a) → Has (pairPoly a b) (.sigma B)
  | sigmaSnd : Has z (.sigma B) → Has (sndPoly z) (instantiate B (fstPoly z))
  | identityIntro : PolyConv p q → Has (.atom .i) (.identity p q)
  | j : Has p (.identity x y) → Has d (motiveAt B x (.atom .i)) →
      Has (jPoly d y p) (motiveAt B y p)
  | conv : Has p A → PolyConv p q → Has q A

/-- The fundamental theorem is proved by induction on the finite typing
    derivation. Index environments vary by raw Conv, and type-parameter links
    vary arbitrarily and heterogeneously. -/
theorem fundamental {p : Poly} {A : Ty} (h : Has p A) :
    ∀ (r : REnv) (η ξ : Env), IndexRelated η ξ →
      ((interpret A).run η).rel r (eval p η) (eval p ξ) := by
  induction h with
  | raw p => intro r η ξ hη; exact eval_index_related p hη
  | @finite t A h =>
      intro r η ξ hη
      rw [interpret_embedFinite]
      exact finite_fundamental h r
  | i A => intro r η ξ hη; exact identity_link (((interpret A).run η).asLink r)
  | k A B =>
      intro r η ξ hη
      exact k_link
        (((interpret A).run η).asLink r) (((interpret B).run η).asLink r)
  | s A B C =>
      intro r η ξ hη
      exact s_link
        (((interpret A).run η).asLink r) (((interpret B).run η).asLink r)
        (((interpret C).run η).asLink r)
  | @allIntro p B hp ih =>
      intro r η ξ hη
      refine ⟨?_,?_,?_⟩
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.left)) η η (index_refl η)
      · apply (all_domain _ _).mpr
        intro P Q R
        have hr := ih (extendEnv R (diagEnv r.right)) ξ ξ (index_refl ξ)
        rw [← interpret_index_transport B hη] at hr
        exact hr
      · intro P Q R
        exact ih (extendEnv R r) η ξ hη
  | @allElim p B A hp ih =>
      intro r η ξ hη
      apply (type_instantiate_rel B A η r _ _).mpr
      exact (ih r η ξ hη).2.2 (((interpret A).run η).obj r.left)
        (((interpret A).run η).obj r.right) (((interpret A).run η).asLink r)
  | app hf ha ihf iha =>
      intro r η ξ hη
      exact (ihf r η ξ hη).2.2 _ _ (iha r η ξ hη)
  | @piIntro b B hb ih =>
      intro r η ξ hη
      refine ⟨?_,?_,?_⟩
      · intro x y hxy
        have hb := ih (diagEnv r.left) (cons x η) (cons y η) (index_cons (index_refl η) hxy)
        have hd := (((interpret B).run (cons x η)).identity r.left _ _).mp hb
        exact (((interpret B).run (cons x η)).obj r.left).raw
          (P01Source.red_conv (abstraction_beta b η x)).symm
          (P01Source.red_conv (abstraction_beta b η y)).symm hd
      · intro x y hxy
        have hb := ih (diagEnv r.right) (cons x ξ) (cons y ξ) (index_cons (index_refl ξ) hxy)
        have hd := (((interpret B).run (cons x ξ)).identity r.right _ _).mp hb
        have he := interpret_index_transport B (index_cons hη (Conv.refl x))
        rw [← he] at hd
        exact (((interpret B).run (cons x η)).obj r.right).raw
          (P01Source.red_conv (abstraction_beta b ξ x)).symm
          (P01Source.red_conv (abstraction_beta b ξ y)).symm hd
      · intro x y hxy
        have hb := ih r (cons x η) (cons y ξ) (index_cons hη hxy)
        exact (((interpret B).run (cons x η)).asLink r).raw
          (P01Source.red_conv (abstraction_beta b η x)).symm
          (P01Source.red_conv (abstraction_beta b ξ y)).symm hb
  | @piElim f B a hf ih =>
      intro r η ξ hη
      rw [interpret_instantiate]
      exact (ih r η ξ hη).2.2 _ _ (eval_index_related a hη)
  | @sigmaIntro b B a hb ih =>
      intro r η ξ hη
      have hd := ih r η ξ hη
      rw [interpret_instantiate] at hd
      have ha := eval_index_related a hη
      change Represented (pairTerm (eval a η) (eval b η)) ∧
        Represented (pairTerm (eval a ξ) (eval b ξ)) ∧ _
      refine ⟨pair_represented _ _,pair_represented _ _,
        (pair_first _ _).trans (ha.trans (pair_first _ _).symm),?_⟩
      have he := interpret_index_transport B
        (index_cons (index_refl η) (pair_first (eval a η) (eval b η)))
      change ((interpret B).run (cons (firstTerm (pairTerm (eval a η) (eval b η))) η)).rel r _ _
      rw [he]
      exact (((interpret B).run (cons (eval a η) η)).asLink r).raw
        (pair_second _ _).symm (pair_second _ _).symm hd
  | @sigmaSnd z B hz ih =>
      intro r η ξ hη
      rw [interpret_instantiate]
      exact (ih r η ξ hη).2.2.2
  | @identityIntro p q hp =>
      intro r η ξ hη
      exact ⟨polyConv_sound hp η,.refl _,.refl _⟩
  | @j p x y d B hp hd ihp ihd =>
      intro r η ξ hη
      have hbase := ihd r η ξ hη
      rw [interpret_motiveAt] at hbase
      simp only [eval] at hbase
      rw [interpret_motiveAt]
      have heq := ihp r η ξ hη
      have hm := interpret_index_transport B
        (index_cons (index_cons (index_refl η) heq.1) heq.2.1.symm)
      rw [hm] at hbase
      exact (((interpret B).run (cons (eval p η) (cons (eval y η) η))).asLink r).raw
        (P01Source.red_conv (eval_j d y p η)).symm
        (P01Source.red_conv (eval_j d y p ξ)).symm hbase
  | @conv p A q hp hpq ih =>
      intro r η ξ hη
      exact (((interpret A).run η).asLink r).raw
        (polyConv_sound hpq η) (polyConv_sound hpq ξ) (ih r η ξ hη)

theorem unary_soundness {p A} (h : Has p A) (ρ : OEnv) (η : Env) :
    (((interpret A).run η).obj ρ).dom (eval p η) :=
  (((interpret A).run η).identity ρ _ _).mp (fundamental h (diagEnv ρ) η η (index_refl η))

theorem substitution_fundamental {p A} (h : Has p A) (σ : Nat → Poly)
    (r : REnv) (η ξ : Env) (hη : IndexRelated η ξ) :
    ((interpret (substIndex σ A)).run η).rel r
      (eval (psub σ p) η) (eval (psub σ p) ξ) := by
  rw [interpret_index_substitution,eval_sub,eval_sub]
  exact fundamental h r (subIndexEnv σ η) (subIndexEnv σ ξ)
    (fun n => eval_index_related (σ n) hη)

theorem type_substitution_fundamental {p A} (h : Has p A) (σ : Nat → Ty)
    (r : REnv) (η ξ : Env) (hη : IndexRelated η ξ) :
    ((interpret (substType σ A)).run η).rel r (eval p η) (eval p ξ) := by
  rw [interpret_type_substitution]
  exact fundamental h (r.substitute (fun n => (interpret (σ n)).run η)) η ξ hη

theorem dependent_all_fundamental {p B} (h : Has p B)
    (r : REnv) (η ξ : Env) (hη : IndexRelated η ξ) :
    ((interpret (.all B)).run η).rel r (eval p η) (eval p ξ) :=
  fundamental (.allIntro h) r η ξ hη

/-- The argument may itself contain Pi/Sigma/Id/All. The substitution is the
    actual two-sort operation, not an ambient decoding/reification postulate. -/
theorem dependent_all_self_instantiation {p B} (h : Has p (.all B)) :
    Has p (instantiateType B (.all B)) := .allElim h

end P01DF
