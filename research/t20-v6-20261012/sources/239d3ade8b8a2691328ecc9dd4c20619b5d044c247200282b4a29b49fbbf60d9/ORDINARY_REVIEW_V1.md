# Independent review: one unknown correlated-root class

Reviewer: `review_dynamic_repair_proofs`. Date: 2026-10-02 UTC.
Ordinary source target: `../attribution-author-freeze-v1`.
Manifest SHA-256: `f99ef03c66d51eb5689f8eff1fcd7af6c2430e7fa8fab78434fa1fdb5a77eae1`.

## Disposition

**The ordinary Theorems A–E are accepted at the explicitly bounded fixed-family observation interface.** No mathematical correction was found necessary in the frozen ordinary source. The author's finite checks were independently replayed from copied bytes; all outputs match. Added Lean lemmas require their own exact-byte receipt before receiving any kernel-verification credit.

This result is conditional on every retained v2 mechanism/institution/service premise and on a warranted family of static root maps with exactly one c-label class. It does not establish that family as an empirical fact. It does not apply to arbitrary map-discovery protocols, partial-control probes, dynamically redesigned families, multiple unknown nonsingleton classes, unrestricted root churn, or a changed authorization/mediation interface.

## Cold proof review

### A. Exact robust root-image safety

The root-image identity is correct. Each shared label outside the special class A contributes a distinct shared root; A contributes one shared root precisely when it intersects both path P and revocation set R. Thus

    |pi_A(P) ∩ pi_A(R)| = |P∩R| − |A∩P∩R| + 1[A meets both P and R].

For nonempty label intersection of size s, including min(c,s) shared labels in A achieves the minimum max(1,s−c+1). Filling A when c>s is possible because c≤m. No map can collapse more than c shared labels into a single root, and nonempty common labels always have a common image.

For disjoint label sets, the image intersection is at most one. Every c-subset meets both sets exactly when c exceeds both complement sizes, equivalently c>m−min(|P|,|R|). This forced-bridging exception is handled rather than lost in the label counting. Since B≥1, even an unavoidable one-root bridge is corruptible. Therefore universal actual-root overlap >B is equivalent to s≥B+c=k+1.

The B≥1 restriction is substantive. For example, m=4,c=3 with P={0,1}, R={2,3} has one common actual root under every compatible map despite no shared label. It suffices for a zero-fault overlap condition, so the positive-B equivalence cannot simply be extended to B=0.

The necessary stale-landing witness uses one fixed map and corrupts at most B shared actual roots. Correct-root coherence across aliases is essential: revocation learned through any label must close every old-command copy owned by that root. The theorem does not prove that physical coherence from shared fault provenance alone.

### B. Observable availability and maximal-world realization

A tainted special root affects c labels; each other tainted root affects one. Thus at most B actual faults affect at most k=B+c−1 labels. If the special root is good, the bound improves to B, which still lies below k.

Every k-set T is a real maximal world, not a fictional independent-label corruption: choose a c-subset A of T, corrupt its one root and the B−1 singleton roots in T\A. B≥1 ensures c≤k; B<m−c+1 ensures k<m. The construction has exactly B distinct actual fault roots and exactly T tainted labels. Any smaller actual tainted-label set extends to a k-set, proving both directions of the availability criterion.

The map/fault envelope is static for the horizon. Different realizations used in universal quantifiers are not simultaneous roots or simultaneous faults in one execution.

### C. Sharp threshold for arbitrary fixed families

For m≤3k, two k-sets can have union size min(m,2k). Universal availability forces an allowed P avoiding the first and an allowed R avoiding the second. Their label intersection has size at most max(0,m−2k)≤k. The robust image criterion then supplies one compatible map and ≤B actual faults violating safety for that allowed pair.

This is a valid quantifier argument: availability in different compatible worlds forces membership in fixed F and G; because every allowed pair must be safe in every world, the final violating pair can be evaluated under a single newly selected fixed map. It is not the invalid combination of independent counterworlds into one actual history.

Conversely, all (m−k)-subsets provide safety and availability when m≥3k+1. Uniform threshold families satisfy exactly q+r>m+k and q,r≤m−k. At equality, q=r=2k+1.

The actual-root minimum is m−c+1=3B+2c−1. Compared with 3B+1 actual roots when the actual map is known and representatives can be selected, the extra count is exactly 2(c−1). This comparison changes the attribution knowledge, not the fault budget. It is not a universal lower bound on all ways to learn attribution.

### D. Cancellation

Any k+1 labels represent at least (k+1)−(c−1)=B+1 actual roots; an untainted acknowledger therefore supplies the continuing physical veto. A selected 2k+1-label path retains at least k+1 good labels, so the retained independent control-port service makes the certificate available.

For any fixed d-label certificate with d≤k, all d labels can be covered by ≤B actual fault roots in a compatible map. If d<c, place them inside the c-class; if d≥c, place a c-class inside them and cover the remaining d−c≤B−1 singleton labels. Hence k+1 is the minimum uniform count-based closure certificate under this uncertainty. This counts the labels' minimum possible actual-root image; it never regards c aliases as c independent roots.

As in v2, this implication requires authenticated original-recipient cleanup, full-command/path/unique-nonce binding, correct-root coherent tombstones before acknowledgement, and independently bounded service despite tainted path members. These remain premises, not outputs of cardinal arithmetic.

### E. Covering and exact macro-attempt count

For uniform q-label paths, a path is untainted exactly when its complement contains the actual tainted-label set T. Every maximal k-set has the fixed-world realization above, so the portfolio problem is precisely C(m,m−q,k).

The expanded observation interface does not invalidate the lower bound: the text explicitly constructs per-label preparation and cancellation replies with identical content and timing across every still-uncovered canonical world. The faulty root can suppress execution while returning those same replies. Complete-command cancellation closes only the current attempt; fresh subsequent nonces avoid state-history disclosure through cancelled commands. The quiescent lower-bound suffix has no owner transitions.

This is a permitted homogeneous transcript for full selected-path preparation/cancellation. It is not a proof that coherent root state is unlearnable under partial cancellation, partial epoch delivery, old-command queries outside the path, state readout, or physical-correlation experiments. Those observations are expressly outside the theorem.

At m=3k+1, q=2k+1, a k-set complement identifies exactly one canonical maximal-fault world in which that path succeeds. Fewer than choose(3k+1,k) distinct trials leave some fixed world uncovered. Uniform averaging over those worlds yields the randomized almost-sure-cap lower bound without exposing private coins. Exhaustive trials attain the bound using the v2 closing mechanism. Phase counts retain the stable-delivery, residual-old-work and finite-horizon qualifications.

## Parameter and source checks

- c=1 reduces to the accepted distinct-root result; the designated singleton class creates no genuine aliasing.
- B=1,c=2 gives m=7 labels, n=6 actual roots, q=r=5, three cancellation labels and 21 macro-attempts.
- The five- and six-label nonuniform-family arguments are valid special cases.
- B<n implies k<m; maximal bad-label sets never exceed the label universe.
- Near-saturation cases (for example c=m−1,B=1) correctly fail availability/safety coexistence even though forced alias bridging can occur.
- The underlying dependency hashes match the accepted dynamic v2 manifest and independent review. The extension imports no new metaphysical or R5 bridge and does not enlarge fixed R5's resources.

## Reproduction evidence

All nine ordinary-freeze entries matched their manifest sizes/hashes before replay. `verify_attribution.py` was run only in `freeze-v1-replay/`, a reviewer-owned copy. It exited zero. `ATTRIBUTION_CHECK_RESULTS.json` and `ATTRIBUTION_COUNTEREXAMPLES.json` match author bytes exactly.

Author finite replay enumerates 2,353,024 actual image-pair cases through m=7, 417,472 robust-equivalence cases, 5,552 map/fault instantiations, 55 feasibility/obstruction parameter cases, and 1,638 forced-bridge cases. Its minimum constructions additionally check 4,069 map/fault instantiations, 459,397 selected paths, 37,754 cancellation root images and 43,692 failed-transcript comparisons. These counts include repeated representations when c=1 and are enumeration-case counts, not necessarily distinct physical worlds.

Reviewer-owned `independent_root_image_checks.py` imports no author implementation and uses explicit partitions/frozenset root images instead of the author's bitmask routine. It passes 2,353,056 image-pair cases for m=2…7, 417,488 robust equivalences, 5,556 fault-world instantiations, 741 canonical maximal-world realizations and 56 obstruction parameter cases. It separately verifies the B=0 forced-bridge exception. Output: `INDEPENDENT_ROOT_IMAGE_RESULTS.json`.

All enumeration is bounded corroboration. The general A–E conclusions above are ordinary proof assessments. The common transcript is an explicitly permitted model construction, not a physical side-channel experiment or proof that no richer experiment could distinguish maps.
