# Unknown root attribution: bounded extension

For m authenticated labels with one unknown fixed c-label root class, singleton
roots elsewhere, and B>=1 actual-root faults, put k=B+c-1. In the declared fixed
observable path/quorum interface:

- Exact robust overlap is at least k+1 shared labels, interpreted through every
  possible actual-root map.
- Safety and repair/revocation availability are possible exactly when m>=3k+1.
- At the minimum, q=r=2k+1 labels and k+1 cancellation labels suffice.
- The exact opaque macro-attempt cap is choose(3k+1,k).
- Actual roots needed are 3B+2c-1, an extra 2(c-1) relative to known attribution.

For one unknown aliased pair and one faulty actual root, five labels over four
roots are insufficient, as are six labels over five roots. Seven labels over
six roots work with 5-label paths/quorums, 3-label cancellation and 21 attempts.
Labels are never assumed to be independent roots.

Read GENERAL_UNKNOWN_CLASS_THEOREM.md for the complete ordinary proofs,
observation contract and countermodels. UNKNOWN_ATTRIBUTION.md develops the
one-pair case. The source family is fixed throughout a session. The negative
claim concerns fixed observable path/quorum families and the stated macro-trial
observations; it does not rule out richer adaptive mapping probes or redesign
after new provenance evidence. All v2 physical, institutional, control-access,
service and horizon conditions remain explicit dependencies.

Portable replay:

    python3 verify_attribution_all.py --lean /path/to/lean-4.19.0/bin/lean --output-dir private-locator:8fbf60e0c0d3d301c6d8

No network or third-party Python package is needed. Exact v2 Lean dependencies
are included. The new Lean source verifies the pulled-back label budget,
sound overlap/cancellation witnesses, maximal-fault-world realization and root
count arithmetic. The sharp image iff, nonuniform-family impossibility and
covering search lower bound are supplied as ordinary proofs, not described as
fully formalized.

Ordinary/test freeze manifest:
`f99ef03c66d51eb5689f8eff1fcd7af6c2430e7fa8fab78434fa1fdb5a77eae1`.
Additive Lean freeze manifest:
`4c0af26b40c1e7f16a37af2bf63d5705f12c09fea1c88375bb7fe1d13b274623`.
Independent review is recorded by its own additive binding when present.
Running a verifier does not itself constitute independent acceptance.

The method uses established fail-prone quorum and covering reasoning. No new
general quorum mathematics, unrestricted mobile-fault theorem, metaphysical
unification, or fixed-R5 defeat is claimed.
