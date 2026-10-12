# Conditional entropy control

Start with RESULT.md. It proves a conditional-coercivity transfer through the inherited fixed-whole-marginal full-law projection, under explicit domain and energy-chain-rule assumptions. Its non-Gaussian quartic example checks the full observed-flux correction. Scope controls retain reaction and separate total versus conditional decay, integrated versus per-fibre decay, and all-law versus centred-Gaussian constants.

This is additive scratch ordinary mathematics. It does not establish general PDE existence/uniqueness, protectively integrate any source, or close T20. AUTHOR_FREEZE.json is author evidence, not independent review.

Requires Python 3 with sympy and mpmath. From this directory:

    python3 verify.py --output-dir private-locator:3eb3920439375ada6738
    python3 -O verify.py --output-dir private-locator:4da4712603ef5803a5c2

Optional --original-root .. checks the external original inputs. Without it, all copied inputs are verified, so extracted archives replay independently of their original paths. Numerical tests have explicit labels; ordinary mathematical proofs and source attribution are in RESULT.md. Test failures use explicit exceptions rather than assert.
