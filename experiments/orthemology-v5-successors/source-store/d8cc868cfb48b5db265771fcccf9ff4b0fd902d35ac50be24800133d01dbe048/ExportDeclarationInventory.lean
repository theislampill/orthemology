import PolynomialTestBoundary
import PolynomialTestAudit
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
import PositiveSeparation
import RestrictedCompiler
import SparsePolynomial
import SubstitutionSyntax
import TypedAlgebra
import TypedStructural
import TypedSyntax
import Lean.Elab.Command
open Lean Elab Command
namespace UnifiedDeclarationInventory

def modules : Array Name := #[`AllBaseLaws, `AllBinderLaws, `AllConstants, `AllFiniteComparison, `AllInheritedPositiveControls, `AllInstantiation, `AllMixedAlgebra, `AllNucleusSyntax, `AllPiLaws, `AllPredicates, `AllRawRenaming, `AllRawSubstitution, `AllSemanticSubstitution, `AllSigmaLaws, `AllSoundness, `AllStructural, `AllStructuralBase, `AllStructuralRename, `AllSyntax, `AllTermAlgebra, `AllTermLemmas, `BareBooleanGatePositive, `BareBooleanGateSyntax, `BoundaryResults, `CheckerControls, `CheckerKernelAudit, `ComputablePrelude, `EffectiveBooleanCertificates, `EffectiveBooleanControls, `EffectiveBooleanInterfaces, `EffectiveBooleanStandardness, `EffectiveCanonicalTests, `EffectiveObserver, `EffectivePartialObserver, `EffectivePrimitiveRecursion, `EffectiveReduction, `EffectiveRuleBoundary, `EffectiveStandardness, `EffectsAndDependence, `ExtensionalRepairAudit, `ExtensionalRepairLemmas, `ExtensionalRepairSoundness, `ExtensionalRepairSyntax, `ExtensionalRepairTheorems, `ExtensionalRepairWitness, `FiniteBridge, `IdentityChecker, `IntensionalIdentityBridge, `IntensionalIdentityModel, `IntensionalIdentityRelations, `IntensionalIdentitySoundness, `IntensionalIdentityTheorems, `IntensionalIdentityWitness, `InternalPolymorphism, `MaskNormalisation, `NormalisationAndNumerals, `P01Candidates, `P01CanonicalCarrierProjection, `P01Certificates, `P01Confluence, `P01ContextualJ, `P01CurryParametricity, `P01DependentControls, `P01DependentCore, `P01DependentFundamental, `P01DependentModel, `P01DependentRepresentation, `P01DependentSubstitution, `P01Examples, `P01LambdaSyntax, `P01ModelWitnesses, `P01Omega, `P01PER, `P01Polynomials, `P01RecursiveModel, `P01SNReflection, `P01SystemF, `P01Translation, `P01TypeAlgebra, `PolynomialTestAudit, `PolynomialTestBoundary, `PositiveSeparation, `RestrictedCompiler, `SparsePolynomial, `SubstitutionSyntax, `TypedAlgebra, `TypedStructural, `TypedSyntax]
run_cmd do
  let env ← getEnv
  let mut rows : Array Json := #[]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let modName := env.header.moduleNames[idx.toNat]!
      if modules.contains modName then
        rows := rows.push <| Json.mkObj [
          ("module", toJson modName.toString),
          ("name", toJson name.toString),
          ("theorem", toJson info.isTheorem),
          ("unsafe", toJson info.isUnsafe),
          ("partial", toJson info.isPartial)]
  liftIO <| IO.FS.createDirAll ".verification-results"
  liftIO <| IO.FS.writeFile ".verification-results/declaration-inventory.json" (Json.pretty (toJson rows))
  logInfo m!"DECLARATION_INVENTORY_PASS modules={modules.size}; declarations={rows.size}"
end UnifiedDeclarationInventory
