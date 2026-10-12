# Targeted confluence source check

2026-10-10, participating root research. This is a narrow theorem-source check, not a full-paper reading or fresh replay of an external formal development.

Ana Cristina Rocha Oliveira and Mauricio Ayala-Rincon, Formalizing the Confluence of Orthogonal Rewriting Systems, EPTCS 113 (2013), 145–152, DOI 10.4204/EPTCS.113.14. Received PDF text through public web read at https://arxiv.org/pdf/1303.7335 . Title/authors/date also verified at https://arxiv.org/abs/1303.7335 . The experimental HTML endpoint failed; the PDF was available.

Read the introduction and definitions through printed pp145–148 (PDF pp1–4). Orthogonal first-order TRSs are left-linear and non-overlapping; confluence does not require termination. The paper attributes the classical result to Rosen 1973 and explains parallel-reduction proof structure. Its own PVS development at that publication date explicitly axiomatizes several technical parallel-reduction facts. Therefore the paper is a source for a standard mathematical theorem, not evidence of a freshly kernel-checked, assumption-free confluence proof for our proposed extended calculus.

Candidate transport obligation: enumerate every extended SKI/nu rule, check left-linearity and absence of nontrivial overlaps at nonvariable positions. Apply the standard confluence theorem only after those conditions are established. Atom/function separation and application strictness require their own argument; confluence alone is not a head-standardisation theorem.

No field-novelty, full-paper reading, external formal replay or source-model soundness credit is assigned here.
