# Source Context, Reacquisition, and Bounded Handoff

## Abstract

A copied or translated occurrence can retain its words while losing the evidence needed to identify its role in the original document. This chapter studies one precise question: whether every occurrence in a selected output list belongs to the original document's unquoted authorial voice. A finite symbolic effect records how an open fragment enters, suspends, restores, and emits source contexts. Its exact entry-depth requirement and source-origin substitutions compose across cuts without supplying missing role values. Once the incoming origins are independently identified, the selected continuation determines a finite set of unresolved original contexts. Under an explicit observation contract, the minimum worst-case cost of a deterministic exact decision is the minimum weighted cover of those contexts by adequate permitted reads. The lower bound requires an all-positive source, single-negative alternatives, and locality of each complete observable response; independence of target labels alone is insufficient. Adequate source-ordered windows retain interval structure after output copying and reordering. A changed service offering only whole witness cards can instead realise arbitrary set-cover incidence. Concrete source constructions and input-size accounts distinguish these claims from an assumption that one request has constant physical cost.

A three-context handoff then distinguishes two equally sized preventive packets. With only two overlapping cards and a one-request allowance, retaining the middle context witness is insufficient, whereas retaining either endpoint witness permits completion. A warranted fixed-task verdict, a genuinely available joint read, or an agreed change to the task can also suffice. Applying an independently supplied principle of care for deliberately organised reliance yields a conditional practical judgment. The read calculation supplies neither that principle nor its applicability to an actual relationship.

The chapter consolidates the public arguments in [1]–[7]. It gives ordinary mathematical proofs and a conditional philosophical application. The associated public reviews [8]–[9] retain their historical scopes. Source authentication, linguistic interpretation, formal execution, empirical success, external peer review, and adoption of this successor are separate matters.

## 1. The attribution question and its evidence

Fix a witnessed source document, a particular snapshot, and an explicitly selected list of output occurrences. The question is:

> Do all these occurrences belong to the original document's own unquoted authorial argumentative or expository voice?

This concerns the role of designated occurrences. The truth of their propositions is a different question. An author may assert a proposition elsewhere while the selected occurrence presents it as an opponent's claim, a quotation, a hypothetical premise, or some other nonauthorial contribution. Equal wording does not resolve that difference. [1, §§1–2]

The receiver is supplied with a structural extraction, selected output identities, transformation records, and a declared menu of possible source-context reads. Some role evidence has been omitted. The source reader's interpretation may be determinate even though the recipient lacks the evidence needed to recover it. The mathematical uncertainty below concerns these incomplete holdings. It does not establish that an actual text has several equally admissible interpretations.

A successful role read must provide an adequately bound context witness: the opening, path, surrounding-role information, or suitable source certificate needed to establish the relevant role. Authentic reproduction of a clause alone need not supply that evidence. Source identity, witness authenticity, parse adequacy, permitted disclosure, and present service availability enter as substantive premises. A symbolic key does not prove them. [3, §§3–4]

The broader distinctions are developed in [Recognition, Warrant and Restoration, §§7.5 and 8.1–8.3][recognition-retention]: task-relative retention, available support, competent uptake, interpretation, communicated content, and continuing access have different warrants. The present chapter supplies a restricted constructive calculation within that setting.

### 1.1 Original role and present force

Let $`O`$ be a finite set of original context-origin keys. A key binds a source, its snapshot, and a particular context occurrence. Equal text from different original contexts has different keys. Two carriers copying the same original context retain one original key while acquiring distinct carrier occurrence identities.

Let

```math
\theta:O\longrightarrow\Gamma
```

assign a context label in the original witnessed document. The label records document-global role separately from the locally represented speaker. Define

```math
x_o=A(\theta(o))\in\{0,1\},
```

where $`A`$ selects the original document's unquoted authorial voice. An author represented inside an opponent's quoted speech does not thereby acquire original-document authorial force at that occurrence. The relevant quotation ancestry must be respected. [1, §2; 3, §2]

Each output also has a current-carrier relation. Two records therefore remain distinct:

| Relation | What must be established |
|---|---|
| Output occurrence to original occurrence, context, and role | Which source occurrence was carried and what role it had there |
| Output occurrence to current carrier context and force | Whether the present carrier asserts, quotes, reports, questions, or otherwise uses it |

A present quotation may accurately report an original authorial assertion. That does not make the present carrier assert the proposition. An old assertion or grant likewise does not become a fresh assertion or permission merely because it is copied. The calculus below tracks continuation within the original source structure; it does not merge these two context relations.

### 1.2 Public handles and permitted observations

The read-cost result uses an explicit interface. Snapshot and origin handles are opaque atoms. A policy may copy them, test equality, use supplied source-coordinate and order relations, and make declared lookups. It may not inspect their representation, interpret role-bearing names, decode a digest, or perform an undeclared content lookup. Policies respect equality-preserving renaming of these atoms. [1, §1; 3, §1]

Different generated sources have different bytes and may have different digests. The argument never changes a role inside one already pinned immutable object and never assumes a hash collision. Its indistinguishability comparison is between the observations permitted by the interface, up to a consistent renaming of opaque handles.

This restriction has practical limits. A reader who recognises a passage, possesses its full source, understands an informative locator, or has access to an exhaustive source table has additional information. That information must enter the model. The abstract interface supplies no cryptographic proof that a real implementation enforces opacity.

The complete initial holdings include the extraction, identities, retained evidence, old task results, order and coverage dictionaries, costs, permissions, and any observable selection of a retained packet. Complete read responses include contextual text, outside values, witness metadata, statuses, lengths, timing when observable, and any authentication outputs on which a policy may branch. The cost theorem will require agreement of these whole observations in its comparison sources. Authenticity alone does not make a response uninformative about an uncovered target.

## 2. Exact effects of open fragments

A concrete source-context configuration is a finite nonempty stack, written top first:

```math
s=[s_0,s_1,\ldots,s_{d-1}],\qquad d\geq1.
```

The current context is $`s_0`$; the later entries are suspended parents. The structural extraction supplies three events:

| Event | Concrete action |
|---|---|
| $`\mathrm{enter}(o)`$ | Prepend the original key $`o`$ |
| $`\mathrm{leave}`$ | Remove the current context, requiring a remaining parent |
| $`\mathrm{emit}(t)`$ | Associate fresh selected output occurrence $`t`$ with the current original key |

An unselected emission has no effect on the selected output record. The full proposition carried by an output remains separate data; the effect records its source attribution. Every admitted execution keeps at least one stack frame after every prefix. The event skeleton and its relation to the source text are supplied interpretations. This machine is not a complete semantics of quotation, irony, belief, mixed quotation, or author commitment. [1, §§2–3]

### 2.1 The finite normal form

Write $`I_0,I_1,\ldots`$ for incoming stack references. A finite effect is

```math
E=(h,P,k,M).
```

Here $`h\geq1`$ is the least required incoming depth; $`P`$ is a finite list of literal original keys, top first; $`k\geq0`$ counts consumed incoming frames; and $`M`$ is an ordered list of pairs $`(t,e_t)`$, where $`e_t`$ is a literal original key or an incoming reference.

For an incoming stack $`s`$, the outgoing stack expression is

```math
P\mathbin{\|}s[k:],
```

where $`\|`$ denotes list concatenation. To evaluate an emission, replace $`I_j`$ by $`s_j`$. Literal keys remain literal. Role values $`\theta(o)`$ are not part of this effect. [2, “Basic normal form”]

Start with

```math
(h,P,k,M)=(1,[],0,[]).
```

Process the events as follows:

1. On $`\mathrm{enter}(o)`$, replace $`P`$ by $`[o]\mathbin{\|}P`$.
2. On $`\mathrm{leave}`$ with nonempty $`P`$, remove its first element.
3. On $`\mathrm{leave}`$ with empty $`P`$, replace $`k`$ by $`k+1`$ and then replace $`h`$ by $`\max(h,k+1)`$, using the new $`k`$.
4. On a selected emission $`t`$, append $`(t,P_0)`$ when $`P`$ is nonempty, and append $`(t,I_k)`$ otherwise.
5. An unselected emission leaves $`M`$ unchanged.

**Theorem 1 — Exact open-fragment effect.** The construction produces a finite effect satisfying $`h\geq k+1`$. Every incoming reference in $`M`$ has index less than $`h`$. A concrete incoming stack is admitted exactly when its depth is at least $`h`$. On every admitted stack, substitution into $`M`$ and $`P\mathbin{\|}s[k:]`$ gives exactly the emissions and final stack of direct execution.

If $`b(u)`$ is the number of enters minus the number of leaves in a prefix $`u`$ of the fragment, including the empty prefix, then

```math
h=1-\min_u b(u).
```

**Proof.** Induct over events. Initially the claims hold. An enter prepends the same key to the symbolic and concrete stack. A leave from nonempty $`P`$ removes the same local frame; the nonempty incoming tail survives. A leave from empty $`P`$ consumes the next incoming frame. The new requirement $`h\geq k+1`$ ensures that a frame remains after it. Earlier requirements remain necessary, which explains the maximum. An emission records the same current reference in both executions. If it records $`I_k`$, the invariant gives $`k<h`$. Later updates never lower $`h`$, so all recorded incoming references remain defined.

A depth-$`d`$ input has depth $`d+b(u)`$ after prefix $`u`$. Every prefix is nonempty exactly when

```math
d+b(u)\geq1\quad\text{for every }u,
```

or equivalently $`d\geq1-\min_u b(u)`$. This proves necessity and sufficiency of the stated minimum depth. In particular, final net height is insufficient: a prefix may empty the stack before a later enter restores its numerical depth. The inductive construction tracks precisely those earlier requirements and yields the displayed final stack and emissions. $`\square`$

A balanced unobserved subscope wholly created and closed within the fragment can disappear from the selected effect. The effect still retains every necessary entry-depth condition. It is not permissible to erase an underflowing prefix merely because the final stack is nonempty.

The distinction between current and suspended contexts is already visible in a two-event suffix. On the incoming stack $`[\mathit{inner},a,\mathit{root}]`$, the fragment “leave; emit $`t`$” emits from $`a`$. Its symbolic emission is $`I_1`$, not $`I_0`$. Preserving only the currently active inner context would lose the original required by this selected continuation.

### 2.2 Serial composition

Let

```math
E_f=(h_f,P_f,k_f,M_f),\qquad
E_g=(h_g,P_g,k_g,M_g),
```

with $`f`$ executed first. Put $`p_f=|P_f|`$ and $`\delta_f=p_f-k_f`$. The substitution into the incoming references of $`g`$ is

```math
\rho_f(I_j)=
\begin{cases}
P_f[j], & j\lt{}p_f,\\
I_{k_f+j-p_f}, & j\geq p_f,
\end{cases}
\qquad
\rho_f(o)=o.
```

The combined emission list is $`M_f`$ followed by $`\rho_f(M_g)`$. Selected target identities are fresh across the fragments; repeated original keys are allowed.

**Theorem 2 — Exact composition.** The composite has entry-depth requirement

```math
h_{fg}=\max(h_f,h_g-\delta_f).
```

Its outgoing form is

```math
(P_{fg},k_{fg})=
\begin{cases}
(P_g\mathbin{\|}P_f[k_g:],\,k_f), & k_g\lt{}p_f,\\
(P_g,\,k_f+k_g-p_f), & k_g\geq p_f.
\end{cases}
```

Together with the substituted emission list, these formulas give the exact effect of the concatenated fragment. Composition is associative as a partial transformation of stacks and selected emissions. [1, §3; 2, “Composition formulas”]

**Proof.** The first fragment accepts depth $`d`$ exactly when $`d\geq h_f`$. Its output depth is $`d+\delta_f`$. The second accepts that output exactly when $`d+\delta_f\geq h_g`$. Their conjunction is $`d\geq h_{fg}`$, proving the exact domain requirement.

The second fragment consumes $`k_g`$ frames from $`P_f\mathbin{\|}s[k_f:]`$. If $`k_g<p_f`$, it consumes only a proper prefix of $`P_f`$, leaving $`P_f[k_g:]\mathbin{\|}s[k_f:]`$. If $`k_g\geq p_f`$, it consumes all of $`P_f`$ and another $`k_g-p_f`$ incoming frames, leaving $`s[k_f+k_g-p_f:]`$. Prepending $`P_g`$ gives the two cases.

The current input position $`j`$ of the second fragment denotes $`P_f[j]`$ in the first case of the substitution definition and the shifted original input position otherwise. Thus every second-fragment emission receives exactly its direct-execution origin. First-fragment emissions remain unchanged.

For three fragments, either parenthesisation admits precisely those inputs on which the same three executions succeed in sequence. On such inputs it returns the same stack and concatenated selected emissions. On all other inputs both parenthesisations reject. This proves associativity of the partial transformation. It does not require every syntactic presentation to have identical unreachable output names. $`\square`$

The formulas concatenate lists, not sets of roles. Their source keys preserve occurrence identity; their role values remain unresolved.

### 2.3 Keyed exits and source-bound cuts

Depth alone cannot validate a closing marker from another source or snapshot. A refinement replaces an unlabelled leave by $`\mathrm{exit}(o)`$, which first requires the current origin to equal the supplied original key $`o`$.

Extend an effect by a finite conjunction $`C`$ of origin-reference equalities. If the symbolic current origin is a literal key $`a`$, an exit checks $`a=o`$. Unequal literals make the domain empty. If the current origin is $`I_j`$, the exit adds $`I_j=o`$ and then performs the leave update. Two distinct required keys for one incoming position also give an empty domain. Equality here is equality of the bound source, snapshot, and context occurrence, rather than equality of its proposition. [2, “Optional keyed exits”; 8, §1]

For a nonempty domain, a stack is admitted exactly when its depth is at least $`h`$ and its substituted equalities satisfy $`C`$. Composition carries

```math
C_{fg}=C_f\wedge\rho_f(C_g)
```

with the depth, emission, and outgoing-stack formulas above.

**Proof of the keyed composition claim.** The first effect must pass its own depth and equality checks. Every reference examined by a second-fragment exit denotes the corresponding expression under $`\rho_f`$. It therefore passes exactly when the substituted equality holds on the original input. Conjoining these conditions gives precisely the domain of sequential execution. On that domain, Theorem 2's stack and emission calculation is unchanged. If a literal contradiction arises, the sequential execution has no admitted input. Associativity follows by the same three-execution argument, including rejection domains. Empty-domain representations need not agree on emissions that can never occur. $`\square`$

For example, the suffix

```math
\mathrm{exit}(f);\quad
\mathrm{exit}(p);\quad
\mathrm{emit}(z)
```

has minimum depth three and requires $`I_0=f`$ and $`I_1=p`$. Its selected emission still refers to $`I_2`$. These checks do not identify $`I_2`$ with any particular original key $`a`$. A separate boundary witness must supply that map.

The refinement rejects a wrong-snapshot exit, an unequal required origin at the right numerical depth, and mutually contradictory requirements for one incoming slot. It admits a correctly bound same-origin continuation. More difficult natural-language scope boundaries remain an interpretation question. Neither balanced markers nor exact key comparisons authenticate their extraction from a real source.

### 2.4 Translation and changed representations

An admitted transformation may alter language, proposition strings, local output identities, and token counts. It must preserve each selected output's original-context reference and the justified source-scope operations, or supply an independently warranted effect with the same action on admitted entry contexts. Fresh local occurrence identities do not replace the original source keys.

Effect correctness then preserves the selected source-attribution references across the changed representation. A translation preserving propositional content alone has not established this premise. A wrapper may also change the current carrier's force while leaving the original-source relation intact. Those are separate transformations and require separate records. [1, §3; 3, §2]

A conventional scope parser supplied with the complete context stack already meets this structural task. The point of the symbolic effect is to make the needed interface explicit when fragments are split and the receiver lacks that stack.

## 3. Deriving the live source dependencies

Different branches may start with different incoming placeholders. At reconvergence, source-bound substitutions identify each relevant placeholder with an original context. Shared originals use the same key; equal strings are insufficient grounds for such identification.

For the selected next decision, substitute those boundary maps into the composed emission lists and collect the distinct resulting keys. If a selected key already has a warranted negative role, the conjunction is false without further role reads. Otherwise remove keys with warranted positive roles. Call the remaining set $`L`$. The unresolved decision is then

```math
Q(x)=\bigwedge_{o\in L}x_o.
```

An empty conjunction is true. The set $`L`$ is derived from the selected continuation and its supplied identity maps. It is not an arbitrary demand to retain every ancestor's annotation. [1, §4]

**Proposition 3 — Query-specific role dependence.** Once the relevant original identities and known roles are fixed as above, the selected query depends only on the roles of the distinct keys in $`L`$. A frame contributes no dependency unless a selected output is attributed to it. Repeated outputs with one original key contribute one factor. If the admitted family includes an all-positive assignment and, for every $`o\in L`$, an assignment changing only that relevant bit to zero, no one of those factors can be discarded as irrelevant.

**Proof.** By Theorems 1–2 and the boundary substitutions, each selected output has one determined original key. The query asks for the authorial-role predicate at each such key. Repeated occurrences of the same Boolean factor leave a conjunction unchanged. Known positives also leave it unchanged; a known negative makes it false. These operations give exactly the displayed formula.

For essential dependence on a particular remaining key $`o`$, compare the admitted all-positive assignment with its single-negative alternative at $`o`$. All other relevant roles agree and the query changes from true to false. Thus the query is not a function of the other relevant roles alone on that admitted family. $`\square`$

The dependence statement is conditional on the admitted source family. Natural nested roles may be correlated. A retained constraint store or packed interpretation can make some role inferable from other evidence. Such information must be preserved in the comparison rather than replaced by an artificial product of independent choices. The grammar construction in §6 supplies a specific family for which the required alternatives are coherent.

This proposition does not establish a universal minimum of $`|L|`$ transmitted bits. An adequate task-specific verdict can settle the conjunction without transmitting every individual role. Nor does a verdict for this conjunction automatically answer later per-occurrence questions. The communication problem of selecting or transmitting an admitted output is treated separately in [Information and Inquiry, §9.4][information-selection]. Here the remaining question is what the declared read service enables a particular receiver to acquire.

### 3.1 Identity acquisition precedes role acquisition

There are two missing objects:

1. The original context denoted by an incoming placeholder.
2. The witnessed role of that identified original context.

A symbolic effect can preserve the placeholder without providing either. The receiver cannot compute a resolved $`L`$ by silently assuming the first object and then charge only for the second.

An actual context-path read may supply both. In the historical source case described by the public predecessors, the first repair supplied an incoming-to-original map and its role together. It was a combined identity-and-role observation. The label-only cover theorem applies to a later phase in which the necessary identity map is retained while some role evidence is missing. This chapter uses the public account of that boundary; it does not repeat the source inspection or acquire the underlying captures. [3, §5; 8, §3]

If a fixed adequate identity-acquisition protocol costs $`c_0`$ and also reveals roles on $`K`$, then, conditional on its actual holdings and absent a known relevant negative, the plan

```math
c_0+\mathrm{cover}(L\setminus K,W)
```

completes the two phases whenever its cover is finite. The second term is exact under the hypotheses of the following theorem. The sum is not claimed optimal among all possible joint identity-and-role protocols. A different joint observation may reveal more information at a different price.

The source-coordinate dictionary, path witnesses, and role-bearing information obtained while constructing them belong in the cost and evidence account. An equally informed conventional implementation receives the same maps and observations.

The three-event calculus also does not infer arbitrary reply-to-objection edges. A reply's document role can be classified without reconstructing every relation in its argument graph. Such reconstruction requires a separately justified interface.

## 4. Exact cost under a declared read service

Let $`W`$ be a finite menu of presently available and permitted reads. A read $`w`$ has a fixed positive cost $`c(w)`$ and a justified role-coverage set $`C(w)\subseteq O`$. Its successful response supplies adequate original-role evidence for every claimed covered key. A copied credential, link, or source name does not itself make a read available or permitted.

For an unresolved demand $`L`$, define

```math
\mathrm{cover}(L,W)=
\min\left\{
\sum_{w\in F}c(w):
F\subseteq W,\quad
L\subseteq\bigcup_{w\in F}C(w)
\right\},
```

with value $`\infty`$ when no cover exists. The empty family covers the empty set at cost zero.

A deterministic policy may choose its next read from the complete preceding observations. It must terminate with the correct Boolean answer on every admitted source. Safe withholding or an unresolved answer is not completion of this particular contract. The source snapshot and labels remain fixed during the task, and read costs add. [1, §5]

### 4.1 The all-positive star

The lower bound uses the following explicit family, conditional on the receiver's entire initial holdings:

- An admitted source $`s^*`$ makes every unresolved relevant $`x_o`$ equal to one.
- For each $`o\in L`$, an admitted source $`s^{(o)}`$ has $`x_o=0`$ and all other relevant roles equal to their values in $`s^*`$.
- The complete initial observations agree across these sources up to the permitted consistent renaming of opaque handles.
- Whenever $`o\notin C(w)`$, the complete observable response to $`w`$ agrees between $`s^*`$ and $`s^{(o)}`$ under that same renaming.

Reads covering a key must also reveal an adequate witness for its role. Response locality and response adequacy are separate requirements: a constant response may satisfy locality while revealing nothing. [3, §6; 8, §1]

The star has only $`|L|+1`$ required source assignments. A full product of independent binary roles is a sufficient stronger construction, but is not necessary for this proof. The word “independent” here must not conceal a missing observation premise: no probability distribution or stochastic independence assumption is being used.

**Theorem 4 — Exact deterministic read cost.** Under the stated star, locality, adequacy, fixed-service, and total-decision assumptions, the minimum worst-case cost of a deterministic completing policy is $`\mathrm{cover}(L,W)`$. If the cover is infinite, no such policy exists.

**Proof.** Follow any completing policy on $`s^*`$. If it terminates before reading a family covering $`L`$, choose an uncovered key $`o`$. The initial holdings agree with those on $`s^{(o)}`$. Induct over the reads on the $`s^*`$ path. Equal observations and determinism give the same next read, up to the admitted handle renaming. That read does not cover $`o`$, so locality supplies the same complete response. The induction therefore gives the same terminating decision in both sources. Their conjunctions differ, a contradiction.

Consequently the all-positive path reads a cover. If a read is repeated, its repeated cost only increases the path cost; the distinct reads on that path still form a cover. The worst-case cost is at least $`\mathrm{cover}(L,W)`$. If no cover exists, the contradiction excludes every total completing policy.

For a finite cover minimum, choose an attaining family, which exists because $`W`$ is finite. Read its members. Return false when an adequate witness gives a relevant zero; otherwise return true after all demanded roles have been covered. Adequacy makes every returned answer correct. The cost is at most the selected cover cost on every admitted source, and the all-positive source requires the full cover under this policy. The upper and lower bounds coincide. $`\square`$

Adaptivity can reduce realised cost on a negative source. It does not reduce this worst-case cost under the theorem's premises. The theorem supplies neither a probability of truth nor an expected-cost optimum.

### 4.2 Why the response premise is substantive

Suppose an outside value $`z`$ equals $`Q`$ and can be read cheaply without covering any individual target origin. The conjunction is then decidable from that response. Independence of the target labels does not remove this channel. A retained old-task result correlated with a current role can likewise reduce the remaining cost. A supposedly unrelated result cannot be ignored merely because it belongs to an earlier task. [3, §6; 9, “Adversarial controls”]

A locator spelling, response length, status, timing, or interpreted authentication payload can carry the same information. If a left-card response additionally reveals the rightmost role, its coverage or fuller observation model must reflect that fact. An actual service with rich contextual evidence may allow a cheaper decision than the restricted cover model predicts.

The corrected theorem therefore compares whole initial holdings and whole responses. It does not retain the weaker claim that target-label independence alone forces cover cost. The public precision document expressly supersedes that weaker formulation. [3, §6]

Locality also does not establish witness sufficiency. A source-role record must contain the opening or path evidence, including exclusion from relevant outer quotation scopes, or an adequate bound certificate. A bare proposition cannot be counted as a role witness simply because a coverage table labels it as one. Establishing those coverage claims is part of defining a real service.

### 4.3 Alternatives change the contract

Several legitimate additions can change or settle the decision:

| Additional holding or service | Consequence |
|---|---|
| A warranted relevant negative | The conjunction is already false |
| Warranted relevant positives | Remove those origins from the residual demand |
| An adequate bound fixed-task verdict | The selected conjunction is already settled |
| A genuinely available whole-source read | Add its actual coverage and price to the menu |
| Permitted singleton reads | Add those alternatives; their total price bounds a finite cover when all roles are covered |
| A richer correlated observation | Recompute decision adequacy from the full responses; simple cover equality may fail |
| A missing or expired query permission | The corresponding operation is absent unless another legitimate route exists |

Cheap singleton reads do not by themselves make optimisation over a mixed menu trivial. Nor may an available whole-source read be withheld from the conventional baseline to make a difficult card instance appear relevant. A promise to read later supplies an operational route only when an actual service, permission, allowance, and adequate evidence relation support it. [1, §§5, 7; 4, §5]

The exact result concerns acquisition under specified holdings. It is not an entropy law or a lower bound against arbitrary encodings. No distribution has been supplied, so this model assigns no Shannon entropy or expected read cost. A binary verdict may have one variable truth bit while requiring substantial binding, authentication, interpretation, and verification material. Counting that bit alone would understate its evidential cost; demanding all raw role bits despite an adequate verdict would overstate its necessity.

### 4.4 Relation to eligible conflict covers

The general identification criterion is already proved in [Objective Normativity and Corrective Cognition, §8.4][normativity-cover]: an eligible family identifies a target exactly when it distinguishes every pair of candidates with different target values. Section 8.5 distinguishes registry cardinality from independently justified acquisition costs and allows a weighted formulation.

The present static cover problem is a direct specialisation. Treat a role assignment as a candidate, its conjunction as the target, and an adequate read as an evidential coordinate. Each all-positive/single-negative pair forces a read covering the changed role. Conversely, a family revealing all relevant roles determines the conjunction. The additional argument here establishes the same cost lower bound for deterministic adaptive policies under complete-response locality. The source-effect calculation supplies the particular roles to which that result applies. This is not a second general theory of conflict covers. [5, §A]

## 5. Source order and the organisation of access

Suppose original contexts have a fixed source order. A source-ordered role-witness window has endpoints and supplies adequate role evidence for every demanded origin between them. This can be implemented by an ordered store of properly bound role records or by a service that completes the required contextual paths. The construction of the store, its authenticity, and the justification of its coverage have separate costs. [1, §6; 3, §7]

### 5.1 Convexity concerns adequate witnesses

Raw text contiguity does not imply the window property. A retrieved span may contain a target clause while omitting the opening of an outer quotation that determines its original role. Some roles in the span may be established by available local evidence while another remains unresolved. The positions of the included words do not by themselves prove convexity of the adequately witnessed origins.

The interval result therefore assumes that coverage, restricted to demanded origins, is convex in their original order. It does not derive this from byte offsets or from an unverified coverage label. The service must also satisfy the complete-response premise if Theorem 4's exact decision-cost equality is to be used. Additional context may be informative in ways that change that equality.

List the distinct demanded original positions as

```math
\ell_1<\ell_2<\cdots<\ell_m.
```

Selected output occurrences may duplicate or reorder them arbitrarily.

**Theorem 5 — Source-order quotient.** For an adequate source-ordered window, its covered demanded keys form a consecutive sublist of $`\ell_1,\ldots,\ell_m`$. Copying and reordering output occurrences cannot change this interval property after outputs with one original key are identified for acquisition purposes.

**Proof.** If a source window covers positions $`\ell_i`$ and $`\ell_k`$ with $`i<j<k`$, its endpoints enclose $`\ell_j`$. The assumed adequate-window contract supplies the role witness for that demanded origin too. Output multiplicity and output order do not occur in this argument. The selected effect changes which original positions are demanded, while their original order and the window's adequacy remain fixed. $`\square`$

The quotient identifies shared acquisition obligations, not output occurrences. Those occurrences retain their distinct identities and current-carrier relations.

The correction is consequential: a source interval can have a scattered image among reordered output copies, but that image is not the appropriate ground set for acquiring the same original role once. Copying alone does not turn the original-source interval problem into arbitrary set cover.

### 5.2 The weighted interval algorithm

For a window with nonempty demanded coverage, let $`r(w)`$ be the largest demanded index it covers. Let $`F(i)`$ be the minimum cover cost for the suffix of demands starting at $`\ell_i`$, using the same read menu. Set $`F(m+1)=0`$ and compute backwards:

```math
F(i)=
\min_{\substack{w\in W\\\ell_i\in C(w)}}
\left(c(w)+F(r(w)+1)\right),
\qquad i=m,m-1,\ldots,1.
```

A minimum over an empty family is infinity. In this recurrence $`r(w)\geq i`$, so each finite candidate uses an already computed later suffix.

**Proposition 6 — Exact interval cover.** Under the adequate-window assumption, $`F(1)=\mathrm{cover}(L,W)`$. Recording an attaining window at each finite entry yields a legal minimum-cost read plan. A direct table uses $`O(m|W|)`$ candidate evaluations after endpoints are known and $`O(m)`$ cost storage. [1, §6]

**Proof.** A window covering $`\ell_i`$ covers every demanded position from $`i`$ to $`r(w)`$ by convexity. Combining it with a cover of the remaining suffix therefore gives a cover of the whole suffix from $`i`$. This proves that each finite recurrence candidate is attainable.

Conversely, consider any finite minimum cover of that suffix. Choose among its windows covering $`\ell_i`$ one with largest right endpoint, say $`w`$. This window covers nothing after $`r(w)`$. The other windows must consequently cover every demanded point of the suffix starting at $`r(w)+1`$. Their total cost is at least the minimum cost of that later suffix. Thus the recurrence includes a candidate costing no more than the selected optimum. Induction from the empty suffix proves equality at every index. If no cover exists, a finite recurrence candidate would construct one, so the infinite value is also exact.

Following stored attaining windows strictly advances the demand index and therefore terminates. A selected window cannot be needed again after its last demanded endpoint. The resulting distinct reads form a legal cover with the computed cost.

For each of the $`m`$ indices, scanning $`W`$ gives the stated number of candidate evaluations. The table and one chosen successor per index use linear storage. This counts arithmetic and comparisons under the supplied cost representation; it is not a bit-complexity bound for arbitrary real costs or a resource bound for authenticating the input metadata. $`\square`$

With unit costs, choose a window covering the earliest uncovered demand with the furthest right endpoint. Replacing a window that covers that first demand by the greedy choice cannot uncover any still-required point up to the replaced endpoint; the greedy endpoint is at least as far. The residual suffix is no larger. Repeating this exchange gives the familiar optimal greedy interval cover. The weighted recurrence and unit-cost rule are conventional algorithms. The source-specific result determines when they remain applicable after fragment transport and copying.

### 5.3 Whole cards supply a different menu

A different successor service may permit only whole context-witness cards in a derived dossier. Each card is a contiguous block in that carrier, assembled from adequate source-backed role records. The records may come from separated original contexts. A whole-card read can therefore cover an arbitrary subset of original keys.

This is a change of permitted access operations. It is not an effect of output copying by itself. If original-source windows, cross-card reads, a live competent reader, or a whole-source operation remain available, they belong in the successor's menu. The card-only model cannot silently remove them.

The distinction is useful even when all underlying facts continue to exist and remain accessible eventually. An adequate ordered service may allow a structured interval plan, whereas a whole-card-only service can give a different minimum acquisition cost. Complex retrieval does not invalidate a conclusion already warranted by retained evidence; it matters when the successor actually needs to acquire the missing roles.

## 6. Realisable sources and explicit resource costs

The source-assignment family and the access menus can be constructed rather than merely postulated as unrelated Boolean tables. The construction supplies a restricted model with a known grammar. It makes no assertion that actual philology offers every binary alternative at a fixed passage. [4]

### 6.1 A coherent family of source documents

For $`n`$ demanded origins and a vector $`x\in\{0,1\}^n`$, form a source with a neutral root and $`n`$ consecutive sibling sections. Section $`i`$ has an explicit opening role token: an own-assertion token for $`x_i=1`$ and a reported-speaker token for $`x_i=0`$. It contains a fixed proposition occurrence and then closes. Give that section origin $`o_i`$.

All assignments have the same event shape

```math
\mathrm{enter}(o_i);\
\mathrm{emit}(t_i);\
\mathrm{leave},
```

the same proposition strings, the same source-coordinate and equality pattern, and different omitted role tokens as required. Every copy of section $`i`$ retains the same original key and therefore the same role. The family does not assign contradictory roles to copies of one source context.

Use equal-width tokens such as ROLE0 and ROLE1, together with fixed-width instance-specific key fields, scope markers, and padding. Source offsets, card lengths, public menus, and declared costs are then assignment-independent. The read interface reveals local role-witness records and treats source bindings as opaque. Role-dependent timing, statuses, interpreted signature payloads, and undeclared content-address lookups are excluded by the observation contract. Under these restrictions, an uncovered role change leaves the entire permitted response unchanged. This realises the all-positive star; the construction also realises the larger full-product family. [3, §§1, 6; 4, §§1, 7]

To make suspended-context restoration essential, insert a balanced, unselected inner report before each selected emission. Alternatively, cut after entering that inner report and place the “leave; selected emit” suffix in a later fragment. The suffix now depends on the restored sibling context. Its identity map and original-role evidence remain separate.

The independent roles occur at sibling sections under the neutral root. An inserted inner report always has nonauthorial document-global force, regardless of its parent's role. Returning restores the parent. This avoids an incoherent construction in which naming an author inside an outer quotation is assumed to create independent original-document authorial force. A different source population with correlated nested roles would require its own star argument. [4, §8]

### 6.2 Exact correspondence with card cover

Take an explicitly listed Set Cover instance with universe $`U=\{1,\ldots,n\}`$, subsets $`S_1,\ldots,S_q`$, and a cardinality budget $`b`$. Construct the preceding source family. Card $`j`$ contains an adequate source-backed role-witness record for each $`i\in S_j`$ and retains each original key $`o_i`$. Permit only whole-card reads, at unit cost, with no crossing of card boundaries and no surviving original-source operation in this stipulated interface.

The selected output catalogue contains one occurrence for every universe element, with its original dependency derived by the fragment effects. The catalogue contains those references, not the missing role witnesses. Public coverage lists identify the original keys in each card; they do not reveal their omitted roles. A universe element with no supporting card remains unresolved.

**Theorem 7 — Whole-card cover correspondence.** In the constructed source/read family, a deterministic exact policy with worst-case cost at most $`b`$ exists exactly when the supplied Set Cover instance has a cover of at most $`b`$ sets. The minimum policy cost equals the minimum card-cover cardinality. Assigning positive declared card costs gives the corresponding weighted equality.

**Proof.** The construction realises the all-positive and each single-negative source. Equal-width local records and the opaque interface satisfy complete-response locality, while a read supplies the role evidence of its listed originals. Theorem 4 therefore applies with demanded set $`\{o_1,\ldots,o_n\}`$ and card coverage $`C(j)=\{o_i:i\in S_j\}`$. A card family covers the demanded keys exactly when the corresponding set family covers $`U`$. The decision and minimum-cost equalities follow. If a demanded element is uncovered, both cover feasibility and exact total decision fail. $`\square`$

For the explicitly listed unit-cost decision problem, this gives the inherited NP-completeness boundary: the construction reduces the standard Set Cover problem, while a proposed finite covering subfamily is a polynomially checkable certificate. The complexity claim is about this finite represented decision problem. It supplies no new hardness technique and makes no claim about verification with arbitrarily represented real costs. [4, §2; 5, §D]

### 6.3 Copies and dictionaries count as input

Let

```math
M=\sum_{j=1}^{q}|S_j|.
```

The unpadded construction contains $`n`$ original contexts, $`M`$ explicit transclusion records, $`q`$ card boundaries, and $`n`$ selected output references. Its origin dictionary contains $`n`$ entries. Each index for an original key uses $`O(\log(n+1))`$ bits in addition to its actual source/snapshot binding.

The syntactic structure therefore has

```math
O(n+q+M)\ \text{nodes}
```

and

```math
O\!\left((n+q+M)\log(n+q+1)\right)
```

indexing bits, plus the actual locator and witness-format material. Constant-size inserted inner reports preserve these orders. There is no implicitly free exponential set of copies. The $`2^n`$ role assignments describe possible inputs used in the argument; the construction does not store or enumerate that entire corpus as one small instance. [4, §3]

A fragment effect stores its selected emission references, finite residual prefix, incoming-tail offset, and depth bound. Its reference count is bounded by its selected emissions plus unmatched local enters. Its integer indices and any keyed preconditions also require representation. Computing an effect and establishing original-key equality consume the fragment and dictionary inputs. Reporting only the number of distinct demanded origins would omit those costs.

These are structural input bounds. They do not measure production parsing time, human reading, source authenticity, or the cost of preparing justified context witnesses.

### 6.4 One request and one byte are different prices

The unit-cost construction counts requests, approvals, or rounds. It does not make arbitrarily long card responses constant-time or equal-bandwidth operations.

An empty card menu already has cost zero for empty demand and cannot cover nonempty demand. For an equal-response-length variant with a nonempty card menu, let

```math
s=\max_j |S_j|.
```

Pad every card to $`s`$ entries using copies of one distinguished irrelevant context $`z`$. Its role is fixed and the selected conjunction does not depend on it. Give all origin/role records the same width within the represented instance and use a common envelope. Every card then has the same response length $`B`$. There are $`O(n+q+qs)`$ structural nodes, with the same explicit binding and indexing qualifications. The separate $`q`$ term counts card boundaries and envelopes even when every card is empty and $`s=0`$. This corrects the predecessor's $`O(n+qs)`$ shorthand for that admitted edge case; no covering or read-cost conclusion changes. This is polynomial in the listed cover instance size.

If read cost is response length, a budget $`bB`$ permits precisely a cardinality-$`b`$ family in this whole-card interface. Padding neither adds relevant evidence nor permits new sub-card or cross-card operations. Real signatures, path records, hashes, and verification work must be added when claiming corresponding physical byte or time costs. The role bit alone is not being presented as a sufficient source witness. [4, §4]

### 6.5 Information preserved and access preserved

Three distinct quantities recur:

| Quantity | What the present result establishes |
|---|---|
| Original source roles needed by the selected continuation | Derived by the effect and boundary substitutions |
| Cost of deciding their conjunction through the declared service | Exact weighted cover under Theorem 4's full hypotheses |
| Total information or physical resources needed by every possible protocol | No general optimum asserted |

The same source facts can remain available under different organisations of access. The cost comparison does not create additional testimonial independence, make copied observations more trustworthy, or change the roles within one snapshot. It identifies the evidence that the receiver still lacks and the operations actually offered to acquire it.

## 7. A bounded handoff with two surviving cards

Consider a constructed attribution workflow that will replace its original role-witness service. The recipient's declared next task has a legitimate final-stage allowance of one permitted request. This is a supplied workflow condition, not a budget inferred from the mathematics. The case does not allege an actual restriction or retirement of any historical source page. [6, §§1–3]

### 7.1 Deriving the task before pricing it

Use three sibling contexts $`a,b,c`$ in that original order. For each $`i\in\{a,b,c\}`$, a split fragment has suffix “leave; emit $`t_i`$” and incoming stack

```math
[\mathit{inner}_i,i,\mathit{root}].
```

Its selected output refers symbolically to $`I_1`$. An independently verified boundary map identifies that reference with original key $`i`$. Map acquisition and justification are prior preparation costs; later role-only reads do not reconstruct them.

After transport and reconvergence, the selected output order is

```math
c,\ a_1,\ b,\ a_2.
```

The two occurrences $`a_1,a_2`$ have fresh carrier identities and the same original $`a`$. Their derived original demand is therefore $`L=\{a,b,c\}`$, with

```math
Q=x_a\wedge x_b\wedge x_c.
```

The current carrier may quote all four outputs. Their current force remains separate from the original-role predicate in $`Q`$.

The recipient initially has the source and snapshot bindings, boundary maps, selected list, source order, coverage index, and any stipulated old-task result concerning a separate context $`d`$. It has no relevant role witnesses or adequate verdict for $`Q`$. These complete holdings are assumed to satisfy the star condition. An old result equal to $`Q`$, or even one revealing $`x_a`$, would be informative and change this case. The earlier completion of a genuinely separate task is not completion of $`Q`$ followed by unexplained forgetting of its answer. [6, §2; 9, “Adversarial controls”]

### 7.2 What the service replacement supplies

Before replacement, one adequate source-ordered read covers $`\{a,b,c\}`$ at cost one. After replacement, the stipulated surviving service offers only:

| Surviving operation | Adequate original-role coverage | Request cost |
|---|---|---:|
| Left card | $`\{a,b\}`$ | 1 |
| Right card | $`\{b,c\}`$ | 1 |

Both cards remain genuinely available and permitted. They expose every required role between them, but the final stage allows only one request. No cross-card read, free singleton lookup, retained whole-source service, or later competent answering service is included in this particular proposed replacement. Any such route that actually remains available must be added.

On the all-positive source, either one-card choice leaves an endpoint unresolved. The corresponding single-negative alternative yields the same complete response and changes $`Q`$. Consequently no deterministic total exact policy completes every admitted case with one request. Two requests suffice. This is the direct two-card instance of Theorem 4. It proves a failure of the stipulated worst-case capacity, not failure on every actual source.

The old joint response may contain more bytes than one new card. No equality of bandwidth, authentication work, or total preparation time is assumed. The comparison concerns the final request allowance conditional on its documented holdings.

Both displayed cards are convex in the original order. This small example does not require arbitrary-incidence hardness and does not contradict Theorem 5.

### 7.3 Which retained witness is sufficient?

Let $`K`$ be the set of valid role witnesses transferred before replacement. A known relevant negative decides $`Q`$ immediately. In the all-positive case, the residual demand is $`L\setminus K`$ and its later request cost is the card-cover number.

The one-witness comparisons below are separately predeclared plans: always retain $`a`$, always retain $`b`$, or always retain $`c`$. The selected origin does not depend on the role values.

| Handoff evidence or service | Residual all-positive demand | Minimum later requests | Meets allowance one |
|---|---|---:|---|
| Two cards only | $`\{a,b,c\}`$ | 2 | No |
| Two cards and witness for $`b`$ | $`\{a,c\}`$ | 2 | No |
| Two cards and witness for $`a`$ | $`\{b,c\}`$ | 1, right card | Yes |
| Two cards and witness for $`c`$ | $`\{a,b\}`$ | 1, left card | Yes |
| Witnesses for all three | Empty | 0 | Yes |
| Adequate bound verdict for $`Q`$ | Query already settled | 0 | Yes |
| Retained adequate joint window | $`\{a,b,c\}`$ | 1 | Yes |

**Proposition 8 — Endpoint and middle retention.** Under the fixed-plan, complete-observation, and service assumptions, retaining either endpoint role permits exact completion within one request. Retaining the middle role alone does not. An adequate relevant negative or fixed-task verdict permits zero later role reads.

**Proof.** With $`x_a`$ retained, a negative value already decides the query; otherwise the right card reveals $`x_b,x_c`$. The symmetric argument applies to retained $`x_c`$. At the all-positive source, one card is necessary for either endpoint plan because the omitted roles include an independently changeable endpoint of the opposite card.

With only $`x_b=1`$ retained, a left read leaves $`c`$ unresolved and a right read leaves $`a`$ unresolved. The respective single-negative alternatives agree with the initial retained witness and chosen response while changing $`Q`$. Hence one request cannot suffice in all cases. Both cards do suffice. The final assertion follows directly from the meaning and adequacy of the negative witness or bound verdict. $`\square`$

The middle witness can be entirely authentic, current, and correctly interpreted. It fails to remove the dependency that prevents one-card completion. Endpoint and middle packets can use the same fixed witness-record envelope and identity dictionary. Their difference is which original role they preserve. This is not a theorem of globally minimum storage.

Maximal retention is unnecessary. There is no need to carry both copies of $`a`$ as independent evidence, every ancestor role, or the full source merely to meet this particular task. If the selected next question concerns only copies of $`a`$, its derived demand is just $`\{a\}`$, and one left-card read suffices without either irrelevant endpoint.

### 7.4 Selection identity and other informative alternatives

A value-dependent selection plan is a different communication channel. For example, under an agreed adequately warranted rule, choosing origin $`a`$ exactly when $`Q`$ is true and $`b`$ otherwise allows the selected identity to communicate $`Q`$. The receiver can then need zero later role reads. This is a permitted alternative to assess, not a violation of the fixed-plan lower bound. The source family conditional on that packet identity no longer has the same initial observations across the required star. [6, §4; 7, control 17; 9]

A separately produced verdict can have the same effect. It must bind the snapshot, selected output list, and original-role predicate, and must be adequate for the recipient under the actual protocol. A signature on a guess or an unqualified source name does not meet that requirement. The variable truth bit is only part of the record and its warrant.

A live competent reader, a maintained joint read, a proper full-source copy or role table, a legitimately agreed two-request allowance, or an informed task revision may also remove the capacity gap. Actual availability, permission, competence, and applicability must be established for each proposed route. Verbal promises alone do not supply those conditions.

A fixed-$`Q`$ verdict has a definite limit. It does not generally answer the stronger question asking for all three individual roles. If the verdict is false and the first read is left, the assignments $`(0,0,0)`$ and $`(0,0,1)`$ have the same verdict and left response while differing at $`c`$. If the first read is right, $`(0,0,0)`$ and $`(1,0,0)`$ have the same verdict and right response while differing at $`a`$. Therefore one deterministic read cannot always recover the role vector even with the conjunction verdict. Two reads suffice. Endpoint evidence plus the opposite card, in contrast, recovers all three roles. This is the different-task control recorded in [9], with its elementary derivation given here.

A changed snapshot or selected list also changes the binding question. An old result applies only under a separately warranted relation to the new task. A copied digest or report heading does not establish that relation.

### 7.5 Exact completion and accepted risk

The exact-task assumption has consequences that an accuracy statistic can hide. In the full eight-assignment family under the uniform distribution, always answering false is correct on seven assignments. Its accuracy is $`7/8`$, but it fails on the all-positive source. It provides no exact total decision.

The historical joined review also records a one-read randomised policy with worst-case success $`2/3`$. An explicit policy attaining that reported level chooses either card with probability $`1/2`$. If a zero is seen, it answers false. If both observed roles are one, it answers true with probability $`2/3`$ and false otherwise. On the all-positive source its success is $`2/3`$. On a source with only $`a`$ negative, or only $`c`$ negative, it succeeds with probability

```math
\frac12+\frac12\left(1-\frac23\right)=\frac23.
```

If $`b`$ is negative, or both endpoints are negative, either card detects a zero, giving success one. These cases cover every negative assignment. This construction witnesses a weaker success contract; no optimality among randomised policies is claimed here. [9, control 6]

Neither $`7/8`$ average accuracy nor $`2/3`$ worst-case success meets the stipulated zero-error completion requirement. A different accepted risk contract requires its own adequacy and proportionality assessment. Mathematics does not choose that contract for the participants. Safe abstention may be appropriate even though it leaves the declared task incomplete; a lucky correct guess does not retrospectively establish that an inadequate plan supplied the required evidence.

## 8. The conditional responsibility of an organiser

The operational argument identifies a capacity difference. A practical conclusion requires a separately supplied account of the relationship and of care. The public bounded-release application attributes that account to an accepted parent argument; this chapter uses the premise at its stated scope and neither revises nor claims a fresh review of that parent edition. [6–7; 9]

The relevant premise is:

> Active organisation or assumption of another subject's legitimate bounded reliance, together with understood exposure and relevant control, supplies a special pro-tanto reason for proportionate care, including fitting transition arrangements.

A pro-tanto reason can be outweighed or qualified by other reasons. It does not make every technically possible assistance obligatory. Related distinctions between substantive relations, valid undertakings, and mere claims to authority appear in [Objective Normativity and Corrective Cognition, §10.5][normativity-relations].

### 8.1 Independent application premises

Let $`G`$ organise the service and $`R`$ be the recipient. The controlled application supplies the following facts and normative premise independently of the read calculation:

1. **Legitimate task.** $`R`$ has a real epistemic good in completing this permissible, specified task within its actual bounded stage. This does not make every later use legitimate.
2. **Organised reliance.** $`G`$ actively installed or assumed the provision, structured $`R`$'s reliance upon it, and accepted responsibility for the impending handoff. Bare ability, authorship, or source position does not establish this relation.
3. **Care premise.** The organised relation supplies the stated special reason for proportionate care. This is an independently defended normative premise, not a theorem about cover numbers.
4. **Knowledge and applicability.** $`G`$ understands the proposed replacement, its consequences for the documented holdings, and the available alternatives. At least one adequate precaution is actually available, permissible, feasible, and proportionate to the stakes. No undefeated competing reason excuses knowingly omitting every such precaution.
5. **Recipient agency and allocation of risk.** $`R`$ has not validly waived the relevant care. Informed refusal, valid limitation, and genuine renegotiation remain possible. Mere foresight that a service may end does not by itself waive negligent preparation.

The operational premises are likewise substantive: actual source and snapshot bindings; justified boundary maps; adequate witnesses; the full initial-observation restriction; the stated surviving menu and permissions; the independently fixed request allowance; exact decision as the required outcome; and fixed origin choice in the compared retention plans. The source family in §6 establishes a coherent mathematical instance of those conditions. It does not prove that a particular real workflow meets them.

The case concerns an intelligent organiser and a subject with a legitimate epistemic purpose. It does not treat the abstract parser as a conscious subject, and it does not infer practical perfection from an organiser's role as a source.

### 8.2 What follows when those premises hold

The operational result establishes that the two-card-only and fixed-middle-witness plans fail the one-request exact contract. It also establishes that an endpoint witness, an adequate fixed-task verdict, and the other genuinely supplied sufficient arrangements can remove that deficit.

Given the independent care and applicability premises, $`G`$ should not knowingly select the inadequate middle-only plan while omitting every available fitting adequate arrangement and then treat unchanged permission and eventual accessibility as sufficient discharge of the handoff responsibility. The preparation decision is the object of the judgment. The argument does not predict compliance or guarantee that every reasonable arrangement will later succeed. [6, §5; 7, “Joined conclusions”]

The requirement is disjunctive and proportionate: arrange an adequate response to the specified exposure. It does not require one canonical packet, permanent preservation of the original service, every future attribution use, or maximal retention. If an adequate accepted verdict is the least burdensome fitting response, the premise permits it. A real agreed revision of the budget or task can also alter what is owed.

The application may matter without a false assurance: deliberately creating or assuming the dependence can be normatively relevant before any separate deceptive promise is made. On the inherited care account, a later change of the organiser's preference need not erase an existing reason. Those are contributions of the parent normative argument, not new deductions from this example.

### 8.3 Controls on the practical inference

Several changes leave the arithmetic intact while changing the normative inference:

| Changed premise | Resulting limit |
|---|---|
| $`G`$ is an equally capable outsider who never organised or assumed the provision | The special relational premise is absent; other rescue reasons require their own argument |
| The task lacks the stipulated legitimate good, or a valid informed limitation changes the undertaking | The scope of care must be reassessed |
| Every adequate precaution is prohibited, impossible, or overwhelmingly costly | The fitting-precaution premise fails; the two-read calculation alone does not forbid proportionate withdrawal |
| $`R`$ competently refuses an adequate offered arrangement | The organiser gains no authority to force the task or assistance; further responsibility depends on the actual informed choice |
| A proportionate arrangement later fails unexpectedly | The case establishes no strict liability or guarantee against every failure |
| An inadequate arrangement happens to produce a correct guess | The outcome alone does not establish adequate prior care |

The practical premise does not authenticate a source record, confer query or disclosure permission, establish recipient warrant, or prove that a source will comply. It also supplies no general jurisdiction of the organiser over the recipient. No conclusion about an actual ultimate source, source-wide practical priority, necessary existence, numerical identity, or essential integrity follows from this constructed handoff. [6, §§5–6; 7, controls 11–15; 9, control 8]

The narrow positive result remains useful: under the admitted evidence and relationship conditions, the exact endpoint-versus-middle calculation selects which modest precaution meets a bounded undertaking. Unchanged permissions and eventual access can coexist with inadequate access for that undertaking. This is an application of an independently defended norm to a particular operational difference.

## 9. Antecedents and the scope of the contribution

The source-specific contribution is the connected calculation: derive post-return original-role dependencies from open fragments, preserve original aliases through transport and reconvergence, calculate exact permitted reacquisition cost under a corrected observation contract, and distinguish adequate source-order access from whole-card access. The bounded handoff applies that calculation to one preventive decision.

The elementary parsing, conjunction, covering, and complexity methods have established antecedents. An ordinary scope parser, shared-identity table, and conventional cover planner supplied with the same evidence and menu reproduce the results. No advantage follows from adopting a special vocabulary. [1, §8; 5]

### 9.1 Earlier programme arguments

The public prior-art screen [5] assigns the following ownership:

- The earlier work on complete operative-state correspondence and future handoff capacity already supplies export-collision, adequate-augmentation, joint-realiser, and resource-contract results, and distinguishes remaining evidence obligations from actually usable permitted reacquisition. A task-relative small packet or an adequate alternative route was already allowed.
- Earlier gluing work owns its coherent-section and common-bearer results. The present stack composition does not recast those as new general gluing theorems.
- Earlier copied-acquisition work owns the conservation of original evidential support under copying. Multiple carrier occurrences do not become independent origins here.
- Earlier versioned operational work owns dependency unions, relevant-version invalidation, absent-obligation version stamps, process-local issuer checks, rechecking immutable sources into a fresh admission, and serialised revision and use. The new context keys neither authenticate sources nor extend that runtime.
- The authority-indexed anchor-cover work already supplies the general eligible target-conflict-cover criterion, eligibility monotonicity, and typed version/authority migration conditions. The restricted read problem is a weighted application, with the adaptive lower bound proved under its additional star and response assumptions.
- The organised-reliance parent supplies the normative reason and release limits. Joining it to the two-card calculation earns the particular precaution-selection judgment, not a second general duty or continuation principle.

The current consolidated conflict-cover and retention treatments are cited at their actual points of use in §§3–4. The received public screen identifies the historical sources and their boundaries. In particular, it distinguishes its accepted public predecessor projection from an earlier local coordination text with two recorded replacements. This chapter neither treats those editions as byte-identical nor claims fresh possession or review of the private antecedent bodies.

### 9.2 External comparisons as inherited source reports

The following comparisons are inherited from the bounded public screen [5]. Its recorded inspection scopes are preserved. No external primary text was newly fetched or independently audited for this chapter, and the screen was not an exhaustive literature or global priority review.

| Antecedent identified by the public screen | Relationship to this chapter | Inspection reported by that screen |
|---|---|---|
| Corin Pitcher's [2005 paper on visibly pushdown expression effects][pitcher] | Richer open-stream effects include unmatched call/return tokens and compositional descriptions; the present three-event effect uses established reasoning | Primary PDF introduction, unmatched-token definitions, and effect/composition discussion; the identified subject-reduction/progression theorem was not independently reproved |
| Kumar, Madhusudan, and Viswanathan's [WWW 2007 streaming paper][streaming] | Nested processing, prefix-sensitive typing, and storage related to nesting depth precede this restricted stack model | Primary PDF abstract, §§1–2, typing definitions, and stated algorithm scope |
| Madhusudan and Viswanathan's [Query Automata for Nested Words manuscript][nested-query] | Future-dependent queries, potential answers, and rereading/storage trade-offs are earlier subjects | Primary manuscript introduction and streaming-space interface; the screen records the publication index's then-current “unpublished manuscript” description |
| Maier's [2014 journal publication on mixed quotation][maier] | Context-sensitive metalinguistic interpretation and unquotation have a broader semantics than this role projection | Primary journal abstract/publication page only; no full semantic audit claimed |
| Charikar, Fagin, Guruswami, Kleinberg, Raghavan, and Sahai's [priced-information work][priced] | Sequential queries and sufficient partial settings precede the elementary grouped-read certificate argument | Primary extended abstract, introduction, and sufficient-set/proof definition; JCSS metadata separately reported at [the DOI][priced-doi] |
| Koutris, Upadhyaya, Balazinska, Howe, and Suciu's [Query-Based Data Pricing][pricing] | Instance-based determinacy, shared views, minimum sufficient view cost, and an explicit Set Cover reduction are close antecedents | Author-hosted primary PDF, determinacy definitions, pricing formula, and §5.5's reduction at printed p. 43:28; [DOI][pricing-doi] recorded |

The screen also reports locating primary copies of conjunctive priced-information work by Laber, Carmo, and Kohayakawa. That preliminary location supports a further comparison lead. Its stronger approximation results are not imported into this chapter.

Changing prices from money to requests, rounds, or response bytes alone creates no new information-cost theory. Likewise, associativity of a restricted symbolic effect is not a new general effect calculus. The bounded contribution concerns the source-role interface and the corrections needed to make its combined access calculation valid.

### 9.3 Failures excluded by the corrected treatment

The distinctions above prevent specific invalid inferences:

1. Treating scattered output copies as proof that original-source interval access has become hard.
2. Inferring an exact read lower bound from target-bit independence while ignoring correlated outside observations.
3. Reading the role of an incoming parent whose original identity has not yet been established.
4. Treating raw text inclusion as adequate evidence of document-global force.
5. Promoting an original assertion into present carrier endorsement or a present grant.
6. Demanding raw role retention despite an adequate fixed-task verdict or another legitimate informative channel.
7. Inferring a duty from a numerical access cost while omitting the relational, normative, and applicability premises.

These were substantive limits of the received argument, including corrections made during its development. Their retention explains the modest scientific claim without claiming a general breakthrough.

## 10. Evidence, editions, and remaining boundaries

### 10.1 What the ordinary proofs establish

The results concern supplied event skeletons, source-origin identities, role interpretations, coverage, permission, cost, and observation relations. Their proofs establish consequences of those inputs. They do not establish the adequacy of an arbitrary natural-language parse or translation, actual source or issuer authenticity, new permission, independent testimonial support, a general policy extractor, numerical identity, or physical continuation.

The source-effect and read-cost arguments are ordinary proofs. The mathematical components, historical finite checks, source inspection, and conditional normative argument have different evidential roles. None becomes a fresh kernel theorem merely by appearing beside checked formal components in a larger collection.

### 10.2 Historical review and finite corroboration

The public bounded checker review [8] accepts the ordinary derivations at their restricted scope and reports independent finite executable comparisons against a concrete stack interpreter, exhaustive small covers, and a separate knowledge-state decision optimiser. Its named controls address underflow, shifted composition, keyed constraints, snapshot identity, nonconvex coverage, retired services, complete-response leaks, adequacy, and richer observation tables. It also reports mutation rejection and agreement with an equally informed conventional baseline.

These public review records are model-assisted research evidence, not external human peer review. They are historical reports at their frozen candidate and runtime. This chapter has not rerun the code, received all historical logs, or extended those finite observations to a universal execution proof. The review explicitly notes that Python strings do not physically enforce opaque handles, supplied role labels are not automatic interpretation, and implementation plan tuples are not a measured production resource bound. No general implementation-to-proof refinement is claimed.

The joined application review [9] separately records the exact two-card comparison, value-dependent selection, informative old results, weaker risk contracts, and stronger future questions. Sections 7–8 state and explain their relevant mathematical or conceptual controls. Their historical execution and custody records remain distinct from the arguments presented here.

### 10.3 The actual-source boundary

The source predecessors describe a bounded inspection of an electronic historical witness and a supplied analytical role extraction. That public account supplies a reported occurrence-fidelity control. Its full-page alternative was available during the reported inspection, and the synthetic service replacement is not attributed to that actual page. The first combined identity-and-role read is also distinct from the later role-only model.

This chapter has read the public argument and review bodies. It has not reacquired the primary captures, repeated a printed collation, verified a translator's production chain, or obtained specialist certification of the linguistic analysis. The separate printed-source collation, source capsule, wording controls, and related later occurrence studies are outside this seven-body consolidation. Their status is not changed by this exposition.

### 10.4 Accepted works and future use

The accepted parent arguments and their exact acceptance scopes remain unchanged. The source-attribution paper's release-candidate status, the bounded checker admission, and the joined application's historical narrow acceptance are separate records. Receipt of those public records does not constitute adoption or external human peer review of this successor.

All arguments necessary for the bounded effect, cost, access-geometry, and handoff results appear above. Any wider application must justify its own source interpretation, observation channel, permissions, task, and practical premises. Preservation of historical evidence and permission to retire source files require their own dispositions; scientific exposition alone does not decide them.

## References and exact public sources

The first seven references are the complete public prose bodies consolidated here. Their links fix the original baseline edition; their existing historical boundaries are retained. References [8]–[9] are public historical reviews used as evidence, not newly executed reviews.

**[1]** *Open-context continuation and source-ordered reacquisition.* Public article, 3 October 2026. [Exact source][source-article]. Git blob: `884dd60b9bcd61deb87054824fc17dafec41e421`. 22,309 bytes.

**[2]** *Exact finite open-fragment algebra.* [Exact source][source-algebra]. Git blob: `10bc898d729e10188afb28d2688415030895c4a6`. 4,428 bytes.

**[3]** *Observation and interpretation contract.* [Exact source][source-oracle]. Git blob: `7b785d845980593fa5fb0775ee1bee747b219761`. 11,935 bytes. Includes the correction from independent-target wording to the complete-response all-positive-star premise and the separate adequate-window requirement.

**[4]** *Realisability, costs and input-size account.* [Exact source][source-resources]. Git blob: `db2aa4ed6097ffd0091639f56338df2da73ad832`. 10,311 bytes.

**[5]** *Prior-art disposition for the restricted context continuation result.* [Exact source][source-antecedents]. Git blob: `de72a6c21c9790ad28cd2e9cb596ea8d95cf98ca`. 10,738 bytes. A bounded reported source screen, with its own primary-reading and edition limits.

**[6]** *Bounded release for a source attribution task.* [Exact source][source-release]. Git blob: `906ba6664e79342415285c27386960ecc8fdc467`. 18,258 bytes. Constructed operational and conditional care application.

**[7]** *Premises and adversarial controls for the bounded release case.* [Exact source][source-premises]. Git blob: `8cd0fc11e387abea5bce96b37310dfd27e15ec6e`. 8,423 bytes.

**[8]** *Independent bounded checker review.* [Exact public review][review-checker]. Historical ordinary-proof and finite-checker disposition; source interpretation and authentication remain separately bounded.

**[9]** *Independent joined bounded-release application review.* 3 October 2026. [Exact public review][review-release]. Historical acceptance at the narrow conditional application scope, with no canonical-change or publication authority.

[recognition-retention]: recognition-warrant-and-restoration.md#75-what-a-bounded-retention-account-must-establish
[information-selection]: ../mathematics/information-and-inquiry.md#94-selecting-a-valid-certificate-rather-than-recovering-a-state
[normativity-cover]: ../foundations/objective-normativity-and-corrective-cognition.md#84-identification-under-independently-eligible-evidence
[normativity-relations]: ../foundations/objective-normativity-and-corrective-cognition.md#105-relations-and-valid-agreements-can-specify-duties

[source-article]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/221a50045570edb56a62012eff862df258f9af0ae51d74d116ff224e5c5498e7/ARTICLE.md
[source-algebra]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b824c43b4f4fad672bb96e930241787b8d07d36a69d49f20ea9d85d2d51b43d2/EXACT_EFFECT_ALGEBRA.md
[source-oracle]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a282ebf891d26ca2e55fc93bdb73fa3159f60a6388545b930076c17fd73c7571/ORACLE_AND_FORCE_PRECISIONS.md
[source-resources]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6e3c5aee5d3c339d8a58a4087ea78ded5b75c616dc18ffa697732d44c16ccae6/REALISABILITY_AND_RESOURCE_ACCOUNT.md
[source-antecedents]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/66e0a9c2856b28ea2c701dba5c88350b4de6c513ff0922232863b17e2744f69d/PRIOR_ART_DISPOSITION.md
[source-release]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a25c4464f85c4b9a8f920b2e208e35164cf821ef69f352d341b4c86046b434a4/BOUNDED_RELEASE_DECISION.md
[source-premises]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/68d885c2cec1f9551dc9899bac224c17ddb3ebd0f9e2858b7989fea19c12c9dc/PREMISE_AND_ALTERNATIVE_LEDGER.md
[review-checker]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1dff5f73b342b3685837468887215898a1754786cf22127497587c99c3622fb5/INDEPENDENT_REVIEW_v1.md
[review-release]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/61deeb33635687c7206fe0b70bf0160d4ed42ad72200f42ef7214bcc2ecb839c/INDEPENDENT_REVIEW_v1.md

[pitcher]: https://fpl.cs.depaul.edu/cpitcher/research/2005-planx-xml-stream-vpe.pdf
[streaming]: https://madhu.cs.illinois.edu/www07.pdf
[nested-query]: https://madhu.cs.illinois.edu/vpquery.pdf
[maier]: https://semprag.org/index.php/sp/article/view/sp.7.7
[priced]: https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarFGKRS.pdf
[priced-doi]: https://doi.org/10.1006/jcss.2002.1828
[pricing]: https://homes.cs.washington.edu/~magda/papers/koutris-jacm15.pdf
[pricing-doi]: https://doi.org/10.1145/2770870


