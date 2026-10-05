/- Universal certificate substitution in the existing P01DF.Has judgement. -/
import SubstitutionSyntax

namespace P01DF.Syntactic
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

 theorem conversion_substitution {p q : Poly} (h : PolyConv p q) (σ : Nat → Poly) :
    PolyConv (psub σ p) (psub σ q) := by
  induction h with
  | refl p => exact .refl _
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik
  | app h k ih ik => exact .app ih ik
  | i p => exact .i _
  | k p q => exact .k _ _
  | s p q r => exact .s _ _ _

/-- All fifteen constructors are reconstructed at the unchanged judgement.
    Neither a typed-context premise nor semantic equality is used. -/
 theorem has_index_substitution {p : Poly} {A : Ty} (h : Has p A) (σ : Nat → Poly) :
    Has (psub σ p) (substIndex σ A) := by
  induction h generalizing σ with
  | raw p => exact .raw _
  | @finite t A h =>
      rw [index_embedFinite]
      exact .finite h
  | i A => exact .i _
  | k A B => exact .k _ _
  | s A B C => exact .s _ _ _
  | allIntro h ih => exact .allIntro (ih σ)
  | @allElim p B A h ih =>
      rw [index_instantiateType]
      exact .allElim (ih σ)
  | app hf ha ihf iha => exact .app (ihf σ) (iha σ)
  | @piIntro b B h ih =>
      rw [← abstraction_naturality]
      exact .piIntro (ih (pup σ))
  | @piElim f B a h ih =>
      rw [index_instantiate]
      exact .piElim (ih σ)
  | @sigmaIntro b B a h ih =>
      rw [polynomial_pair]
      apply Has.sigmaIntro
      simpa only [index_instantiate] using ih σ
  | @sigmaSnd z B h ih =>
      rw [polynomial_snd, index_instantiate, polynomial_fst]
      exact .sigmaSnd (ih σ)
  | identityIntro h => exact .identityIntro (conversion_substitution h σ)
  | @j p x y d B hp hd ihp ihd =>
      rw [polynomial_j, index_motiveAt]
      apply Has.j (x := psub σ x) (ihp σ)
      simpa only [index_motiveAt, psub] using ihd σ
  | conv h hc ih => exact .conv (ih σ) (conversion_substitution hc σ)

/-- The first n original type parameters are replaced simultaneously;
    the remaining original parameters are lowered by n. -/
def finitePrefix (n : Nat) (τ : Nat → Ty) (k : Nat) : Ty :=
  if k < n then τ k else .param (k - n)

 theorem prefix_zero (τ : Nat → Ty) : finitePrefix 0 τ = Ty.param := by
  funext k
  simp only [finitePrefix, Nat.not_lt_zero, ↓reduceIte, Nat.sub_zero]

 theorem prefix_successor (n : Nat) (τ : Nat → Ty) :
    (fun k => substType (cons (τ 0) Ty.param)
      (liftTypes (finitePrefix n (fun j => τ (j+1))) k)) = finitePrefix (n+1) τ := by
  funext k
  cases k with
  | zero => simp only [liftTypes, substType, cons, finitePrefix, Nat.zero_lt_succ, ↓reduceIte]
  | succ k =>
      change substType (cons (τ 0) Ty.param)
        (renameType Nat.succ (finitePrefix n (fun j => τ (j+1)) k)) = finitePrefix (n+1) τ (k+1)
      rw [type_shift_cancel]
      simp only [finitePrefix, Nat.succ_lt_succ_iff, Nat.add_sub_add_right]

/-- Exact finite-finitePrefix elimination identity, before any support bound. -/
 theorem finite_prefix_elimination (A : Ty) (n : Nat) (τ : Nat → Ty) :
    instantiateType (substType (liftTypes (finitePrefix n (fun k => τ (k+1)))) A) (τ 0) =
      substType (finitePrefix (n+1) τ) A := by
  rw [instantiateType, type_composition, prefix_successor]

/-- Repeated existing All introduction followed by reverse All elimination.
    Every external image is passed unshifted to the existing allElim rule. -/
 theorem has_prefix_substitution {p : Poly} {A : Ty} (h : Has p A)
    (n : Nat) (τ : Nat → Ty) : Has p (substType (finitePrefix n τ) A) := by
  induction n generalizing A τ with
  | zero => simpa only [prefix_zero, type_identity] using h
  | succ n ih =>
      have hq := ih (Has.allIntro h) (fun k => τ (k+1))
      have he := Has.allElim (A := τ 0) hq
      simpa only [finite_prefix_elimination] using he

/-- Number of possible free type indices, accounting for All binders.
    Pi and Sigma bind only raw indices. -/
def freeTypeBound : Ty → Nat
  | .param k => k+1
  | .bottom => 0
  | .raw => 0
  | .identity _ _ => 0
  | .arrow A B => max (freeTypeBound A) (freeTypeBound B)
  | .pi B => freeTypeBound B
  | .sigma B => freeTypeBound B
  | .all B => (freeTypeBound B).pred

 theorem type_substitution_agreement (A : Ty) (σ τ : Nat → Ty)
    (h : ∀ k, k < freeTypeBound A → σ k = τ k) : substType σ A = substType τ A := by
  induction A generalizing σ τ with
  | param k => exact h k (Nat.lt_succ_self k)
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb =>
      apply congrArg₂ Ty.arrow
      · apply ha
        intro k hk
        apply h k
        exact Nat.lt_of_lt_of_le hk (Nat.le_max_left _ _)
      · apply hb
        intro k hk
        apply h k
        exact Nat.lt_of_lt_of_le hk (Nat.le_max_right _ _)
  | pi B ih =>
      apply congrArg Ty.pi
      apply ih
      intro k hk
      change substIndex _ (σ k) = substIndex _ (τ k)
      rw [h k hk]
  | sigma B ih =>
      apply congrArg Ty.sigma
      apply ih
      intro k hk
      change substIndex _ (σ k) = substIndex _ (τ k)
      rw [h k hk]
  | all B ih =>
      apply congrArg Ty.all
      apply ih
      intro k hk
      cases k with
      | zero => rfl
      | succ k =>
          change renameType Nat.succ (σ k) = renameType Nat.succ (τ k)
          apply congrArg (renameType Nat.succ)
          apply h k
          change k < (freeTypeBound B).pred
          simp only [Nat.pred_eq_sub_one]
          omega

 theorem finite_prefix_complete (A : Ty) (τ : Nat → Ty) :
    substType (finitePrefix (freeTypeBound A) τ) A = substType τ A := by
  apply type_substitution_agreement
  intro k hk
  exact if_pos hk

/-- Arbitrary simultaneous type substitution preserves the literal source
    polynomial, including opaque composite finite atoms. -/
 theorem has_type_substitution {p : Poly} {A : Ty} (h : Has p A) (τ : Nat → Ty) :
    Has p (substType τ A) := by
  have hp := has_prefix_substitution h (freeTypeBound A) τ
  simpa only [finite_prefix_complete] using hp

 theorem has_index_composition {p : Poly} {A : Ty} (h : Has p A)
    (σ τ : Nat → Poly) :
    Has (psub (fun n => psub τ (σ n)) p)
      (substIndex (fun n => psub τ (σ n)) A) := by
  simpa only [psub_comp, index_composition] using
    has_index_substitution (has_index_substitution h σ) τ

 theorem has_type_composition {p : Poly} {A : Ty} (h : Has p A)
    (σ τ : Nat → Ty) : Has p (substType (fun n => substType τ (σ n)) A) := by
  simpa only [type_composition] using
    has_type_substitution (has_type_substitution h σ) τ

 theorem has_mixed_substitution {p : Poly} {A : Ty} (h : Has p A)
    (σ : Nat → Poly) (τ : Nat → Ty) :
    Has (psub σ p) (substType (fun n => substIndex σ (τ n)) (substIndex σ A)) := by
  simpa only [index_type_interchange] using
    has_index_substitution (has_type_substitution h τ) σ

end P01DF.Syntactic
