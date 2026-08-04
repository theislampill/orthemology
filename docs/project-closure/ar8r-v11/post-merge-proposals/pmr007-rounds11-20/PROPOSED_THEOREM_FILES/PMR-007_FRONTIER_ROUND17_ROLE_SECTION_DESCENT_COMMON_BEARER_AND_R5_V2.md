# PMR-007 Frontier Round 17 V2 — role-section descent, common-bearer semantics, and the R5 plural-realization boundary

```text
round: FRONTIER_ROUND_17_ROLE_SECTION_DESCENT_COMMON_BEARER_R5
version: V2
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repair_of: PMR-007 Frontier Round 17 V1
repository mutation: NONE
current disposition: FROZEN_REPAIRED_PENDING_FRESH_REREVIEW
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

# 1. Central Candidate-C question

Rounds 11 and 12 established, at their exact finite bundle scopes:

```text
MLT-1:
an anchor extends to a coherent section exactly when every based holonomy fixes
that anchor;

SMRB-1:
a uniquely definable universal-underived root role is fixed by every
structure-preserving root holonomy and therefore extends to a unique coherent
section of root-role realizers.
```

The present question is not whether a section exists. It is:

```text
What exact mathematical object is obtained when world-indexed root tokens are
transported coherently, and what additional premise would be needed before that
object could be interpreted as one numerically identical bearer rather than one
lineage/counterpart class?
```

This is a load-bearing Candidate-C burden. It also controls Candidate-A
identity/provenance transport and Candidate-B restoration through version
cycles.

# 2. Typed transport bundle

Let `G=(W,E)` be a finite connected undirected graph. For every world/model/
version `w`, let `B_w` be a finite nonempty bearer set. For every oriented edge
`e:u->v`, let

```text
tau_e : B_u -> B_v
```

be a bijection, with reverse-edge transport `tau_(e^-1)=tau_e^-1`. A path
transport is the corresponding composite.

Let `S_w subseteq B_w` be a nonempty **transport-invariant subbundle**:

```text
tau_e[S_u] = S_v
```

for every edge. The root singleton subbundle supplied by SMRB-1 is the principal
application:

```text
S_w = {g_w}.
```

Form the disjoint tagged union

```text
S* = disjoint_union_w ({w} x S_w).
```

This tagging prevents world-indexed tokens from becoming numerically identical
by notation alone.

# 3. Transport-generated descent relation

Let `~_tau` be the least equivalence relation on `S*` containing every edge
transport pair:

```text
(u,s) ~_tau (v,tau_e(s)).
```

Call an equivalence relation `I` on `S*` an **admissible cross-fibre descent
relation** when:

```text
D1. every edge transport pair is I-related;
D2. every I-class meets every fibre {w} x S_w in at most one element.
```

`D2` is the formal no-collapse guard. Without it, two distinct tokens inside one
world could be called one bearer merely because a transport cycle identified
them.

## Theorem RSD-1 — holonomy criterion for cross-fibre descent

For the connected transport-invariant subbundle `S`, the following are
equivalent:

```text
A. an admissible cross-fibre descent relation I exists;

B. every closed-walk holonomy at every base world fixes every element of S_w;

C. the generated relation ~_tau has no class containing two distinct elements
   from the same fibre.
```

When these conditions hold:

```text
1. I is unique and equals ~_tau;
2. every I-class meets every world fibre in exactly one element;
3. the canonical reduced quotient U_S = S*/~_tau, together with

       j_w : S_w -> U_S,
       j_w(s) = [(w,s)],

   gives injective maps satisfying

       j_v(tau_e(s)) = j_u(s)

   on every edge;
4. among reduced realizations—those satisfying U = union_w j_w[S_w]—this
   quotient realization is unique up to the unique bijection commuting with
   all j_w. Arbitrary codomains with unused elements receive no uniqueness
   claim.
```

### Proof

`A => C`: any equivalence relation satisfying `D1` contains the equivalence
closure `~_tau`. If a `~_tau`-class contained two distinct elements of one
fibre, the containing `I`-class would violate `D2`.

`C => B`: a closed walk based at `w` relates `(w,s)` to
`(w,tau_p(s))`. By `C`, the two same-fibre elements must be equal.

`B => C`: if `(w,s) ~_tau (w,t)` then a finite zig-zag of edge transports and
inverses composes to a closed walk taking `s` to `t`; `B` gives `s=t`.

Under `B`, any path from `u` to `v` maps each `s in S_u` to the same `S_v`
element, since two paths differ by a closed walk. Hence each orbit meets every
connected fibre exactly once. The generated relation is admissible.

For uniqueness, every admissible `I` contains `~_tau`. Each `~_tau` orbit
already meets every world exactly once. Merging two distinct orbits would place
two elements of each world fibre into one `I`-class, contradicting `D2`.
Therefore `I=~_tau`. The quotient construction follows. For reduced-realization uniqueness, let
`(U,j_w)` be any reduced realization satisfying the edge commutation law. Send
`[(w,s)]` to `j_w(s)`. Path independence makes this well defined; injectivity
and fibrewise coverage make it bijective; reducedness leaves no unused elements
on which an additional automorphism could act. The commuting bijection is
therefore unique. ∎

## Corollary RSD-2 — root-role descent without full bearer flatness

Under SMRB-1, take `S_w={g_w}`. Every root holonomy fixes the singleton, so the
root subbundle has one unique descent class:

```text
U_root = {[(w,g_w)] : w in W}
```

with exactly one representative in each world.

This can hold while the full bearer bundle `B` is nonflat and has no admissible
full-bearer descent. A holonomy may fix `g_w` while permuting nonroot bearers.
Therefore:

```text
one coherent root lineage class
!=
path-independent identity for the whole bearer structure.
```

## Corollary RSD-3 — full bearer descent iff full holonomy is flat

Take `S_w=B_w`. An admissible descent relation on all bearers exists exactly
when every holonomy automorphism is the identity on the whole bearer fibre.
Equivalently, the entire bundle descends to one common bearer set through
commuting fibre bijections exactly under full flatness.

SMRB-1 proves only the root-coordinate condition, not full flatness.

# 4. Numerical-identity firewall

`RSD-1` constructs a quotient and a unique transport orbit. It does not decide
what the quotient means metaphysically.

Introduce an explicit semantic bridge:

```text
B_ID:
for root tokens, membership in the same admissible transport-descent class is
sufficient and necessary for numerical transworld identity.
```

Then, and only then, the unique root descent class may be read as one
numerically identical bearer across the declared worlds.

Without `B_ID`, a standard counterpart model satisfies every formal premise:

```text
world w0 contains token g0;
world w1 contains distinct token g1;
tau(g0)=g1;
{g0,g1} is one transport orbit;
g0 != g1 in the disjoint token domain.
```

Thus:

```text
coherent section
=> unique transport lineage/orbit;

coherent section
not=> numerical identity;

coherent section + independently warranted B_ID
=> one bearer relative to that identity semantics.
```

`B_ID` is not supplied by graph theory, model-theoretic definability, formal
isomorphism, source translation, or repository implementation.

# 5. Exact source finding and authority ceiling

The translated-primary Asfahani commentary supplies two directly relevant
source constraints.

## 5.1 Attribute-locus constraint

The commentary argues that an attribute belongs to the locus in which it
subsists; producing or locating speech in another entity does not make that
speech an attribute of the proposed bearer. The same passage generalizes the
point to knowledge, ability, hearing, sight, life, and action-derived names.

At the present authority this supports only the source-relative guard:

```text
role or attribute availability elsewhere
!=
attribute co-instantiation in the root/originator bearer.
```

It does not supply the formal transport theorem, Arabic-primary verification,
or a world-level metaphysical proof.

## 5.2 Intra-world unity-proof constraint

The commentary explicitly criticizes as fallacious a particular **intra-world**
argument that two necessary beings must be composed from what they share and
what distinguishes them. It emphasizes that common abstract necessity exists in
the mind and does not by itself identify or compose individuated externals.

At its exact authority this is a source-relative anti-shortcut against:

```text
shared abstract necessity + individuation
=> composition and unity.
```

Its relation to the transworld transport theorem is only `PARTIAL_OVERLAP`: it
supports the general warning that a shared abstract predicate is not bearer
identity, but it says nothing directly about Kripke counterpart semantics,
graph holonomy, or cross-world numerical identity. The formal theorem is proved
independently.

```text
source artifact:
A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md

SHA-256:
932abd7e2d7b3702d5d6d77d2a4a95ecfb3a9ccbcfbbce7ae750b2bcf55bef7c

authority:
TRANSLATED_PRIMARY_TEXT_ACCESS
NOT_ARABIC_PRIMARY_VERIFICATION
```

# 6. R5 common-model integration

Combine the Round-12 root structure with PMR-M3-01 and PMR-M5-02.

For each of two worlds `wi`, use bearers:

```text
ui       unique universal underived originator/root;
wi_role  bearer of W;
pi_role  bearer of P;
ki_role  bearer of K.
```

Let `ui` actualize the complete registered effect domain. Let the three role
bearers be pairwise distinct, globally present, and coordinated. Transport all
four role positions structure-preservingly between the worlds.

In each world:

```text
unique universal underived root: true;
necessary and external root: true;
G_global: true;
G_plural: true;
G_coord: true;
G_originator_WPK: false;
Creator classification: false.
```

The root tokens form one coherent root descent class. The W/P/K roles also
transport coherently as three distinct classes. Yet the root does not bear any
of W/P/K, so the PMR-M3 `B_creator` antecedent does not fire.

## Result R5-RSD-1

The union of:

```text
unique universal underived root in every world;
full structure-preserving root transport;
root holonomy fixation and one root descent class;
necessary and external originator status;
global W/P/K availability;
pairwise-distinct plural W/P/K realization;
coordinated W/P/K realization;
```

does not entail:

```text
originator co-instantiation of W/P/K;
scoped Creator classification;
one numerically identical root bearer;
mentality, Wisdom, Life, Speech, Names, or revelational identification.
```

This is one common model, not several unrelated guard deletions. It therefore
closes a serious overstrong Candidate-C route:

```text
modal role coherence + plural coordinated attributes
not=> common-bearer Creatorhood.
```

The model is a formal rival control. It is not asserted to be source-theologically
or metaphysically adequate.

# 7. Strongest supportable positive bridge candidate

The dependency-minimal positive program now has the following arrows:

```text
P1. actual-world singleton universal underived root;
P2. connected declared modal domain;
P3. full actualization/dependence structure isomorphisms;

P1 + P2 + P3
=> unique coherent root section                    [SMRB-1]
=> one canonical root transport-descent class      [RSD-2]

P4. independently warranted B_ID semantics;

P1 + P2 + P3 + P4
=> one numerically identical root bearer
   relative to the declared modal/identity model.

P5. root-local co-instantiation of W/P/K in every relevant world;
P6. independently warranted Creator-classification bridge;

P1...P6
=> one Creator-classified bearer across the declared worlds,
   relative to P2-P6.
```

No earlier arrow supplies a later premise. In particular:

```text
root-role uniqueness does not supply B_ID;
B_ID does not supply W/P/K;
W/P/K availability does not supply root co-instantiation;
co-instantiation does not supply source truth or the Creator bridge;
formal Creator classification does not supply revelational identification.
```

# 8. Deletion and strongest-reading controls

## 8.1 Delete holonomy fixation

Use a triangle whose root candidates are `{g,h}` and whose loop swaps them. No
admissible root descent relation exists because one generated class contains
`(w,g)` and `(w,h)` in the same fibre.

## 8.2 Delete the no-collapse guard D2

The equivalence closure of a nontrivial holonomy still exists, but it identifies
distinct same-world bearers. Calling that quotient numerical identity would
launder the very individuation problem under review.

## 8.3 Delete B_ID

The tagged-token counterpart model has one root transport orbit and two distinct
world-indexed tokens. Lineage is coherent; numerical identity is withheld.

## 8.4 Delete root-local W/P/K co-instantiation

The R5 common model preserves global, plural, coordinated, and transported W/P/K
while withholding every role from the root bearer.

## 8.5 Delete the Creator-classification bridge

Even a root bearing W/P/K does not acquire the formal `Creator` predicate unless
the declared bridge is supplied. This is a formal-language control, not a claim
about the true source or metaphysics.

## 8.6 Delete source/world adequacy

Every theorem above remains model-relative. Incorrect effect domains,
accessibility relations, dependence predicates, transports, translations, or
attribute predicates can make a formally valid result irrelevant to the world.

# 9. Cross-candidate attacks

## Candidate A

The descent theorem supplies an exact provenance/identity criterion:

```text
transport edges generate a lineage class;
no same-context collision is equivalent to path-independent identity at the
registered subbundle.
```

Not transferred:

```text
independent acquisition;
warrant;
source truth;
authorization;
evidential rank;
numerical bearer identity.
```

A copied reason or certificate may occupy one descent class without creating a
new evidence root.

## Candidate B

A uniquely preserved restorative target may descend through version cycles
while nonroot policy or burden coordinates retain holonomy. Therefore:

```text
root/target-coordinate stability
not=> whole-state restoration.
```

This supplies a structural dynamic-bypass warning complementary to Round 15.

## Candidate C

The exact current frontier is no longer “find a coherent root section.” It is:

```text
independently justify the modal structure and transport;
decide whether root descent has numerical-identity semantics;
justify bearer-local attribute co-instantiation;
justify the Creator/source/world bridges;
then separately address unity, mentality, Life, Wisdom, Speech, Names, and
revelational identification.
```

# 10. Theorem-family and prior-art disposition

| Object | Family relation | Credit consequence |
|---|---|---|
| `RSD-1` | standard groupoid-orbit/descent and holonomy criterion | zero general mathematical novelty |
| root application | corollary/strengthened interpretation of MLT-1 and SMRB-1 | no duplicate origin |
| full-flatness corollary | standard bundle trivialization criterion | zero general novelty |
| tagged-token nonidentity model | standard counterpart/quotient separation | control only |
| `R5-RSD-1` | fresh post-merge cross-lane common-model integration of SMRB/M3/M5/R5 | scoped research contribution; no historical identity |
| source finding | translated-primary constraint on locus and a criticized unity proof | source-relative only |

No theorem, source, or novelty credit is imported from the CDC prompt or from
external mathematics by analogy.

# 11. Executable verification

The repaired primary checker independently compared:

```text
full holonomy flatness;
transport-generated equivalence classes;
no same-fibre collision;
root-only descent under root-fixing transports;
and the two-world R5 common model.
```

Declared exhaustive classes:

```text
979 connected labelled bundles:
  worlds 1-4;
  fibre size 1-3;
  all connected simple graphs for the declared pairs;
  all edge permutations in those classes.
```

Additional random controls:

```text
24,000 connected four- and five-world bundles with three-element fibres.
```

Results:

```text
flatness/descent mismatches: 0;
root-descent failures in root-fixed cases: 0;
root-fixed but full-nonflat bundles found: 4;
R5 necessary/external guards: exact PASS;
full bearer/effect bijectivity and Act/Dep isomorphism: exact PASS;
R5 common-model guards: exact PASS;
overall: PASS.
```

The checker is finite evidence for the declared classes. It is not the proof,
external review, or metaphysical validation.

# 12. Blocking repairs from the V1 cold audit

```text
R17-F01:
closed by restricting uniqueness to reduced realizations whose codomain is
exactly the union of the fibre images.

R17-F02:
closed by mechanically checking and reporting necessary/external root status.

R17-F03:
closed by adding effect transport and explicit Act/Dep relations, then checking
bearer/effect bijectivity plus preservation and reflection.

R17-F04:
closed by restricting the translated-primary unity finding to an intra-world
anti-shortcut and classifying its transworld relation as PARTIAL_OVERLAP.
```

V1 remains preserved as an unadmitted research candidate.

# 13. Authority and current disposition

```text
RSD-1:
FROZEN_REPAIRED_POST_MERGE_CANDIDATE_PENDING_FRESH_REREVIEW

RSD-2 / RSD-3:
FROZEN_REPAIRED_POST_MERGE_COROLLARIES_PENDING_FRESH_REREVIEW

R5-RSD-1:
FROZEN_REPAIRED_POST_MERGE_COMMON_MODEL_PENDING_FRESH_REREVIEW

source finding:
TRANSLATED_PRIMARY_TEXT_ACCESS
SOURCE_RELATIVE_CONSTRAINT

historical identity:
NONE

general mathematical novelty:
0

external review:
OPEN

owner adoption:
PENDING

integrated champion:
NONE

meniscus:
MENISCUS_NOT_REACHED

natural closure:
NOT_REACHED
```
