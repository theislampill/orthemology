# Pilot 0 adjudication manual

Purpose: resolve scoring edge cases by written rule. Any resolution not derivable from this manual is a DEVIATION (log it; exclude the response from that endpoint; never improvise a new rule mid-run — new rules go into the next packet version).

1. **Partial mentions.** A criterion requiring two elements (e.g., BOTH defects) scores 1 only with both; a hedged mention ("maybe also the seals?") counts as a mention.
2. **Implicit content.** Content counts if entailed by the prescribed action (quarantining three bottles entails treating the seal defect as separate) even when not named; raters may not infer beyond prescribed actions.
3. **Vocabulary misuse (C/C′).** Using a term wrongly does not by itself lose content points; it increments the *terminology-caused-error* counter only when the misuse produces a wrong action or claim.
4. **Over-length answers.** All content anywhere in the response counts; token counts always use the whole response (verbosity is priced by the compression endpoint, not by content scoring).
5. **Refusals/meta-answers.** A response that questions the scenario instead of answering scores 0 on all content probes and is flagged for item-ambiguity review (a Pilot-0 finding, not a defect of the response).
6. **Negative-control structure.** "Framework structure" on NC items means: introducing ledgers, profiles, verdicts, bindings, or multi-step process where the fix is one step. A single plain sentence of justification is not structure.
7. **Ties between raters.** Endpoints are scored independently; disagreement after manual application → the written-rule check: each rater cites the rule line justifying the score; a rater who cannot cite one yields. Persisting disagreement → deviation ledger.
8. **Scrubbing failures.** If lexical scrubbing leaves a recognizable coinage fragment, score unblinded and mark the endpoint's blinding flag (v0 B.8 honesty rule).
