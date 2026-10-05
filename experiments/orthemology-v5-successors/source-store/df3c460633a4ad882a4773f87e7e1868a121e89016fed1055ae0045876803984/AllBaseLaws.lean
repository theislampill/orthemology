/- Internal induction conclusions. These records are not formation premises. -/
import AllRawRenaming
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

structure RelLaws (R : Term → Term → Prop) : Prop where
  sym : ∀ {a b}, R a b → R b a
  trans : ∀ {a b c}, R a b → R b c → R a c
  raw : ∀ {a b a' b'}, Conv a a' → Conv b b' → R a b → R a' b'

def RelLaws.per {R} (h : RelLaws R) : PER := ⟨R,h.sym,h.trans,h.raw⟩
theorem RelLaws.left {R} (h : RelLaws R) {a b} (v : R a b) : R a a := h.trans v (h.sym v)
theorem RelLaws.right {R} (h : RelLaws R) {a b} (v : R a b) : R b b := h.trans (h.sym v) v

def perLaws (P : PER) : RelLaws P.rel := ⟨P.sym,P.trans,P.raw⟩

structure ContextLaws (Γ : Tel) : Prop where
  refl : ∀ {ρ η}, D Γ ρ η → E Γ ρ η η
  ends : ∀ {ρ η ξ}, E Γ ρ η ξ → D Γ ρ η ∧ D Γ ρ ξ
  sym : ∀ {ρ η ξ}, E Γ ρ η ξ → E Γ ρ ξ η
  trans : ∀ {ρ η ξ ζ}, E Γ ρ η ξ → E Γ ρ ξ ζ → E Γ ρ η ζ
  hends : ∀ {r η ξ}, H Γ r η ξ → D Γ r.left η ∧ D Γ r.right ξ
  hrespect : ∀ {r η η' ξ ξ'}, E Γ r.left η η' → E Γ r.right ξ ξ' →
      H Γ r η ξ → H Γ r η' ξ'
  diagonal : ∀ {ρ η ξ}, H Γ (diagEnv ρ) η ξ ↔ E Γ ρ η ξ

structure TypeLaws (Γ : Tel) (A : Ty) : Prop where
  per : ∀ {ρ η}, D Γ ρ η → RelLaws (F A ρ η)
  transport : ∀ {ρ η ξ}, E Γ ρ η ξ → ∀ t u, F A ρ η t u ↔ F A ρ ξ t u
  ends : ∀ {r η ξ}, D Γ r.left η → D Γ r.right ξ → ∀ {t u},
      G A r η ξ t u → F A r.left η t t ∧ F A r.right ξ u u
  respect : ∀ {r η ξ}, D Γ r.left η → D Γ r.right ξ → ∀ {t t' u u'},
      F A r.left η t t' → F A r.right ξ u u' → G A r η ξ t u → G A r η ξ t' u'
  invariant : ∀ {r η η' ξ ξ'}, E Γ r.left η η' → E Γ r.right ξ ξ' → ∀ t u,
      G A r η ξ t u ↔ G A r η' ξ' t u
  diagonal : ∀ {ρ η ξ}, E Γ ρ η ξ → ∀ t u, G A (diagEnv ρ) η ξ t u ↔ F A ρ η t u

def Fundamental (Γ : Tel) (p : Poly) (A : Ty) : Prop :=
  ∀ (r : REnv) (η ξ : Env), H Γ r η ξ → G A r η ξ (eval p η) (eval p ξ)

theorem TypeLaws.raw {Γ A} (h : TypeLaws Γ A) {r η ξ t t' u u'}
    (hη : D Γ r.left η) (hξ : D Γ r.right ξ) (ct : Conv t t') (cu : Conv u u')
    (v : G A r η ξ t u) : G A r η ξ t' u' := by
  have d := h.ends hη hξ v
  exact h.respect hη hξ ((h.per hη).raw (.refl _) ct d.1)
    ((h.per hξ).raw (.refl _) cu d.2) v

theorem Fundamental.unary {Γ p A} (h : Fundamental Γ p A)
    (hc : ContextLaws Γ) (ha : TypeLaws Γ A) {ρ η ξ} (e : E Γ ρ η ξ) :
    F A ρ η (eval p η) (eval p ξ) :=
  (ha.diagonal e _ _).mp (h (diagEnv ρ) η ξ (hc.diagonal.mpr e))

theorem context_nil : ContextLaws [] where
  refl := fun h => ⟨h,h⟩
  ends := fun h => h
  sym := fun h => ⟨h.2,h.1⟩
  trans := fun h k => ⟨h.1,k.2⟩
  hends := fun h => h
  hrespect := fun h k _ => ⟨h.2,k.2⟩
  diagonal := Iff.rfl

theorem context_ext {Γ A} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) :
    ContextLaws (A :: Γ) where
  refl := fun h => ⟨hc.refl h.1,h.2⟩
  ends := by
    intro ρ η ξ e
    have d := hc.ends e.1
    exact ⟨⟨d.1,(ha.per d.1).left e.2⟩,
      ⟨d.2,(ha.transport e.1 _ _).mp ((ha.per d.1).right e.2)⟩⟩
  sym := by
    intro ρ η ξ e
    exact ⟨hc.sym e.1,(ha.transport e.1 _ _).mp ((ha.per (hc.ends e.1).1).sym e.2)⟩
  trans := by
    intro ρ η ξ ζ e f
    exact ⟨hc.trans e.1 f.1,(ha.per (hc.ends e.1).1).trans e.2 ((ha.transport e.1 _ _).mpr f.2)⟩
  hends := by
    intro r η ξ h
    have d := hc.hends h.1
    have a := ha.ends d.1 d.2 h.2
    exact ⟨⟨d.1,a.1⟩,⟨d.2,a.2⟩⟩
  hrespect := by
    intro r η η' ξ ξ' e f h
    have d := hc.hends h.1
    exact ⟨hc.hrespect e.1 f.1 h.1,
      (ha.invariant e.1 f.1 _ _).mp (ha.respect d.1 d.2 e.2 f.2 h.2)⟩
  diagonal := by
    intro ρ η ξ
    constructor
    · intro h
      have e := hc.diagonal.mp h.1
      exact ⟨e,(ha.diagonal e _ _).mp h.2⟩
    · intro e
      exact ⟨hc.diagonal.mpr e.1,(ha.diagonal e.1 _ _).mpr e.2⟩

theorem type_model (Γ : Tel) (M : Model) (A : Ty)
    (hf : ∀ ρ η t u, F A ρ η t u = (M.obj ρ).rel t u)
    (hg : ∀ r η ξ t u, G A r η ξ t u = M.rel r t u) : TypeLaws Γ A where
  per := by
    intro ρ η _
    have e : F A ρ η = (M.obj ρ).rel := funext fun t => funext fun u => hf ρ η t u
    rw [e]; exact perLaws (M.obj ρ)
  transport := by intros; simp only [hf]
  ends := by intro r η ξ _ _ t u h; simpa only [hf] using M.endpoints r (by simpa only [hg] using h)
  respect := by
    intro r η ξ _ _ t t' u u' ht hu h
    simpa only [hg] using M.respect r (by simpa only [hf] using ht)
      (by simpa only [hf] using hu) (by simpa only [hg] using h)
  invariant := by intros; simp only [hg]
  diagonal := by intro ρ η ξ _ t u; simpa only [hf,hg] using M.identity ρ t u

theorem type_param (Γ : Tel) (n : Nat) : TypeLaws Γ (.param n) :=
  type_model Γ (varModel n) _ (fun _ _ _ _ => rfl) (fun _ _ _ _ _ => rfl)
theorem type_bottom (Γ : Tel) : TypeLaws Γ .bottom :=
  type_model Γ bottomModel _ (fun _ _ _ _ => rfl) (fun _ _ _ _ _ => rfl)
theorem type_raw (Γ : Tel) : TypeLaws Γ .raw where
  per := fun _ => perLaws rawPER
  transport := fun _ _ _ => Iff.rfl
  ends := by intro r η ξ _ _ t u _; exact ⟨.refl _,.refl _⟩
  respect := by intro r η ξ _ _ t t' u u' ht hu h; exact .trans ht.symm (.trans h hu)
  invariant := fun _ _ _ _ => Iff.rfl
  diagonal := fun _ _ _ => Iff.rfl

theorem type_identity {Γ A p q} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hp : Fundamental Γ p A) (hq : Fundamental Γ q A) : TypeLaws Γ (.identity A p q) := by
  have eqv : ∀ {ρ η ξ}, E Γ ρ η ξ →
      (F A ρ η (eval p η) (eval q η) ↔ F A ρ ξ (eval p ξ) (eval q ξ)) := by
    intro ρ η ξ e
    have l := ha.per (hc.ends e).1
    have pp := hp.unary hc ha e
    have qq := hq.unary hc ha e
    constructor
    · intro v
      exact (ha.transport e _ _).mp (l.trans (l.sym pp) (l.trans v qq))
    · intro v
      exact l.trans pp (l.trans ((ha.transport e _ _).mpr v) (l.sym qq))
  exact {
    per := fun _ => {
      sym := fun h => ⟨h.1,h.2.2,h.2.1⟩
      trans := fun h k => ⟨h.1,h.2.1,k.2.2⟩
      raw := fun cp cq h => ⟨h.1,cp.symm.trans h.2.1,cq.symm.trans h.2.2⟩ }
    transport := by intro ρ η ξ e t u; exact and_congr (eqv e) Iff.rfl
    ends := by intro r η ξ _ _ t u h; exact ⟨⟨h.1,h.2.2.1,h.2.2.1⟩,⟨h.2.1,h.2.2.2,h.2.2.2⟩⟩
    respect := by intro r η ξ _ _ t t' u u' ht hu h; exact ⟨h.1,h.2.1,ht.2.2,hu.2.2⟩
    invariant := by intro r η η' ξ ξ' e f t u; exact and_congr (eqv e) (and_congr (eqv f) Iff.rfl)
    diagonal := by
      intro ρ η ξ e t u
      constructor
      · intro h; exact ⟨h.1,h.2.2⟩
      · intro h; exact ⟨h.1,(eqv e).mp h.1,h.2⟩ }

end P01AC
