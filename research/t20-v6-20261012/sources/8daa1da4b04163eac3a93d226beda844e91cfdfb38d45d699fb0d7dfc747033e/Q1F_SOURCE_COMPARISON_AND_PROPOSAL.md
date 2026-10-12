# Q1f — guarded reason/version base, VCT, optional TRC

**Primary obligation: PARTIAL.** Exact public statements are now in portable custody; a scoped graph-countermodel analysis, ordinary graph proof and unverified Lean candidate are supplied. Full VCT formalisation is not completed. The optional TRC formal/application layer remains conditional and unperformed.

## 1. Exact queue statement and authoritative status layering

The queue item is:

```yaml
id: Q1f
purpose: guarded reason/version base then VCT and optional TRC wrapper
prerequisites: [Q0]
layers: [PURE, OPTIONAL_WRAPPER]
```

Its packet status is `OPEN_CONDITIONAL_FORMALISATION_QUEUE`; its source queue status is `UNBLOCKED_BUT_NOT_PERFORMED_QUEUE_TARGET`. VCT and TRC are the queue's family labels, not reconstructed historical declaration IDs. Q0 is reusable only at its accepted scoped development and pin, not as blanket historical recovery or compilation authority.

The included `AR8R-PMR007-TEN-RESULT-FORMALIZATION-MAP-V11.yaml` is a **CURRENT_PUBLIC_CORRECTION_OVERLAY**. It records VCT/TRC as `ADMITTED_POST_MERGE_SCOPED_RESULT` with parse, elaboration, kernel and axiom status `NOT_PERFORMED`, external review `OPEN`, owner adoption `PENDING`, and historical identity `NONE`. These later scoped status records govern over the older prose headers “frozen repaired pending fresh rereview.” This P03 packet does not downgrade the admitted ordinary/scoped result and does not promote it to kernel acceptance.

| Target | Exact mapped declaration | Pure dependencies | Wrapper dependencies |
|---|---|---|---|
| PMR-007-VCT-1 / R16_V2 | `VersionCustodyTransport.guarded_reason_dag_composition` | FINITE_REASON_DAG; VERSION_INVALIDATORS | AR2_AR3_REASON_PRESERVING_TRANSPORT |
| VCT wrapper | `VersionCustodyTransport.temporal_eligibility_wrapper` | Same guarded base | Indexed reason-preserving transport and the relevant temporal model |
| PMR-007-TRC-1 / R15_V2 | `TemporalCertificate.model_bound_certificate` | PMR-007-COB-1 | PMR-007-VCT-1; DAEE_CURRENT_VALIDATORS |
| TRC application | `TemporalCertificate.daee_event_local_nonimplication` | Model-relative certificate result | Exact implementation/record correspondence, not just an event label |

The research DAG's Q1f→Q1b edge is OPTIONAL_WRAPPER_ONLY. It does not make the pure graph/game theorem depend on the application wrapper. P12's new co-Büchi work is not presumed available.

## 2. Exact statement custody

The original ZIP contained the queue and declaration map, but not their referenced R15/R16 theorem files. Both were read through the authorised GitHub connector at **exact commit** `03e2604dfcef278b01c60d19b05370fcec4194b6`, then preserved locally. The local bytes independently reproduce the Git blob identities returned by GitHub:

| File in `inputs/supplemental/` | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `PMR-007_FRONTIER_ROUND16_VERSION_CUSTODY_TRANSPORT_AND_TEMPORAL_ELIGIBILITY_V2.md` | 10,299 | `599e9dd9595e26ae857a9a1e7c8a07306a2ec13f25c0c5a0500da544bc45f3ba` | `b665083608bc30a5dcf8faf54a1c1efdccae4621` |
| `PMR-007_FRONTIER_ROUND15_DAEE_TEMPORAL_CERTIFICATE_ARCHITECTURE_V2.md` | 14,916 | `879681edd0f28a35ba9bd87f049ad60c10ea5369474fb8bf2d092de88251299c` | `232ff53bbdad7d402fc9e521eaf3c82e32dd5e78` |

Their full repository paths and transport provenance are in `inputs/SUPPLEMENTAL_IDENTITIES.json`. This is a new pinned public-source read, not historical theorem recovery or owner acceptance. Failed direct-container download attempts are retained separately rather than relabelled successful. No GitHub mutation occurred.

## 3. VCT-1 exact mathematical/implementation scope

A certificate boundary comprises version, frozen claim, provenance root, finite reason-node set, directed dependency edges and **actually discharged** obligations. Each path edge is checked against that actual preceding certificate.

The eleven source guards are preserved individually: (1) input version/claim/root equal the prior output; (2) map domain equals prior nodes; (3) input dependency edges equal prior edges; (4) every input edge maps to an output edge; (5) every output endpoint belongs to the mapped output-node set; (6) preserved obligations were actually discharged at input; (7) preserved plus revalidated obligations cover the complete target-required set; (8) the frozen-claim semantic square commutes; (9) root custody persists unless an independently warranted new root is introduced; (10) authority/delegation, including intermediate re-delegation, is valid; (11) no registered invalidator is open.

The source theorem is finite path composition relative to those contracts, not discovery of a path under private views, a theorem of source truth, a physical model-completeness result, or an assertion that same bytes entail same applicability. Its zero-general-novelty ceiling and indexed AR2/AR3 ancestry remain unchanged.

### Previously negative evidence retained

R16-F01 allowed preserved-obligation laundering; R16-F02 allowed adjacent reason-DAG boundary drift. The V2 source repaired both. Its earlier controls include pairwise-but-noncomposable compatibility, dropped invalidators, non-redelegable authority and semantic noncommutation. They are preserved as source evidence, not replayed for new credit. The standalone historical RP-T2/RP-T40 packets were explicitly absent from the historical source's surfaced bytes; the source's indexed ancestry does not become fresh custody of their exact lost wording.

Specialist A's off-range R7/R9 guard and non-co-Büchi observation scope, Specialist B's incomplete indices, and the missing historical declarations remain separate constraints. The candidate below does not acquire their identities.

## 4. Two countermodels to an untyped graph-guard extrapolation

The proposition tested is **not** VCT with well-formed DAG-typed certificates. It is the stronger, tempting implementation inference:

> Starting from a DAG, exact node-map domain, preservation of every input edge, and output endpoints in the image suffice to make the output a DAG.

That inference is false.

### P03-Q1f-CE01: endpoint collapse

```text
input nodes:  {a,b}
input edges:  {a→b}
map:          a↦x, b↦x
output nodes: {x}
output edges: {x→x}
```

The map has the exact domain, preserves the only source edge, and every target endpoint is in its image. The target has a self-loop.

### P03-Q1f-CE02: injectivity alone is insufficient

```text
input nodes:  {a,b}
input edges:  {a→b}
map:          identity
output nodes: {a,b}
output edges: {a→b,b→a}
```

The map is injective and all graph guards above hold, but the extra reverse edge creates a cycle. Requiring injectivity alone would therefore be an inadequate repair.

The other source guards can be realised without empty obligations: choose a fixed claim and root, exact prior version boundary, one genuinely discharged and preserved obligation d, required set {d}, identity semantic interpretation, valid authority and no open invalidator. The point is confined to graph well-formedness. The finite probe is **not execution of the historical VCT checker** and does not establish that a current checker actually accepts these structures.

If “reason-DAG” is enforced by the type or an explicit validator, both countermodels are outside the theorem's hypotheses. The source theorem is not refuted. The implementation requirement is to retain that well-formedness premise mechanically rather than inferring it from edge preservation or silently weakening DAG to directed graph.

A positive control transports a→b to c→d. The executed probe checks all relevant graph facts and cycle outcomes directly; its three models and raw output are included.

## 5. Proposed finite typed representation and ordinary graph proof

A finite DAG can be represented by a finite node type, an edge predicate and a rank `rho : node → Nat` such that every edge u→v satisfies rho(u)<rho(v). This is a proposed encoding, not a modification to the accepted source definition.

It represents exactly finite DAGs: strict rank growth excludes a closed directed walk. Conversely, a nonempty finite acyclic graph has a vertex with no incoming edge—otherwise repeatedly following predecessors in a finite set yields a cycle. Remove such a vertex, rank the smaller graph inductively, raise those ranks by one and assign the removed vertex zero. This yields a valid rank. The empty graph has the empty ranking. Thus demanding a suitable rank is not a restriction to a special subclass of finite DAGs.

A graph homomorphism f:A→B consists of an actual node function and a proof that every A-edge maps to a B-edge. Its composition with g:B→C is g∘f and preserves edges by applying the two preservation proofs in sequence. A finite chain indexed by its **actual** adjacent graphs has a composite homomorphism by induction on chain length.

For a nonempty directed walk, induct on its construction: a single edge strictly raises rank, and concatenation composes strict inequalities. Mapping the walk along a homomorphism preserves each edge and concatenation. Therefore a homomorphism into a ranked DAG cannot identify the endpoints of a nonempty source walk: their image would be a closed walk with rho(x)<rho(x), impossible.

These elementary ordinary proofs explain both countermodels. No novelty or literature-priority claim is made.

### Authored formal candidate, not a claimed formal result

`proposal/lean/P03GuardedGraph.lean` supplies new, explicitly scoped definitions and proof scripts in namespace `P03Q1f`, importing only Init. The five proposed audit targets are:

```text
P03Q1f.Chain.mapEdge
P03Q1f.walkRank
P03Q1f.Hom.mapWalk
P03Q1f.noClosedWalk
P03Q1f.Hom.noCollapseOfWalk
```

This is **only the graph substrate**. It contains no theorem claiming full version-custody warrant transport, no TRC theorem, no external authority axiom and no claim that an implementation checker matches the encoding. It deliberately does not use the historical mapped declaration names. `P03GuardedGraphAudit.lean` requests exact declarations/types and axiom readbacks.

No Lean executable was available: the recorded `lean --version` invocation could not launch and has capture exit 127. Consequently parsing, elaboration, kernel checking, declaration readbacks and axiom readbacks for these new files are all **UNVERIFIED / NOT_EXECUTED**. No .olean evidence exists or is manufactured. The later handoff pins Lean 4.19.0; accepted 4.32.2 results cannot substitute for it.

## 6. Remaining guarded version/warrant layer: explicit, not assumption-loaded credit

A complete future formalisation must index each certificate by its full context, version, claim, root, reason DAG and actually discharged obligations. It must not identify obligations solely because their text labels agree across versions.

For a proposed typed hop C→C′, let P be preserved obligations, R freshly revalidated obligations and Req(C′) the independently supplied target contract. The remaining proof obligations are:

- P is contained in the **actual** discharged set of C; preserved source evidence has a justified semantic transport into the target context, not mere label equality.
- Each member of R has actual target-indexed revalidation evidence; P∪R covers Req(C′), whose completeness is not chosen after seeing the available evidence.
- The output discharged set is computed from justified preserved/revalidated evidence, not fabricated by declaring the target set discharged.
- The complete adjacent boundaries agree, including the state used for the discharge check; the semantic square, root custody, re-delegation history and registered invalidators are retained separately.

Given those local proofs and a sound initial certificate, the ordinary induction is clear: each required target obligation is covered by a preserved member transported from sound input evidence or by a newly revalidated member. That supplies sound discharged evidence to the next edge. Graph maps compose as above; root/authority/invalidator evidence remains a checked path history. It must not be flattened into an unjustified transitive Boolean authority predicate.

This paragraph is a **specification of the remaining theorem and its conditional proof architecture**, not a new completion claim. In particular the graph candidate does not assume a field `warrant_preserved` and count projecting that field as VCT. Actual semantic preservation, complete target indexing and authority composition still need their declared evidence and formal implementation.

## 7. TRC: exact optional wrapper boundary

R15_V2 defines model-relative acceptance over finite perfect-information games. For CORE_ENTRY, acceptance requires the exact canonical model digest, exact stable kernel and winning region, selected successors inside the winning region, kernel closure, strictly decreasing exact attractor rank outside the kernel and exact rank equality. For CO_BUCHI_PERSISTENCE, it requires the exact nested winning region, successor closure, weak rank decrease at target states, strict decrease at bad states, no reachable bad-containing strategy cycle and exact outer-rank equality. The explicit source fixes K, W_core, W_coB and controllable Pre; the full wording is preserved in the supplemental file.

The old negative evidence remains binding: R15-F01 lacked model-digest binding; R15-F02 checked possible rather than forced progress for CORE_ENTRY. CORE_ENTRY and general co-Büchi persistence must not be merged. The field asserting complete successors for the declared scope is a model-owner assertion; a local checker can bind and require it but cannot prove hidden real transitions absent.

A future TRC wrapper needs the exact P12/PMR-007-COB-1 pure theorem at its admitted hypotheses, the guarded version base, canonical model/eligibility-epoch custody, and implementation correspondence to the named DAEE validators/record. No new P12 result, current runtime model or external-world completeness proof was supplied by this conversation. This layer is conditional/unperformed, not silently imported as a pure prerequisite.

Likewise the historical same-current-record stable/bypass result remains scoped to the exact record and implementations identified in R15. Reading its theorem source does not re-run those validators or establish a present deployment's temporal status. Local CLOSURE is not relabelled RESTORE, human uptake, source truth or world authority.

## 8. Result

Public-statement custody and the guard comparison are complete. The two countermodels are complete only against the untyped extrapolation. The graph proof is ordinary mathematics; its Lean transcription remains unverified. Full VCT formalisation and optional TRC implementation/application acceptance remain open. Q1f therefore stays PARTIAL, with no historical recovery, owner adoption, external review or novelty credit.
