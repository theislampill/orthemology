/- Additive, finite executable certificates for the five actual auxiliary
   source judgments. Every certificate field is finite syntax or a child
   certificate; no proof, semantic value, or arbitrary function is stored. -/
import IntensionalIdentityBridge

namespace AuxiliaryCertificates
open OrthemologyV2 OrthemologyV3 P01D P01AC
open P01AC.Intensional.Plus

inductive StepCert : Type where
  | i (x : Term)
  | k (x y : Term)
  | s (f g x : Term)
  | left (f g x : Term) (child : StepCert)
  | right (f x y : Term) (child : StepCert)
  deriving DecidableEq

def checkStep : StepCert → Term → Term → Bool
  | .i x, t, u => decide (t = .app .i x ∧ u = x)
  | .k x y, t, u => decide (t = .app (.app .k x) y ∧ u = x)
  | .s f g x, t, u => decide (t = .app (.app (.app .s f) g) x ∧
      u = .app (.app f x) (.app g x))
  | .left f g x c, t, u => decide (t = .app f x ∧ u = .app g x) && checkStep c f g
  | .right f x y c, t, u => decide (t = .app f x ∧ u = .app f y) && checkStep c x y

theorem checkStep_sound {c : StepCert} {t u : Term}
    (h : checkStep c t u = true) : Step t u := by
  induction c generalizing t u with
  | i x => simp only [checkStep, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .i _
  | k x y => simp only [checkStep, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .k _ _
  | s f g x => simp only [checkStep, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .s f g x
  | left f g x c ih =>
      simp only [checkStep, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl⟩,hc⟩
      exact .left (ih hc) x
  | right f x y c ih =>
      simp only [checkStep, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl⟩,hc⟩
      exact .right f (ih hc)

theorem step_complete {t u : Term} (h : Step t u) :
    ∃ c : StepCert, checkStep c t u = true := by
  induction h with
  | i x => exact ⟨.i x, by simp [checkStep]⟩
  | k x y => exact ⟨.k x y, by simp [checkStep]⟩
  | s f g x => exact ⟨.s f g x, by simp [checkStep]⟩
  | @left f g h x ih =>
      obtain ⟨c,hc⟩ := ih
      exact ⟨.left f g x c, by simp [checkStep,hc]⟩
  | @right f x y h ih =>
      obtain ⟨c,hc⟩ := ih
      exact ⟨.right f x y c, by simp [checkStep,hc]⟩

inductive RedCert : Type where
  | refl (t : Term)
  | tail (t u v : Term) (step : StepCert) (rest : RedCert)
  deriving DecidableEq

def checkRed : RedCert → Term → Term → Bool
  | .refl t, a, b => decide (a = t ∧ b = t)
  | .tail t u v s r, a, b =>
      decide (a = t ∧ b = v) && checkStep s t u && checkRed r u v

theorem checkRed_sound {c : RedCert} {t u : Term}
    (h : checkRed c t u = true) : Red t u := by
  induction c generalizing t u with
  | refl x => simp only [checkRed, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .refl _
  | tail a b d s r ih =>
      simp only [checkRed, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨⟨rfl,rfl⟩,hs⟩,hr⟩
      exact .tail (checkStep_sound hs) (ih hr)

theorem red_complete {t u : Term} (h : Red t u) :
    ∃ c : RedCert, checkRed c t u = true := by
  induction h with
  | refl t => exact ⟨.refl t, by simp [checkRed]⟩
  | @tail t u v s r ih =>
      obtain ⟨sc,hsc⟩ := step_complete s
      obtain ⟨rc,hrc⟩ := ih
      exact ⟨.tail t u v sc rc, by simp [checkRed,hsc,hrc]⟩

inductive FiniteCert : Type where
  | i (A : TypeCode)
  | k (A B : TypeCode)
  | s (A B C : TypeCode)
  | app (f x : Term) (A B : TypeCode) (fn arg : FiniteCert)
  | allI (t : Term) (B : TypeCode) (body : FiniteCert)
  | allE (t : Term) (B A : TypeCode) (body : FiniteCert)
  | reduce (t u : Term) (A : TypeCode) (body : FiniteCert) (red : RedCert)
  deriving DecidableEq

def checkFinite : FiniteCert → Term → TypeCode → Bool
  | .i A, t, C => decide (t = .i ∧ C = .arrow A A)
  | .k A B, t, C => decide (t = .k ∧ C = .arrow A (.arrow B A))
  | .s A B C, t, D => decide (t = .s ∧ D =
      .arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C)))
  | .app f x A B p q, t, C => decide (t = .app f x ∧ C = B) &&
      checkFinite p f (.arrow A B) && checkFinite q x A
  | .allI t B p, u, C => decide (u = t ∧ C = .all B) && checkFinite p t B
  | .allE t B A p, u, C => decide (u = t ∧ C = instantiateType B A) && checkFinite p t (.all B)
  | .reduce t u A p r, v, C => decide (v = u ∧ C = A) && checkFinite p t A && checkRed r t u

theorem checkFinite_sound {c : FiniteCert} {t : Term} {A : TypeCode}
    (h : checkFinite c t A = true) : FiniteDerives t A := by
  induction c generalizing t A with
  | i B => simp only [checkFinite, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .i B
  | k B C => simp only [checkFinite, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .k B C
  | s B C D => simp only [checkFinite, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .s B C D
  | app f x B C p q ihp ihq =>
      simp only [checkFinite, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨⟨rfl,rfl⟩,hp⟩,hq⟩
      exact .app (ihp hp) (ihq hq)
  | allI t B p ih =>
      simp only [checkFinite, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl⟩,hp⟩
      exact .allI (ih hp)
  | allE t B C p ih =>
      simp only [checkFinite, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl⟩,hp⟩
      exact .allE (ih hp) C
  | reduce t u B p r ih =>
      simp only [checkFinite, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨⟨rfl,rfl⟩,hp⟩,hr⟩
      exact .reduce (ih hp) (checkRed_sound hr)

theorem finite_complete {t : Term} {A : TypeCode} (h : FiniteDerives t A) :
    ∃ c : FiniteCert, checkFinite c t A = true := by
  induction h with
  | i A => exact ⟨.i A, by simp [checkFinite]⟩
  | k A B => exact ⟨.k A B, by simp [checkFinite]⟩
  | s A B C => exact ⟨.s A B C, by simp [checkFinite]⟩
  | @app f x A B hf hx ihf ihx =>
      obtain ⟨p,hp⟩ := ihf
      obtain ⟨q,hq⟩ := ihx
      exact ⟨.app f x A B p q, by simp [checkFinite,hp,hq]⟩
  | @allI t B h ih =>
      obtain ⟨p,hp⟩ := ih
      exact ⟨.allI t B p, by simp [checkFinite,hp]⟩
  | @allE t B h A ih =>
      obtain ⟨p,hp⟩ := ih
      exact ⟨.allE t B A p, by simp [checkFinite,hp]⟩
  | @reduce t u A h r ih =>
      obtain ⟨p,hp⟩ := ih
      obtain ⟨rc,hrc⟩ := red_complete r
      exact ⟨.reduce t u A p rc, by simp [checkFinite,hp,hrc]⟩

inductive PolyCert : Type where
  | refl (p : Poly)
  | symm (p q : Poly) (child : PolyCert)
  | trans (p q r : Poly) (left right : PolyCert)
  | app (f g p q : Poly) (fn arg : PolyCert)
  | i (p : Poly)
  | k (p q : Poly)
  | s (p q r : Poly)
  | bridge (r t : Term)
  deriving DecidableEq

def checkPoly : PolyCert → Poly → Poly → Bool
  | .refl p, a, b => decide (a = p ∧ b = p)
  | .symm p q c, a, b => decide (a = q ∧ b = p) && checkPoly c p q
  | .trans p q r c d, a, b => decide (a = p ∧ b = r) && checkPoly c p q && checkPoly d q r
  | .app f g p q c d, a, b => decide (a = .app f p ∧ b = .app g q) && checkPoly c f g && checkPoly d p q
  | .i p, a, b => decide (a = .app (.atom .i) p ∧ b = p)
  | .k p q, a, b => decide (a = .app (.app (.atom .k) p) q ∧ b = p)
  | .s p q r, a, b => decide (a = .app (.app (.app (.atom .s) p) q) r ∧ b = .app (.app p r) (.app q r))
  | .bridge r t, a, b => decide (a = .atom (.app r t) ∧ b = .app (.atom r) (.atom t))

theorem checkPoly_sound {c : PolyCert} {p q : Poly}
    (h : checkPoly c p q = true) : PolyConvPlus p q := by
  induction c generalizing p q with
  | refl a => simp only [checkPoly, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .refl _
  | symm a b c ih =>
      simp only [checkPoly, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl⟩,hc⟩
      exact .symm (ih hc)
  | trans a b d c e ihc ihe =>
      simp only [checkPoly, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨⟨rfl,rfl⟩,hc⟩,he⟩
      exact .trans (ihc hc) (ihe he)
  | app f g a b c d ihc ihd =>
      simp only [checkPoly, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨⟨rfl,rfl⟩,hc⟩,hd⟩
      exact .app (ihc hc) (ihd hd)
  | i a => simp only [checkPoly, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .i _
  | k a b => simp only [checkPoly, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .k _ _
  | s a b d => simp only [checkPoly, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .s a b d
  | bridge a b => simp only [checkPoly, decide_eq_true_eq] at h; rcases h with ⟨rfl,rfl⟩; exact .bridge a b

theorem poly_complete {p q : Poly} (h : PolyConvPlus p q) :
    ∃ c : PolyCert, checkPoly c p q = true := by
  induction h with
  | refl p => exact ⟨.refl p, by simp [checkPoly]⟩
  | @symm p q h ih =>
      obtain ⟨c,hc⟩ := ih
      exact ⟨.symm p q c, by simp [checkPoly,hc]⟩
  | @trans p q r h k ih ik =>
      obtain ⟨c,hc⟩ := ih
      obtain ⟨d,hd⟩ := ik
      exact ⟨.trans p q r c d, by simp [checkPoly,hc,hd]⟩
  | @app f g p q h k ih ik =>
      obtain ⟨c,hc⟩ := ih
      obtain ⟨d,hd⟩ := ik
      exact ⟨.app f g p q c d, by simp [checkPoly,hc,hd]⟩
  | i p => exact ⟨.i p, by simp [checkPoly]⟩
  | k p q => exact ⟨.k p q, by simp [checkPoly]⟩
  | s p q r => exact ⟨.s p q r, by simp [checkPoly]⟩
  | bridge r t => exact ⟨.bridge r t, by simp [checkPoly]⟩

inductive LookupCert : Type where
  | zero (Γ : Tel) (A : Ty)
  | succ (Γ : Tel) (n : Nat) (A B : Ty) (child : LookupCert)
  deriving DecidableEq

def checkLookup : LookupCert → Tel → Nat → Ty → Bool
  | .zero Γ A, Δ, n, B => decide (Δ = A :: Γ ∧ n = 0 ∧ B = wk A)
  | .succ Γ n A B c, Δ, k, C =>
      decide (Δ = B :: Γ ∧ k = n+1 ∧ C = wk A) && checkLookup c Γ n A

theorem checkLookup_sound {c : LookupCert} {Γ : Tel} {n : Nat} {A : Ty}
    (h : checkLookup c Γ n A = true) : Lookup Γ n A := by
  induction c generalizing Γ n A with
  | zero Δ B =>
      simp only [checkLookup, decide_eq_true_eq] at h
      rcases h with ⟨rfl,rfl,rfl⟩
      exact .zero
  | succ Δ k B C c ih =>
      simp only [checkLookup, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨⟨rfl,rfl,rfl⟩,hc⟩
      exact .succ (ih hc)

theorem lookup_complete {Γ : Tel} {n : Nat} {A : Ty} (h : Lookup Γ n A) :
    ∃ c : LookupCert, checkLookup c Γ n A = true := by
  induction h with
  | @zero A Γ => exact ⟨.zero Γ A, by simp [checkLookup]⟩
  | @succ Γ n A B h ih =>
      obtain ⟨c,hc⟩ := ih
      exact ⟨.succ Γ n A B c, by simp [checkLookup,hc]⟩

end AuxiliaryCertificates

#print axioms AuxiliaryCertificates.checkStep_sound
#print axioms AuxiliaryCertificates.step_complete
#print axioms AuxiliaryCertificates.checkRed_sound
#print axioms AuxiliaryCertificates.red_complete
#print axioms AuxiliaryCertificates.checkFinite_sound
#print axioms AuxiliaryCertificates.finite_complete
#print axioms AuxiliaryCertificates.checkPoly_sound
#print axioms AuxiliaryCertificates.poly_complete
#print axioms AuxiliaryCertificates.checkLookup_sound
#print axioms AuxiliaryCertificates.lookup_complete
