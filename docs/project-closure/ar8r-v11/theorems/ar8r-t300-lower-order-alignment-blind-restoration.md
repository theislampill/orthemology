# AR8R-T300 — lower-order alignment can be blind to causal restoration

## Custody and status

- Historical identity: `AR8R-T300`
- Canonical repaired-payload SHA-256: `c06e384f57ecfc289df9c221cbdb696d312a9187de14794882c8c9fb7e62d3e7`
- Preserved pre-repair SHA-256: `e115e04782125f6ad0e23b28bb96da7fbc1820ae7bb090fe048652271c9f8892`
- Formal status: `VALIDATED_EXACT_CAUSAL_RESTORATION_LOWER_ORDER_PROFILE_BLINDNESS`
- Frontier status: `LOCAL_PROVISIONAL_BREAK`, bounded to the checked construction.
- No general probability novelty is claimed.

## Exact construction

For `n >= 3`, take the uniform even- and odd-parity distributions on
`{0,1}^n`. In this construction, every proper-subset marginal is identical
between the even- and odd-parity distributions, although the full parity target
differs.

Thus an operation can change a declared higher-order target `Q` from false to
true while all one-variable and two-variable marginals—and indeed every
proper-subset marginal—remain unchanged.

## Consequence

Thus pairwise-profile movement is not necessary for target restoration.
In particular, causal target restoration can be invisible to a lower-order
profile even when the matched intervention and target change are exact.

Conversely, a finite mixture construction can change the complete pairwise
profile while the declared parity target remains true before and after. Thus
pairwise-profile movement is not sufficient for target restoration either.
The complete pairwise profile and target-specific restoration are logically
independent on the declared finite class.

## Scope firewall

- The construction concerns a declared parity target and exact marginal profile.
- It shows both that pairwise-profile movement is not necessary and that it is
  not sufficient; it does not characterize arbitrary restoration diagnostics.
- It makes no claim about an arbitrary learned embedding or arbitrary metric;
  metric behavior must be assessed separately.
- It is not empirical evidence about trained systems, people, source truth, or
  metaphysical reality.
- It does not by itself identify a causal mechanism beyond the declared matched
  construction.

Cold audit 146 and repair rereview 147 required target-relative language and the
explicit separation of a pairwise profile from arbitrary representation metrics.
The repaired statement above preserves those limits.
