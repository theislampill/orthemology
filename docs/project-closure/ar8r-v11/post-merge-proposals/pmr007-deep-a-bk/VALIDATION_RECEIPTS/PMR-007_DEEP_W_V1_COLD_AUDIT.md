# PMR-007 Deep W V1 cold audit

Disposition: `REPAIR_REQUIRED`.

The primary checker verifies the finite-set pullback mechanics, but it also
exposes several interpretation defects in V1.

## Blocking findings

### W-F01 — the proposed target key is too coarse

`(target_id, version, recipient_scope)` admits false compatibility when the
analysis version, referent, or semantic contract differs. The executable model
already contains a pair that the coarse key accepts and the full key rejects.

**Required repair:** use a contract key containing target identity, target
version, recipient scope, analysis version, referent identity, and semantic
contract digest. State that this list is model-relative and may need extension.

### W-F02 — a pullback aligns keys; it does not validate components

Invalid profile and warrant objects with equal keys still lie in the raw
pullback. V1's wording risks treating membership as validity.

**Required repair:** first restrict to independently valid subobjects `A*`,
`B*`, and, where used, `C*`; then form the pullback. Preserve component
validation as an upstream burden.

### W-F03 — key authority and referent identity are not proved

A matching `referent_id` is only a registry assertion unless independently
bound to one referent. A digest can also be copied or computed over an
inadequate contract.

**Required repair:** classify target-key construction, H12 source
authentication, H16 referent identification, and contract-digest adequacy as
independent premises.

### W-F04 — the pullback is not a reductive common core

The pullback enforces compatibility between two already defined component
objects. It does not derive profile semantics from warrants, warrants from
profiles, or one explanatory mechanism from both.

**Required repair:** call it a contract-aligned integration interface, not a
common explanatory core or integrated champion.

### W-F05 — target alignment does not entail world truth

Several valid-looking component objects can agree on one false or misdeclared
target key. A third component does not help unless the world-bridge object is
itself independently valid.

**Required repair:** use a valid world-bridge subobject only conditionally and
retain world truth as an independent authority burden.

### W-F06 — pullback pairing does not establish one bearer

A pair `(a,b)` is a structured compatible pair. It is not numerical identity,
co-instantiation in one metaphysical bearer, one intentional subject, or one
causal mechanism.

**Required repair:** add an explicit bearer/identity nontransfer firewall.

### W-F07 — bytes and carrier equality do not transport contract identity

The model correctly exhibits same bytes and same carrier under different
versions. V1 does not state this consequence strongly enough.

**Required repair:** require exact contract-key equality after an authorized
version/analysis transport; same bytes, storage, or carrier is insufficient.

### W-F08 — source and Track-N migration overreach

The target contract may contain source/referent fields, but filling those fields
does not authenticate a source or migrate school-internal premises into neutral
Track T.

**Required repair:** preserve source classification and nonmigration from Deep
S/T.

### W-F09 — finite-set universal property only

The checker covers finite sets and explicit functions. No claim about enriched,
probabilistic, partial, higher-categorical, or dynamic pullbacks is verified.

**Required repair:** retain the finite ordinary-set scope.

### W-F10 — standard categorical ancestry and novelty ceiling

The universal property is the standard pullback construction. Its value is a
typed orthemological application, not new category theory.

**Required repair:** assign zero general novelty and mark every downstream use
as an application/interface result.
