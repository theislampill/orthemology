# Monotone reference-clock successor

This addendum extends the independently accepted cancellation-v5 model. Every
v5 scientific source and imported definition is preserved exactly. The added
operation is explicitly a NEW reference-model operation; it is absent from the
accepted compiled service. All existing service calls retain their exact source
semantics. This is a mathematical safety extension, not an implementation or
physical-clock assurance claim.

## Structural result

`setReferenceTime w now` replaces only `World.now`. For arbitrary `now`, including
a backward value, `setReferenceTime_aligned` preserves the entire `Aligned`
relation with the IDENTICAL common state. Plant, full authentic effective policy,
root memories, fault set, thresholds, completed certificate provenance and raw
control epochs are unchanged. The common state has no clock field, so a clock
update translates to an empty primitive history.

This result requires no new lease-validity or certificate-validity hypothesis:
`Aligned` never requires a stored lease to be live at every intermediate instant.
The exact unchanged runtime preparation and attempt functions re-evaluate their
local admission predicates using the current `World.now`. Following any update,
those checks use the updated annotation. This does not replace or refresh a
correct actor's separate stored `observedTime`, which remains a premise of
`propose`. A currently live actual lease does not make a non-admitting actor
observation valid.

## Event class and correspondence

`MonotoneReferenceEvent` embeds every event of `RuntimeWithCancellationEvent` and
adds `advance now`. The advance constructor has the explicit premise
`w.now ≤ now`. Thus zero advances, equal-time advances and arbitrarily large
forward advances are permitted. Backward updates are excluded from this trace
class, although the unrestricted structural lemma remains true for them.

The inherited events include actual aggregate preparation, attempt, cancellation,
authentic source-bound owner certification and recorded or unrecorded delivery.
All previous restrictions remain: valid bounded full envelopes; authoritative
post-base policy stream; fixed lifetime taint; initial alignment at the stated
raw base; complete post-boundary certificate evidence; atomic whole-plant/time
observation and live non-bypassable mediation. The source-bound owner transition
restrictions are unchanged. The exact installed/draft/control version distinction,
ordered path and full-command identity survive the translation.

`monotone_reference_trace_refines_history` proves a common primitive history and
full final alignment for every finite trace of this explicit enlarged class.
Clock events stutter; actual operation events retain their previously proved
partial effects and timestamp annotations. Current full-policy admission and
full-envelope cancellation transport across the enlarged class. The old v4 and
v5 trace types remain unchanged and retain their constant-clock theorems; the
new class has a different name and a proved monotonicity theorem.

## Expiry derivation and its exact limit

`localStep_before_lease_end` extracts `now < command.leaseEnd` separately from
`CriterionInstallation.InstallGrantValid` and `TypedCriterionGuard.GrantValid`
via the exact imported acceptance theorems. It assumes no additional safety
axiom. At or beyond the fixed command's lease end, the exact local result is
`none`. In an aligned reachable runtime snapshot, a successful attempt would
contradict this bound. Monotonicity therefore gives permanent rejection of that
fixed complete envelope after its lease end across every finite continuation of
`MonotoneReferenceTrace`. Renewal by issuing a different command is not forbidden
or confused with replay of the original envelope.

Backward-time resurrection is a genuine boundary. On the exact unlanded,
uncancelled native installation envelope, time 100 rejects and rollback to 2
accepts again without changing the command or commitments. A theorem excludes
any such endpoint pair from the monotone trace class. Cancellation differs:
changing the annotation cannot erase a durable tombstone, and the controls
retain rejection even after a forward-then-backward pair of updates.

## Non-vacuous exact-source evidence

The controls retain the 3013-byte accepted source, raw installation epoch 2 and
raw repair epoch 3, thresholds n=4, B=1 and q=r=3, and chosen intact path [1,2,3].
They exercise an installation-to-repair trace with reference times 3 and 4;
the full final plant is exactly the existing `repaired` record. Both installation
and repair admit at time 89 and reject at their exact lease boundary 90, before
the grant's expiry 100. Prepared commitments survive the clock update and cannot
bypass the new current-time test. Actor observation 2 remains 2 after a world
update to 90; its old proposal can still be constructed while the live operation
rejects. Observation 0 fails proposal admission even when the actual time 2
operation would succeed.

The chosen path witnesses existence. It is not a strategy that discovers the
fault set. All controls use ordinary kernel-checked proofs, not native-decide or
a custom desired-result axiom.

## Remaining warrant burden

Monotone numerical annotations are not proof of authentic clocks, elapsed time,
physical deadlines, synchronisation, bounded skew or a service implementation of
set-now. Large time jumps can exhaust a lease without useful work. Safety gives
no progress, delivery schedule, stable authorised window, bounded service or
residual-work argument. Full runBatch refinement, alias-runtime composition and
N2/T0/R5 remain separate. Root-copy coherence, actual authority/reservation,
source interpretation and trustworthy plant/time observation remain external.
