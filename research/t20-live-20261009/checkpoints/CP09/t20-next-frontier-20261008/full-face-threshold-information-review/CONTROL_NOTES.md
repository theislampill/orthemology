# Independent control notes

The first reviewer-owned symbolic run stopped at the S_x identity because SymPy did not infer positivity of x+y-xy from unrestricted positive x,y symbols; its residual retained z^c-z*z^(c-1) unsimplified. A minimal diagnostic showed that exposing a positive placeholder for z reduced the difference to zero. The mathematical domain is 0<x,y<1, so z>0. The final checker uses this domain-valid placeholder, then restores the defining expression. No forced power simplification is used. This was a symbolic-harness limitation, not a failed analytic identity or an empirical counterexample.

The failing run did not produce valid CONTROL_RESULTS.json. The final result file is produced only by the successful rerun.

The next run reached the power-CDF chain rule and exposed the same issue for an undefined symbolic function Q. The comment already required Q to be positive, but the constructor had omitted that assumption. A minimal diagnostic with Function('Q', positive=True) reduced the residual to zero; the checker now declares it. No theorem formula was changed.
