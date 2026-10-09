# Independent exact controls

Run `python check_multiroot.py` in this directory using Python's standard library. The script writes `results/INDEPENDENT_CONTROLS.json`; the retained successful stdout is `results/INDEPENDENT_REPLAY.log`.

All arithmetic used for certification is `fractions.Fraction`. Natural logarithms are enclosed by an exact atanh series after exact powers-of-two range reduction. No simulated observations, numerical optimizer, floating-point tolerance or empirical experiment is used.

The successful run checks:

- 2,211 total-route budgets and reciprocal-constant/scaling identities
- 18,688 route/profile cases constructed by multiplying the failure probabilities of individual route occurrences, including 17,344 proper-profile equalities and 1,232 full-profile boundary equalities
- 26,752 interior rational inequality chains, checking both denominator relaxations, exact factorization, every factor bound, and the final constant
- 702 direct Bernoulli KL enclosures below the exact chi-square bound and C(r,k)
- Four randomized history-dependent action trees, with 64, 64, 16 and 64 leaves; direct full-transcript KL and summed conditional KL enclosures overlap and are below N C(r,k)
- 147 upper-menu and sample-coefficient identities
- An exact-log countercontrol showing that an unbalanced baseline permits KL greater than 1/2000 while the claimed C(3,20) would be only 2/6136515
- Deterministic separation with excluded route-addressable gating
- Exact shared-random-root-gate laws versus independent-route laws
- Exact rate sequences disproving any uniform positive variance floor
- Three certified confidence-ratio checks illustrating the failure of uniform log(1/delta) replacement as delta approaches one half

The first run's 12-term logarithm certificate was inconclusive at a highly saturated case. The rerun records ten cases needing 32 terms, all of which then certify the bound. `results/INITIAL_PRECISION_ATTEMPT.md` preserves the obstacle. No analytic claim was weakened and no approximate tolerance substituted.

The largest chi-square/C ratio on the tested interior grid is 54/581 at r=2,k=1,a=(3/4,3/4). This is a finite-grid statistic, not a global optimum or an optimal-constant claim.

The author's code is copied without modification into `author_replay/` and replayed there, so no author or predecessor result file is overwritten. The copied code hash and final output comparison are retained. This replay is separate from the independent controls above.

Finite grids and finite adaptive trees do not prove the continuum-rate theorem or justify the model assumptions. The independent analytic proof provides the universal argument; these controls detect algebraic, boundary, and implementation mistakes in representative exact cases.
