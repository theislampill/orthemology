import EffectiveRenewalBoundary

namespace RenewalControls
open EffectiveRenewal EffectiveRenewal.Contract EffectiveRenewal.Pruning

-- Known diagonal program index zero evaluates to zero, so its copied bit fails.
example : treeCheck [false] = false := by
  simp [treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
example : treeCheck [true] = true := by
  simp [treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
example : treeCheck [] = true := rfl
example (e : Nat) : diagonal 0 e = none := by simp [diagonal, Nat.Partrec.Code.evaln]

-- Uniform finite successes cannot be silently reclassified as commitments.
example : ¬ Committed finitePlan := finitePlans_not_committed
example : ¬ RootedPruned diagonalTree := diagonal_not_rooted_pruned

-- Changed encodings preserve both consequential state coordinates.
example : encoding 1 (false, true) = (true, false) := by decide
example : encoding 2 (false, true) = (false, true) := by decide
example : readout (false, false) = readout (false, true) := rfl
example : readout (delayStep (false, false) true) ≠ readout (delayStep (false, true) true) := by decide
example : abstractState (migrate (initial (false, true)) true) = (false, true) := by
  rw [migrate_abstract]
  simp [initial, abstractState, encoding, twist]
example : request false false (initial (false, true)) = terminate (initial (false, true)) := by
  exact (revocation_terminates _ _ rfl).1
example : ¬ RenewalStep false true (initial (false, true)) (migrate (initial (false, true)) true) :=
  revoked_no_renewal _ _ _
example : ¬ operativeSupport (migrate (initial (false, true)) true) (.instanceToken 0) :=
  predecessor_token_excluded _ _
example : operativeSupport (migrate (initial (false, true)) true) .commonPlatform := trivial

-- A positive, actually enumerable pruned witness: exactly the all-zero prefixes.
def zeroEnum (n : Nat) : Option Word := some (prefixWord (fun _ => false) n)
theorem zeroEnum_computable : Computable zeroEnum :=
  Computable.option_some.comp (prefixWord_computable _ (Computable.const false))
theorem zeroEnum_exact (s : Word) :
    pathPrefixes (fun _ => false) s ↔ ∃ n, zeroEnum n = some s := by
  constructor
  · intro h; exact ⟨s.length, congrArg some h.symm⟩
  · rintro ⟨n, hn⟩
    have hs : prefixWord (fun _ => false) n = s := Option.some.inj hn
    subst s
    simp [pathPrefixes]

def zeroRun (n : Nat) : Word :=
  (enumRun zeroEnum n).get ((enumRun_good (pathPrefixes (fun _ => false)) zeroEnum
    zeroEnum_exact (pathPrefixes_rooted_pruned _) n).choose_spec.1.1)

example : ∃ f : Nat → Bool, Computable f ∧ ∀ n, (fun _ : Word => True) (prefixWord f n) := by
  exact enumerable_pruned_extracts_path (fun _ => True) (pathPrefixes (fun _ => false))
    (fun _ _ => trivial) (pathPrefixes_rooted_pruned _) ⟨zeroEnum, zeroEnum_computable, zeroEnum_exact⟩

-- Fixed-zero scope is essential: another external history can supply path advice.
example : Computable copyInputObserver := copyInputObserver_computable
example : ∃ env : Environment, (∀ n, (env n).1 = true) ∧
    Committed (controllerSnapshot copyInputObserver env) ∧
    (∀ t, diagonalTree (controllerSnapshot copyInputObserver env t)) ∧
    UnboundedOutput (controllerSnapshot copyInputObserver env) := some_environment_supplies_path_advice

#eval (List.range 12).map (fun n => treeCheck (finitePlan n))
#eval zeroRun 6
#eval request false true (initial (false, true))
#eval finiteProcess 5 [true, false, true, true, false] (false, true)
#eval encoding 1 (false, true)
#eval encoding 2 (false, true)
end RenewalControls
