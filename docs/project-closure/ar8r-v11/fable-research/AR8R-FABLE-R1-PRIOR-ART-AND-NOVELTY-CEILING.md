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

Every construction in this round has a classical home. Several of them have
*exact* classical homes, meaning the program's object is not merely similar to a
known object but is the same object under a different name.

## Correspondence table

| Round-1 object | Classical home | Relation |
|---|---|---|
| Fibre-constancy characterization (Core A; T299) | Universal property of the quotient; partition refinement; functional dependency in relational databases | **Identical**; the Lean proof is the standard factorization argument |
| Fibre-constancy characterization | Myhill–Nerode | **Adjacent** — shared factorization ancestry; narrowed from "identical" in the post-review correction, since exact equivalence was never demonstrated |
| Plain separation index | Minimum test collection (Garey–Johnson SP6); separating systems (Rényi, Katona); identifying codes; rough-set reducts | **Identical** |
| Budgeted refinement cost (Core A invariant) | Set Cover | **Equivalent in both directions**; inherits NP-hardness and logarithmic inapproximability |
| Robust separation index | Set multicover; `(f+1)`-separating systems; superimposed codes; robust identifying codes | **Identical** |
| Resource-indexed robust version | Bulk-robust combinatorial optimization (Adjiashvili–Stiller–Zenklusen, 2015) | **Identical model**, including the resource-dependency map |
| Certificate survival radius (Core B) | Minimum hypergraph transversal (Berge) | **Identical** |
| Transversal-versus-packing gap (N1) | König/Lovász duality conditions; set packing hardness | Standard; the program's error was assuming duality without checking its hypotheses |
| Adaptive separation index | Decision-tree complexity; certificate complexity (Nisan); evasiveness | **Identical** |
| Robust adaptive variant | Rényi–Ulam searching with lies | Standard |
| Core B's judgment structure | Substructural sequent calculi with resource annotation | Familiar in kind; the specific rule set is assembled, not novel |

## What is new only *relative to the program's own documents*

These are corrections and classifications, not theorems. They are new to this
repository and not new to mathematics:

1. the transversal-versus-packing refutation of the cutset reading (N1);
2. the exchange-axiom counterexample showing provenance independence is not a
   matroid rank (N1);
3. the identification of the program's robustness model as bulk-robust
   optimization, which supplies an existing literature to draw on;
4. the exact derivation that the hidden-matching model's non-adaptive separation
   index is `mn` with no fault tolerance;
5. the index mismatch showing Candidate 1's `C(t,2)` saving is invisible to the
   separation invariant;
6. the five T299 specification defects;
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
be the achievement. It would not be. In every case examined here the invariant
already exists in the literature, and the substantive question is whether the
*interpretation map* into the program's domain is exact, guarded, or false. That
is where the program's remaining research value sits, and it is also where round 1
found its only genuine results — two of which were negative.

Any future milestone claiming a "new invariant" should first be checked against
this table.
