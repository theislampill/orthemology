# Initial interface inspection

Status: source inspection passed for the two interfaces bound in INITIAL_INTERFACE_IDENTITIES.json. This is not implementation acceptance; no independent compiler invocation has occurred.

AllSyntax exposes genuine recursive All, arbitrary typed Pi/Sigma and typed Id. All formation and introduction use twkTel, and elimination accepts formed open replacement types and explicit result formation. All typing leaves the polynomial unchanged. Its finite instance rule has a finite list of type images, a binder-aware support upper bound, Bottom padding, syntactic image and result formation, and unchanged FiniteDerives. The parameterized image-formation premises are bounded by the finite list length; no semantic membership, law record, or uniformity premise is present. The finite import returns literal atom t.

The finSupport maximum-bound representation may include unused positions, but includes only finitely many and safely covers the binder-aware support. Under finite All it subtracts one, rather than counting the freshly bound parameter as a free image. Finiteness/support lemmas and mixed preservation remain outstanding.

The simultaneous mixed definition weakens type images beneath Pi/Sigma and type-lifts them beneath All; it leaves term images unchanged beneath All. The source conversion relation is referenced unchanged. Existing Raw restrictions, explicit scope on conversion targets, and typed identity proof erasure are retained.

AllPredicates uses a single structural Unary × Hetero recursion. Each All unary clause calls only the smaller body's heterogeneous component; its three clauses are both endpoint uniformities and all unary instances. The heterogeneous All clause contains both endpoint self-memberships and all respectful cross links. D/E/H retain zero-padded finite valuation clauses. Raw syntax and semantics are defined before desired lawfulness.

No obstruction is identified in these interfaces. Still required are all algebra, semantic substitution, syntax-derived laws and uniformity, universal soundness, syntactic substitution, representation, both full translations, witnesses, and controls in the frozen contract. Successful checking of these definitions alone would not discharge any of those theorem obligations.

The independent malformed-replacement control now targets these interfaces: a raw Sigma over totalPER with an unformable Raw-identity codomain has unary related pairs without right self-membership, hence fails even equal-valuation diagonal identity. Its source is prepared but not yet kernel checked.
