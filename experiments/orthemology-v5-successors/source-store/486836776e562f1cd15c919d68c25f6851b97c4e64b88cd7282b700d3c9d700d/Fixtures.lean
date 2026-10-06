import Composition
open ComposedExecution
open CriterionInstallation (Rule)

def target : TypedCriterionGuard.Target :=
  ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
   "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")

def plant (bytes : List Nat) : Plant :=
  { source := ⟨target, bytes, ["pinned-source"]⟩, destination := "fixture-A",
    standard := "exact-source-recovery", draft := bytes ++ [10], draftRevision := 8,
    draftHistory := [[88]], rule := .normalizedLF, ruleVersion := 3,
    ruleHistory := [], unrelated := ["retain-custody"] }

def policy (scope : String) (epoch : Nat := 2) : Policy :=
  { target, destination := "fixture-A", actor := "A", scope, epoch,
    grant := some ⟨"A", "fixture-A", target, epoch, 0, 100, scope⟩ }

def installCommand : CriterionInstallation.InstallCommand :=
  { actor := "A", destination := "fixture-A", target, expectedRule := .normalizedLF,
    expectedVersion := 3, authorizationEpoch := 2, newRule := .exact,
    operation := "install-criterion", observedAt := 1, leaseEnd := 90 }

def repairCommand (bytes : List Nat) : TypedCriterionGuard.Command :=
  { actor := "A", destination := "fixture-A", target, criterion := "C1-exact",
    expectedRevision := 8, authorizationEpoch := 3, payload := bytes,
    operation := "replace-derived", observedAt := 1, leaseEnd := 90 }
