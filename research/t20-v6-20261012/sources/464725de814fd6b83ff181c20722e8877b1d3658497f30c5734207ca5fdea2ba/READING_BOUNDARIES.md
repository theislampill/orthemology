# Primary-source reading record

Retrieved/read 10 October 2026 UTC. “Read” below means continuous text of the listed argument, including its proof, not just a search snippet. Source PDFs and pdftotext -layout outputs are retained with hashes. PDF page numbers here are the printed page numbers, which coincide with physical one-based pages in these arXiv files.

## Curto–di Dio, arXiv:2108.03505v1 (7 August 2021), 20 pages

Authentic primary PDF: https://arxiv.org/pdf/2108.03505v1 . Download through the unversioned PDF endpoint was verified by its v1 header and the arXiv record, which lists only v1.

Continuously read:
- pp.2–7: Section 2 opening heat equation through the complete proof of Theorem 2.10, excluding the following Corollary 2.11. This includes Lemma 2.1, its derivation, arbitrary-sequence Definition 2.3, Gaussian propagation Theorem 2.7, and moment-cone assumptions of Theorem 2.10.
- pp.10–14: paragraph before Definition 2.19 through Definition 2.28 and the paragraph immediately afterward. This includes the polynomial dual heat equation, Theorem 2.23 and proof, Example 2.24, Corollary 2.25, Theorem 2.26, and Corollary 2.27.
- pp.14–18: complete Section 3, from its opening diagonal transport equation through Corollary 3.8 and proof; stop before Section 4.

Did not continuously read pp.8–9's Gaussian reconstruction results or Section 4; do not infer their contents from the theorem index.

Publication metadata was verified on the arXiv abstract and official Oxford Academic article-abstract record: IMRN 2023(17), 14955–14990, DOI 10.1093/imrn/rnac244. The primary author's indexed URL https://homepage.divms.uiowa.edu/~rcurto/heatequation.pdf returned HTTP 404 via both web open and direct retrieval. DOI browsing did not yield the full text. No claim that the 2023 published proof is identical to v1 is made.

## Curto–di Dio–Korda–Magron, arXiv:2211.04416v3 (26 August 2026), 27 pages

Authentic primary PDF: https://arxiv.org/pdf/2211.04416v3 . Download through the unversioned endpoint was verified by its v3 header and arXiv submission history (v1 8 November 2022; v2 13 March 2023; v3 26 August 2026).

Continuously read:
- pp.3–6: Section 1.2 from definitions of C_b^∞ and Schwartz functions through Section 1.3's paper description, including the introductory Burgers discussion. The Burgers numerical formula was not independently endorsed or used in our proof.
- pp.6–9: complete Section 2 (polynomially growing test algebra; Lemma 2.1; Theorem 2.2 and its whole duality proof; Remarks 2.3–2.5; Corollary 2.6; pure reaction illustration).
- p.12 through start of p.13: Theorems 3.9 and 3.10 with their complete convolution/SOS/Waring proofs.
- pp.13–14: Theorem 3.12's Choi–Lam definition, exact threshold statement, and complete Gram-matrix proof. The paragraph after its proof was read but its numerical solver evidence was not adopted.
- pp.16–20: Lemma 3.16 through Corollary 3.25 and Example 3.26, including the full proof of Theorem 3.21 and all quantifiers/proofs of Corollaries 3.22–3.25. Not all these results are accepted as imported theorems: the uniform Corollary 3.22 is explicitly quarantined in RESULT.md.
- pp.21–24: complete Section 4 (Lemma 4.1, Theorem 4.2, examples, and C^∞ extension), then Section 5 summary through before Acknowledgments.

Additional localized lookups: Pos(n,d)'s defining set on pp.1 and 11, without any spatial or coefficient normalization. We did not continuously read every numerical SOS example of Section 3, and did not inspect their external software, code, or empirical controls.

Visual PDF verification: printed pp.14 and 20 rendered locally and read as page images; retained in source-checks/. This verified the exact threshold, quantifier order, and dependent truncated representation statement against the PDF rather than relying only on extraction. Web PDF screenshots returned cache misses; local rendering succeeded.

Source caution outside the main claim: Theorem 4.2 is printed for merely continuous g, although its proof invokes uniqueness of trajectories and the surrounding Lemma 4.1 has stronger smooth bounded hypotheses. We do not rely on a general continuous-field uniqueness assertion. Our affine corollary uses its own global linear ODE flow. This local comparison is not a full audit of that theorem.

## Same PDE/atoms paper, arXiv:2211.04416v1 (8 November 2022), 27 pages

Authentic primary PDF: https://arxiv.org/pdf/2211.04416v1 . Download and PDF header verified.

Continuously read:
- pp.6–10: complete Section 2, through the paragraph before Section 3.
- pp.18–22: complete Section 4, through before Section 5.

Exact version difference material here: v1 Lemma 4.1's mass exponential contains h alone for its non-divergence-form equation; v3 includes h+div g. V3 is used for the comparison. No complete v1–v3 diff or whole-manuscript audit was performed.

## Fitzsimmons–Pitman author-hosted HTML

https://mathweb.ucsd.edu/~pfitz/downloads/kac/kac.html : title, authors, date and abstract prose.
https://mathweb.ucsd.edu/~pfitz/downloads/kac/node11.html : complete Feynman–Kac section prose, from killing-semigroup introduction through final probabilistic discussion, not the following Markov-chain section.

Important limitation: equations in this old HTML are images with generic alt text; their actual images were not read. No specific equation, hypothesis-sensitive theorem, or proof dependency is taken from them. This is only a verified classical-mechanism/context pointer. The HTML is saved for provenance.

## Discovery-only exclusions

ResearchGate, search-result aggregators, citation snippets, author CVs, and search-generated summaries were not used as inspected mathematical originals. The two arXiv PDFs, including their relevant continuous argument sections, are the basis of the substantive comparison. No third-party outreach was undertaken.
