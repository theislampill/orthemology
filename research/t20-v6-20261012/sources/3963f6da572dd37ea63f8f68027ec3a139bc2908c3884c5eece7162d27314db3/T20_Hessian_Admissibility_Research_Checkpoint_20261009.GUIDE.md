# T20 Hessian Admissibility: consolidated checkpoint

Start with READ_ME_FIRST.md and the small INTEGRATION_INDEX.json. They identify the final proofs, source bindings and independent reviews. The large historical source map is optional provenance.

The main new result: for n≥3, every interior start is forward-safe exactly when all lower score derivatives tend to −∞. Combining this with original-clock closure of the coherence sum selects q_i(t)=a t, common a>0: convex negative-Shannon generators t log(t)/a, up to affine terms. The n=2 exception is explicit. Exact dual-coordinate lifetime formulas also distinguish finite from infinite coherent-boundary arrival.

The earlier binary-log result is preserved: exact prediction needs n continuous coordinates in the original clock, versus one coherence-sum coordinate for the normalized clock. “Scalar” means z=Σb_i (or signed defect z−1), not its square. Safety concerns this correction field and domain, not geodesic completeness of the metric.

Written proofs and internal independent review are supported by bounded exact controls. No fresh Lean build, new cognitive/philosophical warrant, repository integration, owner acceptance or final T20 closure is claimed.

Archive: T20_Hessian_Admissibility_Research_Checkpoint_20261009.zip
Bytes: 1299188
SHA-256: 058a71cfeb8088874025b454479533962cbb3ae3187385fc697c9d04deb7c826

Check that hash before extraction. Then, from the extracted package root:

```sh
python3 -B replay/verify_admissibility.py --output ../hessian-admissibility-integrity
```

Python 3.8+ standard library suffices for integrity. READ_ME_FIRST.md gives exact research replay commands and dependencies. A fresh extraction passed integrity, 20 verifier fixture tests, six actual-packet rejection controls and all six research suites, with outputs equal to the frozen JSON.

All 115 predecessor payload files and 16 new frozen component files are preserved. All 110 previous ZIPs, including the separate base checkpoint, were rehashed unchanged; the base ZIP is not embedded. This one archive contains the full combined scoped payload. External academic PDFs and Lean toolchain dependencies remain outside it, with access and evidence limits explicit.
