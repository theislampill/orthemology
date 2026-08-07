# PMR-007 Deep Round J V1 cold audit

```text
audited candidate: PMR-007-UCA-1-CANDIDATE-V1
frozen receipt: PMR-007_DEEP_J_V1_FROZEN_HASHES.sha256
disposition: REPAIR_REQUIRED
```

## Reconstructed theorem

The finite-DAG equivalence is correct. In a finite DAG, every vertex has a root ancestor. Upstream directedness collapses any two roots, and one unique root reaches every vertex. The primary checker verifies 33,867 topologically ordered DAGs through six vertices with no mismatch.

## Blocking findings

### DJ-F01 — ancestry was promoted to sufficient actualization

A graph-theoretic root that reaches every vertex is a unique **lineage root**. It does not follow that the root alone is sufficient for every downstream efficacy. A downstream actualizer may require conjunctive primitive inputs, enabling conditions, abstract order, or external contributors not represented by the ancestry path. V1 repeatedly calls the root a supplier of all efficacy. Narrow the theorem or add explicit compositional-sufficiency and external-input-closure guards.

### DJ-F02 — edge completeness is not explicit enough

`DOMAIN COVERAGE` says relevant actualizers are represented, but a complete vertex set does not guarantee a complete dependency relation. Hidden borrowed-efficacy edges can turn a registered root into a derivative node. Add a separate relation-completeness/custody condition.

### DJ-F03 — vertex unity is not bearer simplicity

A single graph node may denote a distributed collective, composite powers field, or carrier-boxed package. Unique root-node identity does not establish simple substance, one subject, or common-bearer co-instantiation. State the node-granularity dependency explicitly.

### DJ-F04 — same-respect typing must govern transitive closure

If edges mix causal contribution, logical applicability, communication, authorization, or temporal precedence, reachability is not one efficacy lineage. V1 states the intended edge type but does not require that composition preserve that same respect. Add a homogeneous/composable lineage guard.

## Nonblocking notes

1. The cycle and observed-output countermodels correctly show that acyclicity and full-graph quantification are load-bearing.
2. Infinite well-founded extensions are not proved and should remain outside the admitted scope.
3. The result is standard order/graph theory and receives no general mathematical novelty.

## Required repair

```text
rename the exact conclusion UNIQUE_UNDERIVED_LINEAGE_ROOT;
separate the stronger universal-actualizer corollary;
add relation completeness, same-respect composability,
external-input closure, and node-granularity guards;
preserve plural, cyclic, incomplete-registry, separate-order,
and impersonal-root countermodels;
run an independent all-digraph/SCC rereview.
```
