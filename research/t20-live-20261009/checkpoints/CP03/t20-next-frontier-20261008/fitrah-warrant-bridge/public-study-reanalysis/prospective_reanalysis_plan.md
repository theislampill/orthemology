# Focused secondary data reanalysis plan

Target: Tracy, Hart and Martens 2011 Study 4. Status: not executed, because an authenticated usable public participant dataset was not located. This is a prospective specification for possible secondary-data computational reanalysis, written after the published findings were known. It is neither a preregistration nor a new human experiment.

## Data gate

Require a release bound to DOI 10.1371/journal.pone.0017349 and specifically Study 4, through an author, publisher or institutional provenance chain. Record exact public URL, version, license or reuse conditions, download date, SHA256, units and data dictionary. Before analysis, verify that participant identifiers are nonidentifying study keys and that no names, contact details, IP addresses or revealing free text are included. Do not republish participant rows. Stop if lawful provenance or appropriate deidentification cannot be established.

Required fields are mortality versus dental-pain assignment, Sagan versus no-Sagan assignment, Behe-IDT versus Dawkins-ET assignment, four author-evaluation ratings, two theory ratings, and original inclusion and item-missingness indicators. Require documentation of randomization and scoring, which sample supplied each standardization mean and SD, and how missing items were handled. Check recruited N = 269 against the N = 265 implied by reported model df under the ordinary saturated eight-cell model; identify the actual reason from documentation, not an invented exclusion rule. The later follow-up subset is not a pre-treatment baseline and should not replace the original sample.

## One substantive question

Does the Sagan-associated change in the mortality effect appear in theory endorsement itself, or is it appreciably different in author evaluation? Do not substitute a test of one simple effect for a moderation contrast, and do not treat significant versus nonsignificant p-values as a significant difference between outcomes.

Let M = 1 for mortality and 0 for dental pain; S = 1 for Sagan and 0 for no Sagan; T denotes the assigned theory. For endpoint E, define the mortality contrast within a cell as d(E,S,T) = mean(E | M=1,S,T) minus mean(E | M=0,S,T). The IDT framing contrast is D(E,IDT) = d(E,1,IDT) minus d(E,0,IDT). The reported three-way interaction corresponds to D(E,ET) minus D(E,IDT), up to coding/sign. These are different estimands.

First reproduce the documented six-item and two-item standard-score analyses, preserving all eight cells and the reported model. Independently show two theory items averaged on the original 1–7 scale and four author items averaged on that same scale. Display all cell counts, means, SDs, missingness counts, contrasts and confidence intervals. A negative D(theory,IDT) is a framing moderation in the proposed direction; a reversal additionally requires reporting both component directions and their uncertainty. A significant three-way contrast alone does not establish two individually significant, oppositely directed IDT simple effects.

The single consequence-relevant alternative is evaluated by the endpoint difference D(theory,IDT) minus D(author,IDT). Estimate that difference with the actual within-participant endpoint covariance, using a model that represents the two endpoint types as repeated outcomes or an equivalent participant-cluster resampling procedure. Do not infer it from published marginal t/F values. A difference could support endpoint specificity; its absence would not establish exact equivalence without a justified equivalence margin. Retain separate direct-theory and composite results whatever their direction.

Use ordinary two-sided inference, recording rather than opportunistically substituting published directional conventions. Identify the primary IDT theory framing contrast and the one endpoint-type contrast as the small planned family and report both raw and Holm-adjusted p-values if hypothesis tests are used. This choice is a prospective sensitivity design, not a retroactive claim about the authors' prespecified family. Published numerical reproduction remains separate from that alternative-analysis choice. No exploratory selection across populations, endpoints or exclusions may be represented as confirmatory.

## Limits that reanalysis cannot remove

There is no isolated manipulation of meaning versus scientific-authority content or matched reading delay in these observations. Item reanalysis cannot adjudicate all mechanisms of the Sagan package. Nor can these ratings identify recognition of exactly one original source, discriminate that proposition from created secondary causal processes, or test the recognized content's metaphysical truth or epistemic warrant. More precise statistics do not create an unmeasured construct.

## Output if the data gate is later passed

Release code, environment versions, provenance hashes and aggregate results, with item mapping and exclusion accounting. Label the work secondary-data computational reanalysis. Do not call it an independent experiment, replication with new participants, or external human validation. If the data gate fails, report the exact unsatisfied condition and stop rather than fabricate observations.
