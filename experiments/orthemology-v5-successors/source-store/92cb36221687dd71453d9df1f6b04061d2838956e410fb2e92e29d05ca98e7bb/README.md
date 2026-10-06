# One variable root extension reference

This Python reference implements the complete finite comparison theorem for the source-presented one-variable root extension. It accepts only the tagged alternatives ['old', expression] and ['test', pure_expression, pure_expression]. The existing restricted expression syntax supplies natural constants, variable zero, addition, multiplication, and old zero conditionals. New equality tests occur only at the root and return natural 1 or 0.

The module requires the separately supplied restricted reference module certificate_checker.py to be importable. The reviewed dependency has SHA-256 8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef. Only Python's standard library is otherwise required.

To run the test suite, place the dependency on PYTHONPATH, then run python3 -m unittest discover -s . -p 'test_*.py' -v in this directory. There are eight supplied tests and seven independent adversarial controls.

The public entry points validate, tail, evaluate, comparison_bound, distinguish, and equivalent operate on the declared source syntax. comparison_bound returns M for the inclusive finite range 0 through M. distinguish returns a checked natural counterexample or None for universal equality; it does not promise the least counterexample. root_bound validates a finite integer coefficient dictionary and returns the elementary bound used in the proof. Its value on the zero polynomial is bookkeeping only, not a nonvanishing claim.

The implementation uses unbounded Python integers. Finite syntax and unbounded resources are assumed in the mathematical algorithm. Memory exhaustion, recursion limits, interruption, and other runtime failures are not negative identity verdicts. This is independently reviewed and tested reference code, not a kernel refinement theorem. It does not recognize arbitrary P01AC endpoints, produce current-Has identity inhabitants, admit nested new equality tests, or decide the extension at unrestricted arity.
