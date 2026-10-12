import AuxiliaryCertificates
namespace IndependentAuxiliarySourceReview
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000
-- This module imports only the retained source checker, never candidate exactness.
theorem step_i (x t u : Term) : checkStep (.i x) t u = decide (t = .app .i x ∧ u = x) := rfl
theorem step_k (x y t u : Term) : checkStep (.k x y) t u = decide (t = .app (.app .k x) y ∧ u = x) := rfl
theorem step_s (f g x t u : Term) : checkStep (.s f g x) t u = decide (t = .app (.app (.app .s f) g) x ∧ u = .app (.app f x) (.app g x)) := rfl
theorem step_left (f g x t u : Term) (c : StepCert) : checkStep (.left f g x c) t u = (decide (t = .app f x ∧ u = .app g x) && checkStep c f g) := rfl
theorem step_right (f x y t u : Term) (c : StepCert) : checkStep (.right f x y c) t u = (decide (t = .app f x ∧ u = .app f y) && checkStep c x y) := rfl
theorem red_refl (t a b : Term) : checkRed (.refl t) a b = decide (a = t ∧ b = t) := rfl
theorem red_tail (t u v a b : Term) (s : StepCert) (r : RedCert) : checkRed (.tail t u v s r) a b = (decide (a = t ∧ b = v) && checkStep s t u && checkRed r u v) := rfl

theorem finite_i (A C : TypeCode) (t : Term) : checkFinite (.i A) t C = decide (t = .i ∧ C = .arrow A A) := rfl
theorem finite_k (A B C : TypeCode) (t : Term) : checkFinite (.k A B) t C = decide (t = .k ∧ C = .arrow A (.arrow B A)) := rfl
theorem finite_s (A B C D : TypeCode) (t : Term) : checkFinite (.s A B C) t D = decide (t = .s ∧ D = .arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C))) := rfl
theorem finite_app (f x t : Term) (A B C : TypeCode) (p q : FiniteCert) : checkFinite (.app f x A B p q) t C = (decide (t = .app f x ∧ C = B) && checkFinite p f (.arrow A B) && checkFinite q x A) := rfl
theorem finite_allI (t u : Term) (B C : TypeCode) (p : FiniteCert) : checkFinite (.allI t B p) u C = (decide (u = t ∧ C = .all B) && checkFinite p t B) := rfl
theorem finite_allE (t u : Term) (B A C : TypeCode) (p : FiniteCert) : checkFinite (.allE t B A p) u C = (decide (u = t ∧ C = instantiateType B A) && checkFinite p t (.all B)) := rfl
theorem finite_reduce (t u v : Term) (A C : TypeCode) (p : FiniteCert) (r : RedCert) : checkFinite (.reduce t u A p r) v C = (decide (v = u ∧ C = A) && checkFinite p t A && checkRed r t u) := rfl

theorem poly_refl (p a b : Poly) : checkPoly (.refl p) a b = decide (a = p ∧ b = p) := rfl
theorem poly_symm (p q a b : Poly) (c : PolyCert) : checkPoly (.symm p q c) a b = (decide (a = q ∧ b = p) && checkPoly c p q) := rfl
theorem poly_trans (p q r a b : Poly) (c d : PolyCert) : checkPoly (.trans p q r c d) a b = (decide (a = p ∧ b = r) && checkPoly c p q && checkPoly d q r) := rfl
theorem poly_app (f g p q a b : Poly) (c d : PolyCert) : checkPoly (.app f g p q c d) a b = (decide (a = .app f p ∧ b = .app g q) && checkPoly c f g && checkPoly d p q) := rfl
theorem poly_i (p a b : Poly) : checkPoly (.i p) a b = decide (a = .app (.atom .i) p ∧ b = p) := rfl
theorem poly_k (p q a b : Poly) : checkPoly (.k p q) a b = decide (a = .app (.app (.atom .k) p) q ∧ b = p) := rfl
theorem poly_s (p q r a b : Poly) : checkPoly (.s p q r) a b = decide (a = .app (.app (.app (.atom .s) p) q) r ∧ b = .app (.app p r) (.app q r)) := rfl
theorem poly_bridge (r t : Term) (a b : Poly) : checkPoly (.bridge r t) a b = decide (a = .atom (.app r t) ∧ b = .app (.atom r) (.atom t)) := rfl

theorem lookup_zero (Γ Δ : Tel) (A B : Ty) (n : Nat) : checkLookup (.zero Γ A) Δ n B = decide (Δ = A :: Γ ∧ n = 0 ∧ B = wk A) := rfl
theorem lookup_succ (Γ Δ : Tel) (A B C : Ty) (n k : Nat) (c : LookupCert) : checkLookup (.succ Γ n A B c) Δ k C = (decide (Δ = B :: Γ ∧ k = n+1 ∧ C = wk A) && checkLookup c Γ n A) := rfl

-- Discriminating nested/concrete tests, independent of codec/exactness.
def nestedBody : TypeCode := .all (.arrow (.var 1) (.var 1))
def polyIdentity : FiniteCert := .allI .i nestedBody (.allI .i (.arrow (.var 1) (.var 1)) (.i (.var 1)))
def instCert : FiniteCert := .allE .i nestedBody (.var 2) polyIdentity
theorem allE_capture_avoiding : checkFinite instCert .i (.all (.arrow (.var 3) (.var 3))) = true := by decide
theorem allE_capture_reject : checkFinite instCert .i (.all (.arrow (.var 2) (.var 2))) = false := by decide

def idType : TypeCode := .arrow .bottom .bottom
def typedII : FiniteCert := .app .i .i idType idType (.i idType) (.i .bottom)
def redII : RedCert := .tail (.app .i .i) .i .i (.i .i) (.refl .i)
theorem reduce_valid : checkFinite (.reduce (.app .i .i) .i idType typedII redII) .i idType = true := by decide
theorem reduce_wrong_start : checkFinite (.reduce (.app .i .i) .i idType typedII (.refl .i)) .i idType = false := by decide

def A (n : Nat) : Ty := .identity .raw (.var n) (.var n)
def lookup0 : LookupCert := .zero [] (A 0)
def lookup1 : LookupCert := .succ [A 0] 0 (A 1) .raw lookup0
def lookup2 : LookupCert := .succ [.raw,A 0] 1 (A 2) .bottom lookup1
theorem repeated_wk : checkLookup lookup2 [.bottom,.raw,A 0] 2 (A 3) = true := by decide
theorem one_wk_missing : checkLookup lookup2 [.bottom,.raw,A 0] 2 (A 2) = false := by decide
theorem wrong_context : checkLookup lookup2 [.raw,.bottom,A 0] 2 (A 3) = false := by decide

theorem bad_step_child : checkStep (.right .s (.app .i .k) .k (.i .s)) (.app .s (.app .i .k)) (.app .s .k) = false := by decide
theorem bad_reduction_middle : checkRed (.tail (.app .i .k) .s .s (.i .k) (.refl .s)) (.app .i .k) .s = false := by decide
theorem reversed_symmetry : checkPoly (.symm (.app (.atom .i) (.var 0)) (.var 0) (.i (.var 0))) (.var 0) (.app (.atom .i) (.var 0)) = true := by decide
theorem wrong_symmetry : checkPoly (.symm (.app (.atom .i) (.var 0)) (.var 0) (.i (.var 0))) (.app (.atom .i) (.var 0)) (.var 0) = false := by decide
theorem disconnected_trans : checkPoly (.trans (.var 0) (.var 1) (.var 0) (.refl (.var 0)) (.refl (.var 0))) (.var 0) (.var 0) = false := by decide
theorem swapped_bridge : checkPoly (.bridge .i .k) (.app (.atom .i) (.atom .k)) (.atom (.app .i .k)) = false := by decide
theorem collapsed_bridge : checkPoly (.bridge .i .k) (.app (.atom .i) (.atom .k)) (.app (.atom .i) (.atom .k)) = false := by decide
end IndependentAuxiliarySourceReview
