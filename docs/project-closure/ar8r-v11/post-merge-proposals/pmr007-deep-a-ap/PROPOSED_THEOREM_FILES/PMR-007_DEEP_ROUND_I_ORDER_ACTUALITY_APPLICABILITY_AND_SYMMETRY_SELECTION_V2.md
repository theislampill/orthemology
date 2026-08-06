# PMR-007 Deep Round I — order–actuality applicability and neutral realizer selection under symmetry

```text
identity: PMR-007-OAS-1
round: PMR-007-DEEP-I
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
central bridge: NECESSARY_ORDER_TO_CONCRETE_ACTUALITY_TO_PARTICULAR_BEARER_TO_UNITY
repository mutation: NONE
```

## 1. Inherited authority ceiling

The frozen transcendental result establishes only a process-relative underived modal-determinate order under its constitutive and anti-circularity guards. It does not establish that the order has a concrete application, is efficacious, has one particular bearer, or selects a personal realizer. Deep C and Deep H preserve an integrated impersonal order/actualizer rival and realization-label parity.

This round treats four different questions:

```text
A. Does the order apply to any concrete candidate?
B. Does an application site efficaciously realize it?
C. Does the declared neutral structure select one realizer?
D. Is the selected realizer metaphysically unique, personal, or divine?
```

Only C receives a positive mathematical characterization here.

## 2. Typed finite model

Let

\[
\mathcal M=(O,X,Applies,Actualizes,\Sigma)
\]

be a finite many-sorted structure with nonempty sorts `O` and `X`. Fix `o∈O`. Define:

\[
A_o=\{x\in X:Applies(o,x)\},
\qquad
C_o=\{x\in X:Applies(o,x)\land Actualizes(o,x)\}.
\]

`A_o` is the applicability fibre; `C_o` is the effective-realizer fibre. Because both relations belong to the signature, both fibres are invariant under every automorphism fixing `o`.

Let

\[
\Gamma_o=Aut(\mathcal M,o)
\]

act on `C_o`. A **neutral invariant output** is an element `x∈C_o` such that `γx=x` for every `γ∈Γ_o`.

A selector over the isomorphism class of `(M,o)` is equivariant when any isomorphism `h:(M,o)→(M',o')` transports the selected element:

\[
s(M',o')=h(s(M,o)).
\]

## 3. OAS-1A — two independent bridge nonentailments

### Order does not entail applicability

\[
Necessary(o)\land Underived(o)
\not\models
\exists x\,Applies(o,x).
\]

A model with `X={d}` and empty `Applies` is a standard nonempty-sort countermodel.

### Applicability does not entail efficacy

\[
\exists x\,Applies(o,x)
\not\models
\exists x\,[Applies(o,x)\land Actualizes(o,x)].
\]

A model may contain a concrete candidate to which the order is descriptively applicable while no candidate realizes or enforces it.

These are model-theoretic bridge failures, not claims that actuality or exemplification is impossible.

## 4. OAS-1B — exact automorphism-fixed-point characterization

### Theorem

For a fixed finite structure `(M,o)`, the following are equivalent:

1. `C_o` has a neutral invariant output;
2. `C_o` contains a point fixed by every member of `Γ_o`;
3. there exists an isomorphism-equivariant selector on the isomorphism class of `(M,o)`.

### Proof

`1↔2` is definitional. For `2→3`, choose a globally fixed `x∈C_o`. For any isomorphic copy `(M',o')` and any isomorphism `h:(M,o)→(M',o')`, define `s(M',o')=h(x)`. If `h'` is another such isomorphism, then `h^{-1}h'` is an automorphism of `(M,o)` and fixes `x`, so `h(x)=h'(x)`. The definition is therefore well-defined and equivariant. For `3→2`, apply equivariance to every automorphism of `(M,o)`; the selected element must be globally fixed. QED.

### Fixed-point-free and transitive corollaries

If `Γ_o` has no fixed point in `C_o`, no neutral equivariant selection exists. In particular, if `Γ_o` acts transitively on `C_o` and `|C_o|>1`, selection is impossible from the declared neutral structure.

### Unique fixed point

If `C_o` contains exactly one global fixed point, it is the unique neutral invariant output for the frozen isomorphism class. This does **not** by itself provide one bounded first-order formula uniform over every model class; a broader class-level selector requires a rule for each isomorphism class or an independently defined invariant predicate.

## 5. Metaphysical firewall

The theorem concerns what the declared neutral structure can invariantly select. It does not prove that reality contains several realizers or lacks a numerically unique one. A hidden haecceity, additional causal structure, source predicate, or inaccessible fact may break the symmetry. The result is instead a burden theorem:

> Any neutral argument for one particular realizer must exhibit independently warranted symmetry-breaking structure that survives the relevant automorphisms.

Merely naming one candidate, placing all roles in one carrier record, or stipulating one privileged index does not meet that burden.

## 6. Countermodels and positive witness

### I-CM1 — necessary underived order, no application

`O={o}`, `X={d}`, `Necessary(o)`, `Underived(o)`, and `A_o=C_o=∅`.

### I-CM2 — application without efficacy

`O={o}`, `X={x}`, `Applies(o,x)`, but not `Actualizes(o,x)`.

### I-CM3 — symmetric plural actualizers

`C_o={x0,x1}` and the swap is an automorphism. Concrete realization exists; neutral unique selection fails.

### I-CM4 — powers field with equivalent loci

Three concrete loci form one orbit under the declared structure. A concrete powers ontology can coordinate order and efficacy without one neutral-selected bearer.

### I-CM5 — primitive symmetric coupling

Two realizers are coupled to the same order by the same cross-domain law. Genuine coordination exists, but numerical unity does not follow.

### I-CM6 — source-conditioned asymmetry

An authenticated source predicate names `x0`. In the expanded Track-N signature the symmetry is broken; in the neutral signature it remains. This is conditional source identification, not neutral entailment.

### I-CM7 — idle haecceity

A primitive tag singles out `x0` while changing no causal, semantic, normative, or counterfactual relation. Selection without explanatory unification is possible.

### I-PW1 — non-idle invariant rank

`C_o={u,y0,y1}`; `u` has a uniquely minimal independently declared realization rank, while `y0,y1` are exchanged. The rank selects `u`. Whether the rank is metaphysically and epistemically warranted remains a separate burden.

## 7. Central bridge and rival effects

```text
necessary/underived order -> applicability:
NOT ENTAILED

applicability -> efficacy:
NOT ENTAILED

effective realization -> one neutral-selected realizer:
IFF A GLOBAL FIXED POINT EXISTS IN THE DECLARED STRUCTURE

fixed point -> metaphysical numerical uniqueness:
NOT ENTAILED

fixed point -> personal/intellectual/divine realizer:
NOT ENTAILED

strongest R5 rival:
ABSTRACT ORDER + SYMMETRIC OR PLURAL POWERS/ACTUALIZER FIBRE SURVIVES
```

Candidate G gains an exact symmetry-breaking condition but no personal-realizer bridge. Candidate E contributes only if its norm source creates an independently defended non-idle asymmetry. Track N can select conditionally through source predication while remaining nonmigratory.

## 8. Theorem family and novelty

This is a direct application of standard group-action, automorphism-invariance, and isomorphism-equivariance facts. General mathematical novelty is zero. The central contribution is the typed location of the selection burden between abstract order, concrete applicability, efficacy, particularity, and unity.
