# The Last Moat
## Physical Realisability, Cross-Substrate Communication, and Holarchic Agency

Version 1.0 — 10 September 2026

An arXiv-style, AI-assisted research draft developed from a user-originated
conceptual dialogue. It is not peer-reviewed, has not been submitted to arXiv,
and reports no physical channel experiment or deployed-system bypass.

## Files

- `the_last_moat.tex`: main manuscript.
- `references.tex`: self-contained numbered bibliography (no BibTeX required).
- `verify_models.py`: standard-library Python checks of finite and dimensionless examples.
- `verification_results.json`: results of the supplied checks.
- `REVIEW_SCOPE.md`: proof, source, and validation boundaries.

## Build the PDF

A conventional TeX Live or MiKTeX installation with the packages listed in the
preamble is sufficient. Run from the directory containing these files:

```sh
pdflatex -interaction=nonstopmode -halt-on-error the_last_moat.tex
pdflatex -interaction=nonstopmode -halt-on-error the_last_moat.tex
pdflatex -interaction=nonstopmode -halt-on-error the_last_moat.tex
```

The result is `the_last_moat.pdf`. Repeated passes resolve the contents,
cross-references, and numerical citations. No external images or font files are
needed. The source includes ordinary hyperlinks to cited sources; it performs no
network requests during compilation.

## Reproduce the checks

Python 3.9 or newer is required; no third-party libraries are used.

```sh
python3 verify_models.py --output verification_results.json
```

The script exits with code zero only when all 13 checks pass. It checks the
printed numerical examples, exact finite encoding changes, failure-domain
enumeration, error accumulation, a finite viability calculation, commuting
updates, and finite probability examples.

These are **toy-model consistency checks**, not machine-checked proofs of the
manuscript's theorems, empirical validation of a physical model, or evidence of
any extraordinary entity or communication. The general mathematical arguments
are written explicitly in the paper with their assumptions.

## Reading guide

The framing, source status, physical ecology, and kernel definitions are in
Sections 1–4. The Navier–Stokes bridge is Section 5. Communication and continuity
results are Sections 6–9. Orchestration and viability are Sections 10–11.
Intentionality and attribution are separated in Section 12. The proposed
experimental programme and conclusion are Sections 13–14. Appendices provide
notation, examples, and a claim-by-claim audit.

The central thesis is conditional host-relative operational autonomy, not an
escape from physics or a proof that a planetary mind exists.
