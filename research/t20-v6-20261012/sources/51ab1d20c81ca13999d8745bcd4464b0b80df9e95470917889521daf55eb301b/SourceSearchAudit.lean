import SourceSearchControls
import Lean
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``ActualSourceEnumerability.serialCheck_exact,
      ``ActualSourceEnumerability.serialCheck_complete,
      ``ActualSourceEnumerability.primrec_checkCanonical,
      ``ActualSourceEnumerability.runNode_exact,
      ``ActualSourceEnumerability.runList_exact,
      ``ActualSourceEnumerability.checkCanonical_sound,
      ``ActualSourceEnumerability.checkCanonical_exact,
      ``ActualSourceEnumerability.checkCanonical_encode,
      ``ActualSourceEnumerability.derivableCode_iff_certificate,
      ``ActualSourceEnumerability.computable_checkCanonical,
      ``ActualSourceEnumerability.proofSearch_partrec,
      ``ActualSourceEnumerability.proofSearch_nat_partrec,
      ``ActualSourceEnumerability.proofSearch_dom,
      ``ActualSourceEnumerability.proofSearch_mem,
      ``ActualSourceEnumerability.derivableCode_re,
      ``ActualSourceEnumerability.proofSearch_ctxJ,
      ``ActualSourceEnumerability.proofSearch_formJ,
      ``ActualSourceEnumerability.proofSearch_hasJ,
      ``ActualSourceEnumerability.proofSearch_ctxE,
      ``ActualSourceEnumerability.proofSearch_formE,
      ``ActualSourceEnumerability.proofSearch_hasE,
      ``ActualSourceEnumerability.primrec_inhabitantCheck,
      ``ActualSourceEnumerability.inhabitantCheck_sound,
      ``ActualSourceEnumerability.inhabitedTypeCode_iff_candidate,
      ``ActualSourceEnumerability.inhabitantSearch_partrec,
      ``ActualSourceEnumerability.inhabitantSearch_dom,
      ``ActualSourceEnumerability.inhabitedTypeCode_re,
      ``ActualSourceEnumerability.inhabitantSearch_exact,
      ``ActualSourceEnumerability.Controls.invalidClaimSearchUndefined] do
    let (_, audit) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in audit.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for name in audit.visited do
      if name.toString.startsWith "FullPER." || name.toString == "JointCompletion.fundamental" then
        throwError "Semantic oracle in effective source proof {target}: {name}"
    logInfo m!"PASS {target}: standard axioms; no FullPER or source fundamental oracle."
