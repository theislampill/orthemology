# Independent proof review of reset closure

9 October 2026 UTC. This receipt is a written mathematical review of the specified scratch theorem. It is not a kernel certificate, provenance audit, integration approval, or closure decision.

## Bound document

- Document: constructive-t20-20261009/revocation-dependency/THEOREM.md
- SHA-256: 95a636b7eaa8a054657426caeeb569991f6e32ba5bc8f53639d2c919a812aa34
- Review: fresh complete document read and independent proof analysis.
- Outcome: no blocking mathematical finding under the stated full Boolean-product, total-action, independent-reset contract.

## Findings

Theorem 1 is correct. A function on the full finite Boolean product is determined by its essential coordinates. The stable backward dependency set therefore supports output decoding and well-defined updates for every declared action; zero-filling is a valid explicit implementation because the result is independent of the omitted coordinates.

The necessity proof uses the right strengthened induction. It distinguishes every pair differing in a retained coordinate, even when all other coordinates may also differ. Independent resets place the pair in an essentiality witness context without changing the distinguished coordinate. After a coupled action transfers the difference into a previously retained coordinate, the strengthened induction supplies the suffix. Booleanity, admission of every product state, and both-value independent resets are essential to that step and are explicitly assumed.

The action-length bound is correct. At closure depth d, the construction uses at most (d+1)(n-1)+d actions. For nonempty initial support, d is at most n-|I0|, giving n^2-1 when n is positive. The n=1, constant-output, and n=0 edge cases are handled correctly. The proof does not claim optimal distinguishing length.

The quotient and fixed-width bit lower bound follow: continuation-distinguishable states cannot share a deterministic summary with output decoding and named-action updates; all 2^|I*| retained assignments occur. The report correctly limits this to finite control-state encoding rather than the number of real coordinates, an active-RAM bound with a free archive, or total proof-catalogue storage.

Theorem 3 is correct. Removing globally dominated support/cost pairs preserves every terminal output. If a coordinate occurs in an undominated support S of cost k, inventories S and S without that coordinate have different optimum costs; a cost at most k at the latter inventory would dominate the chosen pair. Conversely, outputs cannot depend on coordinates outside the surviving support union. The argument applies separately per verdict and hence to their output tuple.

The residual-pruning discriminator is mathematically valid: the two inventories share the same acquisition-only residual cost frontier but differ after the same withdrawal. Global support dominance remains safe under resets with fixed certificate semantics, while current residual dominance does not supply a withdrawal-complete state. The guarded-action example and dependency chain correctly demonstrate why terminal support alone may omit transition-control dependencies.

The limits are substantive and correct. Removing reset contexts can strictly coarsen the true continuation relation; the OR/acquisition-only example has two classes rather than four. Restricted admissibility, correlated state spaces, actual permission guards, changing source versions, and unbounded histories are excluded rather than silently treated as the same theorem.

## Review boundary

No control run was duplicated for this receipt, as requested. The author's Moore-machine verification and the separate source/provenance review remain distinct evidence. The source-specific claims were checked for mathematical consistency of the displayed examples, not independently re-established against project source documents. This review establishes neither the truth or authority of any guard input nor any human-warrant conclusion.
