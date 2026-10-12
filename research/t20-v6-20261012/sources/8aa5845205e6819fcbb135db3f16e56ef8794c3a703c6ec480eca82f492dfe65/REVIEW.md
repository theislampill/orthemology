# Independent rigidity-to-dependent-section review

Status: PASS for all three frozen author modules and independent binder/source-ancestry controls. No author-source defect found.

## Mathematical and source judgment findings

The total-space argument is actually constructed, not assumed as an additional certificate. For an arbitrary original `Form (N :: Γ) P`, original Has seed p:P(0), and original Has step over Σn:N.P(n), the author constructs a Σ-algebra, folds the Church input in that algebra, and projects to an original Has endomorphism u:N→N. The zero and successor equations of this projected u are original source conversion equations with original Has evidence. Arbitrary HasE evidence r:Rigidity can therefore be eliminated at this u.

The resulting Id(I,u) is eliminated by the original HasE J rule to obtain Id(u n,n), correctly oriented. Source conversion links fst(n D a) to u n. Source J then transports snd(n D a):P(fst(n D a)) to P(n). Families genuinely may depend on the index and the arbitrary ambient context; they are not restricted to constant families or a semantic relation class.

Independent substitution controls verify:
- `totalStepType P = subst (cons nextIndex (fun k => var(k+1))) P`: the total-space binder's index is replaced by successor of its first projection, while ambient variables shift once.
- Instantiation of the curried successor family at n yields exactly P(succ n), with the BooleanPrimitive successor, not a similarly named successor from another namespace.
- Source evidence for both projected laws is constructed from the documented seed and step, with no extra proof certificate.

Input scope matters: P is original Form, and seed/step/input n have original Has evidence. The rigidity hypothesis may be arbitrary HasE evidence. The section outputs are HasE, not an unconditional claim for arbitrary HasE-formed families, HasE seeds/steps, or HasE Church inputs.

`dependent_section_from_rigidity` initially proves pointwise existence. `dependent_section_explicit` strengthens this to the exact polynomial `snd(n D a)` at P(n); `dependent_section_curried` accepts the ordinary curried dependent step. J erasure removes the rigidity witness from the output polynomial, but the typing derivation still depends on its HasE hypothesis. No inhabitant of Rigidity, newly adopted source rule, reflection rule, proof-object uniqueness, or zero/successor computation law follows from this erasure alone.

## Ancestry and validation

Fresh source snapshots are checked with Lean 4.19.0 `--trust=0` against retained objects; there is no baseline rebuild. Transitive Lean constant-ancestry controls for all three section theorems exclude FullPER, GenericFoldTransport, RigidityDiscriminator, HomogeneousOriginal noninhabitation, SourceNaturality, and q-specific conversion facts. The source fold typing lemma is permitted and uses original rules. Printed theorem axiom sets contain only propext, Classical.choice, Quot.sound.

Initiality produces two harmless linter warnings: unnecessary sequencing focus and a no-op change tactic. No errors or admitted proofs. The earlier generic-rigidity review remains frozen and untouched. All reviewer additions are confined to this new review directory.

## Uniform source implication

`UniformSection` now packages a single explicit section polynomial at Πn:N.P(n). Its intermediate `section_has` uses original Has rigidity evidence so inherited original weakening suffices. The stronger presentation `rigidity_implies_section` introduces Rigidity as an ordinary source hypothesis and proves an actual HasE judgment at Rigidity → Πn:N.P(n), uniformly for each original-formed family with original-Has seed and curried step. Family quantification remains metatheoretic; no new universe or calculus rule is introduced.

The independent named control `uniform_from_arbitrary_rigidity` applies this actual implication by HasE.piElim to arbitrary HasE rigidity evidence and produces an explicit uniform section application. Thus the final implication is not limited to original-Has evidence when eliminated; only the intermediate author's direct weakening proof has that restriction. This uses no general HasE weakening theorem. The additional `shifted_at_var` control checks the binder cancellation that recovers the actual family P under n.

All five main author section theorems pass the source-only transitive ancestry audit. Retained baseline objects and the preceding frozen generic-rigidity review were reused without mutation. This is a genuine same-source dependent-section consequence of a still-explicit Rigidity hypothesis; it does not inhabit Rigidity or turn its proved external noninhabitation into an internal negation.
