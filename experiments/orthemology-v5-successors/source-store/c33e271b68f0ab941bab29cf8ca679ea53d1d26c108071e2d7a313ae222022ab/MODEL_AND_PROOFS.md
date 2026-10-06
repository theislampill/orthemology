# Charged versioned interlocks: a bounded dynamic repair family

Fresh Seventh restart, question 3. Baseline: `19de267cd41d2a5eeeb3eaf0b91562f706e2a916`.
This file does not import or reconstruct any missing prior Seventh result.

## 1. Result and its exact ceiling

Consider the **versioned live-interlock family** defined below. A repair attempt
uses a path containing exactly q distinct root-controlled gates. A change of
version or permission becomes effective after acknowledgements from r distinct
roots. At most B distinct roots ever lose any relevant duty during the declared
session horizon. Commitments, revocation memory, root attribution, and physical gates
belong to the same roots and the same budget.

The threshold contract is feasible precisely when

    q + r > n + B,      q <= n - B,      r <= n - B.

Consequently the minimum number of roots is n = 3B+1, with the unique thresholds
q = r = 2B+1 at that minimum. The first condition prevents an old authorization
from landing after effective revocation. The latter two require a repair path
and a revocation quorum to remain available when B roots withhold service.
At the minimum, and under the declared opaque path-failure observations, the
exact worst-case number of sequential path attempts after quiescence is

    N = choose(3B+1, B).

This bound counts a real restrictive interface: an attempt needs **all** q gates
on its selected serial path to cooperate, and a failed attempt exposes no failed
root. It is not a general lower bound for distributed repair, nor a claim that
all architectures need this many trials. Parallelizing every path trades this
sequential cost for physical deployment; exposing verified individual vetoes
changes the observation interface.

The quorum inequality is standard Byzantine-quorum mathematics, not a novelty
claim. The local advance over Sixth is the complete dynamic composition: a
version/permission change, an accounted persistent veto, a repair envelope,
explicit lifetime-fault accounting, a sharp restricted execution bound, and
counterexamples when one of those bridges is removed. No physical installation,
unrestricted mobile-fault tolerance, metaphysical unification, or R5 defeat is
claimed.

## 2. Frozen family before selecting a protocol

### 2.1 World state and the target

The plant implements a total binary-input rule. Its state is either a table
P in {0,1}^2 or an absorbing unsafe state X. The current independently warranted
specification is a descriptor

    D_e = (target_id, target_version, control_epoch=e,
           recipient_id, permission_scope, target_table T_e).

At epoch e the persistent target is P=T_e, on **both** inputs. An authorized
repair R_e replaces the entire table by T_e; R_e is idempotent. X is outside
every target and violates a retained hard safety obligation. Holding changes
nothing. The initial table is defective. Changes can alternate T=(0,1) and
T=(1,0); therefore persistence relative to an obsolete target is insufficient.

An effective version change changes D_e and hence may make the existing table
non-target. It is not itself X. Revoking a recipient's permission while leaving
the target table and target version unchanged is also permitted: it advances
the **control epoch**. An unauthorized write is unsafe even if its bytes happen
to equal the right table. These two cases force version and permission to be
separate from payload correctness.

The family grants the target descriptor's adequacy and the legitimate owner's
authority to request a transition. Those are substantive external inputs, not
conclusions of a fault-tolerance proof. There are no concurrent competing owner
proposals: permitted transitions form one serial sequence, with one pending
transition at a time. This is not a consensus or authority-selection protocol.

### 2.2 Root units and correlations

R={0,...,n-1}, with 0<=B<n. Root i owns all of the following duties together:

1. root-labelled evidence and commitment issuance;
2. local epoch/permission state and acknowledgement issuance;
3. durable epoch-revocation and command-cancellation memory;
4. exact-payload/recipient/version binding for its commitment;
5. the live physical veto on every path copy assigned to i;
6. all active addressing, path-selection, transport and dispatch duties needed
   from i to prepare and execute that path.

Let C_t be the roots whose duties fail at time t, including roots with tainted
relevant state not yet correctly recovered. The premise is

    C* = union over the session of C_t,     |C*| <= B.

The fault pattern may vary with time and roles, and a root may appear correct
before or after a fault. However every root ever faulty is charged once in C*.
An i outside C* obeys every duty throughout the session. A root inside C* may
behave arbitrarily, including giving completely truthful evidence, signing a
valid commitment, falsely acknowledging revocation, and later withholding or
opening its gates. Nothing is inferred from apparent good behavior.

This is a **lifetime-union** bound over the whole claimed session horizon H.
H may be finite; then persistence is only claimed through H. An infinite-horizon
corollary requires the same bound over the entire infinite history. The budget
is not reset after repair, after a version change, or after apparent recovery.
Without that continuing premise no indefinite persistence is established.
It is stronger than
an instantaneous bound |C_t|<=B. No independent sensor/actuator budgets, free
trusted revocation service, or statistically independent failures are assumed.
Different gate copies sharing i count as one root, however many copies exist.
Authentication means a purported i-event violating i's contract charges i to
C*. Its engineering warrant is an assumption, not something derived from a
string bearing i's name.

### 2.3 Actual support and the plant boundary

Every available repair path L is an actual q-subset of R. All q root gates are
live serial interlocks on that path. Plant mutation occurs only by an atomic
landing event on a selected path. At that event **every** actual gate in L must
permit the same complete command. An untainted gate has continuing power to
stop the event. A permission returned earlier is not a cached substitute for
this live veto.

All licensed plant writes, including writes initiated by faulty dispatchers,
must traverse one of these registered q-root paths. A faulty root cannot change
the command after another root's successful final check, open a physical bypass,
write autonomously after landing, or turn a withheld attempt into some other
plant mutation. Those restrictions are exactly the non-bypassable, atomic,
payload-binding causal mechanism being posited. A faulty gate can arbitrarily
open or close **its own** gate; it cannot annul another root's physical veto.

There is no logical certificate-combiner that is silently assumed to enforce
the plant. A displayed quorum has no physical effect by itself. The model's
plant boundary is realized by the serial gates, not by a new trusted common
software gate. An implementation with a corruptible common downstream writer
does not meet this boundary; the deletion test keeps that writer in the same
budget and fails. The finite simulator and Lean proofs verify the declared
semantics. They do not prove these hardware/implementation facts about an
external system. Inert wiring and the plant's stated transition interface are
part of the model boundary; any actual shared active dependency omitted from
the root map defeats applicability until accounted for.

All q-subsets are available paths in the symmetric family. This can mean
reconfigurable serial routing with the declared non-bypassability, or one
prebuilt branch per subset. The latter uses q*choose(n,q) gate occurrences but
only n fault roots. The theorem does not certify an uncharged reconfiguration
controller. Sequential trials count attempts; the physical gate occurrence and
root costs must not be conflated.

The actor's own policy execution is correct in this bounded family. Between its
output and a path's landing, an entirely untainted path must be independently
addressable and executable using only the duties of roots in that path. A
corrupt root outside L cannot prevent, divert, or re-route an all-untainted L
attempt. This is the **causal liveness support** premise, in addition to safety
mediation. If one active common selector g can block every path, g belongs in
every liveness support; the q-subset model and its covering bound are then false.
The selector is not made trustworthy by calling it the controller. The simulator
implements this explicitly declared direct-address interface; it does not prove
that an external dispatcher realizes it.

Control access is additionally **per-root and independently authenticated**:
an untainted selected root receives and answers preparation/cancellation
requests within the declared service bound even when another root on its serial
data path is tainted. Another path root cannot suppress that control port.
Every active dependency of the port is part of its same root's duties. A shared
control-channel blocker is therefore an omitted common support, not a harmless
wire. All-good data-path addressability alone would not imply this condition.

### 2.4 Complete command and commitment

A command is

    K=(target_id,target_version,control_epoch,recipient_id,
       permission_scope,exact target table,nonce,actual path L).

Each untainted i in L grants a commitment only if K matches its locally
authorized descriptor and a live local permission. It binds the **whole** tuple
to its interlock. Its continuing promise is conditional:

    I will permit only this exact authorized operation, while my commitment
    remains live; after revocation I will physically veto it.

It is not a promise that every attempt will succeed, that no root will fail, or
that permission can never be revoked. The model does not need a wall clock;
the commitment spans preparation to its landing or cancellation in the same
bounded session. A real-time expiry would require charged clocks and a timing
model in addition to this result.

At landing an untainted gate compares the actual command with its commitment,
checks its local epoch/recipient/scope, and checks that its revocation memory
does not prohibit the command or permanently cancel its unique nonce/path.
The authenticated requester must be the committed recipient; copying another
recipient's prepared tuple does not impersonate that recipient. A faulty
dispatcher substituting the payload or
recipient causes any untainted gate to veto. This is a live execution contract,
not an inference from having a correct proof file or a signature.

### 2.5 Requested, effective, and external revocation

To transition e to e+1 the legitimate owner requests revocation of e and supplies
the next descriptor. Upon acknowledging this request, an untainted root first
closes every e-commitment and durably records e as revoked. It never again opens
an e-gate in the session. A corrupt root can falsely acknowledge while leaving
its gates open. A root-labelled acknowledgement set S of size r completes the
transition: D_(e+1) becomes current, and all D_e permissions expire. A complete
certificate can be delivered to any correct root so it can install the next
descriptor. With one pending owner transition, acknowledgements cannot certify
two inconsistent owner-selected targets. An untainted acknowledger does not
enable the next descriptor before the full transition certificate exists;
early close is permitted, early new-epoch grant is not.

**Independent institutional premise:** a requested revocation is not yet an
effective cancellation of the reserved right. The legitimate authorization
institution must keep the old lease valid until the specified certificate
completion, or close all affected physical paths sooner. This cannot be
manufactured by redefining the user's actual permission. If actual external
consent can cease immediately, before either condition holds, the theorem does
not authorize an old action. Section 7 gives the evidence-compatible failure.

Thus three events remain distinct: owner request, effective certified control
transition, and actual external permission change. In this family the latter
two coincide by an independently warranted reservation contract. That bridge is
not established merely by quorum algebra.

### 2.6 Observation order

The actor knows the declared contract, root identities, fault budget, target
descriptor and its local entitlement. It sees labelled responses to its own
preparation and knows the selected path. The sequence for an attempt is:

1. actor prepares K and obtains its root commitments;
2. the selected actual path L and complete K are exposed;
3. unobserved root faults and an owner-requested revocation may occur;
4. any revocation quorum may complete;
5. the actual live interlocks determine landing.

The actor has no fresh oracle reporting C*, every other party's messages, or
the last global epoch. Every extra finite polling exchange still has a final
observation followed by the same permitted gap. A valid old commitment can
remain in the actor's evidence after revocation. Protection must come from the
live veto, not from pretending that the actor has learned no change occurred.

A failed path produces no verified identity of a root that blocked it. Before
the first successful trial, the strongest optional effect receipt is NO_EFFECT.
Labelled preparation and cancellation replies are visible, but a faulty root
can send exactly the same replies and timings as an intact root while withholding
only execution. The lower bound uses that admissible homogeneous transcript;
a cancellation certificate is not a fault diagnosis. The batch does not stop
on an untrusted SUCCESS label.

Every macro-attempt has three actor-controlled logical phases:

1. **Prepare:** directly request every root on L; wait the declared bound for
   intact-root replies. If not all q commitments arrive, skip execution.
2. **Execute:** if prepared, submit the exact command and allow the declared
   bound in which an all-untainted path lands. A tainted path may withhold forever;
   the actor does not wait for its acknowledgement to advance to cancellation.
3. **Cancel/close:** send authenticated cancellation of this entire command to
   all q selected roots. An untainted root permanently closes its gate for this
   complete tuple/nonce/path **before** acknowledging. Collect c=B+1 distinct
   selected-root acknowledgements; close the macro-attempt only then.

The original recipient has a separately warranted cleanup right to cancel its
own unique attempts, retained after later action permission is revoked. It
cannot cancel another recipient's command. Authentication is a root duty, and
counterfeit acknowledgement/acceptance is charged to the affected root. The
correct actor never reuses a nonce and never cancels before the execution bound.
Replayed cancellation thus affects only the already closed attempt. Arbitrary
third-party cancellation is rejected; unbounded control-channel starvation is
outside the intact-root bounded-service premise, not silently tolerated.

These phases rely on correct actor scheduling and independently bounded service
of intact control ports. They do not rely on a global cancellation oracle or a
new trusted physical clock. Logical phases are the model's synchronous service
interface; no wall-clock duration is inferred. If respective warranted bounds
are Dp,De,Dc, M attempts use at most M(Dp+De+Dc) logical service units. Where each
bound is one phase, the count is 3M phases, not M primitive rounds.

Feasible q/r thresholds imply q>=2B+1 (Corollary 2.1's inequalities), so at least
q-B>=B+1 selected roots are untainted and answer cancellation. The c=B+1 replies
include at least one untainted root with a continuing physical veto. Therefore a
pending command cannot land after cancellation completion, even if bad roots
later open. A lawful landing that wins the race before cancellation remains the
same idempotent repair; closure does not undo it. Durable tombstones also reject
late preparation/replay for that command, and cancellation preserves all other
fresh-nonce repair routes. Thus even a withheld path releases actor control
safely and in a bounded macro-attempt. This closing mechanism is charged to the
same selected roots, with no additional trusted support.

### 2.7 Objective and allowed persistence claim

Safety requires never entering X and never making an unauthorized or stale
write, even across version and permission changes. Waiting is safe but does not
satisfy repair progress. Liveness is conditional on a final quiescent epoch e*:
after some point no further effective transition or pending revocation occurs,
the actor is authorized for R_e*, the completed final descriptor/certificate is
delivered to the actor and all untainted roots, and intact-root requests complete.
The quantitative cap counts newly initiated final-descriptor macro-attempts
after stable delivery, not attempts from an unobserved last global change. If
delivery occurs during an old attempt, its safe cancellation must finish first;
that residual phase latency is additional. Then the actor must restore the whole target table in a bounded
number of macro-attempts. If H is finite, enough permitted phase slots for that
complete batch must remain inside H; the fault-bound premise cannot be extended
past H by counting more attempts. The restored table must stay
correct through H while e* remains current, the lifetime-union bound continues
to hold, and every mutation remains mediated.

Infinite hostile target changes, permanent loss of permission, unbounded delay,
or new unmediated plant faults are not smuggled into that conclusion. They are
separate deletions of the progress or persistence premises.

## 3. Ordinary proofs of the exact threshold

### Lemma 1: untainted cross-intersection

For any q-subset L and r-subset S,

    |L intersect S| >= q+r-n.

If q+r>n+B, this intersection has more than B elements. As |C*|<=B, there is
i in (L intersect S) outside C*. This root's same fault unit supports both its
revocation acknowledgement and its continuing physical veto. Counting them as
two independent witnesses would be wrong; one untainted shared root suffices.

### Theorem 1: stale action exclusion

Suppose an e-revocation quorum S has completed. By Lemma 1 each possible old
q-path L shares an untainted root i with S. Before acknowledging, i closed all
e-commitments and it retains that veto through landing. Therefore not all gates
of L can be open for an e-command. No old e-command lands after completion.
This also covers permission-only epoch changes and arbitrarily stale copies.
It does not require the actor to observe the revocation certificate.

### Lemma 2: binding and containment

The threshold conditions imply q>B. Indeed r<=n gives q>B directly from
q+r>n+B. Thus every q-path has an untainted gate. That gate permits only the
exact operation and recipient/scope bound in its valid local commitment.
A substituted payload, forged recipient, missing gate, or unsupported command
cannot pass an honest final check under the plant boundary. For a command whose
epoch has become old, Theorem 1 supplies a veto. Every landing therefore is an
actually current, authorized exact repair. Every blocked landing is the identity
on the whole plant and future path resources. The cancellation phase then closes
any pending copy of that command before proceeding to the next macro-attempt.
No failed action silently consumes the only future repair route.

This is why a quorum's content truth alone would not prove containment: the
conclusion also consumes actual non-bypassable mediation and exact landing
binding. These are premises with explicit deletion tests, not proof outputs.

### Lemma 3: cancellation has its own charged threshold

For a certificate formed from c selected-path roots, durable cancellation is
warranted when c>B: at least one acknowledger is untainted, closes before its
acknowledgement, and prevents later landing. If c<=B, all acknowledgers may be
tainted and leave the path open; the packet contains an explicit late-landing
trace. Cancellation availability against withholding requires c<=q-B. Thus the
exact certificate interval is B+1<=c<=q-B. The main q/r conditions imply q>=2B+1,
so c=B+1 is feasible without extra roots. At the minimum-root point it is the
unique cancellation threshold. Distinct root identities and exact command
binding are indispensable to this counting inference.

### Theorem 2: threshold necessity in this family

If q>n-B, choose exactly B roots that withhold every gate. Each q-subset meets
them, so no repair path can land. This defeats the required post-quiescence
progress. If r>n-B, let those roots withhold acknowledgements. No permitted
owner transition can complete; revocation availability fails.

If q+r<=n+B, choose L and S with sizes q,r and intersection size at most B.
Such sets exist because their smallest possible intersection is max(0,q+r-n).
Choose C* of size at most B containing that intersection. First every root
issues a genuine-looking old commitment, so the actor has exactly the old
permitted evidence. In the next gap the owner requests revocation. Untainted
roots in S close old gates and acknowledge; the corrupt intersection falsely
acknowledges while staying open. No untainted root in L is in S. Let every L
gate remain open. The r-certificate completes, so the old action is now stale
or unauthorized, yet the selected q-path can land it.

Compare this evolution with one having the same preparation evidence and no
revocation: a current authorized repair may land. No observer restricted to the
declared evidence can treat the old packet as a warranty of current permission
in both histories. The actor can refuse the exposed unsafe interface, but then
the unchanging good history gives the first-attempt obstruction to guaranteed
progress. The adverse schedule is expressly allowed to act after the selected
path is exposed; this is not an illicit conversion of a static hidden-fault
lower bound into an adaptive one.

The necessity assertion is for **universal path safety plus repair/revocation
availability of this symmetric q/r interface**. It is not a lower bound on every
conceivable state-machine protocol. Restricting which transitions can complete,
adding a currentness oracle, or changing the physical gate interface changes
the family and must be priced separately.

### Corollary 2.1: minimum n and the unique minimal thresholds

Availability gives q+r<=2(n-B). Together with q+r>n+B this implies n>3B, hence
n>=3B+1. At n=3B+1 availability gives q,r<=2B+1. Their sum must exceed 4B+1, so
both equal 2B+1. Conversely n=3B+1 and q=r=2B+1 satisfy all three inequalities.
For n>3B one may choose q=r=n-B. No arithmetic claim is imported from a static
action-alphabet frontier.

## 4. Constructive repair and exact execution cost

### Theorem 3: safe exhaustive repair after quiescence

Fix the final epoch and enumerate all q-subsets of R. For each subset run the
prepare/execute/cancel macro-attempt for the exact authorized repair from the
actor's received descriptor. Ignore untrusted effect receipts and complete the
whole finite list if necessary. The charged cancellation protocol terminates a
withheld path safely, so this is an executable sequence rather than a count of
hypothetically completed trials.

There are at least n-B untainted roots; q<=n-B ensures some enumerated L is
entirely untainted. Its preparation and landing complete before the actor begins
cancellation, and apply R_e*. Every other attempt is either the same adequate R_e* or the identity, by Lemma 2.
Since R_e* is idempotent, their composition repairs the entire target table and
cannot undo it. Hence choose(n,q) attempts suffice. No integrity diagnosis, fresh
fault oracle, uncharged common containment gate, or trusted success receipt is
used. Revocations during earlier attempts can only block old actions safely;
they postpone the quiescent suffix and do not strengthen its conclusion.

There is also an end-to-end strategy under eventual certificate delivery: keep
the greatest valid delivered control epoch in actor-local custody, repeatedly
cycle through the same finite ordered path portfolio for that descriptor, and
adopt a later descriptor when its certificate arrives (resetting the cursor is
allowed on a strictly newer descriptor, not on repeated stale messages).
An old cycle remains safe, although it may do nothing.
If the final certificate eventually reaches the actor and intact roots, a full
final-epoch batch eventually runs and repairs. Without a known dissemination
bound there is no uniform N-slot bound from the last global transition. Once
the actor and all untainted roots have the final descriptor, any N consecutive
cyclic attempts cover the full portfolio, regardless of cursor alignment; the
N-attempt cap applies to newly initiated attempts in that stable-delivery
suffix. The 3N-phase bound starts at the next macro-attempt boundary; an old
in-flight attempt may add its remaining phases before that boundary. This is
not a bound on time spent waiting for certificate delivery. The
simulator's Actor uses its received descriptor, not World.descriptor; a matched
trace demonstrates safe non-repair before actual delivery and repair afterward.

Once repaired, every later allowed landing in the unchanged epoch and declared
horizon is the same adequate idempotent repair and every block is identity.
Therefore the target is invariant through that horizon. An infinite invariant
requires every relevant premise, including the lifetime-union budget, for the
entire infinite history. A later effective target change starts a new obligation; the theorem
does not call the old table correct under the new target.

### Theorem 4: exact worst-case attempts at the minimum-root point

Take n=3B+1 and q=n-B=2B+1. Consider any maximal hidden taint set C of size B.
A q-path L is wholly untainted if and only if L=R\C. To prove the nontrivial
direction, L is a q-element subset of the q-element set R\C, hence equals it.
There are N=choose(n,B) possible such C and N complementary paths.

Use permitted behavior in which corrupt roots issue all expected truthful
commitments and cancellation replies with indistinguishable timing, but any
attempted path intersecting C returns NO_EFFECT without
identifying a blocking root; the entirely good path repairs. Each failed path
then eliminates exactly one candidate C, its own complement, and nothing else.
Along an all-failure observation history, an adaptive deterministic policy must
eventually test every distinct path: if one path L0 is untested, the fixed
scenario C=R\L0 makes every tested path fail. Repeating a path adds no evidence.
An adversary can therefore make the first N-1 distinct paths fail, and N are
necessary in the worst case. The exhaustive protocol attains N.

For a randomized policy purporting to guarantee a cap k<N with probability one
for every fixed C, average over a uniform C independent of its coins. A run can
test at most k of the N candidate complements; conditional on its coins and the
all-failure strategy, success probability is at most k/N. Some fixed C thus
has positive failure probability. Randomization cannot lower the almost-sure
worst-case cap. This is an elementary finite search argument, not an assertion
that the adversary sees hidden coins.

The N-bound permits a success-only truthful receipt, so omitting a trusted
receipt cannot defeat the lower bound. Revealing an authenticated blocking root
would change which candidates a failure eliminates and can improve the bound.
Parallel physical paths can also change latency; their actual mechanism cost is
not zero merely because their root labels overlap.

Examples: B=0 gives (n,q,r,N)=(1,1,1,1); B=1 gives (4,3,3,4); B=2 gives
(7,5,5,21); B=3 gives (10,7,7,120). The usual Sixth f+1 result had different
singleton fail-silent trials and cannot be transplanted to these serial paths.

## 5. What is warranted by a commitment

From the available labelled commitment packet **plus** warranted model facts,
the actor can know that (i) every attempted q-path retains some untainted
payload-binding veto, and (ii) every effective revocation intersects that path
in an untainted enduring veto. Thus attempts are safe even when the actor does
not know which roots are intact or whether an unseen transition completed.
The commitment warrants a conditional executable envelope, not an unchanged
global state. A failed attempt may be the very mechanism making the promise
true after permission changes.

The proof does not warrant the mechanism premises from their own declarations.
For a world application one must independently establish root separation and
the lifetime budget; correct authenticated descriptors and entitlement; actual
reservation semantics; durable revocation; same-command physical mediation;
path completeness; bounded intact service; and quiescence if progress is claimed.
An installed gate may itself fail, so it is charged to its root rather than
treated as a free oracle. The assurance that at most B root duties fail is still
a genuine empirical/architectural premise. Nothing mathematical removes that
last applicability obligation.

## 6. Deletions and failed candidates

The executable fixtures retain the target and all unaffected premises. Failed
candidates are preserved rather than promoted as theorems.

1. **Cached votes instead of live commitment.** For B=1,n=4,q=r=3, let L={0,1,2}
   prepare the old command and cache three OPEN votes. Complete revocation with
   S={1,2,3}; honest shared roots close their live gates. A dispatcher using the
   old cached conjunction nevertheless lands the old action. The certificate
   inequality remains true. Replacing physical live veto with signed old votes
   invalidates the bridge. An honest root's accurate past report is not a
   fault-stability commitment.
2. **Mutable payload after check.** Let a corrupt dispatcher root substitute
   an unsafe payload after commitments were issued. Gates that check only the
   old approved label, rather than the actual complete command at landing,
   allow X. The base live binding rejects it. This failure is possible with one
   charged root and a perfectly correct target proof.
3. **Current authorization deleted.** Keep target_id, target_version and table
   fixed, but complete a permission-only control-epoch change revoking actor A.
   A gate implementation keyed only by target version keeps an old A-command
   open. It makes an unauthorized write. The full tuple's epoch/recipient/scope
   checks and revocation memory reject it. Copied good payload bytes are not a
   transferable or perpetual execution right.
4. **Common downstream gate/writer.** Add an active shared bypass g downstream
   of all q-root gates and allow g to be one of the same B faulty roots. g can
   write X even with the entire labelled certificate unchanged. The theorem is
   inapplicable; g cannot be declared trusted after observing this trace. More
   commitment signatures do not compensate for missing physical mediation.
5. **Instantaneous instead of lifetime budget.** One at a time, corrupt each of
   r acknowledgement roots, let it falsely acknowledge while retaining its old
   local gate state, then restore apparent normal behavior before moving on.
   At most one root is faulty at an instant, but more than B distinct roots have
   lost relevant duties. The historical certificate can have no enduring honest
   overlap with the old path. Current low fault count cannot validate that
   history. This is outside the declared union constraint, not a refutation of
   Theorem 1. State not correctly recovered remains tainted for budget purposes.
6. **B+1 gates with free revocation.** The tempting n=2B+1,q=r=B+1 has surviving
   repair paths and each path has a good gate, but q+r<=n+B for B>=1. Its old path
   and revocation quorum may share only faulty roots. It fails across epochs,
   despite satisfying the singleton-style static containment intuition.
7. **Common selector omitted from liveness support.** A charged root g can
   acknowledge and sign truthfully but drop all selections of an otherwise
   untainted branch. Safety may remain intact, yet restoration never happens.
   This defeats the coverage conclusion unless g is actually included in every
   affected support, in which case an all-intact q-subset may no longer exist.

## 7. Negative results beyond the positive contract

### Immediate external revocation cannot be hidden by a definition

Take two evolutions identical through the actor's last preparation observation.
In H0, the legitimate permission remains valid and the authorized operation
would repair. In H1, actual external permission ceases immediately in the gap,
before any gate receives the fact. All root states and all actor observations
at landing are still the same, and the operation's bytes and target version
have not changed. The same chosen act lands in both; it is unauthorized in H1.
Holding forever avoids this but fails repair in H0. Any always-safe progressing
policy needs a mechanism that couples external permission changes to the
physical landing (or a warranted reservation keeping permission alive).
An r-certificate definition alone does not supply that coupling. This is the
exact surviving independent institutional premise of the positive result.

### No unconditional persistence under permitted endless changes

Even perfect root integrity cannot ensure that one repaired table equals two
different future targets. Let the owner alternate the two different tables
after every completed repair, with valid transitions and permission each time.
The system is non-target immediately after each such change. There is no suffix
in which it stays restored. Consequently eventual-restoration claims consume
quiescence or a different explicitly weaker tracking objective. A bounded
number of unsafe events would not prove persistence of the current rule.

Likewise, a fault that can write directly to the plant after the last attempted
repair defeats persistence while leaving every historic certificate true. The
theorem's complete-mediation assumption covers the future, not merely the
single disclosure-to-intervention interval.

## 8. Sixth, R5 and foundational dependency audit

The source hashes in SOURCE_BINDING.json fix the exact Sixth restoration and
timing reviews and the R5 control. Sixth D's diagnosed-but-destructive static
roots, its exact risk frontier, its f+1 harmless singleton strategy, and its
static/common-gate observations remain admitted at their original interfaces.
This packet does not rerun static alphabet optimization or strengthen the
empirical-controller endpoint.

Added premises here are a physically live q-root conjunction, durable
revocation under the same correlated budget, a certified-effective reservation
institution, lifetime union B, a serial version source, post-change quiescence,
and opaque path-failure observations. Their exact consequences are the
cross-epoch safety inequality, the conditional repair construction, and the
minimal-point attempt bound. Each premise has an independent truth/warrant
obligation; a mathematical witness is not a deployed assurance certificate.

The operational proof does not consume necessary sourcehood, metaphysical
unity, essential truthful agency, or a new norm-fixing theorem. It consumes
only the given target and authority descriptor plus explicit causal contracts.
Removing a proposed foundational explanation while retaining those inputs
leaves the proofs unchanged. Credit the local collective-warrant and restoration
result; withdraw any claimed foundational dependence. No R5 defeat is
established. A separated architecture could be supplied with
the same added premises without a unification bridge, but those stronger
interlocks, certificates, reservation rules and warrants are **not**
retroactively admitted resources of the fixed checked R5 control. The packet
does not claim an already checked R5 realization of all its new mechanisms.

## 9. Verification layers and research limits

The ordinary proofs quantify over all natural parameters satisfying the stated
inequalities and over all permitted histories. The Python suite independently
enumerates finite set systems and executes concrete root/gate traces, including
the preserved failures. Lean checks the finite-count overlap argument,
threshold arithmetic, interlock exclusion and idempotent persistence at their
formal interfaces. Finite tests are not a proof over all parameters; abstract
Lean interfaces are not physical-world certification. The exact search-bound
argument is also supplied ordinarily and regression-tested; the verification
receipt states precisely how much is kernel-checked rather than conflating the
layers.

No GitHub mutation is involved. Lean is the pinned official 4.19.0 toolchain
recorded in LEAN_TOOLCHAIN_RECEIPT.json. No previous Seventh result or denied
AE1 action is a dependency of this fresh packet.
