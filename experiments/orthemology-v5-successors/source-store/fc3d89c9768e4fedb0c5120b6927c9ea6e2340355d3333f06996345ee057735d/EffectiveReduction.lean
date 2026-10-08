/- Semantic reduction for the unchanged F/G model. The representation equations
   are explicit hypotheses; no representability or computability axiom is added. -/
import EffectiveObserver

namespace P01AC.EffectiveCompleteness
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- The configuration numeral convention of the imported representation premise. -/
def numericB : Term := .app (.app .s (.app .k .s)) .k

def numeral : Nat → Term
  | 0 => .app .k .i
  | n+1 => .app (.app .s numericB) (numeral n)

theorem numericB_normal : P01Source.Normal numericB := by
  intro u h
  cases h with
  | left h _ =>
    cases h with
    | left h _ => cases h
    | right _ h =>
      cases h with
      | left h _ => cases h
      | right _ h => cases h
  | right _ h => cases h

theorem numeral_normal (n : Nat) : P01Source.Normal (numeral n) := by
  induction n with
  | zero =>
    intro u h
    cases h with
    | left h _ => cases h
    | right _ h => cases h
  | succ n ih =>
    intro u h
    cases h with
    | left h _ =>
      cases h with
      | left h _ => cases h
      | right _ h => exact numericB_normal _ h
    | right _ h => exact ih _ h

theorem numeral_injective {m n : Nat} (h : numeral m = numeral n) : m = n := by
  induction m generalizing n with
  | zero => cases n with
    | zero => rfl
    | succ n => cases h
  | succ m ih => cases n with
    | zero => cases h
    | succ n => exact congrArg Nat.succ (ih (Term.app.inj h).2)

theorem numeral_conversion_iff (m n : Nat) : Conv (numeral m) (numeral n) ↔ m = n := by
  constructor
  · intro h
    exact numeral_injective (P01Source.normal_unique (numeral_normal m) (numeral_normal n) h)
  · intro h
    exact h ▸ Conv.refl (numeral m)

theorem numeric_outputs_separate : ¬ Conv (numeral 0) (numeral 1) := by
  intro h
  exact Nat.zero_ne_one ((numeral_conversion_iff 0 1).mp h)

/-- This is supplied mathematical evidence, not a new object-language rule. -/
def Represents (h : Nat → Nat) (program : Term) : Prop :=
  ∀ k, Conv (.app program (numeral k)) (numeral (h k))

def run (g : Nat → Nat) (c : Nat) : Nat → Nat
  | 0 => c
  | n+1 => g (run g c n)

theorem iteration_representation {g : Nat → Nat} {program : Term}
    (hg : Represents g program) (c n : Nat) :
    Conv (iterateTerm (stepTerm program) n (numeral c)) (numeral (run g c n)) := by
  induction n with
  | zero => exact .refl _
  | succ n ih =>
    exact (Conv.right (stepTerm program) ih).trans
      ((rawStep_application program (numeral (run g c n))).trans (hg (run g c n)))

theorem observation_representation {g o : Nat → Nat} {G O : Term}
    (hg : Represents g G) (ho : Represents o O) (c n : Nat) :
    Conv (.app O (iterateTerm (stepTerm G) n (numeral c)))
      (numeral (o (run g c n))) :=
  (Conv.right O (iteration_representation hg c n)).trans (ho (run g c n))

/-- Unary validity at the exact fixed carrier, with the actual empty valuation. -/
def EndpointValid (p q : Poly) : Prop :=
  ∀ ρ : OEnv, F C ρ zeroEnv (eval p zeroEnv) (eval q zeroEnv)

/-- Original all-relation-environment identity validity, at the literal proof I. -/
def IdentityValid (p q : Poly) : Prop :=
  ∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv .i .i

theorem identity_valid_iff_endpoint_valid (p q : Poly) :
    IdentityValid p q ↔ EndpointValid p q := by
  constructor
  · intro h ρ
    exact (h (diagEnv ρ)).1
  · intro h r
    exact ⟨h r.left, h r.right, Conv.refl _, Conv.refl _⟩

theorem identity_unary_iff_endpoint_valid (p q : Poly) :
    (∀ ρ : OEnv, F (.identity C p q) ρ zeroEnv .i .i) ↔ EndpointValid p q := by
  constructor
  · intro h ρ
    exact (h ρ).1
  · intro h ρ
    exact ⟨h ρ, Conv.refl _, Conv.refl _⟩

theorem canonical_observation (G O c : Term) (n : Nat) :
    Conv (.app (eval (tester G O c) zeroEnv) (eval (inputNumeral n) zeroEnv))
      (.app O (iterateTerm (stepTerm G) n c)) :=
  (tester_application G O c _).trans
    (Conv.right O (inputNumeral_applied n (stepTerm G) c zeroEnv))

/-- All arbitrary semantic inputs are covered, not just compiled test numerals. -/
theorem endpoint_valid_iff_observations (G O c z : Term) :
    EndpointValid (tester G O c) (constantRaw z) ↔
      ∀ n, Conv (.app O (iterateTerm (stepTerm G) n c)) z := by
  constructor
  · intro h n
    let ρ : OEnv := fun _ => rawPER
    have hn : F N ρ zeroEnv (eval (inputNumeral n) zeroEnv)
        (eval (inputNumeral n) zeroEnv) :=
      unary_fundamental (inputNumeral_has n) ⟨rfl, rfl⟩
    have hρ := h ρ
    rw [C, F_arr] at hρ
    have hc := hρ _ _ hn
    exact (canonical_observation G O c n).symm.trans
      (hc.trans (constantRaw_application z _))
  · intro h ρ
    rw [C, F_arr]
    intro x y hxy
    have hx : F N ρ zeroEnv x x :=
      ((form_sound (N_form Ctx.nil)).2.laws.per (ρ := ρ) rfl).left hxy
    obtain ⟨n, hn⟩ := semantic_church_standardness hx
    exact (tester_application G O c x).trans
      ((Conv.right O (hn (stepTerm G) c)).trans
        ((h n).trans (constantRaw_application z y).symm))

/-- Complete semantic reduction, conditional only on the displayed raw
    representation equations. No computability theorem is asserted here. -/
theorem original_identity_iff_run_zero {g o : Nat → Nat} {G O : Term}
    (hg : Represents g G) (ho : Represents o O) (c : Nat) :
    IdentityValid (tester G O (numeral c)) (constantRaw (numeral 0)) ↔
      ∀ n, o (run g c n) = 0 := by
  rw [identity_valid_iff_endpoint_valid, endpoint_valid_iff_observations]
  constructor
  · intro h n
    exact (numeral_conversion_iff _ 0).mp
      ((observation_representation hg ho c n).symm.trans (h n))
  · intro h n
    exact (h n) ▸ observation_representation hg ho c n

theorem target_formed (G O : Term) (c : Nat) :
    Form [] (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) :=
  .identity (C_form .nil) (tester_has G O (numeral c)) (constantRaw_has (numeral 0))

theorem target_closed (G O : Term) (c : Nat) :
    Scoped 0 (tester G O (numeral c)) ∧ Scoped 0 (constantRaw (numeral 0)) :=
  ⟨has_scoped (tester_has G O (numeral c)), has_scoped (constantRaw_has (numeral 0))⟩

/-- Explicitly typed constants give infinitely many distinct F-classes in C. -/
theorem typed_constant_family_distinct (m n : Nat)
    (h : EndpointValid (constantRaw (iterateTerm .zero m .one))
      (constantRaw (iterateTerm .zero n .one))) : m = n := by
  let ρ : OEnv := fun _ => rawPER
  have hz : F N ρ zeroEnv (eval (inputNumeral 0) zeroEnv)
      (eval (inputNumeral 0) zeroEnv) :=
    unary_fundamental (inputNumeral_has 0) ⟨rfl, rfl⟩
  have hc := h ρ
  rw [C, F_arr] at hc
  have hr := hc _ _ hz
  exact marker_conv_injective
    ((constantRaw_application _ _).symm.trans (hr.trans (constantRaw_application _ _)))

end P01AC.EffectiveCompleteness
