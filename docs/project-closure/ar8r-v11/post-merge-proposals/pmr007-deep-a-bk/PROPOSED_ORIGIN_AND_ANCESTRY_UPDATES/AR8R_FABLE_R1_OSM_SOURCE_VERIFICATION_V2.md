# AR8R Fable Round 1 — OSM source verification V2

## Authority and custody

```text
research identity:
AR8R-FABLE-R1-OSM-SOURCE-VERIFICATION-V2

repository authority checked:
428187cebf7644ff8bf9522455a560eb82d35964

source:
Sun et al., "Learning produces an orthogonalized state machine in the hippocampus"
Nature 640 (2025), DOI 10.1038/s41586-024-08548-w

local access-copy SHA-256:
0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814

source role:
PRIMARY EMPIRICAL / COMPUTATIONAL ARTICLE ACCESS COPY

experiment reproduced:
false

official code reproduced:
false

status:
POST_MERGE_SOURCE_VERIFICATION_FINDING
EXTERNAL_REVIEW_OPEN
OWNER_ADOPTION_PENDING
```

This pass addresses `FABLE-R1-B08`: it checks the quarantined source-specific
notes in `AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md` against the accessible article
bytes. It does not adopt repository changes, reproduce the experiment, or make
Sun et al. an authority for orthemology, noetic structure, proper function, or
metaphysics.

Line locators below refer to the 1,959-line Markdown access copy named above.

## Claim-by-claim adjudication

### OSM-Q1 — imposed world state and fixed-speed Markov idealization

**Quarantined wording:** the world state is imposed, finite, and Markov under a
fixed-speed idealization.

**Source evidence.** At line 1805 the paper defines the combination of position
and trial type as the world state `z`, says that it is not directly observable
to the animal, and says its sequence has the Markov property under the
assumption that the animal always travels at fixed speed. Lines 1807 and 1817
use a discretized 23-step model sequence and a finite symbol alphabet.

**Disposition:** `VERIFIED_WITH_NARROWING`.

```text
verified:
- position + trial type is the authors' modelled world-state variable;
- the Markov claim is explicitly conditional on fixed-speed travel;
- the implemented comparison models use finite discretized sequences.

narrowed:
- the biological environment is not thereby proved to be a finite-state
  Markov process at all spatial, behavioural, or physiological resolutions;
- "imposed" means specified by the task/model analysis, not unreal or merely
  conventional in the experiment.
```

### OSM-Q2 — animal observation versus model alphabet; serialization

**Quarantined wording:** the animal-facing sensory stream and model symbol
alphabet differ; simultaneous visual-cue/reward information is serialized by a
model convention, and the convention is trajectory-load-bearing.

**Source evidence.** Lines 1761 and 190 describe the animal's continuous
virtual-reality task. Line 1807 specifies a seven-symbol one-hot alphabet and
serial sequences in which a reward-cue symbol and water symbol occupy distinct
steps. Line 1801 explicitly reports four alternative encodings: visual then
reward, reward then visual, and combined reward/visual codes. It reports that
all four final learned transition graphs match while the learning order differs.
Extended Data Fig. 8(c–d), lines 1938–1941, reports the corresponding reversals
or loss of the animal-matching pre-R2/pre-R1 order.

**Disposition:** `VERIFIED_AS_MODEL_CONVENTION_WITH_SOURCE_REPORTED_SENSITIVITY`.

The source supports the stronger and more precise statement:

> The headline trajectory comparison is a property of the tested CSCG together
> with a chosen sensory-sequence encoding; the paper itself demonstrates that
> changing the visual/reward encoding can preserve the final learned transition
> graph while changing the decorrelation order.

This does not show that the paper's default encoding is unreasonable, and it
does not erase the source-reported result for that encoding. It blocks treating
the learning-order match as algorithm-only or biological-mechanism
identification.

### OSM-Q3 — what "orthogonalized" measures

**Quarantined wording:** orthogonalization is formally decorrelation; no
subspace principal angles are computed; the reported angle is only a monotone
reparameterization of correlation; centred near-zero correlation can coexist
with raw nonnegative overlap.

**Source evidence.** Lines 206 and 1421–1423 use population-vector correlation
to quantify representational similarity. The Methods section at line 1789
(`Population vector analysis`) defines each vector from mean fluorescence over
neurons in a spatial bin and forms a cross-correlation matrix with Pearson
correlation coefficients. Extended Data Fig. 5, lines 1915–1918, separately
reports population-vector angles that qualitatively mirror the correlation
results. The access copy contains no reported subspace-principal-angle
analysis.

**Disposition:** `PARTIALLY_VERIFIED; TWO SUBCLAIMS RETIRED_OR_RECLASSIFIED`.

```text
verified:
- Pearson population-vector correlation is a principal reported measure;
- PV angles are also reported and said to qualitatively mirror correlation;
- no subspace principal-angle computation is reported in the access copy.

not established from accessible source bytes:
- the exact formula making PV angle a monotone reparameterization of the
  Pearson correlation;
- the assertion that near-zero reported values coexist with substantial raw
  overlap in the actual data.

reclassification:
- the raw-overlap statement may be retained only as an independent mathematical
  countermodel about centred correlation, not as a source finding;
- the monotone-reparameterization sentence must be retired unless the exact
  code or supplementary definition is located.
```

### OSM-Q4 — neural "state machine" and transition matrices

**Quarantined wording:** the state-machine interpretation is based on
representation geometry; no transition matrix is estimated from neural data;
the topological reading is qualitative.

**Source evidence.** Lines 186 and 1423 interpret day-to-day neural geometry as
consistent with an OSM and compare it with the CSCG's learned state transition
graph. Lines 1419 and 1805–1809 describe transition-matrix estimation for the
CSCG/HMM model. The neural analyses reported in the access copy use
population-vector correlations/angles, UMAP, behavioural measures, and
single-cell tuning; no neural transition-matrix estimator is described. The
paper itself cautions at lines 1929–1932 that UMAP depends on hyperparameters
and that its main conclusions are driven by PV angles and correlations.

**Disposition:** `VERIFIED_WITH_ABSENCE_SCOPE`.

The defensible claim is:

> No transition matrix estimated directly from neural recordings is reported in
> this article access copy; the transition graph belongs to the computational
> CSCG comparison, while the biological OSM claim is an interpretation of
> longitudinal representational and behavioural structure.

This is not a claim that no dynamical information exists in the recordings or
that a state-machine interpretation is illegitimate.

### OSM-Q5 — alleged three-element/3.7-bit trajectory capacity

**Quarantined wording:** the trajectory is a three-element order statistic with
at most 13 values and about 3.7 bits of capacity.

**Source evidence.** Figure 4(j), lines 1414–1417, reports normalized threshold
crossing times for key regions. Extended Data Fig. 8 reports continuous
correlation trajectories, threshold times, and several encoding conditions.
The source does not reduce the complete trajectory evidence to one three-item
order statistic, and no 13-value or 3.7-bit capacity statement occurs in the
access copy.

**Disposition:** `RETIRED_AS_UNSUPPORTED_OVERREDUCTION`.

The paper does use a low-dimensional ordering/timing summary for one comparison,
but its evidential object also includes longitudinal matrices and continuous
threshold-crossing times. The `3.7 bits` conclusion is not source authority and
should not remain a load-bearing criticism.

### OSM-Q6 — intervention and causality

**Quarantined wording:** there is no causal intervention on the nervous system;
biological results are observational and ablations are model-side.

**Source evidence.** The Methods describe longitudinal calcium imaging during
behavioural training and environmental/task alterations. Lines 1419–1423 and
1801–1869 describe computational model comparisons, architectural changes,
objectives, and sensory-sequence variants. The biological manipulations change
visual cues and track geometry (lines 1545–1613 and 1761–1771); no neural
stimulation, lesion, or identified-plasticity-rule intervention is reported.
The Discussion explicitly calls mechanistic plasticity rules a future target
(lines 1513–1543 and 1609–1613).

**Disposition:** `VERIFIED_WITH_SCOPE`.

```text
verified:
- no direct neural causal intervention is reported in this access copy;
- the biological evidence is longitudinal/observational under behavioural and
  environmental manipulation;
- computational model variants are interventions on models, not the animal's
  neural mechanism.

not implied:
- the data are causally uninformative in every sense;
- task manipulations are observationally irrelevant;
- the CSCG interpretation is refuted.
```

## Source-result classification after verification

| Source/result | Verified disposition relative to current owners |
|---|---|
| Sensory aliasing separated by sequential context | `DIRECT_BOUNDED_EMPIRICAL_AND_MODEL_INPUT`; does not identify an ortheme or world state |
| Endpoint representational match versus learning trajectory | `GUARDED_INSTANCE_OF_ENDPOINT_PATHWAY_NONIDENTITY`; pathway here is a learning trace, not the repository's factive reasoning-path predicate |
| High prediction performance without global OSM-like geometry | `SOURCE_REPORTED_NONSUFFICIENCY_AT_TESTED_MODEL_SCOPE` |
| CSCG uniquely matches endpoint and order among tested default comparisons | `SOURCE_REPORTED_COMPARATIVE_RESULT_WITH_ENCODING_SENSITIVITY` |
| Continuum/plasticity of single-cell roles | `SOURCE_REPORTED_IMPLEMENTATION_BOUNDARY`; blocks immutable cell-type localization |
| Novel-cue and stretched-track adaptation | `SOURCE_REPORTED_SMALL_N_BOUNDED_ADAPTATION`; no restoration or general transport theorem |
| Neural latent state / CSCG clone / orthemic object | `PRINCIPLED_TYPED_NONIDENTITY` as a project inference |
| PV correlation/angle versus repository geometry predicate | `PARTIAL_MEASUREMENT_CORRESPONDENCE`; no exact reduction established |

## Correction to N3

The source verifies N3's encoding-sensitivity core but not its strongest
rhetoric.

```text
retained:
- alternative sensory encodings preserve the final learned transition graph;
- the decorrelation order changes with encoding;
- trajectory agreement cannot be attributed to the learning algorithm alone;
- trajectory match does not identify a biological mechanism.

retired or narrowed:
- "same endpoint" must mean the reported final learned transition graph, not
  identity of every final probability, representation, or biological state;
- the 13-value / 3.7-bit trajectory-capacity reduction is unsupported;
- near-zero correlation as architectural inevitability requires a separately
  frozen mathematical argument, not source attribution.
```

## Burden effect

```text
FABLE-R1-B08:
DISCHARGED_FOR_THE_QUARANTINED_NOTES_AT_ACCESS_COPY_SCOPE

remaining source burdens:
- exact PV-angle formula or code location, if the monotone-transform claim is
  to be retained;
- reproduction of official analysis/code;
- reproduction of biological or model results;
- external specialist review of this post-merge verification.

repository adoption:
PENDING

milestones completed:
0

integrated champion:
NONE

meniscus:
MENISCUS_NOT_REACHED

natural closure:
NOT_REACHED
```

## What was not transferred

The source supplies no premise for proper function, truth-linked normativity,
human noetic restoration, transcendental orthability, Necessary Being, unity,
agency, divine attributes, Speech, revelation, or empirical validation of
orthemology.
