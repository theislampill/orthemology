# AR8R Fable round 1 — sourcing rows for the prior-art correspondence table

Added in the post-review correction. These rows cover every load-bearing
scholarly attribution in `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md`, as
required by `CONTRIBUTING.md` (Citation requirements). Classification and
relationship only — no source truth is established here, and a complete row is
never evidence that the cited work says what the round-1 text claims.

Verification vocabulary is the repository's: `WEB-VERIFIED`, `RECORD-CONFIRMED`,
`VIA-COMPILATION`, `UNVERIFIED`. Every row below is **`UNVERIFIED`**: round 1
performed no literature search and consulted no edition, and the correction pass
did not add one. Bibliographic metadata is deliberately minimal — author, work,
and year only where those were already named in the round-1 text — because
inventing identifiers would be worse than leaving them absent.

Relationship vocabulary (fail-closed): while a row's verification status is
`UNVERIFIED`, only `AUTHOR_ASSESSED_UNVERIFIED`, `SEARCH_LEAD`, and
`POSSIBLE_ANALOGUE` are admissible relationships. Factual `identical`,
`equivalent`, `inherits`, or already-exists-in-the-literature relations require
a verified row (exact identifier, location, and proposition context).
`scripts/validate_fable_r1_claim_language.py` enforces this.

| Round-1 object | Cited work as named in round 1 | Stable identifier | Claim supported | Relationship | Verification |
|---|---|---|---|---|---|
| Fibre-constancy characterization (Core A; T299) | universal property of the quotient | none supplied | the characterization is standard, not novel | `AUTHOR_ASSESSED_UNVERIFIED` (assessed identical; not verified against any text) | `UNVERIFIED` |
| Fibre-constancy characterization | Myhill–Nerode theorem | none supplied | ancestry of the fibre/partition argument | `POSSIBLE_ANALOGUE` — narrowed from round 1's original stronger wording | `UNVERIFIED` |
| Fibre-constancy characterization | partition refinement; functional dependency in relational databases | none supplied | same argument in other settings | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |
| Plain separation index | minimum test collection, Garey–Johnson problem SP6 | Garey & Johnson, *Computers and Intractability*, 1979 — problem SP6 | the index is a known problem | `AUTHOR_ASSESSED_UNVERIFIED` (assessed identical; not verified against any text) | `UNVERIFIED` |
| Plain separation index | separating systems (Rényi; Katona); identifying codes; rough-set reducts | none supplied | same index under other names | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |
| Budgeted refinement cost (Core A invariant) | Set Cover | none supplied | hardness consequences claimed by round 1 (author-assessed) | `AUTHOR_ASSESSED_UNVERIFIED` (assessed equivalent in both directions; not verified against any text) | `UNVERIFIED` |
| Robust separation index | set multicover; `(f+1)`-separating systems; superimposed codes | none supplied | the robust index is a known problem | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |
| Resource-indexed robust version | bulk-robust combinatorial optimization, Adjiashvili–Stiller–Zenklusen | Adjiashvili, Stiller & Zenklusen, 2015 | a matching resource-dependency model is described in that literature (author-assessed) | `AUTHOR_ASSESSED_UNVERIFIED` (assessed same model; not verified against the text) | `UNVERIFIED` |
| Certificate survival radius (Core B) | minimum hypergraph transversal (Berge) | Berge, *Hypergraphs* | the radius is a transversal number | `AUTHOR_ASSESSED_UNVERIFIED` (assessed identical; not verified against any text) | `UNVERIFIED` |
| Transversal-versus-packing gap (N1) | König/Lovász duality conditions; set packing hardness | none supplied | `τ = ν` needs hypotheses | `AUTHOR_ASSESSED_UNVERIFIED` (assessed application of standard results) | `UNVERIFIED` |
| Adaptive separation index | decision-tree complexity; certificate complexity (Nisan); evasiveness | none supplied | the adaptive index is a known measure | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |
| Robust adaptive variant | Rényi–Ulam searching with lies | none supplied | robust adaptive search is classical | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |
| Core B's judgment structure | substructural sequent calculi with resource annotation | none supplied | the calculus is familiar in kind | `POSSIBLE_ANALOGUE` | `UNVERIFIED` |

## Why every row is UNVERIFIED, and what that costs

The correspondence table's purpose is to **suppress** novelty claims, so an
unverified row is conservative in the direction that matters: it cannot inflate
the program's credit. What it cannot do is establish that any correspondence is
exact. Two consequences:

1. Every relationship above is the author's assessment, marked as such
   (`AUTHOR_ASSESSED_UNVERIFIED` / `POSSIBLE_ANALOGUE`); none is a verified
   finding, and none may be quoted as a factual identity. Myhill–Nerode was
   additionally narrowed on content grounds.
2. `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md` remains correct in its own
   headline (zero novelty claimed) regardless of these rows, because that
   headline is a *refusal* to claim, which no citation is needed to support.

Candidate 1's `mn − C(t,2)` is still not adjudicated for novelty; burden
`FABLE-R1-B05` is unchanged and no row here bears on it.
