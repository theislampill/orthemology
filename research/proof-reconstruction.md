# Source coverage repair

The review of PR #34 at `d663da577c3c5b698ada68bf2e22634fdc643ba8` identified a selection error: published current results depended on supplied bodies excluded as historical. This repair recovers and qualifies existing work. It does not repeat the research or grant T20 acceptance.

All **4,404** previous supplied-source omissions were reconciled: **4,363 restored**, **41 specifically held**. The original 1,984 installed source bodies, 5,625 baseline bindings, v5 and prior T20 remain unchanged. The manifest records every disposition, original/public identity and remaining omission reason. The original private handoff and reversible transformation records remain outside Git.

The two restored full proofs are [Square positivity forces exact dynamics for every coercive polynomial](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10/coercive-square-positivity-20261010__RESULT.md) and [Full tensor moment dynamics under polynomial damping](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a/tensor-realizability-extension-20261010__RESULT.md). Their ordinary proof status, hypotheses, reviews and source-check qualifications are preserved. Publication does not promote them to kernel proofs.

The [current source graph](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json) covers **233 distinct Lean bodies in seven rooted suites**, **323 custom import edges**, **20 direct official import edges**, and **38 ordinary support bindings**. The three newly reconstructed roots use 218 distinct Lean bodies, including all **75** omitted custom supports. Thirteen omitted ordinary proof/review/control records were also recovered. Six originally ambiguous imports and ten further version collisions were resolved using exact original source context and the existing source staging records. Mutation fixtures and unrelated same-named calculi are retained as history where eligible; they are not substituted into current suites.

## Finding and reconstructing sources

From the repository root:

```sh
python -B scripts/resolve_t20_v6_source.py find tensor-realizability
python -B scripts/resolve_t20_v6_source.py resolve 449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a
python -B scripts/resolve_t20_v6_source.py export-suite TypeInhabitationSearch ../t20-v6-type-inhabitation
```

`find` searches preserved source names, identities and repository paths. `resolve` verifies the exact public bytes before returning the binding, including a pinned historical Git object where needed. A held or unavailable identity returns its actual disposition, not a fabricated body. `export-suite` requires a fresh directory outside the repository, verifies the whole current graph and each body, and writes only the selected exact module variants. It also writes `RECONSTRUCTION.json` and `REPLAY_ORDER.txt`; it executes nothing.

| Suite | Exact custom modules | Evidence |
| --- | ---: | --- |
| FamilyComputability | 138 | Repaired source closure and fresh native replay |
| TypeInhabitationSearch | 206 | Repaired source closure and fresh native replay |
| ExplicitRawGap | 140 | Repaired source closure and fresh native replay |
| PRIOR_C05 | 10 | Existing native receipt, exact source inputs retained |
| PRIOR_C06 | 1 | Existing native receipt, exact source inputs retained |
| PRIOR_C08 | 101 | Existing native receipt, exact source inputs retained |
| PRIOR_C09 | 5 | Existing native receipt, exact source inputs retained |

For a native replay, use Lean **4.19.0**, compiler SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, and Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Make the reconstructed directory and that installation's official Mathlib/package libraries available in `LEAN_PATH`. From the fresh reconstructed directory, compile in `REPLAY_ORDER.txt` order:

```sh
while IFS= read -r module; do
  lean --trust=0 -j1 -o "$module.olean" "$module.lean" || exit 1
done < REPLAY_ORDER.txt
```

The [new native receipt](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/verification/REPAIRED_NATIVE_LEAN_RESULTS.json) records fresh compilation of all 218 distinct custom modules for the three recovered roots, with exact source, log and object hashes. These three maps were combined only after checking that no module name selected conflicting bytes. Official compiler/Mathlib objects remain the stated trust boundary. The earlier [117-module receipt](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/verification/NATIVE_LEAN_RESULTS.json) retains its original scope; shared module counts are not independent scientific results.

The source gate now parses actual imports from source bytes, checks declarations and target variants, requires each suite to equal its rooted closure, and binds ordinary dependencies to exact evidence substrings. The source identity universe, current graph and contribution register are pinned. Full-validator negative controls withhold a required body, remove an import declaration despite updating its control hash, replace an identity-only source, inject private manifest metadata and retarget the contribution/review register. Passing this gate establishes source coverage and provenance within this scope, not theorem acceptance.

The [bounded review summary](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/verification/SOURCE_COVERAGE_REVIEWS.json) records separate publication/provenance and scientific source-chain reviews, their evidence digests, resolved findings and limits. Final repository checks and CI remain separate evidence at the exact resulting commit.

## Preserved history and exclusions

All restored Lean bodies are byte-exact. Other transformations are reversible locator/identity or navigation changes; one additional mathematical expression receives code delimiters without changing its characters. Twenty-six scientific/control deltas and one historical Orthemology validator are retained inertly. No patch is applied and no historical validator becomes an active repository gate. Three JSONL finite-fixture/authored-stage bodies retain their exact bytes as `.jsonl.txt`, with their original names and inherited timing/execution status recorded.

The 41 holds consist of 25 binary render variants needing decoded publication qualification; six private intake/transport items; three baseline-redundant Git diffs; three other-project governance excerpts; and four individual private/unqualified items (custody inventory, raw owner instructions, coordination record and unrelated platform skill). None is a supplied controlling dependency in this graph. The three held Git diffs have their complete postimages already present in public baseline history. The 25 render variants have not acquired a decoded-equivalence claim; current curated mentions occur in administrative inventories, not direct proof-body dependencies. Their hashes and precise dispositions remain visible. Rights for the unrelated platform skill remain unresolved, so its body stays private.

Historical document links either target an exact resolved public identity or an [explicit original-context boundary](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/PUBLIC_BOUNDARIES.md). A boundary is not proof completion, and the resolver does not claim to reconstruct every historical workspace. For ordinary tensor/coercive scripts, selected-handoff absence of some author/reviewer receipts and a matching independent input-binding layout remains explicit. Those missing historical outputs are not generated retrospectively. Archived Python control scripts with assertions must never be treated as valid runs under optimization.

The broader scientific limitations remain: missing later R3 successor, unavailable originals, inherited projection equivalence where original preimages are absent, bounded primary-source readings, and uncertified historical research duration. Source recovery and fresh compilation do not supply these missing warrants. No fresh empirical study, whole-volume source authentication, human-specialist endorsement, external novelty, metaphysical warrant, T20 owner acceptance, merge permission or T21 start follows.
