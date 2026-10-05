# Open-context continuation and source-ordered reacquisition

Status: release candidate v1, 3 October 2026. Incorporates an independent model-assisted design review. The ordinary mathematical derivation and the accompanying bounded Python controls have separate evidential roles; no kernel proof is claimed. Bounded project-level application using established symbolic parsing, dependence analysis and covering methods; no new general parsing, authority-cover, query-determinacy or identity theorem is claimed.

## 1. The decision and the access boundary

The receiver is assembling a source-attribution record. The one decision examined here is:

> Are all occurrences in this explicitly selected output list occurrences of the author's own assertoric/counterargument voice in the witnessed document, rather than quotations, reported opponent statements, hypothetical premises, or other nonauthorial roles?

This is a metalinguistic decision about the designated occurrences. It is not a decision about the truth of their propositions, what the author believes elsewhere, who is legally entitled to act, or numerical identity. A source may assert the same proposition elsewhere without turning this quoted occurrence into an author assertion.

The receiver already has a source-bound structural extraction, selected output occurrence IDs, branch transformation records, and an explicit menu of source-context reads. Some force/role labels were not transported. The source parse can be clear while the recipient lacks that information. In the theorem below, uncertainty concerns missing recipient evidence, not genuine linguistic ambiguity.

A context read returns a witnessed role label for specified original context origins, bound to the named snapshot and source loci. Source identity, witness authenticity, parse adequacy, allowed disclosure, and current availability are premises of the mechanism. Neither an origin ID nor our symbolic calculation proves them. The algorithm is allowed to inspect the extraction and read results, not an unrecorded copy of the omitted source context.

The query lower bound uses an explicit opaque-atom oracle API: names/handles support equality, copying and declared lookup, but not representation inspection, role-bearing name interpretation, or undeclared content-address lookup. Distinct synthetic source assignments have distinct bytes/digests; observation equivalence is up to opaque-handle renaming, never a digest collision. Public structure, positions, costs and response sizes are assignment-independent. It does not claim that an unbounded algorithm cannot recover content from a finite digest and a separately known exhaustive candidate table. Any actual informative side channel belongs in the receiver's initial holdings and can change the bound.

## 2. A small source-context machine

Let O be a finite set of original context-origin keys. A key includes source/snapshot identity and a particular source context occurrence. Equal strings and equal propositions do not identify keys. Conversely, two carriers which copy the very same source context retain its one key.

Let theta:O -> Gamma give the context labels in the original witnessed document, where Gamma records document-global force/role separately from local speaker. The present target observes the binary predicate A(gamma): whether that context is the original document's unquoted authorial argumentative/expository voice. Set x_o=A(theta(o)). A locally represented author inside a quote remains quoted for this predicate. Each new carrier occurrence also has a separately retained current-carrier force; that can be quotation/report even when its original-source role is authorial. The theorem does not equate the two or promote an old assertion into a fresh assertion/grant.

A configuration is a nonempty list of origin references, top first:

    [current, suspended_parent_1, suspended_parent_2, ...].

The source-bound structural extraction uses three operations:

- enter(o): prepend o; the previous current context becomes suspended.
- leave: remove the current context, requiring a suspended parent.
- emit(t): record that selected output occurrence t has the current origin reference.

An emitted clause's full proposition remains separate data. The machine tracks a declared source-attribution query; it is not a complete semantics of quotation, belief, irony, mixed quotation, or author commitment. In particular, the source reader must justify where scopes begin and end and which roles their origins have. A quoted author is still represented by a quoted-context origin, not conflated with the present author's voice.

The standard parser with the complete context stack is a strong conventional baseline and is already sufficient. The question is what a split, translated, source-bound transport must preserve when the receiver lacks that stack.

## 3. Exact symbolic effect of an open fragment

An open fragment can start or finish inside a scope. Give its incoming stack formal references I_0,I_1,I_2,..., where I_0 is the current context. Symbolically execute its enter/leave/emit operations, allocating no values to theta.

Only finitely many I_j are inspected. The resulting effect consists of:

1. Its entry-depth requirement, including the need to restore each parent actually popped to.
2. A finite emitted map t -> e_t, where each e_t is either an original key o or an incoming reference I_j.
3. Its outgoing stack expression: a finite prefix of original keys followed by a tail I_k,I_(k+1),... of the incoming stack.

The outgoing prefix can be empty. The entry-depth requirement is kept separately: an enter followed by leave restores I_0 even when the final tail starts at I_0. If a fragment contains further nested material with no selected output and returns to its entry stack, that material can disappear from the effect.

**Effect correctness.** For any concrete incoming stack of adequate depth and any theta, replacing every I_j by its incoming origin key yields exactly the emitted attribution references and outgoing stack obtained by executing the fragment directly.

**Proof.** Induct over the fragment operations. enter prepends the same key in both executions. leave removes the same current reference; the depth requirement excludes underflow. emit consults the same top reference. No step reads or invents a role value. Thus substitution commutes with each step and with their sequence.

This is a derived representation, not an assumption that the desired full state was preserved. It retains only the stack effect and selected attribution references; the full prior text, propositions of unselected clauses, and closed unobserved subscopes are not needed for this query.

The exact finite representation and domain formulas are in EXACT_EFFECT_ALGEBRA.md. In particular E=(h,P,k,M) maps an incoming stack s to P+s[k:], with h=1-minimum prefix net height. Composition with f first has depth max(h_f,h_g-(|P_f|-k_f)); it substitutes local prefix keys or shifted input references into the second effect. The optional keyed-exit refinement checks source-origin equality rather than accepting arbitrary foreign close markers at the same depth.

### Serial composition

To compose E_f then E_g, substitute E_f's outgoing stack expressions for E_g's incoming references. Keep E_f's selected emissions and the substituted emissions of E_g; substitute into E_g's outgoing stack and compose depth requirements.

**Composition theorem.** Whenever the source-bound cut interfaces agree, the composed effect equals the symbolic effect of concatenation fg, up to the chosen names for incoming references. Therefore composition is associative at that extensional effect level.

**Proof.** Effect correctness says the sequential substituted effect and direct fg execution agree for every admissible incoming stack. The symbolic construction follows exactly the same stack operations, so their emitted reference expressions and outgoing tail representation coincide. Substitution of expressions is associative; underflow requirements are precisely those for the corresponding concatenated execution.

This uses ordinary symbolic evaluation and pushdown-effect reasoning. The new claim is its application to the explicit source-cut/attribution interface, not invention of a new parsing principle.

### Nonidentical representation changes

An allowed translation can change proposition strings, local occurrence IDs, token counts and language. It transports each selected output's original context-origin reference and preserves the justified scope operations, or supplies an independently justified effect with the same action on admitted entry contexts. Its concrete local IDs are fresh; its source-context keys are not.

The theorem then gives a positive preservation result across differently represented fragments. A proposition-preserving translation which drops those contextual effects does not satisfy the premise. We do not infer that arbitrary natural-language translations preserve the extracted effect.

## 4. Fork, reconvergence and a genuinely sparse next-task boundary

Each branch effect has its own local identifiers and incoming placeholders. The reconvergence record supplies source-bound substitutions identifying those placeholders with actual boundary contexts. Shared original contexts use one key; distinct contexts are never identified solely because their clauses have the same wording.

The merger performs the substitutions first. These source-bound origin maps are initial evidence for the cost theorem, not consequences of a source name. If a map is missing, a separately charged path/identity observation must obtain it before L can be computed. Such an observation may also supply role witnesses, which then enter initial holdings. No arbitrary reply-to-objection edge is recovered by this three-operation calculus. For the selected next decision, collect the distinct resulting original keys L. Remove keys whose author-role labels are already witnessed true. If any selected key is already witnessed false, the decision is already false. Otherwise the remaining predicate is exactly:

    all_author = AND over o in L of x_o.

This is a derivation from enter/leave/emit and the selected outputs. L is not an arbitrarily stipulated list of required annotations. An old suspended frame appears in L only if a selected output actually occurs after control returns to it. A frame never consulted by this selected continuation does not appear. Multiple output occurrences sharing one context contribute one factor, although their output occurrence IDs stay distinct.

**Query-specific boundary theorem.** Under this machine, the composed decision depends on precisely the unresolved distinct keys in L: every assignment to them gives the displayed conjunction, and if their labels are independently live in {0,1}, deleting any one changes the decision on some admitted input. No role values for other stack frames are needed for this task.

The independent-label clause is essential to the minimality statement. It is a model class of incomplete recipient holdings. If retained evidence constrains labels jointly, some keys may become inferable without being reread. A conventional packed parse forest or constraint store must retain those constraints. We do not promote this conjunction result into a theorem for arbitrary correlated semantic ambiguity.

This is not a claim that one must retain |L| bits under all possible protocols. A trusted source reader could send an adequate task-specific verdict or proof. Our cost result concerns the declared receiver holdings and a particular evidence-access interface, which lacks that verdict. Nor does a verdict for this conjunction automatically answer later questions about individual occurrences.

## 5. Exact permitted-read cost for the one decision

Let W be a finite menu of permitted read windows. Each w has known source-origin coverage C(w) subset O and cost c(w)>0. A successful read reveals authenticated context labels for all keys in C(w). The menu includes only observations the successor may actually perform in the applicable time/access state. A copied credential or address does not create a menu entry.

Assume:

- An admitted all-positive source s* has every unresolved relevant x_o=1. For each o in L there is an admitted source s^(o) with x_o=0 and all other relevant bits unchanged.
- Public metadata is identical in these sources up to equality-preserving opaque-handle renaming. Every read not covering o has the same complete observable response in s* and s^(o), including outside information, context-witness data, status, length and any observable timing. This all-positive-star locality condition excludes hidden summary leaks.
- Reads covering a key return adequate source-role evidence for it. There is no uncounted informative channel. Costs add, and labels do not change during the pinned-snapshot task.
- A policy must decide the conjunction correctly for every admitted source. Unresolved/abstain is safe but is not a completed decision under this contract.

The realisability supplement generates these sources with equal-width ROLE0/ROLE1 tokens, fixed structural metadata and local witness records. Only n+1 star instances are needed for the lower bound. Full independent binary assignments are a sufficient stronger family, not necessary. Independence among target labels alone is insufficient: a cheap outside value equal to their conjunction would defeat the claimed coverage lower bound.

Define cover(L,W) as the minimum total cost of a subfamily whose coverage contains L, or infinity if none exists.

**Exact read-cost theorem.** The minimum worst-case cost of a deterministic adaptive policy completing this decision equals cover(L,W).

**Lower bound.** Follow the policy on s*. Before the policy can answer true, the union of its reads must cover L. If some o remains uncovered, the admitted s^(o) yields the same complete read transcript by locality and makes the decision false. The policy therefore cannot correctly terminate on that transcript. Its all-1 read family is a cover and costs at least cover(L,W).

**Upper bound.** Choose a minimum cover and read its windows. Return false as soon as a witnessed relevant label is 0; otherwise return true when the cover has been read. Every answer is correct, and the all-1 case incurs at most the cover cost.

Adaptivity may improve the realised cost on a negative source but cannot reduce this worst-case bound. The theorem is not a probability-of-truth statement. Unknown-source values, actual inspection, and warranted source interpretation remain distinct.

The exact consequence for a handoff is operational: a successor with a finite cover can complete this decision by the stated read protocol. If its surviving menu fails to cover L, a mere source link is insufficient; some missing task-specific evidence must be carried before retirement or the access interface must be legitimately preserved/replaced. This latter general principle is inherited from H-MOAT; the present effect and cover calculation identifies the exact obligations in this mechanism.

## 6. Source-root quotient preserves interval access

Suppose original contexts have one fixed source order p_1 < ... < p_n. Each allowed read w is a source-ordered role-witness window [a_w,b_w]: it supplies adequate role evidence for every demanded origin in that source-coordinate interval. An ordered store of independently justified context-witness records can implement this contract. Raw contiguous text alone need not: an omitted outer quotation opening can make adequate role coverage nonconvex. Constructing the store, completing paths and justifying coverage are separately charged preparation/warrant obligations. Selected transcluded outputs may duplicate and reorder those original contexts arbitrarily.

First compute L by the source-bound effect composition, then sort its distinct original positions as ell_1 < ... < ell_m. For every source window, C(w) intersect L is a consecutive sublist of this sorted list (possibly empty).

**Interval-quotient theorem.** Copying or reordering the output occurrences cannot turn genuine original-source interval reads into arbitrary set-cover incidence for this decision. After quotienting by shared original context keys, the read problem remains ordered interval covering over the demanded source positions.

**Proof.** If a source interval contains ell_i and ell_k with i<j<k, then it contains ell_j by the order definition. Multiplicity and output order do not enter this implication. The effect computation changes which original positions are demanded, but not the order convexity of an original-source interval.

This corrects an initially plausible but false complexity claim: an interval's image can look scattered among the output copies, yet that scattered image is not the correct ground set for repeated evidence acquisition.

### Exact weighted algorithm

Let F(m+1)=0. For i=m,...,1, set:

    F(i)=min over w containing ell_i of [c(w)+F(1+r(w))],

where r(w) is the last demanded index covered by w. If no window contains ell_i, set F(i)=infinity.

Then F(1)=cover(L,W). An attaining sequence gives a legal minimum-cost read plan. A direct table has O(m|W|) candidate work after coverage endpoints are known, and O(m) cost storage. No algorithm is claimed for establishing the authenticity of the coverage metadata.

**Proof.** A candidate window covers every remaining demanded point from i through r(w); combine it with an optimal suffix cover. Conversely, among the windows of any finite optimal cover that cover ell_i, choose one with greatest right endpoint r. No other such window is necessary solely for a point up through r. The remaining windows cover every demanded point after r. Thus some recurrence candidate costs at most the optimal cover. Together with the constructive upper bound this proves equality, inductively on the suffix.

For unit costs, taking a window containing the earliest uncovered demanded position with furthest right endpoint gives the familiar greedy interval-cover algorithm. Both algorithms are conventional; the application theorem says when they remain applicable despite translated/copying reconvergence.

## 7. Carrier access can genuinely change the problem

A different surviving interface may offer only whole context-witness cards in a derived dossier. Each card is a contiguous block in that dossier, created by concatenating source-backed role records with adequate opening/path evidence; cards can duplicate/reorder original contexts. Reading a card reveals its listed origin labels. The original-source read service is no longer available to the successor.

For this interface, a card's origin coverage need not be an interval in the original source order. This is an additional access operation, not a consequence of copying alone.

**Bounded contrast.** Optimal reread selection over such source-backed cards contains ordinary weighted set cover exactly. Given a universe U and set family S_j, create one original context key per u and one card containing a source-backed adequate role-witness record for every u in S_j. Select a next-attribution task whose derived L is all of U. Give each card its original set cost and permit reads only at whole-card boundaries. The exact read-cost theorem makes the optimal decision cost exactly the given cover optimum.

Conversely any such card instance is a set-cover instance with universe L and subsets C(card) intersect L. The construction explicitly charges n original contexts, sum_j |S_j| transclusion records, the identity dictionary, selected output references and card boundaries. Equal-length padding gives a polynomial response-byte-cost variant; see REALISABILITY_AND_RESOURCE_ACCOUNT.md. The correspondence does not claim new combinatorial complexity theory. It identifies a real protocol distinction: preserving source-coordinate access retains interval structure; preserving only an assembled-card service need not.

A whole-source read, a free per-origin lookup, previously retained labels, or a task-specific source certificate can change or trivialise this comparison. They must not be silently withheld from the strong conventional baseline. In the actual electronic article used below, the full page is presently available, so its actual current query cost is not asserted to be hard.

## 8. Precise novelty and validation ceilings

The proposed project increment consists of the whole derived chain:

- open source-fragment effects identify which suspended contexts the selected continuation actually needs;
- source-bound substitution composes two stages and reconvergence without converting copied contexts into new originals;
- the resulting one-decision predicate has a computable exact evidence-access cost under the stated read model;
- original-source interval access remains tractable after transclusion, while a changed successor access service can have different covering geometry.

The individual symbolic parsing, conjunction query lower bound, interval cover algorithm and set-cover reduction use established methods. Deep CN V2 / PMR-007-AIAC-1 and SPA-R10 already own the internal eligible-anchor/collision-cover principle; the static cost subproblem is a direct specialization. Pitcher already supplies open-stream effect methods; priced-information and query-based-data-pricing literature own the general information-cost methods. PRIOR_ART_DISPOSITION.md records the exact ceiling. H-MOAT retains the general export/next-capacity principles; MLT/RSD retain their gluing results; Sixth retains copied-support conservation; P15 retains version/current-licence transport. No superiority over an equally informed conventional parser/constraint/cover implementation is claimed.

This remains a restricted source-attribution mechanism. It does not supply natural-language parsing correctness, actual source/issuer authentication, new permission, truth preservation of arbitrary translations, a common-policy extractor, a numerical-identity theorem, or a physical continuation experiment. A real case can validate the occurrence distinctions and reproducible source-binding workflow, not the truth of every oracle-model assumption.
