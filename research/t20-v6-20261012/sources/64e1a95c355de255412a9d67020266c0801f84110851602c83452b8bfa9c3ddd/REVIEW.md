# Independent review: constructive Sigma completion

Verdict: PASS within the exact original-source-premise scope below. No change to the frozen source calculus or Sigma countermodel is made or needed.

## Exact theorem and quantifiers

Constructive.lean establishes EtaSchema iff EliminationSchema and EtaSchema iff WeakEliminationSchema. These are Lean metatheoretic propositions. Every context Γ, fibre types A and B, motive P, branch d, and input z is universally quantified. The formation and typing premises are the original Ctx/Form/Has judgments; the resulting eta evidence and eliminator are typed with HasE. B is formed in A::Γ; P is formed in Sigma A B::Γ; d is typed in B::A::Γ at branchType P. There is no constant-fibre, constant-motive, closed-context, closed-input, or simple-type restriction.

This is not a theorem for arbitrary HasE-only motives, branches, or inputs. It does not assume HasE weakening/substitution, and must not be advertised as proving those structural theorems. Nor is either schema a single source type with an internal inhabitant. EtaSchema supplies a potentially different existential proof polynomial e for each source-typed input. The forward implication then supplies the explicit, uniform syntactic expression elim d z e. There is no assertion of one closed source combinator implementing every external schema instance or a definable choice of e.

## Forward construction

pairSub maps the motive's pair variable to pair(var 1)(var 0), with ambient variables shifted by two, matching precisely the branch context b:B,a:A,Γ. pair_substitution constructs a genuine original MixedSubstitution replacing these two variables by b and a, using the dependent type of b instantiated at a. branch_type_at checks that the composed substitution is exactly motive instantiation at pair(a)(b); branch_has invokes the original has_mixed theorem.

For a general input z, reconstruction_has gives an original Has derivation of pair(fst z)(snd z). branch_has supplies d at that reconstruction. identity_sym reverses the supplied HasE identity z=reconstruct z via actual J, using original formed endpoints and motive. transport_source, itself a previously checked explicit HasE.j derivation, then transports the branch result to P[z]. All formation and source typing premises for J are supplied by original structural lemmas and their HasE inclusions. No semantic transport axiom or assumed general HasE substitution is smuggled into the proof.

## Reverse construction

The reverse direction instantiates elimination at etaMotive(S) = Id_(wk S)(var 0, reconstruct(var 0)). This motive is genuinely dependent on the pair variable. eta_motive_formed verifies its original formation, generic_pair_has checks the two-variable canonical pair at the correctly twice-weakened Sigma type, and shifted_body_at handles the dependent second coordinate. canonical_eta_branch constructs original identity evidence I for a canonical pair and its reconstruction using only the source projection beta conversions. The elimination result is exactly the wanted eta identity, via eta_motive_at.

Only the typing part of elimination is used. weak_elimination_implies_eta independently proves this without any computation hypothesis. The strong schema's everywhere-erasure clause is therefore not responsible for necessity.

## Computation and proof sensitivity

The chosen J implementation is the inherited erasing SKI term. elim_erases is raw P01DF.PolyConv at every input, and elim_pair_computation additionally reduces both canonical projections to obtain branchAt d a b. The latter holds for all raw terms d,a,b,e, without typing or equality-of-proofs premises, and is axiom-free. This is an explicit source conversion theorem, not an unproved judgmental-beta claim in a different calculus.

elim_pair_identity separately checks formation and typing of both canonical endpoints and introduces their HasE identity with I. Thus raw conversion and typed propositional computation are distinguished. No UIP or proof-equality theorem is assumed. An independent axiom-free proof-variation control confirms that changing e or f yields the same raw canonical computation without identifying the proofs e and f themselves.

## Independent controls and boundaries

ConstructiveReview.fixed_term checks the exact nonexistential elim term with arbitrary Γ,A,B,P,d,z,e. The independent schema_not_available theorem applies the previously reviewed tagged-model counterexample to an original Has variable of SigmaRaw and proves not EtaSchema. Consequently both WeakEliminationSchema and EliminationSchema are also unavailable in the unchanged rules. The equivalences give explicit conditional transformations; they do not establish either schema. In particular the earlier pair-eta boundary has not been reversed by the constructive follow-through.

Two adversarial files must fail: replacing the original Has branch premise by HasE cannot satisfy elim_of_eta, and omitting its eta witness cannot yield the claimed output typing. Their logs record the intended type mismatches. These negative controls defend the advertised scope rather than merely testing parser rejection.

The result supplies source-strength credit for an explicit completion interface. It does not select an intended interpretation, adopt a new inference rule, show unrestricted HasE structural closure, or justify an ontological or physical conclusion. Original natural-number initiality results remain untouched.

## Reproducibility

The author's frozen Constructive.lean SHA256 is 254b95f0b02765d1b3018f256299af432083ac7f2bcdd0d4d99f538e50c861c7. This review copied and replayed it with Lean 4.19.0 --trust=0 into a fresh output directory, using the independently reviewed Initiality object and existing retained dependencies. The reviewed Initiality source is hash-identical to the author's Initiality source. No baseline was rebuilt and no protected input modified.

The constructive typing and equivalence theorem closures use only propext and Quot.sound; raw computation is axiom-free. The independent nonavailability controls additionally use Classical.choice through previously reviewed model soundness. REVIEW_RECEIPT.json records exact source hashes, commands, outputs, and expected failures; RETAINED_OBJECTS.json pins the reused objects and verifies they remain unchanged.
