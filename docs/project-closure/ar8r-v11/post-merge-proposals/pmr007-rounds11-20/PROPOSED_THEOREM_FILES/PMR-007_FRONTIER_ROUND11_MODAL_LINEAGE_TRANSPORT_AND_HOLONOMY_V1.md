# PMR-007 Frontier Round 11 V1 — modal lineage transport, holonomy, and de re necessity

```text
round: FRONTIER_ROUND_11_MODAL_IDENTITY_TRANSPORT
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
current disposition: FROZEN_PENDING_COLD_AUDIT
```

# Part I — quantifier-order firewall

## 1. World-local uniqueness is not one necessary bearer

Let `W` be a finite set of accessible worlds and let `U(w,x)` mean that `x` is
the unique universal actualizer in world `w` under the declared model.

The modal/dependency claim

```text
for every world w, there exists exactly one x with U(w,x)
```

has quantifier order

```text
forall w exists unique x.
```

It does not entail

```text
exists unique x forall w U(w,x).
```

### Countermodel MLT-CM1

At `w0`, only `a` satisfies `U`; at `w1`, only `b` satisfies `U`, with `a!=b`.
Every world has exactly one universal actualizer, but no one bearer is universal
in both worlds.

Thus CUA-1, even if established separately at every world, gives **de dicto
world-local uniqueness**, not de re necessary numerical identity.

# Part II — a coherent-lineage bridge

## 2. World graph and actualizer fibres

Let `G=(W,E)` be a finite connected undirected world/accessibility graph. Each
world `w` has a nonempty finite fibre `F_w` of candidate universal actualizers.
For every oriented edge `e:u->v`, let

```text
tau_e : F_u -> F_v
```

be a bijection, with `tau_reverse(e)=tau_e^{-1}`. The maps may represent a
counterpart, lineage, source-identity, or version-transport proposal. Their
metaphysical meaning is not defined by the mathematics.

A coherent section is a choice `s(w) in F_w` satisfying

```text
s(v)=tau_e(s(u))
```

on every edge.

For a closed walk `gamma` based at `w0`, write `Hol_gamma` for the composite
transport around the loop.

## 3. Exact anchor-extension theorem

### Theorem MLT-1 — holonomy-fixed anchor criterion

Fix an anchor `a0 in F_w0`. A coherent section with `s(w0)=a0` exists iff

```text
Hol_gamma(a0)=a0
```

for every closed walk `gamma` based at `w0`.

When it exists, the anchored section is unique.

### Proof

Necessity follows by transporting the section around a closed walk and returning
to its anchor value. For sufficiency, define `s(w)` by transporting `a0` along
any path from `w0` to `w`. If two paths are chosen, one followed by the reverse
of the other is a closed walk; the fixed-anchor condition makes the two values
equal. Edge coherence is immediate. Connectedness reaches every world. Any
coherent section must equal this transported value along a path, so it is
unique. ∎

### Corollary MLT-2 — flat transport

If every holonomy map is the identity, every anchor extends uniquely. If the
actual-world fibre `F_w0` is a singleton, there is exactly one coherent global
section.

This is a positive bridge from an actual-world unique anchor to a unique
**cross-world lineage section** under connected, invertible, path-independent
transport.

## 4. Guard-deletion countermodels

### Delete transport custody

World-local singleton fibres without a declared cross-world identity/counterpart
relation establish no numerical or lineage correspondence. Writing the same
name in both worlds does not supply a transport witness.

### Delete path independence

Use a triangle with fibre `{0,1}` at every vertex. Put identity transports on
two edges and a swap on the third. The loop holonomy is the swap and fixes no
anchor. Every world fibre is nonempty and every edge map is bijective, yet no
coherent section exists.

### Delete actual anchor uniqueness

Under flat identity transport and two-element fibres, both anchors extend to
distinct global sections. Coherent lineage exists but is not unique.

### Delete connectedness

An anchor in one connected component does not determine a section in another.
Additional anchors or a global linking premise are required.

# Part III — numerical identity and modality firewalls

## 5. Lineage section is not numerical identity

Even a unique coherent section can select one counterpart token in each world:

```text
s(w0), s(w1), ...
```

without showing those tokens are numerically one transworld entity. The move
from coherent counterpart/lineage to numerical identity requires a separately
stated metaphysical identity semantics.

Therefore:

```text
flat lineage transport + unique anchor
=> unique coherent section;

unique coherent section
not automatically imply
one numerically identical bearer exists in every world.
```

If the transport maps are independently interpreted as preserving numerical
identity rather than counterpart relation, then the coherent section supplies a
conditional de re persistence result. That interpretation is a bridge premise,
not a theorem of the graph.

## 6. Necessary existence versus necessary universal role

A bearer may exist in every accessible world while failing to be the universal
actualizer in some; or each world may have a universal actualizer while no one
bearer persists. Distinguish:

```text
exists x forall w Exists(w,x);
exists x forall w U(w,x);
forall w exists unique x U(w,x);
exists unique x forall w U(w,x).
```

No quantifier order inherits another without explicit existence, role,
identity, and uniqueness bridges.

# Part IV — cross-candidate effects

## 7. Candidate A / TAC / provenance

The `tau_e` maps are reason/identity transport witnesses. Copying one label
across worlds or versions does not create them. Path independence is a
provenance-consistency condition: different transport histories must return the
same typed bearer/certificate, or the lineage claim is incoherent.

This supplies a concrete distinction among:

```text
same registered type;
lineage correspondence;
profile equivalence;
coherent counterpart section;
numerical identity;
evidential independence.
```

It does not recover the missing historical `orthemologous` or `paralemologous`
relations.

## 8. Candidate B / versioned restoration

Target/source versions connected by transport maps can carry a restorative
policy or reason certificate only when transport around revision/fork/merge
cycles is path-independent at the relevant object. Nontrivial holonomy means
that “returning to the same version” can return a different bearer, policy,
reason, or target interpretation, reopening the restoration certificate.

A flat policy transport still does not verify target adequacy or causal
restoration.

## 9. Candidate C / modal ascent

Round 10 supplies actual-world uniqueness conditionally on COMMON+ANCHOR.
MLT-1 identifies the next modal burden:

```text
actual unique universal actualizer
+ connected complete world graph
+ invertible transport
+ anchor-fixed holonomy/path independence
+ numerical-identity-preserving interpretation
=> conditional de re persistence across the declared worlds.
```

Each added premise has a deletion model. The package still does not establish:

```text
that the declared worlds exhaust metaphysical possibility;
that accessibility is the correct modal relation;
that transport preserves numerical identity;
that the bearer is underived/necessary in every world;
mentality, agency, Creator classification, attributes, Names, or revelation.
```

## 10. Updated Candidate-C frontier

```text
C-FRONTIER-5:
source and defend a complete modal domain plus a numerical-identity-preserving,
path-independent cross-world transport for the unique actualizer, without
assuming de re necessity in the transport definition; then prove underivability
and universal-actualizer status persist under that transport and separately
address mentality and attributes.
```

# Part V — ancestry and disposition

## 11. Ancestry and prior-art

| Object | Relation | Credit |
|---|---|---|
| quantifier-order countermodel | standard de dicto/de re separation | no novelty |
| MLT-1 | standard graph parallel transport/holonomy criterion | no novelty |
| TAC/AR3/AR4 use | typed lineage/reason/version transport application | no historical identity |
| Candidate-C use | dependency-minimal modal bridge decomposition | no world-truth credit |

The external Ten Advances corpus is not used. The CDC prompt contributes only
search orchestration.

## 12. Round result

```text
positive objects:
  exact holonomy-fixed anchor criterion;
  unique anchored section theorem;
  flat-transport + singleton-anchor corollary;
  conditional modal-lineage bridge.

negative objects:
  world-local unique actualizers with no one cross-world bearer;
  swap-holonomy cycle with no coherent section;
  flat transport with two global sections when anchor uniqueness is absent;
  disconnected worlds not fixed by one anchor;
  coherent lineage without numerical identity.

updated theorem-strength gap:
  C-FRONTIER-5.

novelty:
  standard graph/holonomy mechanism with substantive orthemological modal and
  provenance application; no new general mathematics claimed.

integrated champion:
  NONE.

meniscus:
  MENISCUS_NOT_REACHED.
```
