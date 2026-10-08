# Recursive dependent All over finite typed telescopes

## Status and scope

This package is a bounded research extension of the accepted finite typed-telescope nucleus. Its complete frozen contract is independently accepted in `review/REVIEW.md`; `review/VERIFICATION.json` binds the exact evidence. This is automated independent review rather than human-specialist validation. The object language has no universe or Type:Type. No canonical source conversion, source polynomial, bracket abstraction, or J tracker is changed.

## Frozen dependencies

The accepted 47-module nucleus is copied byte-for-byte in `sources/`; `ACCEPTED_INPUTS.json` records those identities. Every new module uses the `All` prefix and the `P01AC` namespace. The admitted v5 design digest is `f4eb382dc54e142b14d943affe8602b8dbb2f3097eaea8f6e630f6d182e83545`; the independent admission digest is `e6604b05686d58e8137b0458807e9498f6376ff6518738b457fe0732e4d4f142`; accepted-nucleus reconciliation is independently bound by `f01d93272cd1f805b647d0799b1c97df8a6207a01f7bb281fa118908990c0ca5`.

## Syntax and two kinds of binder

`AllSyntax` defines Param, Bottom, Raw, arbitrary typed Pi and Sigma, typed Id, and recursively generated All. All shifts the free type parameters of its surrounding telescope and leaves term indices unchanged. Pi and Sigma shift term indices in both the substituted body and every replacement type. The paired lifts are not interchangeable without their proved equations.

The finite-instance import retains the exact source `atom t` and its unchanged `FiniteDerives t C` proof. A finite Bottom-default table supplies binder-aware type images, each with a smaller formation certificate. The result also has a finite syntactic formation certificate. No atom/application conversion bridge is assumed or added.

`AllTermAlgebra` and `AllMixedAlgebra` establish literal substitution, renaming, composition, top cancellation, the mixed square, both binder lifts, and both Theta/J coordinates. Explicit capture controls retain simultaneous free term and type parameters beneath nested binders.

## Raw semantics before laws

`AllPredicates.predicates` returns the unary and heterogeneous predicates together by structural recursion on raw type syntax. At All, unary uniformity calls the heterogeneous predicate of the strictly smaller body. Neither lawful PER construction nor a desired soundness theorem participates in this definition. Raw F/G can fail the expected laws on malformed syntax.

D/E/H are raw recursively defined finite-telescope predicates. Valuations are total evaluator environments representing finite tuples, with a zero tail. Type weakening leaves their term coordinates intact. `AllRawSubstitution` and `AllRawRenaming` establish unconditional raw term-substitution and type-renaming equations, including the three telescope weakening equations.

## Conditional semantic replacement

`AllSemanticSubstitution.ImageMatch` states exact image predicates relative to a lawful source REnv. It includes separate unary endpoints, the heterogeneous relation, and both diagonal image equations. It is a metatheorem hypothesis, never a typing or formation premise.

`FG_mixed` is a structural induction on the raw target type. The source parameter REnv remains frozen when the target valuation gains a term prefix; syntactic weakening of the replacement images removes that prefix semantically. Under All, the image REnv extends with the newly selected arbitrary PERs and Link. The unary All uniformity cases use the matching diagonal environments.

`AllInstantiation` derives these hypotheses from the smaller replacement formation-law conclusions. The image PERs are evaluated separately at the left and right target valuations; their Link is the actual heterogeneous replacement predicate. No equality or single shared endpoint is substituted for that Link. No formation of the substituted result is used to justify `FG_mixed`.

## Formation and typing soundness

`AllBaseLaws`, `AllPiLaws`, `AllSigmaLaws`, and `AllBinderLaws` prove the formation-law cases. All transport includes both sides of unary uniformity. Its strong diagonal statement allows unequal E-related valuations. In the reverse direction, body invariance changes the right valuation, the within-Q relation is transported to that valuation, and body respect changes the right result. The proof does not identify the two valuations.

`AllSoundness` uses the generated mutual recursors of Ctx/Form/Has. The hereditary packages are induction conclusions retaining smaller body formation results. All introduction derives uniformity by applying the smaller body typing theorem at arbitrary Links, including endpoint diagonal environments. All elimination and finite imports use only smaller replacement formation conclusions and the conditional structural substitution theorem.

## Finite syntactic maps

The independent syntactic preservation development is in `AllStructuralBase`, `AllStructuralRename`, and `AllStructural`. `MixedTerms` records a finite component list, with each declaration instantiated using its already supplied tail components. Replacement types are formed in the full target context and may depend on all of its variables.

Term image lists have an atom-zero unused tail. Type tables separately have a Bottom unused tail. Identity lists agree with the total variable map only on finite scope. Their action is proved by scoped extensionality, never by an invalid global identity-tail equation. The finite All-elimination context map uses unchanged identity term components and the bounded table `[A,Param 0,...]`. `form_tinst` and `has_tinst` are syntax-only consequences.

## Exact intrinsic interpretation

`AllRepresentation` represents contexts, types, terms, and ordinary term-only substitutions in the accepted intrinsic core, preserving exact polynomial code. `AllContextualJ` invokes the actual accepted contextual J operation, checks both coordinates, and proves exact code and target type.

`AllMixedRepresentation` handles genuinely dependent mixed substitutions separately. Its source intrinsic context stores a joint parameter environment and term valuation. Each target valuation supplies its own image PER environment; unary transport proves equality of these environments along target E. The map uses exactly the finite term image code, including its zero tail. The preceding `MixedTerms.related` theorem retains the genuinely heterogeneous, independently evaluated endpoints and frozen image Link. Joint unary context equality does not replace heterogeneous relation preservation.

## Compatibility and controls

`AllNucleusSyntax` and `AllNucleus` translate every accepted nucleus constructor, preserve literal polynomials, and prove raw unary/heterogeneous and D/E/H agreement. AllFinite becomes recursive All over the finite translation, so compatibility is an explicit grammar translation rather than literal original type identity.

The legacy comparison uses the accepted Type-valued retained derivation tree and its exact erase map to P01DF.Has. Support concerns retained typing syntax, types, motives, explicit replacement types, and displayed conversion endpoints. Hidden internal PolyConv witnesses are not inspected. The broader certificate must include old All introduction/elimination and non-finite dependent All, while the accepted nucleus restriction remains unchanged.

The joined Q control is `All α. Pi x:α. Sigma y:α. Id α x y`, with the exact bracket-abstracted pair polynomial. Q self-instantiation yields `Pi Q (Sigma Q (Id Q var1 var0))`. Open identity and inhabited Sigma replacements, unequal related I/SKK valuations, nested two-sort capture, distinct nonempty Raw fibres, and the inherited typed-Id/J/Raw negative controls accompany the universal results.

## Exclusions

Nothing here establishes canonical unary carrier equality, raw eta, equality reflection through arbitrary Links, normalization, higher identity, arbitrary frontend correctness, full U11 closure, or claims about numerical identity of real bearers. Id is equality in its chosen PER with Conv-I proof witnesses. Existing canonical counterexamples and the source I/SKK obstruction remain unchanged. No source publication, repository mutation, or external contact is part of this package.
