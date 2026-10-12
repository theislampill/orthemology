# Independent converse and exact source-implication review

Status: PASS. Frozen author module and both independent controls freshly replayed without warnings or source defects. Prior reviews remain frozen.

## Exact conclusion

The new theorem is an actual original HasE judgment at the literal type

HasE [] (abstract (abstract (abstract (abstract ident))))
  (arr InternalRecursorPrinciple.Uniqueness SourceRigidity.Rigidity).

Together with the already checked converse-direction theorem, this gives closed source implications in both directions between the exact unchanged formulas Rigidity and Uniqueness. Neither formula is asserted inhabited. No new definition of either principle, source rule, semantic reflection or axiom is introduced.

## Source proof audit

`uniqueness_nat_instance` performs actual source All elimination at the already formed Church type N. It then successively applies the instantiated source proof to zero, successor, u, zero-law evidence, and successor-law evidence. All dependent result types are explicitly formed using original substitution. The resulting NatRecResult is exactly Πn:N.Id_N(u n,n succ zero).

The same instance is independently constructed for I, with original Has evidence that I preserves zero and successor. At each original Has n:N, source J symmetry and transitivity combine the two identities through their common n succ zero endpoint, obtaining Id_N(I n,u n). This does not assume that n succ zero is definitionally equal to n.

`uniqueness_endomorphism` weakens original Has data under a fresh n, abstracts the pointwise HasE identity, and uses the actual inherited HasE.piExt constructor with all endpoint formation and scoping arguments. Its result is exactly Id_(N→N)(I,u), the required Rigidity orientation. The direct helper uses original Has w:Uniqueness for inherited weakening; the final implication binds w as an ordinary original source variable and imposes no extra hypothesis beyond the literal source formula.

The final four introductions bind successor evidence, zero evidence, u:N→N, and the outer Uniqueness hypothesis. Their de Bruijn positions are 0,1,2,3 at the deepest context. Explicit zeroAt/stepAt/resultAt shift equalities and term-closedness of Uniqueness/Rigidity justify the dependent shifts. The final four-abstraction polynomial is checked Scoped 0.

`hasE_scoped` is an ordinary induction over the existing mutual HasE judgment. Introduction and conversion constructors use their supplied scope certificates; eliminations propagate scopes; identity/extensionality proof terms are closed atoms. It proves only source scoping and adds no HasE weakening, substitution, or conversion admissibility principle.

## Validation boundary

Fresh trust-zero replay compiles the frozen author module and two independent controls against retained dependencies, without a baseline rebuild. Independent controls check both exact closed implication judgments, exact instantiated recursor endpoints, the I=u direction, arbitrary HasE scoping, and the final closed term. Full transitive ancestry confirms that the converse does not use the forward Rigidity→Uniqueness proof or recursor_unique_source, and excludes semantic FullPER/GenericFoldTransport, source noninhabitation, SourceNaturality, and q-specific facts. Thus the converse is not circular through the forward result.

No UIP, proof-object uniqueness, arbitrary higher coherence, or inhabitant of either principle is claimed. Previous review manifests and retained objects are checked unchanged.
