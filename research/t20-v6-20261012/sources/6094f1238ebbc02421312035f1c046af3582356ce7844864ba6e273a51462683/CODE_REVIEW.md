# Narrow independent review of iterator repair

11 October 2026 UTC. Checked the root's `ITERABLE_REPAIR.patch`, original and corrected `research/contracts.py`, added iterator regressions, and original `verify_packet.py` test-launch command. No edits to either reference copy.

**Accept the minimal fix.** `affected_nodes` is typed to accept parent iterables, but the original repeated `set(parents)` inside its closure loop exhausts one-shot iterators on the first pass. Therefore a transitive descendant absent from the first pass is lost. Materialising each parent iterable once before the loop, then traversing those stored sets, restores the declared finite reachability semantics. Set materialisation is appropriate: adjacency multiplicity and iteration order have no meaning for reachability. Empty maps, one-shot changed inputs, cycles (if directly supplied), and already changed computed nodes retain the same closure semantics; this function itself does not validate the documented DAG condition.

Scope is narrow: the supplied direct two-hop call is defective in the original, but `replay_dag` already materialises all parents into sets before calling `affected_nodes`. Its ordinary replay path therefore was not exposed to this particular iterator-consumption defect. The fix does not establish completeness of declared dependencies, source warrant, or correctness of arbitrary callbacks. No broader algorithm redesign is needed for this issue.

Independent control: enumerated all 1,024 forward-labelled four-computed-node DAGs with one primitive source. Constructed an independent outgoing-edge graph traversal oracle, rather than using the same closure algorithm as the expected result. The original helper mismatches on 516 cases; the corrected helper mismatches on zero. Result: `ITERATOR_INDEPENDENT_ORACLE.json`.

Fresh direct optimized test execution:

    PYTHONDONTWRITEBYTECODE=1 python -O -m unittest discover -s tests -v

in the corrected-reference directory passed all 55 tests. Log: `CORRECTED_DIRECT_OPTIMIZED.log`. The 3 added regressions separately passed in a direct optimized run as well. `unittest` assertions remain active under Python -O.

Evidence qualification: original `verify_packet.py` line 81 launches `[sys.executable, '-m', 'unittest', ...]`, with no `-O`. Merely running that wrapper with command-line `-O` does not propagate the optimization flag to its child (absent a separately inherited PYTHONOPTIMIZE environment setting). Consequently wrapper-optimized receipts alone are not optimized test-suite evidence. The direct `python -O -m unittest` run above supplies that evidence. This concerns the precision of the verification claim, not an observed additional functional defect.
