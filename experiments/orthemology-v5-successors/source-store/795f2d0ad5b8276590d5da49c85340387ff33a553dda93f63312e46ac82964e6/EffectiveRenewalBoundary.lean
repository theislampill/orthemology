import ContractComputability

/-! Integrated assurance statement. All objects below are concrete definitions,
and every constituent is proved; no missing computability or contract result
is packaged as an axiom. -/

namespace EffectiveRenewal

/-- Standard computability mechanism plus the programme-specific finite contract
lift. The final negative quantifier fixes the always-authorised zero-input
history and an effective observer containing all counted technical support. -/
theorem effective_renewal_boundary :
    Primrec treeCheck ∧ diagonalTree [] ∧ PrefixClosed diagonalTree ∧
    Primrec finitePlan ∧
    (∀ n, (finitePlan n).length = n ∧ diagonalTree (finitePlan n)) ∧
    (∃ f : Nat → Bool, ∀ n, diagonalTree (prefixWord f n)) ∧
    (∀ n inputs q, Contract.Run (Contract.initial q) (Contract.serviceInputs inputs 0 n)
      (Contract.configurationAt (finitePlan n) inputs q n)) ∧
    (∀ observer : Contract.Observer, Computable observer →
      Committed (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero) →
      (∀ t, diagonalTree (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero t)) →
      ¬ UnboundedOutput (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero)) :=
  ⟨treeCheck_primrec, diagonalTree_empty, fun hp ht => diagonalTree_prefix_closed hp ht,
    finitePlan_primrec, fun n => ⟨length_finitePlan n, finitePlan_admitted n⟩,
    exists_mathematical_path, Contract.finite_plan_whole_run,
    Contract.no_supported_zero_input_renewal⟩

/-- The executable finite controller is itself primitive recursive and realises
an actual finite contract-preserving run with exactly the requested renewals. -/
theorem executable_finite_contract_controller :
    (Primrec fun p : Nat × (Word × Contract.State) => Contract.finiteProcess p.1 p.2.1 p.2.2) ∧
    ∀ n inputs q, (Contract.finiteProcess n inputs q).1.length = n ∧
      Contract.Run (Contract.initial q) (Contract.serviceInputs (fun k => inputs.getD k false) 0 n)
        (Contract.finiteProcess n inputs q) :=
  ⟨Contract.finiteProcess_primrec, fun n inputs q =>
    ⟨Contract.finiteProcess_length n inputs q, Contract.finiteProcess_run n inputs q⟩⟩

/-- The exact positive criterion does not require decidability of the ambient
predicate. In particular it holds for every decidable binary tree. -/
theorem exact_effective_pruning_criterion (T : Word → Prop) :
    ((∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n)) ↔
      ∃ R : Word → Prop, (∀ s, R s → T s) ∧ Pruning.RootedPruned R ∧
        Pruning.ComputablyDecidable R) ∧
    ((∃ f : Nat → Bool, Computable f ∧ ∀ n, T (prefixWord f n)) ↔
      ∃ R : Word → Prop, (∀ s, R s → T s) ∧ Pruning.RootedPruned R ∧
        Pruning.Enumerable R) :=
  ⟨Pruning.computable_path_iff_decidable_pruned T,
    Pruning.computable_path_iff_enumerable_pruned T⟩

end EffectiveRenewal
