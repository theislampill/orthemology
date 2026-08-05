# AR8R-FABLE-R1 — prior art and novelty ceiling

Status: research finding. Stated deliberately conservatively. The purpose of this
packet is to prevent the program from claiming novelty it does not have.

**Sourcing.** Every attribution below has a row in
`AR8R-FABLE-R1-SOURCING.md` recording its identifier, the claim it supports, its
exact relationship, and its verification status. All rows are `UNVERIFIED`: round
1 performed no literature search, and the correction pass did not add one. The
relationship words below are the author's assessment, not verified findings.

## Headline

**Zero general mathematical novelty is claimed for anything produced in round 1.**

Every construction in this round is author-assessed to have a classical home.
Every such assessment is `AUTHOR_ASSESSED_UNVERIFIED` or `POSSIBLE_ANALOGUE`
(see `AR8R-FABLE-R1-SOURCING.md`): no source was verified, so no relation below
is a factual identity claim. The assessments exist to *suppress* novelty claims,
which they do regardless of verification; they must not be quoted in the other
direction as established equivalences to specific literature.

## Correspondence table

| Round-1 object | Author-assessed classical home | Relation (all `AUTHOR_ASSESSED_UNVERIFIED` / `POSSIBLE_ANALOGUE`) |
|---|---|---|
| Fibre-constancy characterization (Core A; T299) | Universal property of the quotient; partition refinement; functional dependency in relational databases | Assessed identical (unverified); the Lean proof follows the standard factorization argument |
| Fibre-constancy characterization | Myhill–Nerode | `POSSIBLE_ANALOGUE` — shared factorization ancestry; narrowed from "identical" in the post-review correction, since exact equivalence was never demonstrated |
| Plain separation index | Minimum test collection (Garey–Johnson SP6); separating systems (Rényi, Katona); identifying codes; rough-set reducts | Assessed identical (unverified) |
| Budgeted refinement cost (Core A invariant) | Set Cover | Assessed equivalent in both directions (unverified); the hardness consequences are `DERIVED_BUT_UNVERIFIED` |
| Robust separation index | Set multicover; `(f+1)`-separating systems; superimposed codes; robust identifying codes | Assessed identical (unverified) |
| Resource-indexed robust version | Bulk-robust combinatorial optimization (Adjiashvili–Stiller–Zenklusen, 2015) | Assessed same model (unverified), including the resource-dependency map |
| Certificate survival radius (Core B) | Minimum hypergraph transversal (Berge) | Assessed identical (unverified) |
| Transversal-versus-packing gap (N1) | König/Lovász duality conditions; set packing hardness | Standard application — `τ = ν` needs hypotheses that conjunctive root-sets do not supply. Recorded as an interpretation firewall; no program document assumed the duality (the original "the program's error" wording was withdrawn) |
| Adaptive separation index | Decision-tree complexity; certificate complexity (Nisan); evasiveness | Assessed identical (unverified) |
| Robust adaptive variant | Rényi–Ulam searching with lies | `POSSIBLE_ANALOGUE` |
| Core B's judgment structure | Substructural sequent calculi with resource annotation | `POSSIBLE_ANALOGUE`; the specific rule set is assembled, not novel |

## What is new only *relative to the program's own documents*

These are corrections and classifications, not theorems. They are new to this
repository and not new to mathematics:

1. the transversal-versus-packing interpretation firewall (N1) — a misreading
   forbidden in advance, not a correction to any existing statement;
2. the exchange-axiom counterexample constraining any future matroid-rank
   definition of provenance independence (N1);
3. the author-assessed (unverified) match of the program's robustness model to
   bulk-robust optimization, which names a literature to search;
4. the derivation (`DERIVED_BUT_UNVERIFIED`) that the hidden-matching model's
   non-adaptive separation index is `mn` with no fault tolerance;
5. the index mismatch showing Candidate 1's `C(t,2)` saving is invisible to the
   separation invariant;
6. the T299 specification findings (four defects beyond notation; D4 withdrawn);
7. the observation that the OSM source's trajectory-order result is
   encoding-convention-relative.

## Explicitly not adjudicated

**Candidate 1's `D(m,n,t) = mn − C(t,2)` is not adjudicated for novelty here.**
This round did not perform a literature search in the promise/query model. Its
packet's existing disposition — a strengthened rectangular threshold variant, at
moderate confidence, with external mathematical review and exhaustive prior-art
review both open — is unchanged. The nearest search targets remain evasiveness
(the Aanderaa–Karp–Rosenberg line), hidden matching in communication complexity,
and certificate complexity of threshold functions.

The program's own standing rule applies and is reaffirmed: **failure to locate the
same formula in the same model is not an originality finding.**

## Consequence for the meniscus criteria

Several milestone candidates are stated as though discovering the invariant would
be the achievement. It would not be. In every case examined here the invariant is author-assessed (unverified) to
have a literature counterpart, and the substantive question is whether the
*interpretation map* into the program's domain is exact, guarded, or false. That
is where the program's remaining research value sits, and it is also where round 1
found its only genuine results — two of which were negative.

Any future milestone claiming a "new invariant" should first be checked against
this table.
