/- Independent exact interface controls for the four semantic-reduction modules.
   These intentionally claim no raw representer existence or computability result. -/
import EffectiveRuleBoundary

open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.EffectiveCompleteness

-- Literal original model, fixed carrier, and the three different encodings.
example : N = .all (arr (arr (.param 0) (.param 0)) (arr (.param 0) (.param 0))) := rfl
example : C = arr N .raw := rfl
example : numericB = .app (.app .s (.app .k .s)) .k := rfl
example : numeral 0 = .app .k .i := rfl
example (n : Nat) : numeral (n+1) = .app (.app .s numericB) (numeral n) := rfl
example (n : Nat) : inputNumeral n = abstract (abstract (iterationPoly n)) := rfl
example (g : Nat → Nat) (G : Term) : Represents g G =
    (∀ n, Conv (.app G (numeral n)) (numeral (g n))) := rfl
example (p q : Poly) : EndpointValid p q =
    (∀ ρ : OEnv, F C ρ zeroEnv (eval p zeroEnv) (eval q zeroEnv)) := rfl
example (p q : Poly) : IdentityValid p q =
    (∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv .i .i) := rfl

-- No MarkerFree, Has, closure, or normality premise on the raw semantic input.
example {t : Term} {ρ : OEnv} {η : Env} (ht : F N ρ η t t) :
    ∃ n, ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x) :=
  semantic_church_standardness ht
example (f x : Term) : Link rawPER rawPER := orbitLink f x
example {m n : Nat} (h : Conv (iterateTerm .zero m .one) (iterateTerm .zero n .one)) :
    m = n := marker_conv_injective h

-- Direct current typing, plus both term and type-parameter scope.
example {Γ : Tel} (hΓ : Ctx Γ) : Form Γ N := N_form hΓ
example {Γ : Tel} (hΓ : Ctx Γ) : Form Γ C := C_form hΓ
example {Γ : Tel} (hΓ : Ctx Γ) (G : Term) : Has Γ (rawStep G) (arr .raw .raw) :=
  rawStep_has hΓ G
example (G O c : Term) : Has [] (tester G O c) C := tester_has G O c
example (c : Term) : Has [] (constantRaw c) C := constantRaw_has c
example (n : Nat) : Has [] (inputNumeral n) N := inputNumeral_has n
example (G O : Term) (c : Nat) :
    Form [] (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) :=
  target_formed G O c
example (G O : Term) (c : Nat) :
    Scoped 0 (tester G O (numeral c)) ∧ Scoped 0 (constantRaw (numeral 0)) :=
  target_closed G O c
example (G O : Term) (c : Nat) :
    TyScoped 0 (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) ∧
      Intensional.TyParamScoped 0
        (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) :=
  target_scope_bundle G O c

-- Applied beta only; no equation of unapplied abstractions is requested.
example (G x : Term) : Conv (.app (stepTerm G) x) (.app G x) := rawStep_application G x
example (G O c t : Term) : Conv (.app (eval (tester G O c) zeroEnv) t)
    (.app O (.app (.app t (stepTerm G)) c)) := tester_application G O c t
example (c t : Term) : Conv (.app (eval (constantRaw c) zeroEnv) t) c :=
  constantRaw_application c t
example (n : Nat) (f x : Term) (η : Env) :
    Conv (.app (.app (eval (inputNumeral n) η) f) x) (iterateTerm f n x) :=
  inputNumeral_applied n f x η
example (m n : Nat) : Conv (numeral m) (numeral n) ↔ m = n := numeral_conversion_iff m n
example : ¬ Conv (numeral 0) (numeral 1) := numeric_outputs_separate
example {g : Nat → Nat} {G : Term} (hg : Represents g G) (c n : Nat) :
    Conv (iterateTerm (stepTerm G) n (numeral c)) (numeral (run g c n)) :=
  iteration_representation hg c n
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c n : Nat) : Conv (.app O (iterateTerm (stepTerm G) n (numeral c)))
      (numeral (o (run g c n))) := observation_representation hg ho c n

-- Cross-argument F and all-r G, not a pointwise or diagonal replacement.
example (p q : Poly) : IdentityValid p q ↔ EndpointValid p q :=
  identity_valid_iff_endpoint_valid p q
example (p q : Poly) :
    (∀ ρ : OEnv, F (.identity C p q) ρ zeroEnv .i .i) ↔ EndpointValid p q :=
  identity_unary_iff_endpoint_valid p q
example (G O c z : Term) : EndpointValid (tester G O c) (constantRaw z) ↔
    ∀ n, Conv (.app O (iterateTerm (stepTerm G) n c)) z :=
  endpoint_valid_iff_observations G O c z
example (G O c z : Term) (h : ∀ n, Conv (.app O (iterateTerm (stepTerm G) n c)) z)
    (ρ : OEnv) (x y : Term) (hxy : F N ρ zeroEnv x y) :
    Conv (.app (eval (tester G O c) zeroEnv) x)
      (.app (eval (constantRaw z) zeroEnv) y) := by
  have hv := (endpoint_valid_iff_observations G O c z).mpr h ρ
  rw [C, F_arr] at hv
  exact hv x y hxy

-- Both directions have both representation premises, no restriction on g or o.
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) :
    (∀ r : REnv, P01AC.G (.identity C (tester G O (numeral c))
      (constantRaw (numeral 0))) r zeroEnv zeroEnv .i .i) ↔
      ∀ n, o (run g c n) = 0 := original_identity_iff_run_zero hg ho c
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) (h : IdentityValid (tester G O (numeral c)) (constantRaw (numeral 0))) :
    ∀ n, o (run g c n) = 0 := (original_identity_iff_run_zero hg ho c).mp h
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) (h : ∀ n, o (run g c n) = 0) :
    IdentityValid (tester G O (numeral c)) (constantRaw (numeral 0)) :=
  (original_identity_iff_run_zero hg ho c).mpr h

-- Existential proof interface and sound current / HasE consequences.
example (p q : Poly) :
    (∃ e : Poly, ∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv
      (eval e zeroEnv) (eval e zeroEnv)) ↔ IdentityValid p q :=
  semantic_proof_exists_iff_valid p q
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) :
    (∃ e : Poly, ∀ r : REnv, P01AC.G (.identity C (tester G O (numeral c))
      (constantRaw (numeral 0))) r zeroEnv zeroEnv (eval e zeroEnv) (eval e zeroEnv)) ↔
        ∀ n, o (run g c n) = 0 :=
  (semantic_proof_exists_iff_valid _ _).trans (original_identity_iff_run_zero hg ho c)
example {e p q : Poly} (h : Has [] e (.identity C p q)) : IdentityValid p q :=
  current_identity_implies_valid h
example {e p q : Poly} (h : ExtensionalRepair.HasE [] e (.identity C p q)) :
    IdentityValid p q := hasE_identity_implies_valid h
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) {e : Poly}
    (h : Has [] e (.identity C (tester G O (numeral c)) (constantRaw (numeral 0)))) :
    ∀ n, o (run g c n) = 0 := current_target_implies_run_zero hg ho c h
example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) {e : Poly}
    (h : ExtensionalRepair.HasE [] e
      (.identity C (tester G O (numeral c)) (constantRaw (numeral 0)))) :
    ∀ n, o (run g c n) = 0 := hasE_target_implies_run_zero hg ho c h
example : ∃ f : Nat → Poly, (∀ n, Has [] (f n) C) ∧
    ∀ m n, EndpointValid (f m) (f n) → m = n := infinite_typed_family

#check @original_identity_iff_run_zero
#check @semantic_church_standardness
#check @semantic_proof_exists_iff_valid
