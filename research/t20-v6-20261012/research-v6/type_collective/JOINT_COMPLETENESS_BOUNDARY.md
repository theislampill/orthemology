# A source-bound incompleteness corollary for the completed calculus

New v6 ordinary proof, 11 October 2026. This joins the retained effective-source and full-PER results. It is not a fresh kernel theorem, and has no claim about a newly named concrete omitted index.

## Exactly used retained results

- `BoundedHaltingPR.lean`, SHA bc669cde2038e1ce800f5697afc4a244ce544371f37134054054a95273d6298a: actual Mathlib bounded evaluator has a retained PR-program representative; actual nonhalting index set is not r.e. The PR representative is existential, with finite-family choice in its proof, not an extracted general translator from proofs to runtime programs.
- `FullPERTests.lean`, SHA 1e8900ea5a9dd296986391acb1d887c8658b6806165c22191485a61615516edf, and `FullPERHalting.lean`, SHA 8b8951ef7d1f932717226176b17700bf7a8a6beb4f78d0433376ecfc3ae92ba2: for a fixed actual PR f, A_e=programType f e is old-Has formed, and both full-PER semantic inhabitation and the fixed semantic witness K I are valid exactly when machine e does not halt. Consequently some such family has non-r.e. valid-index set.
- `FamilyComputability.lean`, SHA b77fabcd8d512e8839edf137482285511b544e2f4267f2a02ab67635f544f9a4: for each fixed f, e ↦ encode(programType f e) is primitive recursive in the literal retained codec.
- `TypeInhabitationSearch.lean`, SHA d1817d9500c9d25436d55309b344dd93b04a0268836824f96218427c99c6eb60: closed actual HasJ inhabitation on canonical type codes is r.e., by a separate term-plus-certificate projection, not merely by enumeration of supplied-term judgments.
- `JointSoundness.lean`, SHA 31b121c690e0 (full hash in source ledger): actual HasJ soundness in FullPER, including both recursively closed dependent Sigma elimination and induction rules. `FullPER.F_arr` interprets the internal arrow with its actual cross-argument relation.

These complete source bodies were read. The codec, grammar and computability dependencies remain separately tracked for source-level examination; their imported conclusions are not expanded into blanket credit.

## Corollary and proof

There exists an old-Has-formed closed type A that is full-PER valid but has no closed HasJ inhabitant. Moreover its internal negation arr A Bottom has no closed HasJ inhabitant either.

Choose the fixed f given by the retained non-r.e. family theorem. Let S(e) mean ∃p, HasJ [] p (programType f e). This is r.e. by the exact canonical-code type-inhabitation theorem and the proved computable family map. Full HasJ soundness gives S(e) ⇒ Holds(programType f e). If the converse held for every e, Holds on this family would be r.e., contradicting the retained non-r.e. theorem. Classically choose a valid omitted e and set A=programType f e. Its old formation is part of the family theorem.

For the negation claim, choose any admissible full-PER type environment, for example the constant raw-conversion environment already defined and proved admissible in FullPERHalting. Validity supplies a semantic self-related inhabitant a of A at the empty term environment; in this family the uniform K I witness can be used. If HasJ [] r (arr A Bottom) existed, full soundness and F_arr would let its interpreted function act on the pair (a,a). Its result would belong to the empty interpretation of Bottom, a contradiction.

The second paragraph is a direct semantic countermodel to an internal negation derivation. It does not turn an external implication into an internal source arrow. It also does not invoke internal derivability of A, which the first paragraph excludes.

## Bounds

This does not identify a specific machine index or synthesize the omitted type. It does not assert that every semantic-valid type is independent, that source typing is decidable, or that every stronger extension is incomplete under arbitrary rules. It concerns exactly the fixed effective HasJ calculus and its proved full-PER model. The successful new induction/Sigma rules, closed-N canonicity and finite-certificate enumeration coexist with this global limitation.

This joins two formerly separate boundaries: concrete completion repairs particular original HasE deficits, while recursive enumerability prevents a sound effective presentation from exhausting the full-PER semantic validity family.
