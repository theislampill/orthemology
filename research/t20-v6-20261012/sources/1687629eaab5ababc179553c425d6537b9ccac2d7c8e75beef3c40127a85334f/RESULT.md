# Closed typed Church source-identity completeness

Status: isolated constructive research, not integration or closure of T20/#9.

## New checked result

For every actual `HasE [] n N`, where `N` is the unchanged Church input type, and its computably extracted generic-open count `k`, the package derives:

`HasE [] I (Id_N n (inputNumeral k))`.

The original source polynomial `n` is retained. This is typed source identity, not raw conversion of `n` to a numeral.

For two supplied actual closed Church typings `hp : HasE [] p N` and `hq : HasE [] q N`, all of the following are equivalent:

- `HasE [] I (Id_N p q)`;
- existence of any source witness `r` with `HasE [] r (Id_N p q)`;
- equality of `extractIteration p hp` and `extractIteration q hq`;
- the original inherited semantic relation `F N rho zeroEnv (eval p zeroEnv) (eval q zeroEnv)`, for any fixed type environment `rho`.

`EffectiveChurchIdentity.decideTypedIdentity` and `decideTypedIdentityExists` are executable Lean decision functions taking the two typing proofs. Five executable guard checks cover both outcomes, witness existence, and raw-nonconvertible but typed-identical endpoints.

## Exact structural obstacle and its resolution

The old scalar-instance proof could type `n f a : A` by conversion to the extracted finite iteration. Actual `piExt` additionally requires `n f : End` in `[End]`; two-argument conversion alone did not supply this premise.

The separate `hase-church-structural-20261010` package proves actual `HasE` type-parameter renaming and term-variable renaming by finite mutual induction over all unchanged constructors. Every `piExt` and `allExt` typing, formation, scoping, and family premise is retained. This gives:

- `Structural.has_closed : HasE [] p A -> CtxE Gamma -> HasE Gamma p A`;
- `Structural.closed_church_weaken : HasE [] n N -> HasE [End] n N`.

No old-`Has` weakening theorem is mistaken for an extended-system result. The structural package uses no normalization, semantic reflection, or new rule.

## Proof structure

1. Preserve the same closed source endpoints and obtain their generic observation conversion from the already checked count extractor.
2. Type their fully applied endpoints using the existing scalar-instance argument.
3. Use the actual newly proved closed weakening to type their once-applied endpoints.
4. Introduce the leaf identity by the unchanged conversion rule; use two actual `piExt` rules and one actual `allExt` rule to derive identity at `N`.
5. Independently, any source identity implies equal counts via the original inherited `ExtensionalRepair.unary_fundamental`, `IdentityComplexity.related_same_index`, and raw marker tests. This necessary direction requires no new source weakening and is not attributed to the newer open full-PER theorem.
6. Relate literal `inputNumeral k` to its generic observation via the actual imported bracket abstraction. Combine with the extractor's exact `PolyConvPlus` certificate.

## Controls

- Equal numeral inputs produce an affirmative executable decision.
- Distinct numeral inputs produce a negative executable decision.
- A kernel theorem excludes every identity witness between numeral 2 and numeral 3.
- At Church type `N`, literal `I` and packed literal `SKK` have source identity but are not `PolyConvPlus`-convertible. This explicitly prevents conflating typed canonicity with the false raw-canonicity claim.

## Scope

This supplies constructive source-identity completeness and an effective equality decision on the promised domain of already-supplied closed Church typings. It is stronger than observation-only count extraction.

It does not decide whether arbitrary untyped polynomials inhabit `N`. It does not prove completeness for arbitrary types or contexts. It does not produce one internal bound-variable scalar-fusion proof, promote a metatheorem over every closed input into that universal judgment, or close original T20/#9.

## Verification

Run `python3 hase-closed-church-identity-20261010/replay.py` from any working directory. It verifies pinned prerequisite sources, manifests, receipts, the Lean binary, 92 baseline objects, four scalar objects, three structural objects, and the frozen extractor object. It then freshly compiles only the three new modules with Lean 4.19.0 `--trust=0`.

The new identity modules depend only on `propext`, `Classical.choice`, and `Quot.sound`. The separate structural port needs only `propext` and `Quot.sound`. No baseline rebuild, protected repository mutation, publication, integration, or closure is performed.
