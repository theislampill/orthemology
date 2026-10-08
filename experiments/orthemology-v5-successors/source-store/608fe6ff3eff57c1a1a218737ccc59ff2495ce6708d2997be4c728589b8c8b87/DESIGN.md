# One shared finite interpretation: design awaiting implementation approval

Date: 7 October 2026. Status: **PROPOSED; NOT IMPLEMENTED; NOT KERNEL CHECKED**.
This document specifies a concrete interpretation, not a new general theorem or
a conjunction of unrelated existential witnesses. The companion
`MAPPING_AND_COMPATIBILITY.md` is the exact interface and acceptance contract.

## 1. Scope and frozen inputs

Use the reviewed definitions and theorem bodies unchanged:

| Component | Binding | Core source SHA-256 |
|---|---|---|
| Original-bearer A and retained B/C | `../original-bearer-bridge/MANIFEST.json`: `ac92a3ff320ee3c754e8e0e9b9b37fb2460aab56336614f9a8be81d61d27304e` | `OriginalBearerBridge.lean`: `086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99` |
| Approved narrow inherited import derivative | Owned by the preceding packet; only its first import line differs from the historical source | `SourceIdentityDerived.lean`: `51b8a964e5854cd383afd5a862554126d4f8ebcf4a301e435ef795ac2c5cbb54` |
| Anchored field account | `../anchored-source-bridge/SOURCE_MANIFEST.json`: `305ab6251e9f28b45894c4f5f5270a88de7a10020b87d929b4173577eb9b3de7` | `src/AnchoredSourceBridge.lean`: `2a3c7de1e7a9028345bae3d059d7cc6398f4067326e10db915d8d89b55fcb3d1` |
| Source-owned veracity | `../veracity-boundary/SHA256SUMS`: `161989fec72e5cc231547378db4c7890f8b4e49e6fe77f220a81d97904eed1b2` | `src/VeracityBoundary.lean`: `b199d8d367d296e34582aa7241a34db0fe5bcd5aaf70d57b8008e4adf506043f` |

The independent reviews report no blocking scientific findings. Read:
`../original-bearer-independent-review/REVIEW.md`,
`../anchored-source-independent-review/REVIEW.md`, and
`../veracity-independent-review/REVIEW_REPORT.md`.
Veracity's paragraph-numbering explanation has a separate documentation erratum;
it needs no source edit or scientific replay. The owner objective is
`../../owner-instructions/Pasted text(20261007-075932).txt`; the selected target is
`../root-analysis/JOINT_NONVACUITY_TARGET.md`.

## 2. Carrier types and finite-table convention

Every displayed carrier is a separate finite inductive type except the explicit
equalities below. Every tuple not listed is **false**. Repeated table values are
chosen interpretations, not definitions identifying distinct interface fields.
No primitive calls `Complete`, `GlobalCoverage`, `Necessary`, `Veracity`, or any
target conclusion to decide its truth.

| Carrier | Values and intended role |
|---|---|
| `W` | `w0, w1, w2`; actual, another received-existence alternative, complete-absence alternative for creatures |
| `B` | `g, h, x, l, r, m, z`; two originals, received agent, and four received effect bearers |
| `R` | `rg, rh, rx, rl, rr, rm, rz`; concrete intrinsic resource tokens, distinct from bearers and contribution tokens |
| `E` | `a, b, k, o`; left production, right production, mixed production, outside production |
| `C` | `cx, cl, cr, cm, cz`; concrete productive contribution/respect tokens |
| `Token` | `u, v`; g's report and x's report |
| `Content` | `present, absent`; contextual claims that l exists / l does not exist |
| `Exercise` | `sayG, sayX, provideA, provideB, provideK, provideO, actX` |

Literal type identifications: original-bearer target `T = B`; anchored source
`S = B`; veracity source `Source = B`; veracity occasion `Occasion = W`.
There are no copied source enums and no transport between different values
called g. Put `L = {w0,w1}` and `D = {x,l,r,m,z}` only as table abbreviations.

The third world is deliberate: x both survives as received in another world
and is wholly absent in a further world. Constitutive reception therefore has
a live cross-world instance; contingency is not merely change of a token act.
These worlds are an interpreted finite domain, not certified possible worlds.

## 3. Complete A/B/C primitive interpretation

Instantiate `OriginalBearerBridge.Framework W B R B` as follows.

| Primitive | Exact interpretation |
|---|---|
| `actual` | `w0` |
| `existsAt` | `{(w,g),(w,h) : w in W} union (L × D)` |
| `wholeReceived` | `L × D` |
| `dep` | `{(w,g,x),(w,g,l),(w,g,r),(w,g,m),(w,h,z) : w in L}` |
| `resourceActual` | every member of R |
| `resourceReceived` | `{rx,rl,rr,rm,rz}` |
| `intrinsic` | `{(g,rg),(h,rh),(x,rx),(l,rl),(r,rr),(m,rm),(z,rz)}` |
| `targetReceived` | `D` |
| `relevant` | `{(rg,x),(rg,l),(rg,r),(rg,m),(rh,z),(rx,m),(rl,m),(rr,m)}` |

`dep` represents the broad existential-reception predicate in this finite
ontology; it is not declared to exhaust efficient causation or all kinds of
grounding. Its supplier is the original existential provider in these tables.
The separate direct-support relation below includes genuine proximal agency.
No bearer-to-own-intrinsic-resource efficient edge is introduced.

Canonical A witness: **target x, resource rg, bearer g**. Relevant received
resources of m do not supply its original-completion witness. For target x the
only relevant resource is rg, and rg's only intrinsic bearer is g. Thus applying
the component theorem at x cannot silently select h. Separately h/rh witnesses
original completion of the outside effect z.

Support transport has true antecedents, for example `(x,rx)` at w0. Both need
and reception have true antecedents for x and all four effects. Representation
has both received and nonreceived cases at every world. g and h exist in every
world and receive in none; no uniqueness of original or necessary reality is
assumed or true in this structure.

## 4. Complete anchored-account primitive interpretation

Instantiate `AnchoredSourceBridge.Account B E C`.

| Primitive | Exact interpretation |
|---|---|
| `Field` | `{a,b,k}` |
| `ActualOccurrence` | `{a,b,k,o}` |
| `Req` | `{(a,cx),(a,cl),(b,cr),(k,cx),(k,cl),(k,cr),(k,cm),(o,cz)}` |
| `Operative` | the same eight tuples, independently specified |
| `EntireOrig` | `{(g,cx),(g,cl),(g,cr),(g,cm),(h,cz)}` |
| `ActualOriginal` | `{(g,a),(g,b),(g,k),(h,o)}` |
| `ModeRole` | the same four tuples, independently specified |
| `Qualified` | `{g}` |
| `ModeDefect` | empty |

Anchor is `(g,a)`. The nontrivial connection is `a -- k -- b`, witnessed by cl
and cr (cx additionally witnesses a--k). There is no a--b overlap. k is a real
third occurrence with its own new contribution cm, not an artificial union
declared actual by notation. The prior concrete contributions remain its
history-inclusive requisites; cm is not identified with cl or cr.

C does not contain provider identities. The `EntireOrig` relation remains the
component's unrestricted relation, even though this particular table satisfies
both field CND and the stronger global CND. Select only **FieldCND** in the
principal theorem. Do not infer general CND from this table.

## 5. Explicit productive and resource links

These supplementary tables make the shared interpretation inspectable. They do
not alter the component signatures or create new universal bridge axioms.

| Relation or function | Exact interpretation |
|---|---|
| `ProducedAt : B -> E -> Prop` | `{(x,a),(l,a),(r,b),(m,k),(z,o)}` |
| `OccursAt : W -> E -> Prop` | `L × E` |
| `ContributionBearer : C -> B` | `cx↦x, cl↦l, cr↦r, cm↦m, cz↦z` |
| `ContributionResource : C -> R` | `cx↦rx, cl↦rl, cr↦rr, cm↦rm, cz↦rz` |
| `OriginalResourceUsed : R -> C -> Prop` | `{(rg,cx),(rg,cl),(rg,cr),(rg,cm),(rh,cz)}` |
| `DirectSupport : B -> B -> Prop` | `{(g,x),(g,l),(g,r),(x,m),(l,m),(r,m),(h,z)}` |
| `SupportAncestor : B -> B -> Prop` | `{(g,x),(g,l),(g,r),(g,m),(x,m),(l,m),(r,m),(h,z)}` |
| `DerivedAct : B -> E -> Prop` | `{(x,k)}` |
| `DerivedUses : B -> E -> C -> Prop` | `{(x,k,cx),(x,k,cl),(x,k,cr)}` |
| `MediateUse : E -> E -> C -> Prop` | `{(a,k,cx),(a,k,cl),(b,k,cr)}` |
| `TokenOccurrence : Token -> E` | `u↦b, v↦k` |
| `TokenBearer : Token -> B` | `u↦r, v↦m` |
| `ModeExercise : E -> Exercise` | `a↦provideA, b↦provideB, k↦provideK, o↦provideO` |
| `ProductivelySupportsToken : B -> Token -> Prop` | `{(g,u),(g,v)}` |
| `Authenticated : Token -> Prop` | empty |

`DirectSupport` records actual productive use, not only temporal precedence.
`SupportAncestor` is independently listed; verify that it is exactly the
positive-length reachability relation of DirectSupport, before any coverage
theorem is applied.
The intended reading of cx includes x's received productive capacity rx;
its original provision by g does not make rx intrinsic to g. The resource rg
is intrinsic to g and relevant to x; its use at cx ties the A witness to the
actual field anchor. The finite local equalities and incidence facts in the
companion contract must be checked, rather than assumed as prose alone.

h has an actual received effect z at o and a real resource rh. h has no direct
support edge, entire-original contribution, mode role, or actual-original use
inside the selected field or its incoming support domain. No contribution of
h is hidden to force g's uniqueness. Adjoining o enlarges the field, breaks
connectedness from a and g's coverage, and requires a new application.

## 6. Complete veracity primitive interpretation

Instantiate `VeracityBoundary.Model B W Token Content Exercise`.

| Primitive | Exact interpretation |
|---|---|
| `asserts` | `{(w,g,u,present),(w,x,v,absent) : w in L}` |
| `trueAt` | `{(w0,present),(w1,present),(w2,absent)}` |
| `knowsFalse` | `{(w0,g,absent),(w1,g,absent),(w2,g,present),(w0,x,absent),(w1,x,absent)}` |
| `aware` | the same four tuples as `asserts`, independently specified |
| `deliberate` | `{(w,g,u),(w,x,v) : w in L}` |
| `exercise` | `u↦sayG, v↦sayX` |
| `actual` | `{(w,g,sayG),(w,g,provideA),(w,g,provideB),(w,g,provideK),(w,h,provideO),(w,x,sayX),(w,x,actX) : w in L}` |
| `fitting` | all preceding actual tuples except `(w,x,sayX)`, for w in L |
| `shortcoming` | `{(w,x,sayX) : w in L}` |

The same literal g has full `Package` and `Factive`; the same x is a received
contingent bearer, genuine productive agent, and false assertion owner. x has
K/A/C/D/N/ExerciseBridge/Factive but fails P. D and N have live x-side instances.
g knows that `absent` is false at w0 without asserting it. Knowledge here is
only the displayed negative-truth fragment, not a full omniscience model.

The speech token u is true, v is false, and g productively supports both.
Actual source provision `provideK` is fitting for g while x's own exercise
`sayX` is a shortcoming and unfitting. Those are different source/exercise
pairs, not a transfer of x's defect or assertion to g. `actX` records a genuine
created productive exercise separately from the assertoric defect.

## 7. Necessary vacuity disclosure

The model has substantive existence, received resources, live transport,
cross-world receipt, mixed production, proper source roles, extra nonspeech
fitting exercises, knowledge of false content, and two real assertions.
Nevertheless, under the good-g package:

- no in-field incomplete qualified g-role can trigger Classification(g);
- no false g-owned assertion can trigger K(g)'s false-content branch;
- no g-owned counterfeit can trigger D(g);
- this chosen model gives g no shortcoming, so N(g)'s antecedent is empty.

Trying to make the first three antecedents true while retaining all selected
premises would contradict the component conclusions. We will not manufacture
such witnesses. Their discriminating role is documented by the already reviewed
component removal controls. Live x-side D/N and g's extra actual conformance
show that the underlying predicates have real content without changing source.
The full joint instance is a consistency test, not a fresh minimality proof.

## 8. Optional independent strict-ancestry compatibility

If included, use the already specified actual relation `SupportAncestor` on B,
whose equality to positive-length direct-support reachability is checked
independently of any coverage conclusion. Selected domain
`{g,x,l,r,m}` is predecessor-closed and excludes h and z.

Finite inspection should show strictness, transitivity, nontrivial edges,
connectedness of the selected domain, and `Below(g,y)` for every selected y.
Thus the exact LocalCover formula holds there, including at g by reflexivity
of Below; no self-production edge occurs. Each listed requisite and its
contribution bearer lies in the represented support cone of its effect, and
no incoming h-branch is omitted. Keep this a separate finite compatibility
certificate. It is **not** a theorem that every incidence account yields this
ancestry, that the source-mode assumptions imply strict ancestry, or that the
open general Sixth-refinement obligation has been discharged.

## 9. Approval gate and stopping condition

No Lean file, executable checker, build, download, or source modification was
performed to produce this design. Implementation may begin only after root
approves this design. Use a new isolated output directory and the already
available official Lean 4.19.0 toolchain; import exactly the reviewed cores and
the approved inherited derivative. Do not import component fixture enums or
replay the broad earlier suite.

The proposed implementation stops after: the table interpretation and exact
same-witness checks pass; the existing theorem calls are read back; import and
source identities remain bound; the narrow overclaims in the companion fail
for their intended reasons; a fresh independent review finds no blocking defect.
Until then the model is proposed, not verified. Success would establish only
relative consistency/nonvacuity of this **selected formal signature**. It would
not establish metaphysical possibility, actual existence, eligibility of the
interpreted predicates, all unformalised source doctrines, or revelation.
