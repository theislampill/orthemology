# Observation and interpretation contract

Status: clarifications to DERIVED_INTERFACE_v1 and the source fixture. These are part of the theorem contract, not optional implementation details.

## 1. Opaque-handle oracle model

The cost theorem's adversary argument ranges over generated synthetic sources, not alternative contents of one actual immutable byte object. Each generated source has its own concrete bytes and, if used, its own digest. We never flip a role label inside an already pinned real snapshot.

In the formal read interface, snapshot handles and origin handles are opaque atoms. The policy may copy them, test equality, follow the supplied source-coordinate dictionary, and submit them to the declared read API. It may not inspect an atom's representation, decode a digest, branch on a human-readable role name hidden in a locator, or use an undeclared content lookup. The public grammar skeleton, coverage index, costs, and equality/order relations are identical across the generated role assignments; these metadata contain no extra role information.

The lower-bound pair therefore gives the same observable transcript in this explicit API model, up to the unique equality-preserving renaming of opaque snapshot atoms. It need not give identical raw cryptographic hash strings. Authentication is supplied by the abstract read contract; its cryptographic implementation is not proved here.

A more general theorem could replace opacity by an explicitly given prior relation on public metadata and source labels, but then the full independence premise and the simple cover optimum may fail. We do not claim that broader result.

For the actual source fixture, the analyst's readable key legend and full source capture are not part of the restricted receiver packet. The model recipient receives neutral keys, allowed source lookup coordinates, and no role-bearing article labels beyond what is explicitly counted. An actual reader who recognises the passage, already has its full context, or can interpret a role-bearing locator has additional evidence and may need fewer reads. The fixture does not prove that a knowledgeable human or language model must be ignorant of the attribution.

## 2. Global role, local speaker and present carrier force

Each source context's theta(o) records its role **in the original witnessed document**. A records whether that occurrence belongs to the original document's unquoted authorial argumentative/expository voice. It is not merely the name of the locally represented speaker. An author quoted inside a reported opponent's speech does not regain original-document authorial force just because the local speaker string equals the author's name.

A source-backed translated/transcluded occurrence also has a separate current-carrier context. An output record should therefore preserve two relations:

    output occurrence -> original source occurrence/context/role
    output occurrence -> current carrier occurrence/context/force

The theorem's selected query concerns the first relation. A present quotation can faithfully report an original authorial assertion while the current carrier's speech act is only quotation/report. No rule in the theorem promotes an original-source assertion into a new present assertion or a new grant. If the application instead asks about the current author's endorsement, it must run the appropriate current-carrier analysis and supply that independent interpretation contract.

The source-fragment effects model source-structural continuation, including suspension/return in that original source. A modern wrapper may change the current-carrier force without changing the retained original-source effect. Treating the two stacks as one would be a semantic error. The minimum read cost concerns missing source-role evidence only; it does not resolve any independent uncertainty about the current carrier's stance.

## 3. A read returns a context witness, not just repeated content

For an original-source interval, a successful read must supply the opening/role/path material needed to establish every covered theta(o), including relevant exclusion from outer quotation scopes. Merely encountering the target proposition within the interval is not coverage of its source-role dependency. Coverage metadata must be justified at that stronger level.

For a carrier card, the card must contain the original-role context witness or an equally adequate bound source certificate for each claimed covered key. A bare quotation of the clause with no original role context does not reveal theta(o). The cardinality/padding construction uses source-backed **context-witness records**, each containing the relevant opening label and local scope evidence, rather than bare proposition strings.

This extra material counts in the explicit card size and read cost. An authentic quote string alone can remain insufficient; the same source word cannot be counted as a role witness merely because the coverage index claims it.

## 4. The remaining authentication and interpretation boundary

Opaque handles make the mathematical observation restriction exact; they do not implement physical source authentication. Context-witness records make the information being queried explicit; they do not make a false parse correct. The actual case supplies directly inspected electronic source context and a reviewable interpretation. A real deployment would still need reliable source capture, version matching, evidence authenticity, an appropriate parser/reviewer and genuinely available, permitted reads.

## 5. Boundary identity acquisition is a separate phase

There are two distinct missing objects:

1. Which original source context an incoming placeholder I_j denotes.
2. What witnessed role label theta that identified context has.

Symbolic effect composition can retain I_j without resolving either object. The exact live-origin set L and the interval/card cover theorem apply only after the relevant placeholder-to-original-key map is available and adequately bound. If that identity map is absent, the receiver cannot first construct L by pretending to know it.

SOURCE_CASE_v1's first repair obtains a context-path witness which supplies both I_2 -> a and theta(a). It is therefore a **combined identity-and-role observation**, not an example of the narrower label-only cover oracle. Its one actual context read is charged as an acquisition step. The subsequent two-carrier handoff can retain the now verified identity map while omitting selected role witnesses; that is the exact phase to which the cover theorem applies.

If a fixed boundary-acquisition protocol costs c0 and reveals role values on K as a by-product, the displayed label-read result gives a completing cost c0 + cover(L minus K, W), subject to immediate negative termination when a known relevant role is false. This is a sufficient composed plan and an exact optimum for the second phase conditional on its actual holdings. It is not a theorem that this sum is optimal among all possible joint identity-and-role acquisition protocols.

The source-coordinate dictionary, its construction, role-bearing metadata, and each path witness must be charged and preserved. The matched conventional baseline receives exactly the same map, path witnesses and costs.

The initial gate also mentioned absent reply-to-objection targets. The present enter/leave/emit calculus does not infer arbitrary reply-reference edges. A reply may be classified by its document role without resolving every edge in the argument graph. Recovery of those edges is outside this theorem unless a separately justified encoding supplies them. The actual-source case's third-objection/third-reply comparison is a distinct-origin control; it is not evidence for a new reply-reference reconstruction algorithm.

## 6. Corrected lower-bound premise: all-positive star and transcript locality

Independence only among the queried target bits is insufficient if a read also exposes informative outside values or richer correlated metadata. For example, an outside bit z equal to the conjunction of two target bits could decide the task at cost 1 without covering either target origin. Source authentication does not rule out that information channel.

The corrected sufficient premise is this explicit **all-positive star** in the admitted source family:

- There is an admitted source s* in which every unresolved relevant x_o is 1.
- For each o in L, there is an admitted source s^(o) with x_o=0, every other relevant bit equal to its s* value, and the same public structure/metadata up to permitted opaque-atom renaming.
- For every read window w with o not in C(w), the **complete observable response** to w is identical in s* and s^(o), under that same renaming. This includes outside-label information, context text, witness metadata, statuses, lengths, timing if observed, and authentication outputs admitted to policy control.

Reads covering o return a sufficient role witness for it. The declared responses disclose no uncounted correlation that defeats the star comparison. The full-product local-role-token grammar with fixed unrelated metadata and local role records supplies this condition. Only n+1 source assignments are needed for the lower-bound proof; the earlier 2^n construction is a convenient stronger realisability family.

The lower-bound proof now follows the policy on s*. If an origin o remains uncovered, every answer in that path is the same on s^(o), so the complete decision path and answer are the same, although the conjunction differs. Thus the all-positive path covers L. The upper-bound proof is unchanged.

This correction supersedes the weaker independent-label wording of DERIVED_INTERFACE_v1 section 5. It is not an assertion about every natural source or every context-witness response. If actual witnesses contain more information, that information must enter the observation model; the optimal cost can be lower. This is a substantive negative control for any later executable checker.

## 7. Interval coverage is a service property, not a fact about raw text

The interval theorem requires **source-ordered role-witness windows**: origins have a fixed original-source order, and each permitted window reveals an adequate role witness for every demanded origin whose position lies between the declared endpoints. Equivalently, its justified coverage restricted to demanded origins is convex in that order.

Raw text contiguity does not imply this property. A paragraph may lie inside a quote whose opening is outside the retrieved span; one enclosed role may be inferable while another is not. Such a window can have nonconvex justified coverage even though the bytes came from one interval. The theorem must not silently substitute raw byte inclusion for adequate role coverage.

One permitted realization is an ordered store of source-bound role-witness records, each carrying the original opening/path evidence or a justified certificate. Another is a context-completing source service that returns the necessary evidence for every requested origin in an interval. Constructing that store, completing paths and validating its coverage are explicit costs and warrant burdens. Their existence is not proved by the interval dynamic program.

The service's responses must still satisfy the oracle locality premise if the exact worst-case lower bound is claimed. Additional contextual facts may instead make a richer, cheaper decision possible. A conventional baseline receives the same record service and all response information.

The actual complete-page observation supplies the context for the small displayed fixture; no theorem is claimed that arbitrary page slices implement a convex role-witness service. The access-contract comparison is between declared adequate role-record windows and declared adequate role-record cards, not between unanalysed raw text snippets.
