/- Literal substitution and finite-scope algebra for typed telescopes. -/
import AllSyntax

namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01DF.Syntactic (polynomial_shift_substitution polynomial_shift_cancel
  polynomial_lift_composition)

@[simp] theorem subst_id (A : Ty) : subst Poly.var A = A := by
  have hl : pup Poly.var = Poly.var := by funext n; cases n <;> rfl
  induction A with
  | param n => rfl
  | bottom => rfl
  | all B ih => simp only [subst, ih]
  | raw => rfl
  | pi A B ha hb => simp only [subst, hl, ha, hb]
  | sigma A B ha hb => simp only [subst, hl, ha, hb]
  | identity A p q ha => simp only [subst, ha, psub_id]

theorem subst_comp (A : Ty) (σ τ : Nat → Poly) :
    subst τ (subst σ A) = subst (fun n => psub τ (σ n)) A := by
  induction A generalizing σ τ with
  | param n => rfl
  | bottom => rfl
  | all B ih => simp only [subst, ih]
  | raw => rfl
  | pi A B ha hb => simp only [subst, ha, hb, polynomial_lift_composition]
  | sigma A B ha hb => simp only [subst, ha, hb, polynomial_lift_composition]
  | identity A p q ha => simp only [subst, ha, psub_comp]

/-- Substitution beneath one binder commutes literally with weakening. -/
theorem subst_wk (A : Ty) (σ : Nat → Poly) :
    subst (pup σ) (wk A) = wk (subst σ A) := by
  simp only [wk, subst_comp]
  rfl

theorem subst_wk_cancel (A : Ty) (a : Poly) (σ : Nat → Poly) :
    subst (cons a σ) (wk A) = subst σ A := by
  rw [wk, subst_comp]
  rfl

@[simp] theorem inst_wk (A : Ty) (a : Poly) : inst (wk A) a = A := by
  rw [inst, subst_wk_cancel, subst_id]

theorem subst_inst (B : Ty) (a : Poly) (σ : Nat → Poly) :
    subst σ (inst B a) = inst (subst (pup σ) B) (psub σ a) := by
  simp only [inst, subst_comp]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      change σ n = psub (cons (psub σ a) Poly.var) (pren Nat.succ (σ n))
      rw [polynomial_shift_cancel, psub_id]

theorem subst_motiveAt (B : Ty) (y e : Poly) (σ : Nat → Poly) :
    subst σ (motiveAt B y e) =
      motiveAt (subst (pup (pup σ)) B) (psub σ y) (psub σ e) := by
  simp only [motiveAt, subst_comp]
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

/-- The two-variable motive substitution is two successive instantiations. -/
theorem motiveAt_inst (B : Ty) (y e : Poly) :
    motiveAt B y e = inst (inst B (pren Nat.succ e)) y := by
  simp only [motiveAt, inst, subst_comp]
  congr 1
  funext n
  cases n with
  | zero =>
      change e = psub (cons y Poly.var) (pren Nat.succ e)
      rw [polynomial_shift_cancel, psub_id]
  | succ n => cases n <;> rfl

@[simp] theorem motiveAt_wk_wk (A : Ty) (y e : Poly) :
    motiveAt (wk (wk A)) y e = A := by
  simp only [motiveAt, subst_wk_cancel, subst_id]

theorem subst_arr (A B : Ty) (σ : Nat → Poly) :
    subst σ (arr A B) = arr (subst σ A) (subst σ B) := by
  simp only [arr, subst, subst_wk]

/-- Finite type parameters are unaffected by term substitution. -/
@[simp] theorem subst_fin (C : TypeCode) (σ : Nat → Poly) :
    subst σ (fin C) = fin C := by
  induction C with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [fin, subst_arr, ha, hb]
  | all B ih => simp only [fin, subst, ih]

@[simp] theorem wk_fin (C : TypeCode) : wk (fin C) = fin C :=
  subst_fin C _

@[simp] theorem inst_fin (C : TypeCode) (a : Poly) : inst (fin C) a = fin C :=
  subst_fin C _

@[simp] theorem motiveAt_fin (C : TypeCode) (y e : Poly) :
    motiveAt (fin C) y e = fin C := subst_fin C _

/-- A substitution only needs scoped images for the finitely many source variables. -/
def ScopedSub (n m : Nat) (σ : Nat → Poly) : Prop :=
  ∀ k, k < n → Scoped m (σ k)

theorem scoped_mono {n m : Nat} {p : Poly} (h : Scoped n p) (hnm : n ≤ m) :
    Scoped m p := by
  induction p with
  | var k => exact Nat.lt_of_lt_of_le h hnm
  | atom t => trivial
  | app f a hf ha => exact ⟨hf h.1, ha h.2⟩

theorem scoped_subst {n m : Nat} {p : Poly} {σ : Nat → Poly}
    (h : Scoped n p) (hs : ScopedSub n m σ) : Scoped m (psub σ p) := by
  induction p with
  | var k => exact hs k h
  | atom t => trivial
  | app f a hf ha => exact ⟨hf h.1, ha h.2⟩

theorem scoped_rename {n m : Nat} {p : Poly} {r : Nat → Nat}
    (h : Scoped n p) (hr : ∀ k, k < n → r k < m) : Scoped m (pren r p) :=
  scoped_subst h hr

theorem scoped_wk {n : Nat} {p : Poly} (h : Scoped n p) :
    Scoped (n+1) (pren Nat.succ p) :=
  scoped_rename h (fun _ hk => Nat.succ_lt_succ hk)

theorem scopedSub_lift {n m : Nat} {σ : Nat → Poly} (h : ScopedSub n m σ) :
    ScopedSub (n+1) (m+1) (pup σ) := by
  intro k hk
  cases k with
  | zero => exact Nat.zero_lt_succ m
  | succ k => exact scoped_wk (h k (Nat.lt_of_succ_lt_succ hk))

theorem scopedSub_id (n : Nat) : ScopedSub n n Poly.var := fun _ hk => hk

theorem scopedSub_comp {n m l : Nat} {σ τ : Nat → Poly}
    (hs : ScopedSub n m σ) (ht : ScopedSub m l τ) :
    ScopedSub n l (fun k => psub τ (σ k)) :=
  fun k hk => scoped_subst (hs k hk) ht

theorem scopedSub_cons {n m : Nat} {σ : Nat → Poly} {a : Poly}
    (ha : Scoped m a) (hs : ScopedSub n m σ) : ScopedSub (n+1) m (cons a σ) := by
  intro k hk
  cases k with
  | zero => exact ha
  | succ k => exact hs k (Nat.lt_of_succ_lt_succ hk)

theorem scoped_pair {n : Nat} {a b : Poly} (ha : Scoped n a) (hb : Scoped n b) :
    Scoped n (pairPoly a b) := by
  simpa only [pairPoly, Scoped, true_and] using And.intro ha hb

theorem scoped_fst {n : Nat} {z : Poly} (h : Scoped n z) : Scoped n (fstPoly z) :=
  ⟨h, trivial⟩

theorem scoped_snd {n : Nat} {z : Poly} (h : Scoped n z) : Scoped n (sndPoly z) :=
  ⟨h, trivial, trivial⟩

theorem scoped_j {n : Nat} {d y e : Poly}
    (hd : Scoped n d) (hy : Scoped n y) (he : Scoped n e) : Scoped n (jPoly d y e) :=
  ⟨⟨⟨trivial, ⟨trivial, hd⟩⟩, hy⟩, he⟩

theorem scoped_drop_absent {n : Nat} {p : Poly}
    (h : Scoped (n+1) p) (hf : freeZero p = false) : Scoped n (drop p) := by
  induction p with
  | var k =>
      cases k with
      | zero => simp [freeZero] at hf
      | succ k => exact Nat.lt_of_succ_lt_succ h
  | atom t => trivial
  | app f a ihf iha =>
      have hfa : freeZero f = false ∧ freeZero a = false := by
        simpa only [freeZero, Bool.or_eq_false_iff] using hf
      exact ⟨ihf h.1 hfa.1, iha h.2 hfa.2⟩

/-- The unchanged abstraction backend removes exactly the leading scope slot. -/
theorem scoped_abstract {n : Nat} {p : Poly} (h : Scoped (n+1) p) :
    Scoped n (abstract p) := by
  induction p with
  | var k =>
      cases k with
      | zero => simp [abstract, freeZero, Scoped]
      | succ k =>
          rw [abstract_absent (.var (k+1)) (by rfl)]
          exact ⟨trivial, Nat.lt_of_succ_lt_succ h⟩
  | atom t =>
      rw [abstract_absent (.atom t) (by rfl)]
      exact ⟨trivial, trivial⟩
  | app f a ihf iha =>
      by_cases hf : freeZero (.app f a) = true
      · rw [abstract_present_app _ _ hf]
        exact ⟨⟨trivial, ihf h.1⟩, iha h.2⟩
      · have hfalse := Bool.eq_false_of_not_eq_true hf
        rw [abstract_absent _ hfalse]
        exact ⟨trivial, scoped_drop_absent h hfalse⟩

theorem tyScoped_mono {n m : Nat} {A : Ty} (h : TyScoped n A) (hnm : n ≤ m) :
    TyScoped m A := by
  induction A generalizing n m with
  | param k => trivial
  | bottom => trivial
  | all B ih => exact ih h hnm
  | raw => trivial
  | pi A B ha hb => exact ⟨ha h.1 hnm, hb h.2 (Nat.succ_le_succ hnm)⟩
  | sigma A B ha hb => exact ⟨ha h.1 hnm, hb h.2 (Nat.succ_le_succ hnm)⟩
  | identity A p q ha =>
      exact ⟨ha h.1 hnm, scoped_mono h.2.1 hnm, scoped_mono h.2.2 hnm⟩

theorem tyScoped_subst {n m : Nat} {A : Ty} {σ : Nat → Poly}
    (h : TyScoped n A) (hs : ScopedSub n m σ) : TyScoped m (subst σ A) := by
  induction A generalizing n m σ with
  | param k => trivial
  | bottom => trivial
  | all B ih => exact ih h hs
  | raw => trivial
  | pi A B ha hb => exact ⟨ha h.1 hs, hb h.2 (scopedSub_lift hs)⟩
  | sigma A B ha hb => exact ⟨ha h.1 hs, hb h.2 (scopedSub_lift hs)⟩
  | identity A p q ha =>
      exact ⟨ha h.1 hs, scoped_subst h.2.1 hs, scoped_subst h.2.2 hs⟩

theorem tyScoped_wk {n : Nat} {A : Ty} (h : TyScoped n A) : TyScoped (n+1) (wk A) :=
  tyScoped_subst h (fun _ hk => Nat.succ_lt_succ hk)

theorem tyScoped_inst {n : Nat} {B : Ty} {a : Poly}
    (hB : TyScoped (n+1) B) (ha : Scoped n a) : TyScoped n (inst B a) :=
  tyScoped_subst hB (scopedSub_cons ha (scopedSub_id n))

theorem tyScoped_motiveAt {n : Nat} {B : Ty} {y e : Poly}
    (hB : TyScoped (n+1+1) B) (hy : Scoped n y) (he : Scoped n e) :
    TyScoped n (motiveAt B y e) :=
  tyScoped_subst hB (scopedSub_cons he (scopedSub_cons hy (scopedSub_id n)))

theorem tyScoped_fin (C : TypeCode) (n : Nat) : TyScoped n (fin C) := by
  induction C with
  | var k => trivial
  | bottom => trivial
  | arrow A B ha hb => exact ⟨ha, tyScoped_wk hb⟩
  | all B ih => exact ih

theorem lookup_lt {Γ : Tel} {n : Nat} {A : Ty} (h : Lookup Γ n A) : n < Γ.length := by
  induction h with
  | zero => exact Nat.zero_lt_succ _
  | succ h ih => exact Nat.succ_lt_succ ih

/-- Source conversion is closed under literal polynomial substitution. -/
theorem polyConv_subst {p q : Poly} (h : P01DF.PolyConv p q) (σ : Nat → Poly) :
    P01DF.PolyConv (psub σ p) (psub σ q) := by
  induction h with
  | refl p => exact .refl _
  | symm h ih => exact .symm ih
  | trans h₁ h₂ ih₁ ih₂ => exact .trans ih₁ ih₂
  | app hf ha ihf iha => exact .app ihf iha
  | i p => exact .i _
  | k p q => exact .k _ _
  | s p q r => exact .s _ _ _

end P01AC
