# Independent review: finite skyline readout

8 October 2026 UTC. Prospective mathematical review only. Historical floor remains UNVERIFIED. No protected integration, empirical calibration, physical instrument assurance, kernel verification, novelty priority, or closure claim.

## Verdict

PASS for the bounded finite-probe transport theorem and its stated resource bounds. The exact reviewed author/dependency hashes are in SOURCE_BINDINGS.json. Independent executable evidence is in INDEPENDENT_RESULTS.json. This review does not independently reprove the already reviewed ideal skyline mean/variance theorem or the face-only KL asymptotic theorem; it checks the transport and the assumptions required to consume those results.

## Mathematical inspection

1. Quantization uses ceil(Lx), not floor(Lx): x <= j/L iff ceil(Lx) <= j, including x=0 and x=1. A quantized minimum always has an original minimal ancestor mapping to it, proving K_L <= K for arbitrary finite multisets. Distinct original minima can merge or become dominated. Coordinate-bin injectivity suffices to preserve all pairwise coordinate orders and hence K_L=K; it is not necessary.
2. The search enumerates genuine occupied minimal grid locations. The first search minimizes x within y<=b; the second minimizes y within that x prefix. Any witness must equal both selected coordinates. After recording (a,y), every still-unreported minimum has y'<y. This proves completeness, terminates on every finite grid, handles duplicate points and ties, and avoids a negative query after y=0. Empty input consumes one miss.
3. Each first-true search makes at most ceil(log2(L+1)) new calls, with its upper endpoint already known true. Including all repeated existence calls and the possible final miss gives T<=K_L+1+2 K_L ceil(log2(L+1)). No cached answer is incorrectly counted as free. Singleton searches cost zero.
4. Joe command-space margins are H_c(t)=1-(1-t)^c, not uniform. Each nonzero bin has probability at most L^-c; the zero bin has zero mass. Independence of different routes yields a pair collision probability sum p_j^2<=L^-c. The union bound over two coordinates and N(N-1)/2 pairs gives N(N-1)L^-c. Within-route coordinate independence is not used. The uniform world has the same upper bound since L^-1<=L^-c.
5. For R vectors, the error event is bounded unconditionally by Rm(m-1)L^-c. The coupling does not condition the ideal testing law on collision-free vectors. Therefore no independence or distribution claim is accidentally inherited after such conditioning. On the matching event the ideal and implemented decisions are identical, so the per-world error adds alpha+eta. Fresh-vector independence is still required for the imported variance-of-average test.
6. The exact integer predicate L^n q^(n+1)>=p^(n+1), with p/q=m(m-1)R/eta, is equivalent to the required resolution inequality. Doubling followed by integer binary search gives the least admissible positive L and terminates. No floating root rounding is used. For n>=2 the mean gap, variance bound and midpoint comparison are rational.
7. The n=1 repair is valid: delta_1>1/4, Var(K)<=1/4, and a threshold 1+1/8 gives ideal P1 error at most 16/R. P0 always has count one. Thus R>=ceil(16/alpha) and the same collision budget provide a finite rational implementation without a transcendental comparison.
8. For fixed error split, R=O(n^4/log n), log L=O(log n), worst per-vector probes O(n log n), and expected per-vector probes O((log n)^2). The expectation bound follows pathwise from K_L<=K, without conditioning. Total worst probes O(n^5) and expected probes O(n^4 log n) follow. These are upper bounds, not optimal rates or evidence of a total-probe improvement.

## Comparator and observation scope

The matching face-only comparator counts every independent retained vector from its first observation and assumes unconditional terminal correctness at fixed error below 1/2. The finite skyline protocol starts exactly R vectors, terminates after finitely many actual endpoint calls, and has unconditional per-world error alpha+eta. Taking alpha+eta<1/2 therefore gives a genuine independent-vector improvement over the existing Omega(n^4) lower bound for unrestricted adaptive face-only words. Its interior probes are outside that lower-bound channel. This consumes the existing KL theorem rather than re-proving it. There is no contradiction and no inferred improvement in total probes.

The oracle requires unchanged retained thresholds throughout a vector, separately read nonlatched outputs, coordinate-separable threshold-AND routes, OR endpoint semantics, noiseless responses at selected rational command coordinates, known n/c and reference calibration, and independent fresh vectors. Extraction itself is pathwise and does not need a statistical law; the transport probability needs independent routes with the stated margins; the ideal-test rate needs the particular joint hard-pair law. None establishes physical selection, precision, retention, reset feasibility, or calibration. Dominated routes remain unidentifiable from an individual skyline.

## Independent replay and scope of evidence

Run from the workspace root:

    python t20-next-frontier-20261008/finite-skyline-readout-review/independent_checks.py

Dependencies: Python standard library only. The script loads only the author's extract/grid_resolution function AST nodes, without importing or executing their top-level code and without modifying author files. Its independent reference enumerates per-column minima and successive record lows, rather than using the author's pairwise dominance reference.

Passed checks:

- All subsets of grids L=1,2,3: 16, 512, and 65,536 inputs. This includes arbitrary point counts up to the entire 4-by-4 grid.
- All multisets with 0 through 6 points on the 3-by-3 grid: 5,005 inputs, including repeated coordinates and identical points.
- 132,600 quantizations of rational-grid multisets; 23,260 collision-free cases; 21,055 strict losses, demonstrating that unconditional count preservation would be false.
- 243 exact integer resolution/minimality checks, including n=1, larger n, and general helper edge cases with A<=1.

There were no failed checks in this independent run. Finite exhaustive checks are implementation diagnostics, not proof of the general probability bounds or asymptotic theorem. General claims above were checked analytically. No Monte Carlo, external bibliographic investigation, or Lean/kernel replay was performed for this review.

## Final binding correction

An initial integrity guard expected the author's announced pre-final hash 81c71dd5339c41e0f73b53617392267c0dcaaf8ac708cea5d0710b73abcafdcb and stopped before replay because the author had concurrently made the root-requested introductory wording correction. This was an integrity/version check failure, not a mathematical or executable-control failure. The final wording correctly says the packet “does not establish an improved total-probe bound,” rather than suggesting an impossibility theorem. The replacement final hash 6687a8f2f56290427297bba1cfef6c8c14a58878ffa0010805550f0cd632b0d5 was checked explicitly, the disposable author replay passed, and SOURCE_BINDINGS.json binds this final version. No author files were changed by this reviewer.
