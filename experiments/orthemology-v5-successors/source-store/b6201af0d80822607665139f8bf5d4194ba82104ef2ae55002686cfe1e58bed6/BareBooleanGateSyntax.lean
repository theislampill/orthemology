/- Isolated research probe. No modification of the accepted packages. -/
import EffectivePrimitiveRecursion
namespace P01AC.BareBooleanGateSyntax
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive

/-- A polynomial whose only atoms are the three primitive combinators. -/
def Pure : Poly → Prop
  | .var _ => True
  | .atom t => t = .i ∨ t = .k ∨ t = .s
  | .app f a => Pure f ∧ Pure a

theorem pure_psub {p : Poly} (hp : Pure p) (σ : Nat → Poly)
    (hσ : ∀ i, Pure (σ i)) : Pure (psub σ p) := by
  induction p with
  | var i => exact hσ i
  | atom t => exact hp
  | app f a hf ha => exact ⟨hf hp.1, ha hp.2⟩

theorem pure_pren {p : Poly} (hp : Pure p) (r : Nat → Nat) : Pure (pren r p) :=
  pure_psub hp _ (fun _ => trivial)

theorem pure_abstract {p : Poly} (hp : Pure p) : Pure (abstract p) := by
  induction p with
  | var i =>
      cases i <;> simp [abstract, freeZero, Pure, drop, pren, psub]
  | atom t =>
      simpa [abstract, freeZero, Pure, drop, pren, psub] using hp
  | app f a hf ha =>
      by_cases h : freeZero (.app f a) = true
      · rw [abstract_present_app _ _ h]
        exact ⟨⟨Or.inr (Or.inr rfl), hf hp.1⟩, ha hp.2⟩
      · have hn : freeZero (.app f a) = false := Bool.eq_false_iff.mpr h
        rw [abstract_absent _ hn]
        exact ⟨Or.inr (Or.inl rfl), pure_pren hp Nat.pred⟩

theorem pure_scoped_psub {p : Poly} {k : Nat} (hp : Pure p) (hs : Scoped k p)
    (σ : Nat → Poly) (hσ : ∀ i, i < k → Pure (σ i)) : Pure (psub σ p) := by
  induction p with
  | var i => exact hσ i hs
  | atom t => exact hp
  | app f a hf ha => exact ⟨hf hp.1 hs.1, ha hp.2 hs.2⟩

theorem pure_inputNumeral (n : Nat) : Pure (inputNumeral n) := by
  apply pure_abstract
  apply pure_abstract
  induction n with
  | zero => trivial
  | succ n ih => exact ⟨trivial, ih⟩

theorem pure_succPoly : Pure succPoly :=
  pure_abstract (pure_abstract (pure_abstract ⟨trivial, ⟨⟨trivial, trivial⟩, trivial⟩⟩))

theorem pure_pair {p q : Poly} (hp : Pure p) (hq : Pure q) : Pure (pairPoly p q) := by
  exact ⟨⟨Or.inr (Or.inr rfl), ⟨⟨Or.inr (Or.inr rfl), Or.inl rfl⟩,
    ⟨Or.inr (Or.inl rfl), hp⟩⟩⟩, ⟨Or.inr (Or.inl rfl), hq⟩⟩

theorem pure_fst {p : Poly} (hp : Pure p) : Pure (fstPoly p) :=
  ⟨hp, Or.inr (Or.inl rfl)⟩
theorem pure_snd {p : Poly} (hp : Pure p) : Pure (sndPoly p) :=
  ⟨hp, ⟨Or.inr (Or.inl rfl), Or.inl rfl⟩⟩

theorem pure_recImages (i : Nat) : Pure (recImages i) := by
  cases i with
  | zero => exact pure_fst trivial
  | succ i =>
    cases i with
    | zero => exact pure_snd trivial
    | succ i => trivial

theorem pure_recPoly {g h : Poly} (hg : Pure g) (hh : Pure h) : Pure (recPoly g h) := by
  apply pure_snd
  exact ⟨⟨trivial, pure_abstract (pure_pair ⟨pure_succPoly, pure_fst trivial⟩
    (pure_psub hh recImages pure_recImages))⟩,
    pure_pair (pure_inputNumeral 0) (pure_pren hg Nat.succ)⟩

theorem compile_pure {r : Nat} (f : PR r) : Pure f.compile := by
  induction f with
  | zero r => exact pure_inputNumeral 0
  | succ => exact ⟨pure_succPoly, trivial⟩
  | proj i => trivial
  | @comp r k f gs ihf ihgs =>
    apply pure_scoped_psub ihf
      (show Scoped k f.compile by simpa [NatCtx] using has_scoped f.compile_has)
    intro i hi
    simpa only [dif_pos hi] using ihgs ⟨i,hi⟩
  | prec g h ihg ihh => exact pure_recPoly ihg ihh

theorem choice_pure (b : Bool) : Pure (choicePoly b) :=
  pure_abstract (pure_abstract trivial)

theorem discriminator_pure : Pure zeroDiscriminator :=
  pure_abstract ⟨⟨trivial, ⟨Or.inr (Or.inl rfl), choice_pure true⟩⟩, choice_pure false⟩

theorem simFamily_pure (f : PR 2) (e : Nat) : Pure (simFamily f e) :=
  ⟨pure_abstract (pure_abstract ⟨discriminator_pure, compile_pure f⟩), pure_inputNumeral e⟩

/-- Closing a pure polynomial introduces no observation marker from zeroEnv. -/
theorem pure_closed_markerFree {p : Poly} (hp : Pure p) (hs : Scoped 0 p) (η : Env) :
    MarkerFree (eval p η) := by
  induction p with
  | var i => exact False.elim (Nat.not_lt_zero i hs)
  | atom t =>
    rcases hp with h | h | h <;> subst t <;> trivial
  | app f a hf ha => exact ⟨hf hp.1 hs.1, ha hp.2 hs.2⟩

/-- Raw application structure is exposed; compound raw atoms are not retained. -/
def expose : Term → Poly
  | .app f a => .app (expose f) (expose a)
  | t => .atom t

theorem expose_step {t u : Term} (h : Step t u) : P01DF.PolyConv (expose t) (expose u) := by
  induction h with
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _
  | left h x ih => exact .app ih (.refl _)
  | right f h ih => exact .app (.refl _) ih

theorem expose_conv {t u : Term} (h : Conv t u) : P01DF.PolyConv (expose t) (expose u) := by
  induction h with
  | refl => exact .refl _
  | step h => exact expose_step h
  | symm h ih => exact .symm ih
  | trans h k ih hk => exact .trans ih hk

theorem expose_eval_pure {p : Poly} (hp : Pure p) (hs : Scoped 0 p) (η : Env) :
    expose (eval p η) = p := by
  induction p with
  | var i => exact False.elim (Nat.not_lt_zero i hs)
  | atom t =>
    rcases hp with h | h | h <;> subst t <;> rfl
  | app f a hf ha => exact congrArg₂ Poly.app (hf hp.1 hs.1) (ha hp.2 hs.2)

/-- For this pure closed fragment, raw conversion really does lift to the
    unchanged PolyConv. No arbitrary-atom conversion rule is introduced. -/
theorem pure_closed_conversion {p q : Poly}
    (hp : Pure p) (hq : Pure q) (sp : Scoped 0 p) (sq : Scoped 0 q)
    (h : Conv (eval p zeroEnv) (eval q zeroEnv)) : P01DF.PolyConv p q := by
  have hc := expose_conv h
  simpa only [expose_eval_pure hp sp, expose_eval_pure hq sq] using hc

#print axioms pure_closed_markerFree
#print axioms compile_pure
#print axioms simFamily_pure
#print axioms pure_closed_conversion
end P01AC.BareBooleanGateSyntax
