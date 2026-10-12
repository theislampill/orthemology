# Dynamic repair: portable scientific checkpoint v2

Fresh Seventh restart, residual question 3, from the exact Sixth inputs.
Baseline commit identifier: `19de267cd41d2a5eeeb3eaf0b91562f706e2a916`.

## Findings

For the declared versioned live-interlock family, cross-epoch safety and
availability require q+r>n+B with q,r<=n-B. Minimum n is 3B+1, uniquely with
q=r=2B+1. Per-attempt cancellation also uses the same roots: B+1 acknowledgements
give a lasting veto and are obtainable because q>=2B+1.

At the minimum, the exact worst-case opaque repair budget is choose(3B+1,B)
prepare/execute/cancel macro-attempts. More generally it is C(n,n-q,B), a classical
covering number. The supplied exact small tradeoff frontier has B=1 attempts
4,3,2 at n=4,5,6, and B=2 attempts 21,11,8,6 at n=7,8,9,10.

These results require an independently warranted reservation institution,
lifetime-union root budget, actual non-bypassable gates, independently addressed
authenticated control ports, bounded intact service, and a sufficiently long
final authorized quiescent suffix. They do not establish those world facts.
Immediate external revocation, a common physical/selection bottleneck, cached
votes, stale permissions, and instantaneous-only fault bounds have preserved
counterexamples. No R5 defeat or metaphysical conclusion is claimed.

## Read and reproduce

1. MODEL_AND_PROOFS.md fixes the full family, observation order, ordinary proofs,
   cancellation correction, persistence horizon, and premise deletions.
2. COVERING_TRADEOFF.md gives the exact support/attempt reduction and ordinary
   optimality proofs. COVERING_WITNESSES.json contains the actual portfolios.
3. DynamicInterlock.lean and CoveringCore.lean are kernel-checked components.
4. dynamic_interlock.py implements the declared finite model; verify_dynamic.py
   and verify_covering.py replay all finite controls without external packages.
5. SOURCE_BINDING.json binds exact Sixth inputs and their included source copies.
   PRIOR_ART.md records primary-source comparisons and the novelty ceiling.

Full isolated replay:

    python3 verify_all.py --lean /path/to/lean-4.19.0/bin/lean --output-dir private-locator:e814707695f88c100e05

The toolchain is official Lean 4.19.0, with no Mathlib dependency. Its origin and
download checksum are in LEAN_TOOLCHAIN_RECEIPT.json. The verifier does not
download software or mutate a repository. The optional solver generator under
exploration uses SciPy to rediscover upper witnesses; it is not needed for
verification or for the ordinary optimality proofs.

The simulator is a mathematical model, not a deployed gate. Path assertions
check the declared input domain; they are not an extra trusted enforcer.
World ground truth classifies an already permitted bad landing as unsafe; it
does not prevent that landing or inform Actor. Actor uses its own received
descriptor and fixed identity. Receipt bookkeeping is distinct from Root's
actual logical veto/tombstone state.

## Checkpoint status

Author replay passes; independent v2 review is pending. The immutable v1 was
reviewed with required corrections: bounded termination of withheld attempts,
finite-horizon/cap-origin clarity, and fixed-R5 scope. v2 implements charged
cancellation and clarifies those claims. See REVIEW_CHANGELOG.md. Do not present
this checkpoint as an independently accepted or physically certified result.

Ordinary arguments, finite enumeration, and Lean coverage are separately listed
in the replay receipt. In particular, the full C(9,4,2) lower proof is ordinary;
only its finite four-edge sublemma is additionally kernel-checked.
