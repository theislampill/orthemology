# PMR-007 Deep Round BK V1 — cold audit

```text
candidate: PMR-007-NCBD-1 V1
disposition: REPAIR_REQUIRED
review relation: same-program procedural cold audit; not external review
frozen-hash verification: PASS 4 / 4
```

## Blocking findings

### BK-F01 — local-domain and global-bearer syntax were mixed

V1 quantifies local bearers `x in D_w` and later writes one `g` as though it
were literally a member of every local domain. A global bearer sort or an
explicit occurrence-to-bearer map is required before cross-world numerical
identity is even well typed.

### BK-F02 — primary checker omitted the declared ROOT predicate

The theorem separates existence, root role, and underivability, while the V1
checker used only `EXISTS and UNDERIVED`. This implementation mismatch must be
repaired before admission.

### BK-F03 — transport coherence was not represented in the primary checker

The checker verified a constant-domain same-object condition but not the
counterpart/transport structure. Coherent lineage and numerical identity must
remain separate, with an explicit distinct rereview in local occurrence
semantics.

### BK-F04 — frame-relative persistence was called necessity too quickly

Existence and root status at every index of one declared finite frame is
frame-relative modal persistence. It becomes metaphysical necessity only under
an independently warranted modal semantics and complete intended frame.

### BK-F05 — underivability remained world- and graph-relative

`UNDERIVED(w,o)` means no predecessor in the declared grounding graph at that
world. It is not automatically independent self-subsistence, aseity, or
nonborrowed actuality.

### BK-F06 — the guard package was presented as exact/minimal

Coverage, numerical identity, and concreteness are load-bearing in the supplied
deletion models. Coherence and frame scope are certification guards. V1 did not
prove global premise minimality across all modal semantics and must not say so.

### BK-F07 — abstract order and concrete occurrence need separate sorts

The abstract-order countermodel should not simulate absence of concreteness by
merely setting a predicate false on bearer objects. V2 must explicitly separate
an abstract order sort from local bearer occurrences.

### BK-F08 — B_ID is a hard bridge, not a free equality convention

Counterpart transport, one role section, one lineage class, and one numerical
bearer are different. V2 must leave the chosen cross-world identity semantics
unproved and must not use a constant-domain checker as its authority.

### BK-F09 — source and world conclusions were not reachable

Even a declared necessary concrete root does not entail originator,
actualizer, Creator, unity, intellect, personality, or the revealed referent.
Those later bridges require independent premises.

### BK-F10 — ancestry and novelty must be reconciled

The quantifier firewall, coherent root section, and identity firewall are
already controlled by Rounds 11, 12, and 17. Deep BK is a B4/B5 bridge
reconciliation and receives no independent general theorem origin or novelty.

## Required repair

1. Introduce global bearers and local occurrences with an occurrence-to-bearer
   identity map.
2. Keep role, existence, underivability, and concreteness distinct.
3. Restrict the executable primary checker to an explicitly declared
   constant-domain special case.
4. Run a distinct local-occurrence rereview with independent global labels and
   transport controls.
5. Replace “exact minimal package” with scoped sufficient package and explicit
   load-bearing deletion controls.
6. Preserve frame, modal, identity, source, and later-ascent firewalls.
