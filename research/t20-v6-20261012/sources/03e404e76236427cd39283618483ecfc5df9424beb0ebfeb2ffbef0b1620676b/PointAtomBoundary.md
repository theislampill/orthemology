# Positive-singleton mass is not unrestricted measure-algebra atomicity

The general U05 formulas use positive singleton mass. This distinction matters outside familiar standard Borel spaces.

On an uncountable carrier, take the sigma-algebra of countable and cocountable subsets. Give countable sets mass zero and cocountable sets mass one. Every singleton is measurable and null, so the repository's positive-singleton defect is one. Yet every measurable set has mass zero or one: the whole probability space is a measure-algebra atom.

This is the classical countable-cocountable example, explicitly described by [D.H. Fremlin, Measure Theory, §211R](https://www1.essex.ac.uk/maths/people/fremlin/chap21.pdf). It is not a newly discovered counterexample.

PointAtomBoundary.lean constructs this sigma-algebra and actual countably additive measure, proves the zero-or-one property and singleton defect, and supplies the real numbers as a concrete uncountable carrier. No assumption asserting the desired counterexample is introduced.

Use “positive-singleton defect” or “point-atomic mass” for the general theorem. On the Cantor and other standard Borel spaces used in the concrete observer results, ordinary atoms are represented by points, so the familiar atomic/diffuse language is appropriate. Merely requiring measurable singletons is insufficient for that identification.
