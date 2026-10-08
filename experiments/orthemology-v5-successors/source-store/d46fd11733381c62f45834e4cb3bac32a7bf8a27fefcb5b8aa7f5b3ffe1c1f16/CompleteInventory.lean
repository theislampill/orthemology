import AllBaseLaws
import AllBinderLaws
import AllConstants
import AllFiniteComparison
import AllInheritedPositiveControls
import AllInstantiation
import AllMixedAlgebra
import AllNucleusSyntax
import AllPiLaws
import AllPredicates
import AllRawRenaming
import AllRawSubstitution
import AllSemanticSubstitution
import AllSigmaLaws
import AllSoundness
import AllStructural
import AllStructuralBase
import AllStructuralRename
import AllSyntax
import AllTermAlgebra
import AllTermLemmas
import BareBooleanGatePositive
import BareBooleanGateSyntax
import BoundaryResults
import CheckerControls
import CheckerKernelAudit
import ComputablePrelude
import EffectiveBooleanCertificates
import EffectiveBooleanControls
import EffectiveBooleanInterfaces
import EffectiveBooleanStandardness
import EffectiveCanonicalTests
import EffectiveObserver
import EffectivePartialObserver
import EffectivePrimitiveRecursion
import EffectiveReduction
import EffectiveRuleBoundary
import EffectiveStandardness
import EffectsAndDependence
import ExtensionalRepairAudit
import ExtensionalRepairLemmas
import ExtensionalRepairSoundness
import ExtensionalRepairSyntax
import ExtensionalRepairTheorems
import ExtensionalRepairWitness
import FiniteBridge
import IdentityChecker
import IntensionalIdentityBridge
import IntensionalIdentityModel
import IntensionalIdentityRelations
import IntensionalIdentitySoundness
import IntensionalIdentityTheorems
import IntensionalIdentityWitness
import InternalPolymorphism
import MaskNormalisation
import NormalisationAndNumerals
import P01Candidates
import P01CanonicalCarrierProjection
import P01Certificates
import P01Confluence
import P01ContextualJ
import P01CurryParametricity
import P01DependentControls
import P01DependentCore
import P01DependentFundamental
import P01DependentModel
import P01DependentRepresentation
import P01DependentSubstitution
import P01Examples
import P01LambdaSyntax
import P01ModelWitnesses
import P01Omega
import P01PER
import P01Polynomials
import P01RecursiveModel
import P01SNReflection
import P01SystemF
import P01Translation
import P01TypeAlgebra
import PolynomialTestAudit
import PolynomialTestBoundary
import PositiveSeparation
import RestrictedCompiler
import SparsePolynomial
import SubstitutionSyntax
import TypedAlgebra
import TypedStructural
import TypedSyntax
import EffectiveTree
import CommittedOutput
import PrunedWitness
import RenewalContract
import ContractComputability
import EffectiveRenewalBoundary
import LookaheadFiniteSearch
import LookaheadAdmission
import LookaheadBoundary
import PolicySynthesisReduction
import ProgressCuts
import ReductionBasics
import ResetComponent
import SkeletonUnion
import UnaryPolynomial
import UnaryFiniteDescription
import UnaryExpressions
import UnaryNormalForm
import UnaryWitnesses
import UnaryExpressivity
import UnaryCurrentIdentityBoundary
import UnaryCertificateSyntax
import UnaryCertificateSoundness
import GlobalProofClosure
import Lean.Elab.Command
import Lean.Util.CollectAxioms
open Lean Elab Command
namespace SixteenthRecoveredCompleteInventory

def modules : Array Name := #[`AllBaseLaws, `AllBinderLaws, `AllConstants, `AllFiniteComparison, `AllInheritedPositiveControls, `AllInstantiation, `AllMixedAlgebra, `AllNucleusSyntax, `AllPiLaws, `AllPredicates, `AllRawRenaming, `AllRawSubstitution, `AllSemanticSubstitution, `AllSigmaLaws, `AllSoundness, `AllStructural, `AllStructuralBase, `AllStructuralRename, `AllSyntax, `AllTermAlgebra, `AllTermLemmas, `BareBooleanGatePositive, `BareBooleanGateSyntax, `BoundaryResults, `CheckerControls, `CheckerKernelAudit, `ComputablePrelude, `EffectiveBooleanCertificates, `EffectiveBooleanControls, `EffectiveBooleanInterfaces, `EffectiveBooleanStandardness, `EffectiveCanonicalTests, `EffectiveObserver, `EffectivePartialObserver, `EffectivePrimitiveRecursion, `EffectiveReduction, `EffectiveRuleBoundary, `EffectiveStandardness, `EffectsAndDependence, `ExtensionalRepairAudit, `ExtensionalRepairLemmas, `ExtensionalRepairSoundness, `ExtensionalRepairSyntax, `ExtensionalRepairTheorems, `ExtensionalRepairWitness, `FiniteBridge, `IdentityChecker, `IntensionalIdentityBridge, `IntensionalIdentityModel, `IntensionalIdentityRelations, `IntensionalIdentitySoundness, `IntensionalIdentityTheorems, `IntensionalIdentityWitness, `InternalPolymorphism, `MaskNormalisation, `NormalisationAndNumerals, `P01Candidates, `P01CanonicalCarrierProjection, `P01Certificates, `P01Confluence, `P01ContextualJ, `P01CurryParametricity, `P01DependentControls, `P01DependentCore, `P01DependentFundamental, `P01DependentModel, `P01DependentRepresentation, `P01DependentSubstitution, `P01Examples, `P01LambdaSyntax, `P01ModelWitnesses, `P01Omega, `P01PER, `P01Polynomials, `P01RecursiveModel, `P01SNReflection, `P01SystemF, `P01Translation, `P01TypeAlgebra, `PolynomialTestAudit, `PolynomialTestBoundary, `PositiveSeparation, `RestrictedCompiler, `SparsePolynomial, `SubstitutionSyntax, `TypedAlgebra, `TypedStructural, `TypedSyntax, `EffectiveTree, `CommittedOutput, `PrunedWitness, `RenewalContract, `ContractComputability, `EffectiveRenewalBoundary, `LookaheadFiniteSearch, `LookaheadAdmission, `LookaheadBoundary, `PolicySynthesisReduction, `ProgressCuts, `ReductionBasics, `ResetComponent, `SkeletonUnion, `UnaryPolynomial, `UnaryFiniteDescription, `UnaryExpressions, `UnaryNormalForm, `UnaryWitnesses, `UnaryExpressivity, `UnaryCurrentIdentityBoundary, `UnaryCertificateSyntax, `UnaryCertificateSoundness]
run_cmd do
  let env ← getEnv
  for modName in modules do
    unless env.header.moduleNames.contains modName do throwError "MISSING_IMPORTED_PROJECT_MODULE {modName}"
  liftIO <| IO.FS.writeFile "module-inventory.json" (Json.pretty (toJson (modules.map Name.toString)))
  let mut rows : Array Json := #[]
  let mut proofs : Array Name := #[]
  let mut excluded : Array Json := #[]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let modName := env.header.moduleNames[idx.toNat]!
      if modules.contains modName then
        rows := rows.push <| Json.mkObj [
          ("module", toJson modName.toString), ("name", toJson name.toString),
          ("theorem", toJson info.isTheorem), ("unsafe", toJson info.isUnsafe),
          ("partial", toJson info.isPartial)]
        if info.isTheorem then
          if info.isUnsafe || info.isPartial then throwError "THEOREM_EXCLUSION_FORBIDDEN {name}"
          proofs := proofs.push name
        else if info.isUnsafe || info.isPartial then
          excluded := excluded.push <| Json.mkObj [
            ("module", toJson modName.toString), ("name", toJson name.toString),
            ("reason", toJson "explicit nonproof compiler/runtime auxiliary; never a theorem exclusion")]
  unless proofs.size > 0 do throwError "EMPTY_THEOREM_ROOT_SCOPE"
  let (closure, axioms) ← RecoveredIntegrationAudit.auditFullProofClosure proofs
  liftIO <| IO.FS.writeFile "declaration-inventory.json" (Json.pretty (toJson rows))
  liftIO <| IO.FS.writeFile "proof-roots.json" (Json.pretty (toJson (proofs.map Name.toString)))
  liftIO <| IO.FS.writeFile "nonproof-auxiliary-exclusions.json" (Json.pretty (toJson excluded))
  logInfo m!"RECOVERED_COMPLETE_PROOF_COVERAGE_PASS modules={modules.size}; declarations={rows.size}; theoremRoots={proofs.size}; closure={closure}; logicalOnly=true; axioms={axioms}; excludedNonproof={excluded.size}"
end SixteenthRecoveredCompleteInventory
