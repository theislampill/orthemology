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

Relationship vocabulary: `identical`, `specialization`, `application`,
`adjacent`, `analogy only`.

| Round-1 object | Cited work as named in round 1 | Stable identifier | Claim supported | Relationship | Verification |
|---|---|---|---|---|---|
| Fibre-constancy characterization (Core A; T299) | universal property of the quotient | none supplied | the characterization is standard, not novel | `identical` | `UNVERIFIED` |
| Fibre-constancy characterization | Myhill–Nerode theorem | none supplied | ancestry of the fibre/partition argument | `adjacent` — **narrowed from round 1's "identical"** | `UNVERIFIED` |
| Fibre-constancy characterization | partition refinement; functional dependency in relational databases | none supplied | same argument in other settings | `adjacent` | `UNVERIFIED` |
| Plain separation index | minimum test collection, Garey–Johnson problem SP6 | Garey & Johnson, *Computers and Intractability*, 1979 — problem SP6 | the index is a known problem | `identical` | `UNVERIFIED` |
| Plain separation index | separating systems (Rényi; Katona); identifying codes; rough-set reducts | none supplied | same index under other names | `adjacent` | `UNVERIFIED` |
| Budgeted refinement cost (Core A invariant) | Set Cover | none supplied | NP-hardness and log-inapproximability inherited | `identical` | `UNVERIFIED` |
| Robust separation index | set multicover; `(f+1)`-separating systems; superimposed codes | none supplied | the robust index is a known problem | `adjacent` | `UNVERIFIED` |
| Resource-indexed robust version | bulk-robust combinatorial optimization, Adjiashvili–Stiller–Zenklusen | Adjiashvili, Stiller & Zenklusen, 2015 | the resource-dependency model already exists | `identical` model as described | `UNVERIFIED` |
| Certificate survival radius (Core B) | minimum hypergraph transversal (Berge) | Berge, *Hypergraphs* | the radius is a transversal number | `identical` | `UNVERIFIED` |
| Transversal-versus-packing gap (N1) | König/Lovász duality conditions; set packing hardness | none supplied | `τ = ν` needs hypotheses | `application` of standard results | `UNVERIFIED` |
| Adaptive separation index | decision-tree complexity; certificate complexity (Nisan); evasiveness | none supplied | the adaptive index is a known measure | `adjacent` | `UNVERIFIED` |
| Robust adaptive variant | Rényi–Ulam searching with lies | none supplied | robust adaptive search is classical | `adjacent` | `UNVERIFIED` |
| Core B's judgment structure | substructural sequent calculi with resource annotation | none supplied | the calculus is familiar in kind | `adjacent` | `UNVERIFIED` |

## Why every row is UNVERIFIED, and what that costs

The correspondence table's purpose is to **suppress** novelty claims, so an
unverified row is conservative in the direction that matters: it cannot inflate
the program's credit. What it cannot do is establish that any correspondence is
exact. Two consequences:

1. The word `identical` in the round-1 table is the author's assessment, not a
   verified finding. Where the correction pass judged the evidence weaker than
   `identical`, the row above says so — Myhill–Nerode is the one case where the
   original wording was narrowed.
2. `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md` remains correct in its own
   headline (zero novelty claimed) regardless of these rows, because that
   headline is a *refusal* to claim, which no citation is needed to support.

Candidate 1's `mn − C(t,2)` is still not adjudicated for novelty; burden
`FABLE-R1-B05` is unchanged and no row here bears on it.
