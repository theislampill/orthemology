# Public study reproducibility and endpoint check

8 October 2026. Target: Tracy, Hart and Martens (2011), Study 4. Järnefelt, Canfield and Kelemen (2015) was a bounded data-availability fallback. No authors were contacted and no participants were recruited.

## Result

**A participant-level computational reanalysis could not be performed from the public materials located in this bounded search.** The deliverable is a reproducibility-obstruction report, inspection of actual stimuli and endpoints, and a reproducible check of printed statistical arithmetic. It is not an independent experiment, external human validation, or replication. It does not establish that the data do not exist or are unavailable through every possible route.

Two narrowly verified reporting discrepancies qualify particular significance claims. They do not establish which field was misprinted, misconduct, a failed experiment, or the failure of the other reported effects.

## What was located

The [PLOS article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0017349) and publisher PDF were retrieved. The relevant passages were checked in HTML, XML and rendered PDF pages 8 and 10. All four supporting DOC files were downloaded and inspected:

- [S1](https://doi.org/10.1371/journal.pone.0017349.s001): Dawkins and Behe passages used in Studies 1, 2, 4 and 5
- [S2](https://doi.org/10.1371/journal.pone.0017349.s002): pooled scale means and reported summary tests; no participant rows, codebook or executable analysis
- [S3](https://doi.org/10.1371/journal.pone.0017349.s003): matched passages for Study 3, not the Study 4 stimuli
- [S4](https://doi.org/10.1371/journal.pone.0017349.s004): Sagan passage used in Study 4

The [author-laboratory publication entry](https://drjesstracy.com/publications/topic/trends-in-science/) links a paper PDF; the inspected [research-tools page](https://drjesstracy.com/research-tools/) did not identify this dataset. Exact/targeted title, author and DOI web searches included OSF, Figshare, Zenodo, Harvard Dataverse, Borealis and relevant institutional domains. Two direct OSF title-filter queries returned no records. DataCite DOI queries returned 6 and 12 records respectively; all were supporting files of later citing studies, not data for either target study. These searches are scoped discovery attempts, not comprehensive repository inventories.

For the fallback, the [Boston University publication entry](https://www.bu.edu/cdl/ccl/publications/) linked the [published article](https://www.bu.edu/cdl/files/2015/04/Creator-online-publication1.pdf). Its appendices contain instructions and aggregate model results. No participant-level release was located through those materials or the targeted repository routes. Direct publisher retrieval returned HTTP 403; that route is a retrieval limitation, not evidence of absent data.

## Printed arithmetic and preserved results

The following are calculations from printed statistics, not estimates recomputed from observations. Ordinary F upper-tail probabilities equal two-sided t probabilities when numerator df is one. A directional t equivalent requires an independently justified direction; simply halving an F p-value is not a default ANOVA procedure.

| Location and endpoint | Printed statistic | Recomputed ordinary p | Directional t equivalent |
| --- | ---: | ---: | ---: |
| Study 4 theory-only Sagan MS by author interaction, PDF p 8 | F(1,131) = 2.69 | .103379 | .051689 |
| Study 4 theory-only three-way interaction, PDF p 8 | F(1,257) = 6.07 | .014405 | .007203 |
| Study 4 theory-only IDT simple effect within Sagan, PDF p 8 | t(64) = 2.86 | .005714 | .002857 |
| Study 5 theory-only ET simple effect, PDF p 10 | t(94) = 1.47 | .144901 | .072451 |
| Study 5 theory-only interaction, PDF p 10 | F(1,94) = 5.17 | .025256 | .012628 |
| Study 5 theory-only IDT simple effect, PDF p 10 | t(94) = 3.23 | .001706 | .000853 |
| Study 5 six-item ET simple effect, explicitly one-tailed, PDF p 10 | t(94) = 1.80 | .075069 | .037534 |

In Study 4, the text says both theory-only effects held, prints F = 2.69 and t = 2.86, then gives p < .05. The displayed F cannot support the interaction's asserted significance. In Study 5, the text calls both theory-only simple effects significant and gives all p < .05; displayed t = 1.47 cannot support that claim for ET. Allowing ordinary rounding to the nearest .01 leaves the most favorable directional probabilities above .05: .051531 and .071777 respectively. Thus routine printed rounding, even combined with a directional convention, does not reconcile these two claims. A typesetting, transcription, or other reporting error remains possible; the available evidence does not select the wrong field.

The other rows retain their own arithmetic status. In particular, the Study 4 theory-only three-way interaction and IDT simple effect remain compatible with p < .05. It would be wrong to conclude from the smaller interaction's discrepancy that the whole framing result disappears, or to claim that the effect concerns only author liking. All labels, inputs, ordinary and directional probabilities, and rounding intervals are retained in JSON. Run `python recompute_reported_statistics.py` to regenerate `arithmetic_results.json`.

## What the actual material discriminates

S1 packages scientific assertions with named authors and rhetorical claims of evidential strength. Its Dawkins passage also extends skepticism about design beyond biology, while Behe's passage advocates design across life and cosmology. Consequently these are specific persuasive passages, not interchangeable operationalizations of every creator proposition. S4 combines meaning in scientific inquiry with scientific truth-seeking, personal problem-solving, and caution about answers outside science. These are actual stimulus features, not a finding that any particular feature caused the response. [S1](https://doi.org/10.1371/journal.pone.0017349.s001), [S4](https://doi.org/10.1371/journal.pone.0017349.s004).

The measured theory statements ask about evidential support and the best explanation of life's origins. The authors acknowledge ambiguity in origins wording. The six-item score also includes four author evaluations. Study 4 uses seven-point items, an eight-cell between-person design, and no neutral reading passage for the no-Sagan group. Its reported recruited N is 269; residual df 257 in an eight-cell saturated ANOVA implies 265 complete cases if that conventional model was used. The reason for that four-case difference is not supplied by participant records here. [Methods and Study 4 results](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0017349).

The content distinction matters independently of statistical significance. Acceptance of a theory of biological change can coexist logically with belief in a creator using secondary causal processes. Disagreement with a named author's argument cannot establish denial of every creator proposition. None of these endpoints separately measures one ultimate source, exactly one creator, rejection of created intermediaries, or the truth-directed reliability of recognition. Conversely, response sensitivity cannot by itself disprove those metaphysical propositions. This is an endpoint-mapping limit, not a verdict on biological evolution or on fitrah.

Even a correctly reproduced interaction would identify the experimental package's moderation of these ratings. Because Sagan content, an authoritative attribution and additional reading/delay were not independently crossed with matched controls, reanalysis of these same observations could not isolate meaning alone from all those alternatives. The paper itself acknowledges the delay limitation. A meaningful alternative supported by existing item-level data would be author evaluation versus theory endorsement; the exact contrasts and required covariance information are specified in `prospective_reanalysis_plan.md`.

## Precise obstruction and stopping condition

Missing are authenticated public participant-level Study 4 condition assignments and six item responses, inclusion/missingness decisions, a codebook, and scoring/model materials sufficient to settle case selection and standardization. S2's pooled means do not identify eight experimental cell means, variances or within-person item covariance. Reconstructing invented participants from them would add unverified assumptions, not recover the data. No such reconstruction was attempted.

No correction to these statistical entries was located in the inspected publisher record. The article's linked comment threads were also checked; correction-search details and any unrelated comments are recorded in `source_search_log.json`. This is not a universal absence claim or an assertion of historical novelty.

The bounded public-data branch ends here. Reopen only upon an authenticated, lawfully public, appropriately deidentified target dataset and adequate documentation, or separately authorized author outreach. No outreach or private-access request is implied. The prospective plan is not a preregistration: reported results were already known when it was written.

## Package boundaries

This folder contains original analysis, provenance hashes, lawful source links, a prospective plan, and reproducible aggregate arithmetic only. It excludes participant data, full copyrighted source texts and source-page images. Existing research files were not modified. No new empirical verification credit is assigned to the unavailable participant-level analysis.
