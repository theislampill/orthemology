# Arbitrarily small fixed linear slack admits uninformed repair

Status: ordinary source-derived extension. The source's special case is c=1; no historical-priority or fresh-kernel claim is made.

Exact controlling source: ApproximateRepairIdentification, SHA256 16f467976b9d30b5fe1bfa5997e7378dcf391e989d17aaed4e69224da0686261, lines 8–11 (literal predicate) and 34–42 (c=1 control), read in full. The full source/import binding is in READING_LEDGER.json and IMPORT_REUSE.json.

Proposition. For real c,a,e with c>0, 0≤a≤min(c,1), and e≥0, the zero-information output q=1/2 satisfies BinaryApproxGood a e (c*e) q. Consequently, for any positive disturbance sequence e_n→0, the same constant zero-query output succeeds at every n for an uncountable interval of norm parameters, while eta_n/e_n=c.

Proof. At q=1/2, subtract the left side of each defining score inequality from the right side. The resulting margins are respectively

  a*e + a*e^2 + c*e,
  (c-a)*e + a*e^2.

Both are nonnegative from the stated premises. Since min(c,1)>0, its interval from zero is nondegenerate and uncountable. Instantiate the same one-point private-state law and the never-ask controller for every parameter; neither the state nor the output contains the parameter. The event is certain at every time. If e_n>0 then eta_n/e_n=c identically. The private state law is shared and the unused oracle can be fixed, so this counterexample does not evade the causal theorem by parameter-coding a seed.

A slightly broader ordinary consequence: if eta_n/e_n→c>0 and e_n>0, every fixed a in [0,min(c,1)) eventually satisfies eta_n≥a*e_n, hence the same two margins establish eventual uninformed repair. The threshold time may depend on a. This is an uncountable interval of positive eventual-success parameters.

Scope. This sharpens the source's c=1 counterexample to arbitrarily small positive constant linear slack. It does not assert that eta=o(e) is necessary for every possible countability result or characterize oscillating tolerance ratios; useful subsequences can change that question. It uses the source's weak two-state repair predicate, not strict improvement, arbitrary losses or an empirical behavioral claim.
