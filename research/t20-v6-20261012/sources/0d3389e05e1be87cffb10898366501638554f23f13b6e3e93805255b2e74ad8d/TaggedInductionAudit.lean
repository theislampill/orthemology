import TaggedSubstitution
import Lean

/- Check the transitive kernel declaration dependencies, rather than only
   grepping the new source for prohibited completion principles. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``TaggedInduction.dependent_induction,
      ``TaggedInduction.hereditary_nat, ``TaggedInduction.dependent_induction_sound] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for forbidden in [``JointCompletion.sigma_eta, ``JointCompletion.sigma_elimination,
        ``JointCompletion.dependent_induction, ``FullPER.F,
        ``FullPER.TypeLaws, ``FullPER.Fundamental, ``FullPER.ContextLaws] do
      if report.visited.contains forbidden then
        throwError "Forbidden semantic dependency in {target}: {forbidden}"
    logInfo m!"PASS {target}: only standard Lean axioms; no FullPER semantic interpretation, Sigma eta, or joint-completion soundness dependency."
