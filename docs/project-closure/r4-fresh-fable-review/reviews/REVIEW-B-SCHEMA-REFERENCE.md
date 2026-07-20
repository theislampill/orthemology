# Review B — schema/reference audit (fresh Fable recovery review)

Scope: schemas, examples, fixtures, validators, exemptions on the final
review branch. Surfaced model: `claude-fable-5`.

- **Unresolved references**: `validate_internal_references.py` green over the
  whole corpus; ghost-citation probe (P3) fails as required. Cross-record
  reference resolution (claim/token/evidence/handoff/rel_spec/inheritance)
  green; ghost-metaortheme mutation family semantic-killed.
- **Namespace collisions**: bundle-global id uniqueness + global token_id
  rule enforced; duplicate-id mutation families killed; I32 collision fixture
  rejected.
- **False cross-episode joins**: token claim-scope checked only against the
  owning episode's ledgers (D4); no all-token-to-all-ledger comparison exists
  (verified in code, not just fixtures).
- **Cycle gaps**: analysis-inheritance and precedence cycles both rejected
  (I29–I31, I36–I37; families 22–23); claim dependency cycles detected.
- **Temporal-order gaps**: one found and repaired this review (P7): naive
  `decision_time` passed both layers. Now a recursive timestamp sweep in
  `collect_issues` rejects any time-of-day-bearing timestamp that is not
  timezone-aware (pure dates remain legitimate); pinned by I45.
- **Conditional residual gaps**: disposition-conditional field requirements
  enforced; the 19 declared-equivalent mutation survivors are exactly the
  redundancy/empty-list classes with stated reasons; deleting both
  conditional refs IS killed.
- **Schema-valid but semantically contradictory bundles**: the invalid corpus
  (I29–I45) all schema-valid by design and semantically flagged; 0 unjustified
  mutation survivors at the final tree.
- **Overbroad exemptions**: the reference-exemption registry has exactly 3
  external paths (owner-named) + 1 retired path (resolving successor);
  matching is exact set membership; hardened this review against external
  shadowing (P4) and repository escape; stale exemptions fail.

Blocking findings: **none**. The P7 class is repaired and pinned.
