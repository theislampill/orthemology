import EffectiveBooleanInterfaces
import EffectiveBooleanControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive

example : N = Ty.all (arr (arr (.param 0) (.param 0)) (arr (.param 0) (.param 0))) := rfl
example (n : Nat) : canonical n = eval (inputNumeral n) zeroEnv := rfl
example : CB = arr N (.all (arr (.param 0) (arr (.param 0) (.param 0)))) := rfl
example {t : Term} {ρ : OEnv} {η : Env} (h : F B ρ η t t) :
    ∃ b : Bool, ∀ x y, Conv (.app (.app t x) y) (pick b x y) := boolean_standardness h
example {p q : Poly} (hp : Has [] p CB) (hq : Has [] q CB) :
    BoolValid p q ↔ BoolTests p q := bool_valid_iff_tests hp hq
example {p q : Poly} (hp : Has [] p CB) (hq : Has [] q CB) :
    ¬ BoolValid p q ↔ Mismatch p q := invalid_iff_mismatch hp hq
example {r : Nat} (f : PR r) : Has (NatCtx r) f.compile N := f.compile_has
example {r : Nat} (f : PR r) (η : Env) (v : Nat → Nat) (h : EnvNat r η v) :
    NatObs (eval f.compile η) (f.denote v) := f.compile_obs η v h
example (f : PR 2) : Has [] (simulator f) (arr N (arr N B)) := simulator_has f
example (f : PR 2) (e : Nat) :
    P01AC.BooleanIdentity.IdentityValid (simFamily f e) constantChoice ↔
      ∀ n, f.denote (inputs n e) = 0 := original_identity_iff_all_zero f e
example (f : PR 2) (e : Nat) :
    Form [] (.identity CB (simFamily f e) constantChoice) := family_identity_formed f e
example {e p q : Poly} (h : Has [] e (.identity CB p q)) : BoolValid p q :=
  P01AC.BooleanIdentity.current_identity_implies_valid h
