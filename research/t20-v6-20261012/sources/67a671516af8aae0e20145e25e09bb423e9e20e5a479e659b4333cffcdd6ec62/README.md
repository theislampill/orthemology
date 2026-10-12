# Concrete SKI + atoms + case operational algebra

## Verified artifact

`CaseOperational.lean` is standalone (`import Std`) and checks with Lean 4.19.0.
It defines the actual carrier syntax and rules; it does not assume an algebra
contract, confluence, atom separation, or head-origin.

Verification command from the workspace root:

```sh
.toolchains/lean-4.19.0-linux/bin/lean \
  -o homogeneous-per-model-20261010/operational/CaseOperational.olean \
  homogeneous-per-model-20261010/operational/CaseOperational.lean
```

The checked output is in `check.log`. Confluence, conversion joining,
head-origin, atom separation, and atom/function disjointness depend only on
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`. The case
combinator's saturated function law `nu_fun` has no axioms. There are no
`sorry`, `admit`, or user-declared axioms in the source. No protected source or
baseline was modified or rebuilt.

## Exact syntax and rules

Let T be the closed finite terms over constants I, K, S, a0, a1, ν and binary
application, written left-associatively. The function weak-head values are
exactly:

- I
- K
- K x
- S
- S x
- S x y
- ν
- ν x

Their arguments are arbitrary closed terms, with no normalization assumption.
The atoms are a0 and a1. The one-step relation is the compatible closure of:

- I x → x
- K x y → x
- S x y z → x z (y z)
- ν f a0 → a0
- ν f a1 → a1
- ν f v → f v for each of the eight function-value schemas above

Thus this is a finite first-order TRS with exactly thirteen root schemas.
`Step.nuF` has a `RawFun` premise solely to package those eight disjoint
syntactic schemas. It is not a semantic or conversion-dependent side condition.

## Mathematical confluence proof

Every left side is linear. Distinct left-side root patterns do not unify:
I/K/S/ν heads distinguish the main families, and the ten ν argument patterns
(two atoms, eight function shapes) are mutually disjoint first-order patterns.
Every proper nonvariable subterm of a left side is a constant or an unsaturated
K, S, or ν spine. None unifies with a redex left side. Consequently the TRS has
no critical overlaps and is orthogonal. The orthogonal-TRS confluence theorem
therefore applies, including to this nonterminating system.

The Lean source does not import or assume this metatheorem. It proves
confluence directly by parallel developments:

1. `Par` performs any collection of compatible reductions at once, reducing
   rule arguments in parallel and duplicating their reducts at an S step.
2. `dev` computes the complete development of the redexes present in a term.
3. `par_fun` proves that parallel reduction preserves each of the eight
   function weak-head shapes. In particular, reducing inside a recognized
   ν argument cannot destroy its recognized shape.
4. `par_develop` proves t ⇒ u implies u ⇒ dev(t).
5. Hence `par_diamond` gives a common parallel successor for any two parallel
   successors of one term.
6. The standard strip argument proves the reflexive transitive closure of
   parallel reduction confluent.
7. `step_par` and `par_red` place compatible one-step and parallel reductions
   between the same reflexive transitive closures. This gives `confluence`.
8. `conv_join` derives Church–Rosser for the explicitly defined symmetric
   transitive conversion relation.

The ν cases are included throughout, rather than imported from a theorem for
the smaller SKI carrier.

## Head-origin proof

First prove the reduction statement: if t a →* v, where v is an atom or
function weak-head value, then t →* w for some function weak-head value w.

Inspect the first root contraction of the original application, if one exists.
Before it, all steps occur in the two arguments of that application, so its
left child has reduced from t. Immediately before root contraction, that left
child is one of I, K x, S x y, or ν f. Each is a function weak-head value.
If no root contraction occurs, the final term remains an application.
An application that is a weak-head value has one of the shapes K x, S x,
S x y, or ν x; its left child is again a function weak-head value reached
by reduction from t. This proves reduction-level head-origin.

Every reduction of a function weak-head value preserves its outer function
shape; reductions can only affect its arbitrary stored arguments. Atoms
have no outgoing step. Thus every reduct of any atom/function weak-head
value is again such a value.

If t a converts to a value v, Church–Rosser gives a common reduct u of t a
and v. The latter shape-preservation observation makes u a value. Apply the
reduction-level argument to t a →* u, and embed the resulting reduction from
t into conversion. This is `head_origin`.

## Separation and quotient carrier

Both a0 and a1 are distinct normal forms. If they were convertible,
Church–Rosser would give a common reduct, which would have to equal both
constants. This contradiction is `atom_distinct`.

Similarly, no atom is convertible to any function weak-head value: a common
reduct would both be that atom and have a function weak-head shape.
The stronger saturated statement is `atom_not_fun`.

Define D = T / Conv. Conversion is an equivalence and a congruence, so
[f]·[x] = [f x] is a well-defined total application on the concrete quotient.
The I/K/S equations hold because they are root reduction rules. The classes
[a0] and [a1] are distinct. Let F consist of classes represented by function
weak-head values, and A = {[a0], [a1]}. Then:

- A and F are disjoint.
- If d·e belongs to A ∪ F, then d belongs to F.
- [ν]·f·[ai] = [ai], for i = 0,1.
- If v belongs to F, then [ν]·f·v = f·v.

The last equation holds for every representative convertible to a function
value, not merely a syntactic weak-head value: use congruence to convert the
argument to its function representative, take the ν rule, then convert back.
This is exactly the checked `nu_fun` theorem.

## Lean API

Namespace: `CaseOperational`.

- `T`: constructors `i`, `k`, `s`, `a0`, `a1`, `nu`, `app`
- `RawFun : T → Prop`: exactly the eight syntactic function-value forms
- `Step`: compatible one-step reduction for the exact rules
- `Red := Star Step`: reflexive transitive reduction
- `Conv`: constructors `refl`, `step`, `symm`, `trans`
- `Conv.left`, `Conv.right`, `Conv.app`: conversion congruence
- `Conv.i`, `Conv.k`, `Conv.s`: SKI conversion equations
- `AtomVal t := Conv t .a0 ∨ Conv t .a1`
- `FunVal t := ∃ v, RawFun v ∧ Conv t v`
- `raw_fun_val`: `RawFun t → FunVal t`
- `funVal_back`: `Conv t u → FunVal u → FunVal t`
- `confluence`: `Red t u → Red t v → ∃ w, Red u w ∧ Red v w`
- `conv_join`: `Conv t u → ∃ w, Red t w ∧ Red u w`
- `head_origin`: `(AtomVal (.app t a) ∨ FunVal (.app t a)) → FunVal t`
- `atom_distinct`: `¬ Conv .a0 .a1`
- `atom_not_fun`: `AtomVal t → ¬ FunVal t`
- `nu_atom0 f`: `Conv (.app (.app .nu f) .a0) .a0`
- `nu_atom1 f`: `Conv (.app (.app .nu f) .a1) .a1`
- `nu_fun f`: `FunVal v → Conv (.app (.app .nu f) v) (.app f v)`

For an importing isolated module, include this directory in `LEAN_PATH` and
write `import CaseOperational`. The quotient construction in this README is a
mathematical corollary; the checked file works directly with T and Conv.

## Scope boundary

This establishes the operational carrier and its exact required properties.
It does not by itself formalize a type grammar, homogeneous PER closure,
HasE interpretation, or whole-language soundness. Those semantic obligations
remain separate from these fully discharged operational obligations.
