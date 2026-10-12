# Homogeneous PER closure and concrete adapter

## Verified scope

This addition proves closure rather than assuming it. `HomogeneousPER.lean` is a
conditional algebraic theorem, not by itself a model construction.
`ConcreteUniverse.lean` instantiates it in the independently checked
`CaseOperational` SKI-plus-case algebra. Whole-source formation and fundamental
soundness are separate obligations owned by the source-soundness development.

## Relations and universe

For an applicative carrier D with conversion, a relation is eligible precisely
when it is a conversion-saturated PER and is either universal, Atom-supported,
or Fun-supported. Supported means `R x x → P x`. No assumption says every
carrier element is Atom or Fun; undefined/stuck elements may remain outside both.

The relations are exactly the dependent shapes in `FullPER.F`:

- Pi(A,B)(f,g) means for all A-related x,y, B(x)(f x,g y).
- Sigma(A,B)(z,w) means A(first z,first w) and B(first z)(second z,second w).
- first z = z K; second z = z KI.
- A family is extensional when A(x,y) implies literal relation equality B(x)=B(y).
- Only fibers over supported inputs `A x x` need be eligible.

## Assumptions and where used

- Conversion is an equivalence and an application congruence. Saturated PERs
  contain endpoints related by conversion.
- Atom and Fun are disjoint. Generic closure and Church membership do not use
  this field; the concrete construction proves it, and its separation arguments
  depend on it.
- If f x is Atom or Fun, then f is Fun. This is the operative closure premise.
  The concrete algebra proves it from its reduction/confluence theorem.
- Pi/Sigma PER laws use extensionality of B and supported-fiber PER laws.
- Intersections choose a nonuniversal constituent if one exists, otherwise they
  are universal, including an empty intersection.
- Pi is universal if every supported fiber is universal. Otherwise an actual
  supported input with a nonuniversal fiber forces every supported operator to
  be Fun. No unsupported input is used as a witness.
- The exact biconditional “Pi nonuniversal iff a supported fiber is nonuniversal”
  additionally uses the K constant-function conversion law and fiber saturation.
  Strictness alone does not justify the converse. The concrete adapter supplies K.
- Sigma over a nonuniversal base uses first-projection strictness. Over a universal
  base, extensionality makes all fibers equal; then it is universal or
  second-projection strictness forces Fun support.
- Nu membership needs only its conversion equations: nu f x converts to x on
  Atom inputs and to f x on Fun inputs. Related endpoints share the same support
  stratum. The universal relation is immediate. This proves preservation of
  pairs of related endomaps, not merely each endomap separately.

## Files

- `HomogeneousPER.lean`: generic saturated PER laws, closure, guarded principal
  conversion classes, the exact Pi criterion, and impredicative Church relation.
- `ConcreteUniverse.lean`: concrete S/H/U adapters; empty/top/I-class and identity
  eligibility; concrete closure and nu Church membership.
- `GuardControls.lean`: checked finite counterexamples. Omitting family
  extensionality can destroy Sigma symmetry even with eligible fibers and valid
  strictness. Omitting strictness can create a mixed, nonuniversal Pi support
  from homogeneous eligible inputs. An empty domain makes Pi universal even
  when its off-domain fibers are empty.
- `replay.py`: fresh trust-zero compilation of only this addition and the new
  operational dependency, with source hashes and axiom checks. It does not rebuild
  any frozen source-theory or mathlib baseline.

## Replay

Run `python3 homogeneous-per-closure-20261010/replay.py` from the workspace.
Lean 4.19.0 is taken from the existing `.toolchains` directory. Only core Lean/Std
and the new `CaseOperational` source are used. The successful receipt is
`validation/REPLAY.json`; all compiler output is in `validation/REPLAY.log`.
