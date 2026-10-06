/- Interfaces from semantic validity to the existing sound typing systems.
   These are not a kernel proof of recursive enumerability or non-enumerability. -/
import EffectiveReduction
import ExtensionalRepairTheorems

namespace P01AC.EffectiveCompleteness
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- Existence of an arbitrary semantic proof has exactly the literal-I target. -/
theorem semantic_proof_exists_iff_valid (p q : Poly) :
    (∃ e : Poly, ∀ r : REnv, G (.identity C p q) r zeroEnv zeroEnv
      (eval e zeroEnv) (eval e zeroEnv)) ↔ IdentityValid p q := by
  constructor
  · rintro ⟨e, he⟩
    apply (identity_valid_iff_endpoint_valid p q).mpr
    intro ρ
    exact (he (diagEnv ρ)).1
  · intro h
    exact ⟨.atom .i, h⟩

theorem target_scope_bundle (G O : Term) (c : Nat) :
    TyScoped 0 (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) ∧
    Intensional.TyParamScoped 0
      (.identity C (tester G O (numeral c)) (constantRaw (numeral 0))) := by
  refine ⟨form_scoped (target_formed G O c), ?_⟩
  change ((0 < 1 ∧ 0 < 1) ∧ (0 < 1 ∧ 0 < 1)) ∧ True
  exact ⟨⟨⟨Nat.zero_lt_succ 0, Nat.zero_lt_succ 0⟩,
    ⟨Nat.zero_lt_succ 0, Nat.zero_lt_succ 0⟩⟩, trivial⟩

theorem infinite_typed_family :
    ∃ f : Nat → Poly, (∀ n, Has [] (f n) C) ∧
      ∀ m n, EndpointValid (f m) (f n) → m = n := by
  exact ⟨fun n => constantRaw (iterateTerm .zero n .one),
    fun n => constantRaw_has _, typed_constant_family_distinct⟩

theorem hasE_identity_implies_valid {e p q : Poly}
    (h : ExtensionalRepair.HasE [] e (.identity C p q)) : IdentityValid p q := by
  apply (identity_valid_iff_endpoint_valid p q).mpr
  intro ρ
  exact (ExtensionalRepair.unary_fundamental h (ρ := ρ) ⟨rfl, rfl⟩).1

theorem current_identity_implies_valid {e p q : Poly}
    (h : Has [] e (.identity C p q)) : IdentityValid p q :=
  hasE_identity_implies_valid (ExtensionalRepair.has_inclusion h)

theorem hasE_target_implies_run_zero {g o : Nat → Nat} {G O : Term}
    (hg : Represents g G) (ho : Represents o O) (c : Nat) {e : Poly}
    (h : ExtensionalRepair.HasE [] e
      (.identity C (tester G O (numeral c)) (constantRaw (numeral 0)))) :
    ∀ n, o (run g c n) = 0 :=
  (original_identity_iff_run_zero hg ho c).mp (hasE_identity_implies_valid h)

theorem current_target_implies_run_zero {g o : Nat → Nat} {G O : Term}
    (hg : Represents g G) (ho : Represents o O) (c : Nat) {e : Poly}
    (h : Has [] e
      (.identity C (tester G O (numeral c)) (constantRaw (numeral 0)))) :
    ∀ n, o (run g c n) = 0 :=
  (original_identity_iff_run_zero hg ho c).mp (current_identity_implies_valid h)

end P01AC.EffectiveCompleteness
