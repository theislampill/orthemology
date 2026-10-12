# Q1f — guarded reason/version transport, layer separation and formal target

## Disposition

**PARTIAL — EXACT IRREDUCIBLE BLOCKER: native compilation and declaration/type/axiom/artifact readback of the new scoped graph-plus-VCT candidates under Lean 4.19.0 has not run because exact toolchain acquisition is blocked in this host.** The ordinary finite-DAG equivalence, layer independence, evidence/semantic/path composition and the optional-wrapper separation are supplied below. This is not a generic “graph-only proof remains to be extended” boundary.

`HOST_EXECUTION_BLOCKED` and `FORMAL_RESULT_UNPROVED` are separate facts. Missing execution is not evidence that the theorem is false. Static review is not elaboration; this run caught and corrected two wrong imported field/function names and strengthened the authority-path conclusion to retain re-delegation. Rejected draft preimages remain visible. No newly created source has `.olean` or kernel credit.

## 1. Exact source, later status and preservation

Q1f is the original queue target “guarded reason/version base then VCT and optional TRC wrapper”, with Q0 prerequisite. Its exact source records, selectors and inputs are in `inputs/P03_OBLIGATION_CONFIRMATIONS.json`. The ordinary VCT target is the pinned R16 V2 statement, not reconstructed from its acronym. Its source bytes are:

    PMR-007_FRONTIER_ROUND16_VERSION_CUSTODY_TRANSPORT_AND_TEMPORAL_ELIGIBILITY_V2.md
    bytes 10299
    SHA256 599e9dd9595e26ae857a9a1e7c8a07306a2ec13f25c0c5a0500da544bc45f3ba
    Git blob b665083608bc30a5dcf8faf54a1c1efdccae4621

The separately pinned R15 V2 TRC source has 14916 bytes and SHA256 `879681edd0f28a35ba9bd87f049ad60c10ea5369474fb8bf2d092de88251299c`. Both exact sources were already added and verified in attempt1 and are preserved there. The later V11 formalisation map identifies VCT/TRC as admitted post-merge **scoped ordinary results**, with formal execution not performed and owner/external review boundaries distinct. Its later scope-specific status governs over older pending-review headings; nothing here downgrades the admitted ordinary result.

R16's repaired conditions bind the actual preceding certificate: version/claim/root, exact node-map domain and exact input dependency-edge set; preservation of dependency edges; output edge endpoints in the mapped node carrier; genuinely discharged preserved obligations; preserved plus revalidated obligations covering the independent full target requirement; semantic commutation; root custody or separately warranted independent new root; authority and intermediate re-delegation; no registered open invalidator. The recorded F01/F02 repairs are not undone or rerun for new historical credit.

Attempt1's two graph countermodels remain binding: edge preservation alone, even injective edge preservation with additional target edges, does not imply that the target is acyclic. They **do not refute VCT with its finite-DAG premise enforced**.

## 2. Layer matrix: conditions, independence and sufficient strengthening

All predicates in this table are relative to an independently fixed target contract and policy epoch. They do not certify an external world's truth, permission or currentness by being written as a local Boolean.

| Layer | Source condition | Target/transport condition | Follows from prior layers? | Smallest sufficient condition used here |
|---|---|---|---|---|
| Finite graph/DAG | Actual finite reason-node set and dependency DAG | Target finite DAG; map actual source nodes and every edge | No: added target edges can create a cycle despite injectivity | Independently require target acyclicity, or an equivalent finite topological rank witness; do not infer it from the map. |
| Exact adjacent boundary | Version, frozen claim, root, nodes, edges and discharged obligations are the actual preceding output | The next hop consumes that entire frame, not a separately compatible lookalike | No: matching a version string permits a different reason DAG or obligation state | An indexed composable path, or equality checks over the whole actual frame. |
| Discharged evidence | Every actually discharged source obligation has evidence valid for its source-indexed contract | Every target discharge is preserved with a valid contract transport, or freshly proved at the target | No: a graph and a token called “preserved” contain no proof that it was discharged or remains valid after a contract change | `P⊆D_source`; valid transport for each P; target-valid fresh witnesses for R; target output D=P∪R. |
| Target requirement coverage | Source discharged set may cover a different requirement | Independently fixed full target requirement Q is included in P∪R | No: validity of some transported reasons does not imply completeness of the target burden list | Q⊆P∪R, with Q not chosen after seeing the available reasons. |
| Semantic preservation | A fixed source claim interpretation in a source semantic state | Each hop's semantic square commutes under its declared interpretation map | No: valid evidence for one proposition need not establish another | A local commuting-square proof for each hop, then composition; source truth is a separate input to truth transport. |
| Authority / admissibility | Authority is available for the declared hop in the fixed policy | Each hop is authorised and each intermediate is allowed to re-delegate | No: semantics/graphs can be sound while a recipient lacks permission or capability | Local authority witnesses plus explicit intermediate re-delegation; retain an authorised path, not invented direct/transitive permission. |
| Version / currentness | Source certificate has its recorded version; target uses the fixed current policy epoch | Target version is allowed and no relevant registered invalidator is open | No: same bytes and valid old reasons survive a context change that invalidates their use | Re-evaluate/bind version and registered invalidator guards at the declared epoch. No future-epoch promise. |
| Root / custody | Recorded root and exact prior boundary | Same root or a specifically warranted new independent root | No: an edge map or copied bytes can be relabelled with another root | Per-hop root relation with its witness; compose the root path. Endpoint identity only when every root step is identity. |
| Application guards | Application, authenticity/evidence, capability, permission and independence requirements belong to the target use | The target-use contract is actually discharged | No: the pure graph or version base is not a world-application theorem | Encode the relevant target requirements and obtain their independent proofs/authority inputs; do not derive them from transport syntax. |

The final row is the accepted pure/application distinction, consistent with PMR-AGCOM-01's independent App/Auth/Ver/Evid/Cap/Perm/InvClosed contract. It is not a new claim that pure graph composition solves those predicates. Optional TRC adds different temporal-model and application obligations; those are treated in section 7, not smuggled into Q1f's pure prerequisites.

### Concrete independence witnesses

The new finite proposal model uses actual finite graph sets, evidence tokens interpreted against source/target contracts, a two-world semantic table and explicit permissions/version/invalidator/root records. Starting from one valid two-hop path, its eight changed models respectively exhibit: a preserved token invalid under a changed target evidence contract; an uncovered independently required target obligation; absent local authority; absent intermediate re-delegation; a disallowed new epoch/version; an open registered invalidator; a noncommuting semantic table; and a new root without a witness. Each separates its layer from the remaining local conditions. Raw models and expected failing guards are in `evidence/vct-layers-normal/LAYER_MODELS.json`.

Two valid-path controls reject overstrong conclusions: a permitted A→B→C path need not grant a direct A→C permission; and a path with an independently warranted new root need not have equal endpoint roots. These controls prevent the proposed theorem from accidentally strengthening VCT by discarding legitimate paths.

These are finite countermodels to omitted-condition extrapolations, not an independent re-review of the historical VCT checker, and not proof that external permissions or evidence are valid in the world.

## 3. Ranked finite DAGs: exact ordinary equivalence, still proposed encoding

Let G=(V,E) be a finite directed graph, including possible self-loops in the input grammar. The following are equivalent:

    (i) no nonempty directed closed walk;
    (ii) there is r:V→Nat such that E(u,v) implies r(u)<r(v).

(ii)⇒(i): along a nonempty walk, transitivity gives a strict increase. A closed walk would yield r(v)<r(v), impossible.

(i)⇒(ii): every directed walk has distinct vertices; a repeated vertex would give a nonempty closed subwalk. Hence its length is at most |V|−1. Set r(v) to the greatest length of a directed path ending at v, including the zero-length path. This maximum exists in the finite nonempty set of eligible lengths. If E(u,v), a longest path ending at u cannot already contain v without creating a cycle; append the edge to get a path of length r(u)+1 ending at v. Thus r(v)≥r(u)+1. When V is empty the unique empty function suffices.

Therefore the ranked-DAG representation is not a stronger graph property **at the stated finite scope**. It remains a separately proposed data representation: the ordinary equivalence is not a compiled conversion of the deployed reason-DAG JSON. A finite carrier enumeration must faithfully map the actual node names to `Fin n`; the rank is auxiliary witness data, not new authority.

A DAG homomorphism may identify unrelated nodes. It cannot identify endpoints joined by a nonempty directed walk: the image would be a nonempty closed walk in the target. Composition maps every edge and walk by induction. These are the exact graph facts in the preserved graph candidate, not a claim that injectivity by itself is enough.

The new emitted-certificate representation additionally has `onto`, making its target node carrier exactly the map image. R16 speaks of the mapped output-node set. If a separate consumer permits additional isolated target nodes, the ordinary graph and warrant path proofs still apply, but this particular surjective representation requires an explicit image restriction/adapter. It is a declared representation proposal, not an assertion that every possible legacy wire format already satisfies onto.

## 4. Evidence composition is constructed, not assumed as whole-path warrant

Fix an obligation index type O. At each frame a let Q_a be its independent required predicates, D_a its actually discharged set, and Valid_a(o) its target-indexed evidence validity. Define

    Sound(a) := for every o∈D_a, Valid_a(o),
    Closed(a) := for every o∈Q_a, Valid_a(o).

For each hop a→b provide P (preserved) and R (revalidated) with:

    P ⊆ D_a;
    o∈P and Valid_a(o) imply Valid_b(o);
    o∈R implies Valid_b(o);
    D_b = P ∪ R;
    Q_b ⊆ P ∪ R.

These are local evidence/contract witnesses. No field asserts `Sound(a) → Sound(b)` or the desired whole-path conclusion. If source and target evidence contracts are definitionally identical, the carry proof is identity; if they change, an actual indexed transport proof or fresh revalidation is needed. Calling a token preserved does not manufacture it.

**One-hop theorem.** Sound(a) implies Sound(b) and Closed(b).

Proof: for o∈D_b, split the exact union. In P, inclusion in D_a supplies Valid_a and the local carry proof supplies Valid_b; in R use the fresh target proof. For required o∈Q_b use the same cases via coverage. This explains exactly why target-contract drift and requirement omission are independent obstructions.

**Finite-path theorem.** For an exactly composable nonempty path, Sound at the initial frame implies Sound and Closed at its final frame.

Proof: induction on the path. The one-hop soundness result supplies the next input's Sound; exact frame indexing prevents switching to a merely same-version certificate with a different D/graph/claim. At the last hop, the coverage argument closes the final requirement. If zero-hop transport is desired, final closure additionally requires the initial frame already be Closed; this candidate intentionally uses nonempty paths and does not hide that base-case premise.

This is a formalisation proposal for the finite guarded contract. Its validity predicates still need interpretation by the independent source/target evidence contracts. Local formal composition neither identifies an external source nor proves that an omitted real-world obligation does not exist.

## 5. Semantics, authority, roots and currentness compose differently

For a semantic hop a→b with map f, require for every source world w:

    Meaning_b(f(w)) ↔ Meaning_a(w).

For b→c with g, transitivity of the two equivalences gives

    Meaning_c(g(f(w))) ↔ Meaning_a(w).

Induction proves the path square. Actual truth transport additionally assumes Meaning_a(w). A preserved structure is not a proof that the original proposition was true.

Authority is **not assumed transitive**. Define `AuthorityPath(p,a,b)` inductively: a permitted single hop; or a permitted first hop a→m, permission to re-delegate at m, and a permitted remaining path m→b. The new candidate constructs this guarded path from the input path. The intermediate re-delegation witness occurs in the conclusion's proof; it is not discarded into a bare transitive closure that would make that premise irrelevant. No direct permission p.authority(a,b) follows without a separate policy theorem.

Root custody uses a per-hop relation whose alternatives distinguish root identity from an independently warranted new root. Its transitive path is retained. If every allowed root step is equality, induction yields equal endpoint roots. Without that additional restriction the equal-root conclusion is false and is not part of the main theorem.

A single Policy object fixes the epoch and version/invalidator predicates. Each hop carries the target guards; induction selects the final ones. This proves currentness only relative to that specified policy, not at a later time or under new invalidators. `epoch` is a model-binding coordinate, not a device that generates evidence. A real new epoch may preserve some guards after revalidation; the proof does not automatically transfer simply because its bytes are unchanged.

Combining these independent arguments with graph composition gives the strongest ordinary result:

> A nonempty path over exact finite-DAG frames, with local target-indexed preserved/fresh evidence covering each independently fixed target requirement, commuting semantic maps, permitted hops and intermediate re-delegation, valid per-hop root custody and target version/registered-invalidator witnesses at one declared policy, transports initial discharged-evidence soundness to final soundness and target closure. It supplies a composed dependency map, a semantic square, a guarded authority path and a root path, together with final currentness guards. It neither invents direct authority nor asserts endpoint root identity when warranted new roots are allowed.

This uses the source guards at their actual scopes. The necessary interpretation/representation choices are separately labelled proposals; the accepted VCT wording is not overwritten.

## 6. Formal candidates, exact pin and executed acquisition boundary

`formal/P03GuardedGraph.lean` is the exact preserved attempt1 graph-only source. `formal/P03GuardedVCT.lean` adds evidence, semantic, complete-frame, policy, guarded-authority-path and composition structures. `P03Audit.lean` requests type/declaration/axiom readbacks for fourteen named theorem targets plus separate model-definition readbacks and restates the full main theorem's expected type. All sources use only core imports; this new pure development does not need Mathlib to be downloaded merely to attempt compilation.

Required pin:

    Lean 4.19.0 / 6caaee842e94
    Lake 5.0.0-6caaee8
    repository Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b

The original `lean-toolchain`, Lake file and dependency manifest are included/bound. The Mathlib pin applies when compiling the separately mapped whole-project sources, not as a hidden dependency of the new core-only module.

This continuation executed local compiler/cache discovery; a direct `lean --version` launch; official Elan installer acquisition; exact official Lean4.19 binary acquisition; and a source-tag acquisition attempt. Native network requests failed at DNS resolution. A separate download tool also failed to obtain the binary. These are actual acquisition attempts, not another assertion that exit127 alone proves unavailability. Raw command/exit/stdout/stderr records and the separately labelled tool-response transcription are in `evidence/TOOLCHAIN_STATUS.json` and its bound evidence paths.

No compiler bytes, new `.olean`, observed theorem type, observed axiom set or formal parse/elaboration result exist. `formal/EXPECTED_TARGETS.json` is a requested inventory, not observed output. Static name corrections and constructor inspection do not change this boundary. The deterministic external runner compiles fresh graph/VCT/audit modules under the exact native executable, preserves raw output and artifacts, checks the expected audited names and absence of forbidden axioms/errors, and fails closed when unavailable. A later run must inspect those readbacks before any target promotion; this packet grants none in advance.

The accepted mapped-native 4.19.0 results and the separate 4.32.2 results stay at their existing scopes. The original strict-wrapper genuine FAIL remains separate from both, and from this run's host acquisition block. No missing historical declaration is recreated under its old identity.

## 7. Optional TRC is not a pure-Q1f prerequisite

The R15 TRC result additionally needs the exact finite temporal model, canonical model binding, eligible action menus, successor/model completeness assumptions, exact fixed points and rank/strategy conditions. Its CORE_ENTRY and co-Büchi objectives are distinct; current local closure is not already temporal persistence. P12's pure COB/action framework and a DAEE application bridge are not supplied here as new PASS results.

Q1f can supply the guarded-version component to that optional wrapper. It does not acquire a blocker from optional TRC when proving the pure finite reason/version theorem, and it does not grant TRC implementation, world-model completeness or DAEE restoration credit when the base theorem succeeds. P02's finite probability/parity work is also not a pure VCT prerequisite.

Thus the remaining **required** Q1f execution gate is the exact native formal run and its readbacks, not additional ordinary research hidden behind “graph-only”, not owner adoption, and not waiting on P02/P12. Optional application claims remain separately unasserted.
