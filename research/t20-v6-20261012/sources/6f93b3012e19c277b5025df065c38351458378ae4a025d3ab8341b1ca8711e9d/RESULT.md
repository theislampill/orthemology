# Finite full Raw carriers collapse: the K-only obstruction

10 October 2026. Isolated research extension, not integrated or adopted.
The original universal HasE `W` target and its negation remain open.

## Result

Every finite carrier A with a total operation `app : A → A → A` and one
element K satisfying `(K · x) · y = x` for every x,y is a singleton.
Consequently a nontrivial such carrier is infinite. S, I, pairing, full
function spaces, parametricity, typed extensionality, and impredicativity
are unnecessary. This is an elementary classical combinatory-algebra fact,
not a field-novel theorem.

The proof is shorter than the proposed pairing argument. The map
`x ↦ K · x` is injective, since application of equal outputs to K recovers
the inputs. Finiteness makes this map surjective. Choose a with `K · a = K`.
Then, for every x, `K · x = (K · a) · x = a`. Injectivity gives x=y for any
x,y. K supplies inhabitation, so the subsingleton cannot be empty.

`FiniteK.lean` proves the injectivity, collapse from a preimage of K,
finite subsingleton result, explicit cardinal-one result, and infinitude
under nontriviality. A Unit model checks the sharp surviving case.

## Actual source bridge

The source is the retained `ExtensionalRepairSyntax` and its unchanged
`Poly`, `Term`, and `PolyConvPlus` dependencies. In the actual context
`[Raw, Raw]`, the new file proves with actual HasE constructors:

- `var 0 : Raw` and `var 1 : Raw`;
- `K · var 0 · var 1 : Raw`, using rawAtom and two rawApp rules;
- its conversion to `var 0`, using the original K conversion generator;
- the corresponding actual Raw identity with witness I.

Both the original `P01DF.PolyConv.k` and retained `PolyConvPlus.k`
judgements are checked. The obstruction uses the direct K rule; the
atom/application bridge is unnecessary. The optional identity control
is not a premise of the semantic no-go.

The semantic contract is explicit. `RawDenotation A` interprets every
raw atom in A, every variable by its assigned A-value, and every Poly
application by one total operation A×A→A. `Sound` requires equality of
interpretations for actually Raw-typed, convertible polynomials in that
two-variable context, for all A-valued assignments. Applying this
contract to the displayed source K judgement derives the algebraic K
law for arbitrary x,y. `finite_raw_subsingleton` and
`nontrivial_raw_infinite` follow. `no_bool_raw` rejects Bool as the whole
carrier under this contract; `singleton_raw_sound` proves that the
one-point Raw fragment survives.

This is a conditional requirement on ordinary equality-valued,
compositional Raw semantics. It does not assert that unary membership
soundness alone supplies semantic equality, or that every conceivable
notion of semantics has this contract. A setoid/PER interpretation must
be considered on its application-closed equality classes before the
finite-carrier conclusion applies.

## Full finite quotients

`RawImages.lean` handles the actual closed raw syntax independently of
open-context valuations. A surjective denotation from original Term to
A that preserves all application composition and original raw Conv
as equality gives a TotalK algebra, directly from `Step.k`.

In particular, if r is an equivalence on original Term, contains raw
Conv, and is a congruence for every application, then a finite
`Quotient r` is a singleton. `finite_raw_congruence_universal` proves
that r must relate every pair of original raw terms. This is the exact
full-congruence-quotient obstruction, not an objection to arbitrary
finite observation summaries.

## Limits that remain important

- Finite typed data, including a Bool carrier inside an infinite Raw
  interpretation, are not excluded.
- Finite bounded tests, finite observation summaries, restricted future
  contexts, concolic exploration, and partial/bounded approximations
  need not retain a total compositional application plus the global
  K law. This result neither invalidates them nor turns them into full
  source countermodels. Merely calling an algebra partial is not an
  automatic escape if all the K applications used in this proof remain
  defined with the same global law.
- Singleton Raw does not by itself imply that every type-indexed
  carrier is a singleton. That would require an additional faithful
  embedding or other independently proved bridge. No whole-HasE
  singleton-Raw model is constructed or ruled out here.
- A candidate requiring two distinguishable Raw observations cannot
  use a finite full Raw carrier. A candidate separating only other
  typed carriers needs separate analysis.
- No new Church-carrier cardinality consequence is claimed. The
  existing source standardness and numeral-separation results are not
  re-proved or relabeled. There is no HasE noninhabitation proof,
  decision of universal W, repository integration, or audit closure.

## Duplication check and verification

The discovery pass searched 207 unique-content source/result files
from the existing HasE packets, original P01 formal sources, and
identity-frontier records. Its only matching finite-full-Raw mention
was the preceding family-obstruction packet's explicit avoidance of a
two-element full Raw model. `BoundaryResults.no_erased_full_sections`
was also read: that erased full-section obstruction is different and
does not already prove this finite K-only result. The search receipt
does not claim exhaustive mathematical novelty.

Four new Lean modules compile at Lean 4.19.0 with `--trust=0`, reusing
the retained objects rather than rebuilding the baseline. `INPUTS.json`
binds 30 inherited source/object pairs against the prior prerequisite
rebuild receipt, plus the external source/object import closure. The
replay checks all bindings before and after compilation. Original
sources and objects are never written.

`DependencyAudit.lean` checks the full axiom closure against ordinary
Lean propext, Classical.choice, and Quot.sound. Separately, it checks
the declaration-body graph for the actual source rule uses and excludes
I/S reduction, the atom/application bridge, All, typed extensionality,
and J rule use. These two checks are intentionally distinct: the full
type dependency closure of a theorem mentioning a mutual inductive
grammar may contain every constructor, even when its proof uses only
the displayed rules. No new mathematical axiom, admitted proof, or
unsafe/native evaluator shortcut is introduced.

Replay from this directory's parent:

    python3 hase-finite-raw-obstruction-20261010/replay.py

For a separate copy, pass `--workspace` pointing at the retained
workspace and optionally `--output` naming a new output directory.
This author packet does not itself claim independent review.
