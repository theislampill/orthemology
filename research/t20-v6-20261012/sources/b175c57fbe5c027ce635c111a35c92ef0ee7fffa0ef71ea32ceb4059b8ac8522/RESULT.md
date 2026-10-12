# Exact finite mixed substitution and finite type-code operations

## Proved, without computability hypotheses

All operations use the existing source encoding unchanged and have Mathlib primitive-recursiveness plus exact source correspondence:

- `renameTyCode` for actual `P01AC.trename` with finite numeric renamings, and `twkCode` for actual `P01AC.twk`.
- `mixedCode` for actual corrected `P01AC.mixed`, with finite polynomial and finite type environments.
- `tinstCode` for actual `P01AC.tinst` and `tsubstImagesCode` for actual `P01AC.tsubst (P01AC.typeImages images)`.
- `twkListCode` for mapping actual twk over a telescope, with an explicit equality of source-code lists. This statement is at List Nat representation and is not silently identified with a natural telescope code.
- `renameTypeCode` and `shiftTypeCode` for actual finite TypeCode renaming.
- `substituteTypeCode` for actual TypeCode substitution with finite environments; `instantiateTypeCode` exactly realizes `OrthemologyV3.instantiateType`.
- `finCode` for actual `P01AC.fin` and `finSupportCode` for actual `P01AC.finSupport`.

Main interfaces include `primrec_mixedCode` / `mixedCode_exact`, `primrec_tinstCode` / `tinstCode_exact`, `primrec_tsubstImagesCode` / `tsubstImagesCode_exact`, `primrec_instantiateTypeCode` / `instantiateTypeCode_exact`, and the corresponding fin/support pairs.

## Faithful two-sort environment updates

Polynomial environments retain the previously proved finite images plus shifted variable tail. Type environments consist of a finite list of actual type images, a Boolean choosing a shifted-parameter tail or Bottom-default tail, and the numerical tail shift. These distinguish single type instantiation from finite typeImages.

The actual mixed rules are preserved:

- Under pi/sigma: lift polynomial substitution by pup, and apply actual wk to every stored type image. Its free term variables shift; its type parameters do not.
- Under all: keep the polynomial environment unchanged, prepend the new type parameter zero, and apply actual twk to stored type images. The shifted-parameter tail advances; an absent Bottom-default image remains Bottom.

Exact extensional environment lemmas `finiteTyEnv_term` and `finiteTyEnv_type`, and exact code updates `termLift_exact` and `typeLift_exact`, supply these transitions. No arbitrary function environment is claimed computable.

The TypeCode operation is proved directly for its own four-constructor syntax and actual `rename`, `upSub`, `substitute`, and `instantiateType`. It is not transported silently through the different Ty datatype.

## Discriminating controls

Controls compare finite typeImages with single tinst on the same body under nested all binders; preserve new bound type parameters; retain Bottom beyond a finite image list; shift free term variables inside stored type images under pi/sigma; leave term substitution unchanged under all while shifting type parameters; exercise two nested term binders; test TypeCode capture-avoiding instantiation; and check both finSupport and fin compilation.

Four false controls must reject: a shifted-param fallback in place of Bottom, missing wk on a stored type image under pi, an erroneous term lift under all, and capture-causing TypeCode instantiation.

## Remaining boundary

These are total code-level realizers exact on genuine encoded inputs. Malformed/noncanonical inputs are totalized and are not claimed equivalent to the operational decoder. The parallel canonical validity theorem supplies representability; a checker sound on every accepted canonical code and complete on actual certificate encodings suffices for derivability r.e.

Remaining assembly includes exact Rule.conclusion/premises/checkSide code maps, finite auxiliary certificate checking, derived branch/motive/induction syntax templates, list/telescope natural-code transport where needed, and final certificate-tree checking/existential closure. The deep finite mixed-substitution dependency itself is now discharged. This packet does not yet prove actual Joint/E derivability r.e., integrate sources, or close T20.

## Verification

Run `python hase-coded-mixed-transformations-20261010/verify.py`. The script recompiles the twelve source modules of the frozen predecessor and all nine new modules with Lean 4.19 `--trust=0` into fresh output. Four false controls must reject. All inherited and new source/object pins are checked before and after. No full-baseline rebuild or protected source edit occurs.

Central axiom audits allow only propext, Classical.choice, and Quot.sound. Failed attempts and source-name inspections remain in diagnostics; they are not accepted proof inputs.
