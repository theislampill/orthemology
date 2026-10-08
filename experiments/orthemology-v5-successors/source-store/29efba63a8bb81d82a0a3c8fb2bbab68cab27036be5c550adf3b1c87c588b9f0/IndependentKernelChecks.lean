import ExtensionalRepairTheorems
import Lean
import Lean.Util.CollectAxioms

open Lean Elab Command Meta
open P01AC OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.ExtensionalRepair

namespace IndependentTypedExtensionalReview

-- Literal target, independent of the author's definitional names.
example : HasE [] (.atom .i)
    (.identity (.all (.pi (.param 0) (.param 0)))
      (.atom .i) (.atom (.app (.app .s .k) .k))) := separation_has
example (r : Poly) : ¬ HasE [] r
    (.identity .raw (.atom .i) (.atom (.app (.app .s .k) .k))) := raw_separation_no_has r
example : ¬ ∃ r : Poly, HasE [] r
    (.identity .raw (.atom .i) (.atom (.app (.app .s .k) .k))) := raw_separation_uninhabited
example {Γ p A} : HasE Γ p A → P01AC.TermSound Γ p A := has_sound
example {Γ A} : FormE Γ A → P01AC.FormSound Γ A := form_sound
example {Γ} : CtxE Γ → P01AC.ContextLaws Γ := context_sound
example {Γ p A} : HasE Γ p A → ∀ r η ξ, P01AC.H Γ r η ξ →
    P01AC.G A r η ξ (eval p η) (eval p ξ) := fundamental
example {r p q : Poly} : HasE [] r (.identity .raw p q) →
    Conv (eval p zeroEnv) (eval q zeroEnv) := closed_raw_identity_conversion
example : HasE [] (.app (.atom .k) (.atom .i))
    (.pi (.param 0) (.identity (.param 0)
      (.app (.atom .i) (.var 0)) (.app (.atom (.app (.app .s .k) .k)) (.var 0)))) :=
  pointwise_evidence_has
example : abstract (.atom .i) = .app (.atom .k) (.atom .i) := bracket_I_exact
example {Γ p A} : P01AC.Has Γ p A → HasE Γ p A := has_inclusion
example {Γ p A} : P01AC.Intensional.Plus.HasPlus Γ p A → HasE Γ p A := plus_has_inclusion
example (r : Poly) : (¬ P01AC.Has [] r P01AC.Intensional.separationB) ∧
    (¬ P01AC.Intensional.Plus.HasPlus [] r P01AC.Intensional.separationB) :=
  preserved_old_noninhabitation r

-- The dependent fibre and both All uniformity clauses are literally old F.
example (A B : Ty) (ρ : OEnv) (η : Env) (f g : OrthemologyV2.Term) :
    P01AC.F (.pi A B) ρ η f g =
    (∀ x y, P01AC.F A ρ η x y → P01AC.F B ρ (cons x η) (.app f x) (.app g y)) := rfl
example (B : Ty) (ρ : OEnv) (η : Env) (f g : OrthemologyV2.Term) :
    P01AC.F (.all B) ρ η f g =
    ((∀ (P Q : PER) (R : Link P Q), P01AC.G B (extendEnv R (diagEnv ρ)) η η f f) ∧
     (∀ (P Q : PER) (R : Link P Q), P01AC.G B (extendEnv R (diagEnv ρ)) η η g g) ∧
     ∀ P, P01AC.F B (cons P ρ) η f g) := rfl
example (B : Ty) : inst (subst (pup (fun n => Poly.var (n+1))) B) (.var 0) = B :=
  schema_pi_body_instantiate_shift B

-- Directly specified finite rule contracts from the written schema.
def expectedPiSchema : ∀ {Γ A B p q h},
    FormE Γ A → FormE (A :: Γ) B → FormE Γ (.pi A B) →
    HasE Γ p (.pi A B) → HasE Γ q (.pi A B) →
    FormE (A :: Γ) (.identity B (.app (pren Nat.succ p) (.var 0)) (.app (pren Nat.succ q) (.var 0))) →
    FormE Γ (.pi A (.identity B (.app (pren Nat.succ p) (.var 0)) (.app (pren Nat.succ q) (.var 0)))) →
    HasE Γ h (.pi A (.identity B (.app (pren Nat.succ p) (.var 0)) (.app (pren Nat.succ q) (.var 0)))) →
    FormE Γ (.identity (.pi A B) p q) →
    Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
    TyScoped Γ.length A → TyScoped (Γ.length + 1) B →
    HasE Γ (.atom .i) (.identity (.pi A B) p q) := @HasE.piExt

def expectedAllSchema : ∀ {Γ B p q h},
    FormE (twkTel Γ) B → FormE Γ (.all B) →
    HasE Γ p (.all B) → HasE Γ q (.all B) →
    FormE (twkTel Γ) (.identity B p q) → HasE (twkTel Γ) h (.identity B p q) →
    FormE Γ (.identity (.all B) p q) →
    Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
    TyScoped Γ.length B → HasE Γ (.atom .i) (.identity (.all B) p q) := @HasE.allExt

private def renamedCore (n : Name) : Name :=
  if n == `P01AC.Ctx then `P01AC.ExtensionalRepair.CtxE
  else if n == `P01AC.Form then `P01AC.ExtensionalRepair.FormE
  else if n == `P01AC.Has then `P01AC.ExtensionalRepair.HasE
  else if n == `P01DF.PolyConv then `P01AC.Intensional.Plus.PolyConvPlus
  else if n == `P01AC.Intensional.Plus.CtxPlus then `P01AC.ExtensionalRepair.CtxE
  else if n == `P01AC.Intensional.Plus.FormPlus then `P01AC.ExtensionalRepair.FormE
  else if n == `P01AC.Intensional.Plus.HasPlus then `P01AC.ExtensionalRepair.HasE
  else n

run_cmd do
  let pairs := #[(`P01AC.Ctx, `P01AC.ExtensionalRepair.CtxE, 2, 2),
    (`P01AC.Form, `P01AC.ExtensionalRepair.FormE, 7, 7),
    (`P01AC.Has, `P01AC.ExtensionalRepair.HasE, 18, 20),
    (`P01AC.Intensional.Plus.CtxPlus, `P01AC.ExtensionalRepair.CtxE, 2, 2),
    (`P01AC.Intensional.Plus.FormPlus, `P01AC.ExtensionalRepair.FormE, 7, 7),
    (`P01AC.Intensional.Plus.HasPlus, `P01AC.ExtensionalRepair.HasE, 18, 20)]
  for (old, fresh, oldCount, freshCount) in pairs do
    let .inductInfo oi ← getConstInfo old | throwError "not inductive {old}"
    let .inductInfo ni ← getConstInfo fresh | throwError "not inductive {fresh}"
    unless oi.ctors.length == oldCount && ni.ctors.length == freshCount do
      throwError "constructor counts changed"
    for i in [:oldCount] do
      let oc ← getConstInfo oi.ctors[i]!
      let nc ← getConstInfo ni.ctors[i]!
      let transformed := oc.type.replace fun e => match e with
        | .const n ls => some (.const (renamedCore n) ls)
        | _ => none
      let same ← liftTermElabM <| isDefEq transformed nc.type
      unless same do throwError "old constructor type changed: {oc.name} vs {nc.name}"
      logInfo m!"EXACT_RETAINED_CONSTRUCTOR {oc.name} = {nc.name}"
  for (actual, expected) in #[(`P01AC.ExtensionalRepair.HasE.piExt,
       `IndependentTypedExtensionalReview.expectedPiSchema),
      (`P01AC.ExtensionalRepair.HasE.allExt, `IndependentTypedExtensionalReview.expectedAllSchema)] do
    let a ← getConstInfo actual
    let e ← getConstInfo expected
    unless ← liftTermElabM <| isDefEq a.type e.type do
      throwError "extensional schema mismatch {actual}"
    logInfo m!"EXACT_NEW_SCHEMA {actual}\n{a.type}"
  let .inductInfo pc ← getConstInfo `P01AC.Intensional.Plus.PolyConvPlus | throwError "not inductive"
  unless pc.ctors == [`P01AC.Intensional.Plus.PolyConvPlus.refl,
    `P01AC.Intensional.Plus.PolyConvPlus.symm, `P01AC.Intensional.Plus.PolyConvPlus.trans,
    `P01AC.Intensional.Plus.PolyConvPlus.app, `P01AC.Intensional.Plus.PolyConvPlus.i,
    `P01AC.Intensional.Plus.PolyConvPlus.k, `P01AC.Intensional.Plus.PolyConvPlus.s,
    `P01AC.Intensional.Plus.PolyConvPlus.bridge] do throwError "unexpected conversion generator"
  logInfo "CONVERSION_EXACT_EIGHT_IMPORTED_GENERATORS"

run_cmd do
  let env ← getEnv
  let allowed := #[`propext, `Quot.sound, `Classical.choice]
  let mut count := 0
  let mut compilerAux := 0
  for (n, info) in env.checked.get.constants.toList do
    if `P01AC.ExtensionalRepair |>.isPrefixOf n then
      if info.isUnsafe || info.isPartial then
        compilerAux := compilerAux + 1
        logInfo m!"COMPILER_AUXILIARY {n}: unsafe={info.isUnsafe} partial={info.isPartial}"
      if let .axiomInfo _ := info then throwError "new candidate axiom {n}"
      let axs ← Lean.collectAxioms n
      for a in axs do
        unless allowed.contains a do throwError "unexpected transitive axiom {a} in {n}"
      logInfo m!"INDEPENDENT_AXIOMS {n}: {axs}"
      count := count + 1
  unless count >= 156 do throwError "namespace size requires review: {count}"
  logInfo m!"INDEPENDENT_AXIOM_PASS {count} declarations; {compilerAux} compiler auxiliaries; no new axioms"

-- Compiler-generated executable stages are present in imported .olean files.
-- They must not occur in the logical dependency closure of any safe declaration.
run_cmd do
  let env := (← getEnv).checked.get
  let mut todo : List Name := []
  let mut roots := 0
  for (n, ci) in env.constants.toList do
    if (`P01AC.ExtensionalRepair |>.isPrefixOf n) && !ci.isUnsafe && !ci.isPartial then
      roots := roots + 1
      todo := n :: todo
  let mut seen : NameSet := {}
  let mut visited := 0
  while !todo.isEmpty do
    let n := todo.head!
    todo := todo.tail!
    unless seen.contains n do
      seen := seen.insert n
      visited := visited + 1
      let some ci := env.find? n | throwError "missing kernel declaration {n}"
      if ci.isUnsafe || ci.isPartial then throwError "unsafe/partial logical dependency {n}"
      for d in ci.type.getUsedConstants do todo := d :: todo
      if let some v := ci.value? then
        for d in v.getUsedConstants do todo := d :: todo
      if let .inductInfo i := ci then todo := i.ctors ++ todo
  logInfo m!"LOGICAL_SAFETY_CLOSURE_PASS {roots} safe namespace roots; {visited} total reachable declarations; no unsafe or partial dependencies"

-- Dependency DAG inspection is of proof values, not just theorem names.
run_cmd do
  let mut todo := [`P01AC.ExtensionalRepair.separation_has]
  let mut seen : NameSet := {}
  let mut piSites : Array Name := #[]
  let mut allSites : Array Name := #[]
  while !todo.isEmpty do
    let n := todo.head!
    todo := todo.tail!
    unless seen.contains n do
      seen := seen.insert n
      let ci ← getConstInfo n
      if let some v := ci.value? then
        let refs := v.getUsedConstants
        if refs.contains `P01AC.ExtensionalRepair.HasE.piExt then piSites := piSites.push n
        if refs.contains `P01AC.ExtensionalRepair.HasE.allExt then allSites := allSites.push n
        for d in refs do
          if `P01AC.ExtensionalRepair |>.isPrefixOf d then todo := d :: todo
        logInfo m!"WITNESS_PROOF_DEPENDENCIES {n}: {refs}"
  unless piSites == #[`P01AC.ExtensionalRepair.arrow_identity_has] do
    throwError "unexpected PiExt witness sites: {piSites}"
  unless allSites == #[`P01AC.ExtensionalRepair.separation_has] do
    throwError "unexpected AllExt witness sites: {allSites}"
  for forbidden in [`P01AC.ExtensionalRepair.has_sound, `P01AC.ExtensionalRepair.form_sound,
      `P01AC.ExtensionalRepair.fundamental, `P01AC.ExtensionalRepair.fundamental_pi_ext,
      `P01AC.ExtensionalRepair.fundamental_all_ext] do
    if seen.contains forbidden then throwError "witness uses soundness: {forbidden}"
  logInfo m!"WITNESS_FINITE_SYNTACTIC_CONSTRUCTION_PASS PiExt={piSites} AllExt={allSites}"

end IndependentTypedExtensionalReview
