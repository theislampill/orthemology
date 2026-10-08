/- Literal substitution algebra for the unchanged raw-index dependent syntax. -/
import P01DependentFundamental

namespace P01DF.Syntactic
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

 theorem polynomial_shift_substitution (p : Poly) (σ : Nat → Poly) :
    psub (pup σ) (pren Nat.succ p) = pren Nat.succ (psub σ p) := by
  simp only [pren, psub_comp]
  rfl

 theorem polynomial_shift_cancel (p : Poly) (a : Poly) (σ : Nat → Poly) :
    psub (cons a σ) (pren Nat.succ p) = psub σ p := by
  simp only [pren, psub_comp]
  rfl

 theorem polynomial_lift_composition (σ τ : Nat → Poly) :
    (fun n => psub (pup τ) (pup σ n)) = pup (fun n => psub τ (σ n)) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact polynomial_shift_substitution (σ n) τ

 theorem index_identity (A : Ty) : substIndex Poly.var A = A := by
  have h : pup Poly.var = Poly.var := by funext n; cases n <;> rfl
  induction A with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => simp only [substIndex, psub_id]
  | arrow A B ha hb => simp only [substIndex, ha, hb]
  | all B ih => simp only [substIndex, ih]
  | pi B ih => simp only [substIndex, h, ih]
  | sigma B ih => simp only [substIndex, h, ih]

 theorem index_composition (A : Ty) (σ τ : Nat → Poly) :
    substIndex τ (substIndex σ A) = substIndex (fun n => psub τ (σ n)) A := by
  induction A generalizing σ τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => simp only [substIndex, psub_comp]
  | arrow A B ha hb => simp only [substIndex, ha, hb]
  | all B ih => simp only [substIndex, ih]
  | pi B ih => simp only [substIndex, ih, polynomial_lift_composition]
  | sigma B ih => simp only [substIndex, ih, polynomial_lift_composition]

 theorem index_shift_substitution (A : Ty) (σ : Nat → Poly) :
    substIndex (pup σ) (substIndex (fun n => .var (n+1)) A) =
      substIndex (fun n => .var (n+1)) (substIndex σ A) := by
  rw [index_composition, index_composition]
  rfl

 theorem index_type_renaming (A : Ty) (σ : Nat → Poly) (r : Nat → Nat) :
    substIndex σ (renameType r A) = renameType r (substIndex σ A) := by
  induction A generalizing σ r with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [substIndex, renameType, ha, hb]
  | all B ih => simp only [substIndex, renameType, ih]
  | pi B ih => simp only [substIndex, renameType, ih]
  | sigma B ih => simp only [substIndex, renameType, ih]

 theorem type_renaming_composition (A : Ty) (r s : Nat → Nat) :
    renameType s (renameType r A) = renameType (fun n => s (r n)) A := by
  induction A generalizing r s with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [renameType, ha, hb]
  | pi B ih => simp only [renameType, ih]
  | sigma B ih => simp only [renameType, ih]
  | all B ih =>
      simp only [renameType, ih]
      congr 2
      funext n
      cases n <;> rfl

 theorem type_renaming_shift (A : Ty) (r : Nat → Nat) :
    renameType (liftRen r) (renameType Nat.succ A) =
      renameType Nat.succ (renameType r A) := by
  rw [type_renaming_composition, type_renaming_composition]
  rfl

 theorem type_substitution_renaming (A : Ty) (r : Nat → Nat) (τ : Nat → Ty) :
    substType τ (renameType r A) = substType (fun n => τ (r n)) A := by
  induction A generalizing r τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [renameType, substType, ha, hb]
  | pi B ih => simp only [renameType, substType, ih]; rfl
  | sigma B ih => simp only [renameType, substType, ih]; rfl
  | all B ih =>
      simp only [renameType, substType, ih]
      congr 2
      funext n
      cases n <;> rfl

 theorem type_renaming_substitution (A : Ty) (r : Nat → Nat) (τ : Nat → Ty) :
    renameType r (substType τ A) = substType (fun n => renameType r (τ n)) A := by
  induction A generalizing r τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [renameType, substType, ha, hb]
  | pi B ih =>
      simp only [renameType, substType, ih]
      congr 2
      funext n
      exact (index_type_renaming (τ n) _ r).symm
  | sigma B ih =>
      simp only [renameType, substType, ih]
      congr 2
      funext n
      exact (index_type_renaming (τ n) _ r).symm
  | all B ih =>
      simp only [renameType, substType, ih]
      congr 2
      funext n
      cases n with
      | zero => rfl
      | succ n => exact type_renaming_shift (τ n) r

 theorem index_type_interchange (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    substIndex σ (substType τ A) =
      substType (fun n => substIndex σ (τ n)) (substIndex σ A) := by
  induction A generalizing σ τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [substIndex, substType, ha, hb]
  | pi B ih =>
      simp only [substIndex, substType, ih]
      congr 2
      funext n
      exact index_shift_substitution (τ n) σ
  | sigma B ih =>
      simp only [substIndex, substType, ih]
      congr 2
      funext n
      exact index_shift_substitution (τ n) σ
  | all B ih =>
      simp only [substIndex, substType, ih]
      congr 2
      funext n
      cases n with
      | zero => rfl
      | succ n => exact index_type_renaming (τ n) σ Nat.succ

 theorem type_identity (A : Ty) : substType Ty.param A = A := by
  have ht : liftTypes Ty.param = Ty.param := by funext n; cases n <;> rfl
  have hi : liftIndices Ty.param = Ty.param := rfl
  induction A with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [substType, ha, hb]
  | pi B ih => simp only [substType, hi, ih]
  | sigma B ih => simp only [substType, hi, ih]
  | all B ih => simp only [substType, ht, ih]

 theorem type_composition (A : Ty) (σ τ : Nat → Ty) :
    substType τ (substType σ A) = substType (fun n => substType τ (σ n)) A := by
  induction A generalizing σ τ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb => simp only [substType, ha, hb]
  | pi B ih =>
      simp only [substType, ih]
      congr 2
      funext n
      exact (index_type_interchange (σ n) (fun k => .var (k+1)) τ).symm
  | sigma B ih =>
      simp only [substType, ih]
      congr 2
      funext n
      exact (index_type_interchange (σ n) (fun k => .var (k+1)) τ).symm
  | all B ih =>
      simp only [substType, ih]
      congr 2
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          change substType (liftTypes τ) (renameType Nat.succ (σ n)) =
            renameType Nat.succ (substType τ (σ n))
          rw [type_substitution_renaming, type_renaming_substitution]
          rfl

 theorem type_shift_cancel (B A : Ty) :
    substType (cons A Ty.param) (renameType Nat.succ B) = B := by
  rw [type_substitution_renaming]
  exact type_identity B

 theorem index_instantiate (B : Ty) (a : Poly) (σ : Nat → Poly) :
    substIndex σ (instantiate B a) =
      instantiate (substIndex (pup σ) B) (psub σ a) := by
  simp only [instantiate, index_composition]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      change σ n = psub (cons (psub σ a) Poly.var) (pren Nat.succ (σ n))
      rw [polynomial_shift_cancel, psub_id]

 theorem index_instantiateType (B A : Ty) (σ : Nat → Poly) :
    substIndex σ (instantiateType B A) =
      instantiateType (substIndex σ B) (substIndex σ A) := by
  simp only [instantiateType, index_type_interchange]
  congr 1
  funext n
  cases n <;> rfl

 theorem index_motiveAt (B : Ty) (y p : Poly) (σ : Nat → Poly) :
    substIndex σ (motiveAt B y p) =
      motiveAt (substIndex (pup (pup σ)) B) (psub σ y) (psub σ p) := by
  simp only [motiveAt, index_composition]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      cases n with
      | zero => rfl
      | succ n =>
          change σ n = psub (cons (psub σ p) (cons (psub σ y) Poly.var))
            (pren Nat.succ (pren Nat.succ (σ n)))
          rw [polynomial_shift_cancel, polynomial_shift_cancel, psub_id]

 theorem index_embedFinite (A : TypeCode) (σ : Nat → Poly) :
    substIndex σ (embedFinite A) = embedFinite A := by
  induction A with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [embedFinite, substIndex, ha, hb]
  | all B ih => simp only [embedFinite, substIndex, ih]

 theorem polynomial_pair (a b : Poly) (σ : Nat → Poly) :
    psub σ (pairPoly a b) = pairPoly (psub σ a) (psub σ b) := rfl
 theorem polynomial_fst (z : Poly) (σ : Nat → Poly) :
    psub σ (fstPoly z) = fstPoly (psub σ z) := rfl
 theorem polynomial_snd (z : Poly) (σ : Nat → Poly) :
    psub σ (sndPoly z) = sndPoly (psub σ z) := rfl
 theorem polynomial_j (d y p : Poly) (σ : Nat → Poly) :
    psub σ (jPoly d y p) = jPoly (psub σ d) (psub σ y) (psub σ p) := rfl

end P01DF.Syntactic
