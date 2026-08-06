# PMR-007 Frontier Round 12 V1 — structure-preserving modal root bundles

```text
round: FRONTIER_ROUND_12_STRUCTURE_PRESERVING_MODAL_ROOT_BUNDLE
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
current disposition: FROZEN_PENDING_COLD_AUDIT
```

# Part I — exact typed setting

## 1. World-indexed dependence structures

Let `G=(W,E_G)` be a finite connected undirected graph of declared worlds,
models, or versions. At every node `w`, fix a finite structure

```text
M_w = (B_w, Eff_w, Act_w, Dep_w)
```

where:

- `B_w` is the bearer/actualizer domain;
- `Eff_w` is the declared complete effect domain for this formal model;
- `Act_w(b,e)` means bearer `b` actualizes effect `e`;
- `Dep_w(b,c)` means bearer `b` is derivatively dependent on `c` in the
  declared dependence relation.

Define

```text
Universal_w(b)  iff  forall e in Eff_w, Act_w(b,e);
Underived_w(b)  iff  there is no c in B_w with Dep_w(b,c).
```

These are formal predicates relative to the declared domains and relations.
They are not thereby world-true metaphysical predicates.

For every oriented graph edge `r:u->v`, let

```text
phi_r^B   : B_u   -> B_v
phi_r^Eff : Eff_u -> Eff_v
```

be bijections whose reverse-edge maps are their inverses. Call the pair a
**full root-structure transport** when it preserves and reflects both declared
relations:

```text
Act_u(b,e)  iff  Act_v(phi_r^B(b), phi_r^Eff(e));
Dep_u(b,c)  iff  Dep_v(phi_r^B(b), phi_r^B(c)).
```

Thus each edge is an isomorphism of the typed actualization/dependence
structure. This is stronger than shared labels, matching profiles, or an
arbitrary bearer bijection.

# Part II — positive theorem

## 2. Edge invariance

Every full root-structure transport preserves and reflects `Universal` and
`Underived`:

```text
Universal_u(b) iff Universal_v(phi_r^B(b));
Underived_u(b) iff Underived_v(phi_r^B(b)).
```

The first equivalence follows from effect-domain bijectivity plus `Act`
preservation/reflection. The second follows from bearer bijectivity plus `Dep`
preservation/reflection.

## 3. SMRB-1 — a definable singleton root kills root holonomy

Assume that at one anchor node `w0`:

```text
there exists exactly one g0 with Universal_w0(g0);
Underived_w0(g0).
```

Then:

1. every closed-walk holonomy based at `w0` fixes `g0`;
2. there is a unique coherent section `g_w in B_w` extending `g0` through the
   bearer transports;
3. at every node `w`, `g_w` is the unique `Universal_w` bearer;
4. at every node `w`, `Underived_w(g_w)`.

### Proof

A closed-walk composite is an automorphism of `M_w0`. By edge invariance, it
maps the singleton set of `Universal_w0` bearers to itself; therefore it fixes
`g0`. Round 11 MLT-1 then gives a unique coherent section extending `g0`.
Transport along any path preserves and reflects `Universal`, so `g_w` is
universal. If another bearer at `w` were universal, inverse transport to `w0`
would produce a second universal bearer there, contradicting uniqueness.
`Underived` is preserved along the same path. ∎

## 4. Exact gain over a flatness assumption

SMRB-1 does **not** require every holonomy automorphism to be the identity on
the whole bearer fibre. Holonomy may permute non-root bearers. Singleton
structural definability forces only the root coordinate to be fixed.

Therefore the modal-lineage burden is narrowed from:

```text
prove globally flat transport on every represented object
```

to:

```text
prove full structure-preserving transport and actual-node singleton root status;
root path independence then follows inside the declared bundle.
```

This is a conditional mathematical gain. It does not establish either premise.

# Part III — deletion and strongest-reading countermodels

## 5. Delete singleton root status

Let every node have bearers `{0,1}`, one effect actualized by both, and empty
`Dep`. Both bearers are universal and underived. On a triangle, use two
identity transports and one swap. Every edge map is a full structure
isomorphism, but loop holonomy swaps the two roots and fixes neither. No
anchored coherent root section exists.

Thus structural transport without singleton definability does not remove root
holonomy.

## 6. Delete `Act` preservation

At `w0`, let only bearer `0` actualize every effect. At `w1`, let only bearer
`1` do so. Use the identity bearer bijection. It is a bijection but not an
`Act`-isomorphism; transport sends the actual root to a non-root.

Thus carrier bijection, shared naming, or profile similarity does not preserve
the universal-actualizer role.

## 7. Delete `Dep` preservation

Use the same unique universal bearer `0` at both nodes and identity bearer and
effect maps. Let `0` be underived at `w0`, but let `Dep_w1(0,1)` hold. The maps
preserve actualization but not dependence, and underivability is lost.

Thus actualizer-role persistence does not by itself establish underivability
persistence.

## 8. Delete connectedness

The anchor root controls only its connected component. Another component can
contain a different unique root or no root. A global result requires connected
coverage or separately supplied anchors and compatibility data.

## 9. Delete effect-domain completeness

A bearer can be universal over a registered effect subset while failing on an
unregistered effect. Adding the missing effect can destroy singleton root
status without changing the old reduct. `Eff_w` completeness is therefore a
world/source bridge, not a free consequence of the formal theorem.

## 10. Delete numerical-identity semantics

The coherent section may select one counterpart token per node. Even when
unique and structurally invariant, it does not establish that those tokens are
one numerically identical transworld bearer. Numerical identity requires a
separate interpretation of the transport maps.

# Part IV — cross-candidate integration

## 11. Candidate A / reason and provenance transport

Replace `Universal` by a uniquely characterized warranted certificate or
bearer role and replace `Act/Dep` by the complete obligation/dependency
structure. A full source-to-target isomorphism fixes the unique definable role
through a version cycle even when it permutes irrelevant internal records.

Transferred:

```text
path-consistency method;
unique definable-role invariant;
full obligation/dependency preservation requirement.
```

Not transferred:

```text
truth of obligations;
authority;
recipient applicability;
numerical bearer identity;
evidential independence.
```

This is compatible with AR3/AR4 reason/version transport, but it does not create
a new historical theorem identity.

## 12. Candidate B / restoration under revision cycles

A uniquely characterized restorative target or policy is path-independent at
that coordinate under full target/transition/dependency isomorphisms. Non-root
or non-target records may still exhibit holonomy. This sharpens the Round 11
version-cycle control.

Not transferred:

```text
objective target adequacy;
causal efficacy;
actor-local implementability;
stability under non-isomorphic revision;
scalar route-gradient.
```

## 13. Candidate C / modal ascent

Round 10 CUA-1 conditionally supplies an actual-node singleton universal
actualizer from `COMMON+ANCHOR`. SMRB-1 supplies the next conditional step:

```text
actual-node singleton universal underived bearer
+ connected declared modal/version graph
+ full actualization/dependence structure isomorphisms
=> unique coherent section of universal underived bearers.
```

This removes a separate root-flatness premise but leaves every world/source
bridge open:

```text
COMMON and ANCHOR truth;
complete effect and bearer domains;
correct modal domain and accessibility;
full structure-preserving transport;
numerical-identity interpretation;
metaphysical rather than model-relative dependence;
mentality, agency, Creator classification, attributes, Names, revelation.
```

The R5 plural control is excluded only after singleton root status is
independently warranted in the complete declared structure. It remains live
against incomplete domains, non-isomorphic worlds, counterpart-only transport,
and every later attribute bridge.

# Part V — ancestry, evidence use, and disposition

## 14. Theorem-family and prior-art relation

| Object | Relation | Credit consequence |
|---|---|---|
| definability under isomorphism | standard model-theoretic invariance | no general novelty |
| singleton fixed by automorphisms | elementary group-action fact | no general novelty |
| MLT-1 composition | corollary/application of Round 11 | no duplicate origin |
| CUA-1 composition | conditional use of Round 10 | no premise-truth transfer |
| AR3/AR4 application | typed version/lineage specialization | no historical identity |

## 15. Exact evidence-use record

```text
upstream supplied:
  Round 10 CUA-1 singleton-root mechanism;
  Round 11 MLT-1 holonomy-fixed anchor criterion;
  Candidate A obligation/provenance transport distinctions;
  Candidate B target/version-cycle distinctions;
  Candidate C underivability and modal-arrow burden.

transferred:
  formal singleton root premise;
  graph transport method;
  structure-isomorphism guard;
  role and dependency invariants;
  deletion-model obligations.

not transferred:
  source/world truth of COMMON or ANCHOR;
  modal-domain completeness;
  numerical identity;
  metaphysical dependence adequacy;
  mentality or attributes;
  theorem novelty or meniscus credit.

reverse feedback:
  Candidate A must preserve the complete dependency signature, not only a
  visible certificate profile;
  Candidate B can derive target-coordinate path independence from unique
  definability only under revision isomorphism;
  Candidate C no longer needs global flatness on every bearer, but must source
  complete structure-preserving transport and identity semantics.
```

## 16. Updated Candidate-C frontier

```text
C-FRONTIER-6:
independently warrant the complete effect/bearer/dependence structures and the
modal coverage relation; establish that the cross-world maps are full
actualization/dependence isomorphisms and preserve numerical identity rather
than mere counterpart lineage; then test whether those premises are available
without assuming de re necessity or the desired one-Creator conclusion, and
separately bridge the persistent underived actualizer to mentality and the
Divine attributes.
```

## 17. Round disposition

```text
positive object:
  SMRB-1 — definable singleton root fixed by all root holonomy and extended to
  one coherent universal-underived section.

strongest negative objects:
  plural-root holonomy;
  role loss under non-Act-preserving bijection;
  underivability loss under non-Dep-preserving transport;
  disconnected coverage;
  incomplete-effect reduct;
  counterpart/numerical-identity nonimplication.

novelty:
  standard isomorphism and group-action mechanisms with a substantive
  cross-candidate modal/root application; no new general mathematics claimed.

integrated champion:
  NONE.

meniscus:
  MENISCUS_NOT_REACHED.
```
