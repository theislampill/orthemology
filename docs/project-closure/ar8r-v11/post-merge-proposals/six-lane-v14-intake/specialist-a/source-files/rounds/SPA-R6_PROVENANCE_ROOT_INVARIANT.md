# SPA-R6 — provenance-root nonmultiplicity under copying and synchronization

**Status:** specialist-local formalization of the repository's existing
provenance/TAC-SAC noncollapse discipline; no historical reconstruction or
novelty.

## Frozen DAG semantics

Each episode is a node in a finite acyclic lineage graph.

- `copy`, `transform`, and `sync` nodes inherit the union of predecessor roots.
- `acquire` nodes inherit predecessor roots and add one fresh authenticated root.
- root labels, carriers, episodes, lineages, copies, and evidential independence
  remain distinct coordinates.

## Invariant

Adding a pure copy/transform/synchronization node does not enlarge the global
root set. Only a typed authenticated acquisition adds a fresh root in this
semantics.

## Countermodels and firewalls

- One root followed by 100 copies yields 101 episodes and still one root.
- Synchronizing two root-bearing episodes unions availability but does not make
  carriers or episodes numerically identical.
- Two distinct root labels may share a hidden upstream anchor, so root
distinctness alone does not prove stochastic or evidential independence.
- Equal root sets do not imply equal carriers, episodes, or lineages.

## Executable evidence

The checker exhausts 23,369 valid operation sequences through five nodes and
performs 92,740 node-level invariant checks with zero failures. Seven mutants
are killed, including root creation by copy or sync, carrier/root count
collapse, distinct-root independence, root-set numerical identity, and
capability/authorization/warrant collapse.

## Conclusion ceiling

```text
AUTHENTICATED_LINEAGE_ROOT_ACCOUNTING_ONLY
NO_TAC_SAC_HISTORICAL_IDENTITY
NO_NUMERICAL_IDENTITY
NO_EVIDENTIAL_INDEPENDENCE
NO_COMMON_KNOWLEDGE_OR_WARRANT
```
