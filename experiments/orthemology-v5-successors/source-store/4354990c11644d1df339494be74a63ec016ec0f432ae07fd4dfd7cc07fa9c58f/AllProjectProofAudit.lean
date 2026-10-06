import PolynomialTestBoundary
import PolynomialTestAudit
import BareBooleanGatePositive
import BareBooleanGateSyntax
import CheckerControls
import CheckerKernelAudit
import ComputablePrelude
import IdentityChecker
import MaskNormalisation
import PositiveSeparation
import RestrictedCompiler
import SparsePolynomial
/- Independent, module-selected proof audit of archived project outputs. -/
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
import BoundaryResults
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
import IntensionalIdentityBridge
import IntensionalIdentityModel
import IntensionalIdentityRelations
import IntensionalIdentitySoundness
import IntensionalIdentityTheorems
import IntensionalIdentityWitness
import InternalPolymorphism
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
import SubstitutionSyntax
import TypedAlgebra
import TypedStructural
import TypedSyntax
import Lean.Elab.Command
import Lean.Util.CollectAxioms
open Lean Elab Command
namespace IndependentAllProjectProofAudit

def modules : Array Name := #[`AllBaseLaws, `AllBinderLaws, `AllConstants, `AllFiniteComparison, `AllInheritedPositiveControls, `AllInstantiation, `AllMixedAlgebra, `AllNucleusSyntax, `AllPiLaws, `AllPredicates, `AllRawRenaming, `AllRawSubstitution, `AllSemanticSubstitution, `AllSigmaLaws, `AllSoundness, `AllStructural, `AllStructuralBase, `AllStructuralRename, `AllSyntax, `AllTermAlgebra, `AllTermLemmas, `BareBooleanGatePositive, `BareBooleanGateSyntax, `BoundaryResults, `CheckerControls, `CheckerKernelAudit, `ComputablePrelude, `EffectiveBooleanCertificates, `EffectiveBooleanControls, `EffectiveBooleanInterfaces, `EffectiveBooleanStandardness, `EffectiveCanonicalTests, `EffectiveObserver, `EffectivePartialObserver, `EffectivePrimitiveRecursion, `EffectiveReduction, `EffectiveRuleBoundary, `EffectiveStandardness, `EffectsAndDependence, `ExtensionalRepairAudit, `ExtensionalRepairLemmas, `ExtensionalRepairSoundness, `ExtensionalRepairSyntax, `ExtensionalRepairTheorems, `ExtensionalRepairWitness, `FiniteBridge, `IdentityChecker, `IntensionalIdentityBridge, `IntensionalIdentityModel, `IntensionalIdentityRelations, `IntensionalIdentitySoundness, `IntensionalIdentityTheorems, `IntensionalIdentityWitness, `InternalPolymorphism, `MaskNormalisation, `NormalisationAndNumerals, `P01Candidates, `P01CanonicalCarrierProjection, `P01Certificates, `P01Confluence, `P01ContextualJ, `P01CurryParametricity, `P01DependentControls, `P01DependentCore, `P01DependentFundamental, `P01DependentModel, `P01DependentRepresentation, `P01DependentSubstitution, `P01Examples, `P01LambdaSyntax, `P01ModelWitnesses, `P01Omega, `P01PER, `P01Polynomials, `P01RecursiveModel, `P01SNReflection, `P01SystemF, `P01Translation, `P01TypeAlgebra, `PolynomialTestAudit, `PolynomialTestBoundary, `PositiveSeparation, `RestrictedCompiler, `SparsePolynomial, `SubstitutionSyntax, `TypedAlgebra, `TypedStructural, `TypedSyntax]

run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[`propext, `Quot.sound, `Classical.choice]
  let mut roots : Array Name := #[]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if modules.contains env.header.moduleNames[idx.toNat]! && info.isTheorem then
        roots := roots.push name
        let axioms ← Lean.collectAxioms name
        for axiomName in axioms do
          unless allowed.contains axiomName do
            throwError "INDEPENDENT_NONSTANDARD_AXIOM {name} -> {axiomName}"
  unless roots.size > 0 do throwError "NO_PROJECT_THEOREMS"
  let mut pending := roots.toList
  let mut seen : NameSet := {}
  let mut count := 0
  let mut foundAxioms : Array Name := #[]
  for _ in [:1000000] do
    match pending with
    | [] => break
    | name :: rest =>
      pending := rest
      if !seen.contains name then
        seen := seen.insert name
        count := count + 1
        let some info := env.checked.get.find? name |
          throwError "INDEPENDENT_UNCHECKED_DECLARATION {name}"
        if info.isUnsafe || info.isPartial then
          throwError "INDEPENDENT_UNSAFE_OR_PARTIAL_DEPENDENCY {name}"
        if info.isAxiom then
          unless allowed.contains name do throwError "INDEPENDENT_UNAPPROVED_AXIOM {name}"
          foundAxioms := foundAxioms.push name
        pending := info.type.getUsedConstants.toList ++ pending
        if let some value := info.value? true then
          pending := value.getUsedConstants.toList ++ pending
        match info with
        | .inductInfo value => pending := value.ctors ++ pending
        | .recInfo value =>
          for rule in value.rules do pending := rule.rhs.getUsedConstants.toList ++ pending
        | _ => pure ()
  unless pending.isEmpty do throwError "INDEPENDENT_AUDIT_INCOMPLETE"
  logInfo m!"INDEPENDENT_ALL_PROJECT_PROOF_AUDIT_PASS modules={modules.size}; theoremRoots={roots.size}; checkedClosure={count}; axioms={foundAxioms}; unsafeOrPartial=0"
end IndependentAllProjectProofAudit
