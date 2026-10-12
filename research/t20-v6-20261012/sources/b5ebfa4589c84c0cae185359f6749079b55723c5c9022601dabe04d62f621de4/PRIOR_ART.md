# Primary-source checks and contribution ceiling

Checked 2026-10-02. The core proofs are self-contained; these sources establish
the pre-existing mathematics and prevent novelty or scope inflation.

## Byzantine quorum intersection

Dahlia Malkhi and Michael Reiter, *Byzantine Quorum Systems*, STOC 1997, author
PDF, §5.1, Definition 5.1 and Corollary 5.5 (printed pp.573–574; PDF pp.5–6):
https://malkhi.com/files/byzquorums-STOC1997.pdf

Their dissemination-quorum conditions require a nonfaulty intersection and an
available quorum; the threshold specialization already yields n>3f. §3.1 fixes
authenticated communication and fail-prone sets; the introduction explicitly
discusses correlated failures. Therefore neither the overlap principle nor the
3B+1 number is new here. The interlock model adds a separately posited physical
veto and reservation semantics; their data-dissemination result does not certify
either. Their *opaque masking* terminology is a different technical concept from
our observation of an opaque failed physical path and is not imported.

## Lease mechanisms and their assumptions

Cary G. Gray and David R. Cheriton, *Leases: An Efficient Fault-Tolerant Mechanism
for Distributed File Cache Consistency*, SOSP 1989, §§2 and 5:
https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15712-s12/www/papers/gray89.pdf

The paper treats time-limited rights and explicitly states clock/failure
assumptions. It does not provide Byzantine protection for a freely corruptible
physical repair gate. Our bounded-session commitment deliberately avoids a
real-time expiry claim. Adding one would require actual clock and timing duties
to be budgeted. This comparison concerns mechanism assumptions, not a proposed
improvement on the cited cache protocol.

## Mobile faults and recovery

Miguel Castro and Barbara Liskov, *Proactive Recovery in a Byzantine-Fault-Tolerant
System*, OSDI 2000, introduction, §3, and §4.7:
https://www.usenix.org/events/osdi2000/castro/castro.pdf

They distinguish a bound over system lifetime from a bound over a recovery
vulnerability window. Recovery, authentication refresh and state transfer
carry explicit obligations. The current packet supplies none of that machinery
and therefore retains its stronger bounded-session lifetime-union premise.
Calling that premise an instantaneous or unrestricted mobile-fault guarantee
would be false. The paper's implementation limitations are also expressly
reported (§6.3), illustrating why a simulated mechanism is not a hardware
certification.

## Covering theory

J. Schönheim, *On coverings*, Pacific Journal of Mathematics 14 (1964),
pp.1405–1411, the publisher's original text:
https://msp.org/pjm/1964/14-4/pjm-v14-n4-s.pdf

The point-incidence ceiling bound used here is classical covering theory. Its
elementary pair case is reproved in COVERING_TRADEOFF.md; no new bound is claimed.

Daniel M. Gordon, Greg Kuperberg and Oren Patashnik, *New constructions for
covering designs*, author text:
https://arxiv.org/abs/math/9502238

The standard C(v,k,t) object and constructive covering methods predate this
packet. The maintained La Jolla repository defines this object and records,
among many known cases, C(9,4,2)=8:
https://dmgordon.org/covering-designs/
https://ljcr.dmgordon.org/cover/show_cover.php?k=4&t=2&v=9

Our witnesses were generated locally rather than copied from that table, and
their coverage is checked directly. Our optimality proofs are the ordinary
arguments supplied with them. Database/solver claims are corroboration, not a
substitute for those proofs.

## Scoped contribution

No novelty is claimed for quorums, leases, fault-set intersection, covering
designs, finite search lower bounds, or the displayed small covering numbers.
Relative to the exact Sixth input, the contribution is one complete declared
dynamic composition and its evidence/mechanism audit: current authorization,
old commitment, correlated taint, physical veto, actor-local custody, and
post-quiescence repair are no longer conflated. The support/attempt reduction
then gives an exact cost for that particular interface. Foundational source
claims and R5's status are unchanged.
