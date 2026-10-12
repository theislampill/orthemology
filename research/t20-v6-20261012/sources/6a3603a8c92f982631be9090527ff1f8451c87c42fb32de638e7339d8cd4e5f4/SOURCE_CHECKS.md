# Primary source checks for determinate initial positivity

Checked 10 October 2026 UTC. Scope: classical moment-theory hypotheses and attribution only; no independent certification of the entire hierarchy proof.

Original reviewed artifact: `determinate-initial-positivity-20261010/RESULT.md`.

Original reviewed SHA-256: `83c6dda6b1709c707f0854a4b6c7ee20facb7af3409b2ebf8cb29b3a453554ed`.

Conclusion: the cited classical inputs support the construction. One minor source-description correction was proposed below. This record does not certify any subsequently changed RESULT bytes. No RESULT edits or baseline builds were performed by this source reviewer. All publication findings below are paraphrases, with fewer than 200 words per publication.

## Jablonski Jung and Stochel

Z. J. Jablonski, I. B. Jung, J. Stochel, *A Non-hyponormal Operator Generating Stieltjes Moment Sequences*, arXiv:1110.0249v1, section 2.1.

- [Printed p.4](https://arxiv.org/pdf/1110.0249v1#page=4): Stieltjes existence is equivalent to positive semidefiniteness of both Hankel families `(c_(i+j))` and `(c_(i+j+1))` at every finite order. The source's term positive definite expressly uses a nonnegative quadratic-form inequality.
- [Printed p.5](https://arxiv.org/pdf/1110.0249v1#page=5): N-extremality means polynomial density in L2; N-extremal supports have no finite accumulation points.
- [Printed p.6](https://arxiv.org/pdf/1110.0249v1#page=6): for an S-indeterminate sequence, equation (2.1.6) and following paragraphs identify the Krein measure as N-extremal, supported on `[0,infinity)`, with zero in its support. Together these facts imply an isolated zero atom with positive mass.
- Proposed citation fix: replace the claim that the preceding JJS discussion describes supports as entire-function zero sets with its actual no-finite-accumulation statement. The zero-set description appears in Berg-Christensen, printed p.100.

Inspection: web-extracted PDF text plus locally rendered images of pp.4-6.

Downloaded PDF: `private-locator:67ebd29960d16d442acd`.

PDF SHA-256: `5696a9312200be9140cc122def39ffe70e2717e5018e95b71f09e977fe678478`.

## Berg and Christensen

Christian Berg, J. P. R. Christensen, *Density questions in the classical theory of moments*, Annales de l'Institut Fourier 31(3) (1981), 99-114.

- [Theorem 7, printed p.111](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf#page=14): for an indeterminate N-extremal probability `mu = sum a_n delta_(x_n)`, removing the entire atom `a_0 delta_(x_0)` yields a determinate positive measure. Determinacy is Hamburger, under the definitions on printed p.100. Positive scalar normalization therefore supports RESULT's probability normalization.
- [Printed p.112](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf#page=15): the proof concludes; the following section expressly distinguishes complete deletion from finitely changing positive atom weights, which preserves indeterminacy and N-extremality.
- [Printed p.106](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf#page=9): Theorem 3's proof states `a_n h(x_n,x_n) = 1`, supporting the atom/kernel identity used in RESULT section 8.
- [Printed p.100](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf#page=3): supports of indeterminate N-extremal measures are described as zero sets of an entire function.

Inspection: web-extracted PDF text, with local rendered-image verification of pp.111-112.

Downloaded PDF: `private-locator:df60184f82c670d99279`.

PDF SHA-256: `d83014552f522c82c42581c515358aee9a0f3558ad5281079cf2672ad93a9685`.

## Kuba and Panholzer

Markus Kuba, Alois Panholzer, *On moment sequences and mixed Poisson distributions*, author preprint associated with arXiv:1403.2712.

- [Lemma 1, pp.8-10](https://www.dmg.tuwien.ac.at/kuba/preprintMomseq.pdf#page=8): the transferred Carleman condition is the Hamburger condition `sum mu_(2n)^(-1/(2n)) = infinity`, not the Stieltjes condition in RESULT. The distinction in RESULT is correct.
- [Proposition 2, p.7](https://www.dmg.tuwien.ac.at/kuba/preprintMomseq.pdf#page=7): its hypothesis includes an mgf in a neighborhood of zero including `-rho`; mere moment determinacy does not supply that hypothesis.
- Source caveat: Lemma 1 prints `rho >= 0`, but its equivalence requires `rho > 0`; at zero the mixed Poisson variable is identically zero. RESULT uses positive `s`, so this endpoint issue does not affect its application.

Inspection used web-rendered PDF text only. No publication byte hash is asserted.

## Schmudgen

Konrad Schmudgen, *On the multidimensional K-moment problem*, arXiv:2011.04025v1.

- [Theorem 1, p.2, equations (5)-(6)](https://arxiv.org/pdf/2011.04025v1#page=2): assumes `L(p^2) >= 0`, `L(x_j p^2) >= 0`, and `sum L(x_j^n)^(-1/(2n)) = infinity`; concludes existence and uniqueness of a Stieltjes representing measure.
- Taking dimension one and `L(x^n) = c_n` gives exactly the needed Stieltjes Carleman criterion. For an existing Stieltjes sequence the two positivity hypotheses are automatic. The same page, equation (4), independently states the one-dimensional two-Hankel-family existence criterion.

Inspection used web-rendered PDF text only. No publication byte hash is asserted.

## Preservation scope

The downloaded publications and rendered page images are inspection materials outside the compact review directory. They are excluded from the final compact archive. The two publication hashes above identify actual downloaded bytes; no byte hash is inferred from a URL, metadata, or extracted text.
