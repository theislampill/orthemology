/- Literal, capture-avoiding algebra of the independent term and type binders. -/
import AllTermAlgebra

namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01DF.Syntactic (polynomial_shift_substitution polynomial_shift_cancel
  polynomial_lift_composition)

@[simp] theorem trename_id (A : Ty) : trename id A = A := by
  have h : liftRen id = id := by funext n; cases n <;> rfl
  induction A with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [trename, ha, hb]
  | sigma A B ha hb => simp only [trename, ha, hb]
  | identity A p q ha => simp only [trename, ha]
  | all B ih => simp only [trename, h, ih]

theorem trename_comp (A : Ty) (r s : Nat → Nat) :
    trename s (trename r A) = trename (fun n => s (r n)) A := by
  induction A generalizing r s with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [trename, ha, hb]
  | sigma A B ha hb => simp only [trename, ha, hb]
  | identity A p q ha => simp only [trename, ha]
  | all B ih =>
      simp only [trename, ih]
      congr 2
      funext n
      cases n <;> rfl

theorem subst_trename (A : Ty) (σ : Nat → Poly) (r : Nat → Nat) :
    subst σ (trename r A) = trename r (subst σ A) := by
  induction A generalizing σ r with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [subst, trename, ha, hb]
  | sigma A B ha hb => simp only [subst, trename, ha, hb]
  | identity A p q ha => simp only [subst, trename, ha]
  | all B ih => simp only [subst, trename, ih]

theorem trename_wk (A : Ty) (r : Nat → Nat) :
    trename r (wk A) = wk (trename r A) :=
  (subst_trename A _ r).symm

theorem subst_twk (A : Ty) (σ : Nat → Poly) :
    subst σ (twk A) = twk (subst σ A) := subst_trename A σ _

theorem twk_wk (A : Ty) : twk (wk A) = wk (twk A) := trename_wk A _

theorem trename_twk (A : Ty) (r : Nat → Nat) :
    trename (liftRen r) (twk A) = twk (trename r A) := by
  simp only [twk, trename_comp]
  rfl

/-- The type lift commutes with term weakening of every replacement image. -/
theorem tup_wk (τ : Nat → Ty) :
    tup (fun n => wk (τ n)) = fun n => wk (tup τ n) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact twk_wk (τ n)

theorem tup_subst (τ : Nat → Ty) (σ : Nat → Poly) :
    tup (fun n => subst σ (τ n)) = fun n => subst σ (tup τ n) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact (subst_twk (τ n) σ).symm

@[simp] theorem tup_param : tup Ty.param = Ty.param := by
  funext n
  cases n <;> rfl

@[simp] theorem mixed_param (A : Ty) (σ : Nat → Poly) :
    mixed σ Ty.param A = subst σ A := by
  induction A generalizing σ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [mixed, subst, ha]; exact congrArg (Ty.pi _) (hb _)
  | sigma A B ha hb => simp only [mixed, subst, ha]; exact congrArg (Ty.sigma _) (hb _)
  | identity A p q ha => simp only [mixed, subst, ha]
  | all B ih => simp only [mixed, subst, tup_param, ih]

@[simp] theorem mixed_id (A : Ty) : mixed Poly.var Ty.param A = A := by
  rw [mixed_param, subst_id]

/-- Renaming free parameters before a mixed map only reindexes its type images. -/
theorem mixed_trename (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) (r : Nat → Nat) :
    mixed σ τ (trename r A) = mixed σ (fun n => τ (r n)) A := by
  induction A generalizing σ τ r with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [trename, mixed, ha, hb]
  | sigma A B ha hb => simp only [trename, mixed, ha, hb]
  | identity A p q ha => simp only [trename, mixed, ha]
  | all B ih =>
      simp only [trename, mixed, ih]
      congr 2
      funext n
      cases n <;> rfl

/-- Output type renaming leaves all polynomial images literally unchanged. -/
theorem trename_mixed (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) (r : Nat → Nat) :
    trename r (mixed σ τ A) = mixed σ (fun n => trename r (τ n)) A := by
  induction A generalizing σ τ r with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [mixed, trename, ha, hb, trename_wk]
  | sigma A B ha hb => simp only [mixed, trename, ha, hb, trename_wk]
  | identity A p q ha => simp only [mixed, trename, ha]
  | all B ih =>
      simp only [mixed, trename, ih]
      congr 2
      funext n
      cases n with
      | zero => rfl
      | succ n => exact trename_twk (τ n) r

/-- Input term substitution composes only the polynomial component. -/
theorem mixed_subst (A : Ty) (δ σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (subst δ A) = mixed (fun n => psub σ (δ n)) τ A := by
  induction A generalizing δ σ τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [mixed, subst, ha, hb, polynomial_lift_composition]
  | sigma A B ha hb => simp only [mixed, subst, ha, hb, polynomial_lift_composition]
  | identity A p q ha => simp only [mixed, subst, ha, psub_comp]
  | all B ih => simp only [mixed, subst, ih]

/-- Output term substitution acts on both components, without re-substituting images. -/
theorem subst_mixed (A : Ty) (σ δ : Nat → Poly) (τ : Nat → Ty) :
    subst δ (mixed σ τ A) =
      mixed (fun n => psub δ (σ n)) (fun n => subst δ (τ n)) A := by
  induction A generalizing σ δ τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb =>
      simp only [mixed, subst, ha, hb, polynomial_lift_composition, subst_wk]
  | sigma A B ha hb =>
      simp only [mixed, subst, ha, hb, polynomial_lift_composition, subst_wk]
  | identity A p q ha => simp only [mixed, subst, ha, psub_comp]
  | all B ih => simp only [mixed, subst, ih, tup_subst]

/-- A mixed map lifted under a term binder preserves the old, weakened type. -/
theorem mixed_wk (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (fun n => wk (τ n)) (wk A) = wk (mixed σ τ A) := by
  simp only [wk, mixed_subst, subst_mixed]
  rfl

/-- A mixed map lifted under All preserves the old, type-weakened type. -/
theorem mixed_twk (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ (tup τ) (twk A) = twk (mixed σ τ A) := by
  simp only [twk, mixed_trename, trename_mixed]
  rfl

theorem mixed_term_lift_comp (σ₂ : Nat → Poly) (τ₁ τ₂ : Nat → Ty) :
    (fun n => mixed (pup σ₂) (fun k => wk (τ₂ k)) (wk (τ₁ n))) =
      (fun n => wk (mixed σ₂ τ₂ (τ₁ n))) := by
  funext n
  exact mixed_wk (τ₁ n) σ₂ τ₂

theorem mixed_type_lift_comp (σ : Nat → Poly) (τ₁ τ₂ : Nat → Ty) :
    (fun n => mixed σ (tup τ₂) (tup τ₁ n)) =
      tup (fun n => mixed σ τ₂ (τ₁ n)) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact mixed_twk (τ₁ n) σ τ₂

/-- General literal composition of simultaneous, independently lifted maps. -/
theorem mixed_comp (A : Ty) (σ₁ σ₂ : Nat → Poly) (τ₁ τ₂ : Nat → Ty) :
    mixed σ₂ τ₂ (mixed σ₁ τ₁ A) =
      mixed (fun n => psub σ₂ (σ₁ n)) (fun n => mixed σ₂ τ₂ (τ₁ n)) A := by
  induction A generalizing σ₁ σ₂ τ₁ τ₂ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb =>
      simp only [mixed, ha, hb, polynomial_lift_composition, mixed_wk]
  | sigma A B ha hb =>
      simp only [mixed, ha, hb, polynomial_lift_composition, mixed_wk]
  | identity A p q ha => simp only [mixed, ha, psub_comp]
  | all B ih => simp only [mixed, ih, mixed_type_lift_comp]

@[simp] theorem tsubst_id (A : Ty) : tsubst Ty.param A = A := mixed_id A

theorem tsubst_comp (A : Ty) (τ₁ τ₂ : Nat → Ty) :
    tsubst τ₂ (tsubst τ₁ A) = tsubst (fun n => tsubst τ₂ (τ₁ n)) A := by
  simp only [tsubst, mixed_comp, psub]

/-- The term/type square has a simultaneous right side. -/
theorem subst_tsubst (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    subst σ (tsubst τ A) = mixed σ (fun n => subst σ (τ n)) A := by
  simp only [tsubst, subst_mixed, psub]

@[simp] theorem tinst_twk (B A : Ty) : tinst (twk B) A = B := by
  simp only [tinst, tsubst, twk, mixed_trename]
  exact mixed_id B

/-- Top type substitution cancels weakening even in a dependent replacement. -/
theorem mixed_twk_cancel (B A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ (cons A τ) (twk B) = mixed σ τ B := by
  simp only [twk, mixed_trename]
  rfl

/-- Both term binders of Theta/J lift every dependent replacement twice. -/
theorem mixed_wk_wk (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup (pup σ)) (fun n => wk (wk (τ n))) (wk (wk A)) =
      wk (wk (mixed σ τ A)) := by
  rw [mixed_wk, mixed_wk]

theorem tup_wk_wk (τ : Nat → Ty) :
    tup (fun n => wk (wk (τ n))) = fun n => wk (wk (tup τ n)) := by
  rw [tup_wk, tup_wk]

theorem mixed_inst (B : Ty) (a : Poly) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (inst B a) =
      inst (mixed (pup σ) (fun n => wk (τ n)) B) (psub σ a) := by
  simp only [inst, mixed_subst, subst_mixed, subst_wk_cancel, subst_id]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      change σ n = psub (cons (psub σ a) Poly.var) (pren Nat.succ (σ n))
      rw [polynomial_shift_cancel, psub_id]

theorem mixed_motiveAt (B : Ty) (y e : Poly) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (motiveAt B y e) =
      motiveAt (mixed (pup (pup σ)) (fun n => wk (wk (τ n))) B)
        (psub σ y) (psub σ e) := by
  simp only [motiveAt, mixed_subst, subst_mixed, subst_wk_cancel, subst_id]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      cases n with
      | zero => rfl
      | succ n =>
          change σ n = psub (cons (psub σ e) (cons (psub σ y) Poly.var))
            (pren Nat.succ (pren Nat.succ (σ n)))
          rw [polynomial_shift_cancel, polynomial_shift_cancel, psub_id]

theorem mixed_arr (A B : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (arr A B) = arr (mixed σ τ A) (mixed σ τ B) := by
  simp only [arr, mixed, mixed_wk]

theorem mixed_tsubst (B : Ty) (σ : Nat → Poly) (τ υ : Nat → Ty) :
    mixed σ τ (tsubst υ B) = mixed σ (fun n => mixed σ τ (υ n)) B := by
  simp only [tsubst, mixed_comp, psub]

/-- The All elimination square preserves the unchanged polynomial component. -/
theorem mixed_tinst (B A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (tinst B A) =
      tinst (mixed σ (tup τ) B) (mixed σ τ A) := by
  simp only [tinst, tsubst, mixed_comp, psub_id]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      change τ n = mixed Poly.var (cons (mixed σ τ A) Ty.param) (twk (τ n))
      rw [mixed_twk_cancel, mixed_id]

theorem subst_tinst (B A : Ty) (σ : Nat → Poly) :
    subst σ (tinst B A) = tinst (subst σ B) (subst σ A) := by
  simpa only [mixed_param, tup_param] using mixed_tinst B A σ Ty.param

theorem trename_inst (B : Ty) (a : Poly) (r : Nat → Nat) :
    trename r (inst B a) = inst (trename r B) a :=
  (subst_trename B _ r).symm

theorem trename_motiveAt (B : Ty) (y e : Poly) (r : Nat → Nat) :
    trename r (motiveAt B y e) = motiveAt (trename r B) y e :=
  (subst_trename B _ r).symm

theorem trename_arr (A B : Ty) (r : Nat → Nat) :
    trename r (arr A B) = arr (trename r A) (trename r B) := by
  simp only [arr, trename, trename_wk]

theorem trename_tinst (B A : Ty) (r : Nat → Nat) :
    trename r (tinst B A) = tinst (trename (liftRen r) B) (trename r A) := by
  simp only [tinst, tsubst, trename_mixed, mixed_trename]
  congr 1
  funext n
  cases n <;> rfl

theorem tsubst_wk (B : Ty) (τ : Nat → Ty) :
    tsubst (fun n => wk (τ n)) (wk B) = wk (tsubst τ B) := by
  have h : pup Poly.var = Poly.var := by funext n; cases n <;> rfl
  simpa only [tsubst, h] using mixed_wk B Poly.var τ

theorem tinst_wk (B A : Ty) : tinst (wk B) (wk A) = wk (tinst B A) := by
  have h : (fun n => wk (cons A Ty.param n)) = cons (wk A) Ty.param := by
    funext n
    cases n <;> rfl
  simpa only [tinst, h] using tsubst_wk B (cons A Ty.param)

/-- Both orders of binder lifting give the identical mixed substitution. -/
theorem mixed_term_type_lifts (B : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (tup (fun n => wk (τ n))) B =
      mixed (pup σ) (fun n => wk (tup τ n)) B := by
  rw [tup_wk]

theorem mixed_double_term_type_lifts (B : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup (pup σ)) (tup (fun n => wk (wk (τ n)))) B =
      mixed (pup (pup σ)) (fun n => wk (wk (tup τ n))) B := by
  rw [tup_wk_wk]

theorem mixed_twk_wk (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (tup (fun n => wk (τ n))) (twk (wk A)) =
      twk (wk (mixed σ τ A)) := by
  rw [mixed_twk, mixed_wk]

theorem tsubst_trename (A : Ty) (τ : Nat → Ty) (r : Nat → Nat) :
    tsubst τ (trename r A) = tsubst (fun n => τ (r n)) A :=
  mixed_trename A Poly.var τ r

theorem trename_tsubst (A : Ty) (τ : Nat → Ty) (r : Nat → Nat) :
    trename r (tsubst τ A) = tsubst (fun n => trename r (τ n)) A :=
  trename_mixed A Poly.var τ r

theorem tsubst_twk (A : Ty) (τ : Nat → Ty) :
    tsubst (tup τ) (twk A) = twk (tsubst τ A) := mixed_twk A Poly.var τ

theorem tsubst_arr (A B : Ty) (τ : Nat → Ty) :
    tsubst τ (arr A B) = arr (tsubst τ A) (tsubst τ B) := mixed_arr A B Poly.var τ

theorem tyScoped_trename {n : Nat} {A : Ty} (h : TyScoped n A) (r : Nat → Nat) :
    TyScoped n (trename r A) := by
  induction A generalizing n r with
  | param k => trivial
  | bottom => trivial
  | raw => trivial
  | pi A B ha hb => exact ⟨ha h.1 r, hb h.2 r⟩
  | sigma A B ha hb => exact ⟨ha h.1 r, hb h.2 r⟩
  | identity A p q ha => exact ⟨ha h.1 r, h.2⟩
  | all B ih => exact ih h (liftRen r)

theorem tyScoped_twk {n : Nat} {A : Ty} (h : TyScoped n A) :
    TyScoped n (twk A) := tyScoped_trename h _

theorem tyScoped_tup {n : Nat} {τ : Nat → Ty} (h : ∀ k, TyScoped n (τ k)) :
    ∀ k, TyScoped n (tup τ k) := by
  intro k
  cases k with
  | zero => trivial
  | succ k => exact tyScoped_twk (h k)

/-- Term scope is preserved by a mixed map with scoped type images. -/
theorem tyScoped_mixed {n m : Nat} {A : Ty} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : TyScoped n A) (hs : ScopedSub n m σ) (ht : ∀ k, TyScoped m (τ k)) :
    TyScoped m (mixed σ τ A) := by
  induction A generalizing n m σ τ with
  | param k => exact ht k
  | bottom => trivial
  | raw => trivial
  | pi A B ha hb =>
      exact ⟨ha h.1 hs ht, hb h.2 (scopedSub_lift hs) (fun k => tyScoped_wk (ht k))⟩
  | sigma A B ha hb =>
      exact ⟨ha h.1 hs ht, hb h.2 (scopedSub_lift hs) (fun k => tyScoped_wk (ht k))⟩
  | identity A p q ha => exact ⟨ha h.1 hs ht, scoped_subst h.2.1 hs, scoped_subst h.2.2 hs⟩
  | all B ih => exact ih h hs (tyScoped_tup ht)

/-- One type binder and one term binder protect both coordinates of an image. -/
theorem capture_both_sorts :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.all (.pi .raw (.param 1))) =
      .all (.pi .raw (.identity (.param 1) (.var 1) (.atom .i))) := rfl

/-- The design's term-dependent example keeps the older variable free. -/
theorem capture_term_under_all_pi :
    tsubst (cons (Ty.identity .raw (.var 0) (.atom .i)) Ty.param)
      (.all (.pi .raw (.param 1))) =
      .all (.pi .raw (.identity .raw (.var 1) (.atom .i))) := rfl

/-- The double term lift in Theta/J shifts the old endpoint by exactly two. -/
theorem capture_both_sorts_double_term :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.all (.pi .raw (.sigma .raw (.param 1)))) =
      .all (.pi .raw (.sigma .raw (.identity (.param 1) (.var 2) (.atom .i)))) := rfl

/-- Interchanging the two binder sorts yields the same protected coordinates. -/
theorem capture_term_then_type :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.pi .raw (.all (.param 1))) =
      .pi .raw (.all (.identity (.param 1) (.var 1) (.atom .i))) := rfl

/-- Bound type parameter zero is never replaced while the outer image is shifted. -/
theorem capture_bound_type_retained :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.all (.pi (.param 0) (.identity (.param 1) (.var 0) (.var 1)))) =
      .all (.pi (.param 0)
        (.identity (.identity (.param 1) (.var 1) (.atom .i)) (.var 0) (.var 1))) := rfl

/-- The captured term endpoint is genuinely different from the correct result. -/
theorem capture_term_not_zero :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.all (.pi .raw (.param 1))) ≠
      .all (.pi .raw (.identity (.param 1) (.var 0) (.atom .i))) := by
  intro h
  cases h

/-- The captured type parameter is likewise not the literal substitution. -/
theorem capture_type_not_zero :
    tsubst (cons (Ty.identity (.param 0) (.var 0) (.atom .i)) Ty.param)
      (.all (.pi .raw (.param 1))) ≠
      .all (.pi .raw (.identity (.param 0) (.var 1) (.atom .i))) := by
  intro h
  cases h

end P01AC
