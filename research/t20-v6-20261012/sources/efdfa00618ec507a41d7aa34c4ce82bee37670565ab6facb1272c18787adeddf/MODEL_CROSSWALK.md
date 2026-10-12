# Semantic-owner crosswalk for the directive/normative qualification

## Result

The inspected model already **allows three distinct semantic owners**. It explicitly separates a normative standard from an actor's represented/adopted standard, and it keeps factual correctness, evidence support, decision-time justification, authorization, and action separate. Nothing inspected forces a mistaken source-law attribution to make every practical-duty claim false.

For this particular application, a small **claim-indexed registration** is still needed: identify the source-law proposition, the adopted criterion/attribution, and the evidence-relative practical-duty proposition, with separate truth conditions, evidence, time, and warrant. This is an application schema using existing slots, not a correction to the core ontology or a new mathematical result. Its third proposition requires substantive normative support; a declared analysis, a passed validator, or V3e alone does not establish that support.

This is a targeted check, not an exhaustive absence claim about the repository.

## Source pin and scope

Repository: theislampill/orthemology, commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`.

Local core, H-formalisation, and companion files were the copies supplied for this task in `constructive-t20-20261009/sources/`. H-formalisation and companion Git blob hashes match the repository pin. The supplied core has one additional trailing LF; all substantive text and cited line numbers match. An exact pinned copy is saved as `sources/orthemic-core-pinned.md`. DAEE documents, Decisions 0025/0033, and the T07 criterion section were retrieved at the exact repository pin through the connector. Byte identities and read boundaries are recorded in `MODEL_INPUT_BINDINGS.json`. The current header/status strings are reported as source provenance only; old review/merge holds are not treated as present philosophical conclusions.

The primary division's interpretation and normative appraisal belong to the parent analysis. The electronic item is not treated as the complete chapter. No primary-text discovery or independent primary verification is claimed here.

## Exact model support

### 1. Normative type versus represented/adopted criterion

[DAEE meta-noetic note](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/applications/daee-epistemics/META-NOETIC-MEMETICS-AND-DYNAMIC-ORTHING.md), §1, lines 18–31:

- μ is the repeatable metaortheme type, described as the normative standard.
- μ̃(α,t) is the actor/institution's represented, adopted, or embodied version.
- μ̄(e,j) is the episode-local case binding; execution is a fourth separate object.
- Exact boundary: “μ̃ is neither the normative type, nor a case binding, nor the actor's whole noetic profile.”

Its §3, lines 51–60, explicitly makes type history, represented-version history, and case-token history different histories. An edge labelled replacement therefore does not itself say which semantic owner changed.

[DYNAMIC-CROSSWALK.yaml](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/applications/daee-epistemics/DYNAMIC-CROSSWALK.yaml), `bearers[mu-tilde_{alpha,t}].non_claims`, adds “not ground truth”. Decision 0025 §1 gives the same separation and calls the represented bearer an application-level object rather than a new core primitive.

[Dynamic companion](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/companion/dynamic-orthing-noetic-learning-and-orthability.md), §2, local lines 29–43, additionally separates inferred placement (belief, never ground truth), objective result O*(m;A), and truth linkage.

**Consequence:** (a) and (b) must not be collapsed. However, not every source-law proposition is a metaortheme. If the proposition concerns what a source commanded or forbade, register it as a claim; use μ only for a qualifying higher-order configuration.

### 2. A source-law attribution and a practical-duty claim can have different truth values

[Core formalization](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/orthemic-core-formalization.md):

- §2.2, lines 152–166: H is ordered typed evidence; w is authority to act, “distinct from evidence and from executor identity”; A owns the declared analysis; Q records each proposition, target/version, property class, success surface, evidence, relevant warrant, verification status, and non-claims. Claims and residual obligations are explicitly different.
- §3.2, line 310: the worked warrant-state distinction is “authorized vs factually established”, with states authorized/established/both/neither; its policy must never launder either into the other.
- §4.1, lines 415–430: V1 is claim-wise truth under the analysis; V2a asks whether available evidence meets the declared bar.
- §4.1, lines 507–511: V3e concerns reasonableness “given exactly the evidence then available” under a declared decision standard. It is decision-time indexed.
- §4.1, lines 512–514: V4a concerns route admissibility under constraints in force.
- §4.1, lines 553–566: pathway adequacy excludes V1 and factive token truth linkage.

**Consequence:** a false source-law claim and a true evidence-relative-duty claim can coexist as separately owned propositions. An episode-wide conjunction can fail because the first claim is false without making the second claim false. Conversely, reasonable belief or authorized action is not automatically a genuine duty. V3e, w, and V4a should not be renamed into duty truth.

### 3. Several standards are possible, but the application must supply their relationship

Core §3.1, lines 279–300, distinguishes the higher-order state configuration from its conditional meta-policy and limits governed components to O/I/E/D/R/V/W. Objectives, task, and the governance meta-level are excluded. Core §3.4, lines 338–376, permits multiple configurations, demands declared precedence for genuine conflicts, distinguishes existence/authenticity/recovery/authorization/current force of recovered instructions, and allows undetermined selectors with declared conduct.

Core §3.4, lines 377–388, blocks inflation: a candidate μ must govern a named component, have in-advance competing states, make a counterfactual operational difference, and not be a first-order ortheme or tunable policy parameter in disguise.

**Consequence:** evidence-relative practical duty can be an object-level normative claim under the governing doctrine, with an associated policy. It does not require a third species of metaortheme. A general higher-order rule about acting under available evidence may qualify separately if it meets the existing test.

### 4. Revision must preserve which owner and time changed

[Decision 0033](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/decisions/0033-governed-corrective-search-and-transition-witness.md), §§2–4:

- Admissible correction is not strict soundness.
- The witness separately records governing types, represented standards, case tokens, evidence, delta, before/after states, verdicts, and non-claims.
- A single episode cannot silently revise the global standard.
- Fast episode correction and slow standard/ecology/analysis revision remain distinct.

[H formalisation](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-formalisation/orthing_formalisation_v1.md), Definition 6.4 and Theorem 6.5, local lines 370–395: active state differs from retained history; replacement requires linked successors; supersession requires lineage; semantic validity additionally requires substantive truth and applicability. Exact boundary: “A shape check cannot produce that truth.”

**Consequence:** changing the adopted criterion or current evidence-relative duty need not change the underlying source-law proposition. Conversely, an unchanged source norm does not imply unchanged present applicability. A historically correct duty claim indexed to t must not be silently rewritten as though it were never true when circumstances change at t+1.

### 5. Retained-standard repair is not full-authority-basis replacement

[T07-CRITERION-V3](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/experiments/orthemology-v5-successors/groups/t07-technical/README.md#t07-criterion-v3), “Premises” and “Limits”, retains the exact-byte fidelity standard and identified source while changing the acceptance criterion. Its explicit limit is: “Retained-standard repair does not resolve Candidate E full-basis authority replacement.” It also separates criterion installation from document repair, and copied adequacy from recipient-specific permission.

**Consequence:** a correction of the represented criterion, or of its attribution to the source, is not automatically replacement of the full norm-fixing basis. The new practical-duty owner should state whether it is governed by a retained evidence-relative norm. This source distinction is enough for the present comparison; no missing general normative-replacement calculus is inferred, and no historical Candidate E hold is used to settle the present philosophical question.

## Compact possible application interface

Use three separately identified Q entries and the existing references:

1. **Source-law target claim.** Exact source proposition; source identity/authentication; normative analysis and school scope; target occurrence; actual source-law status; supporting evidence and defeaters. Do not infer it from μ̃.
2. **Represented/adopted criterion or attribution.** Actor, time, criterion content/version, carrier/provenance, exact proposition the actor attributes to the source, and how it directs conduct. Use μ̃ for a standard, inferred placement for a particular belief.
3. **Evidence-relative practical-duty claim.** Actor, decision time, available evidence/capacity conditions, action or restraint, normative ground for why those conditions impose a duty, jurisdiction/scope, defeaters, and separate truth/support statuses. Link it to the source-law target without defining their truth values to agree.

Add an explicit relationship record: what kind of relation connects them (attribution, support, application, authorization, or replacement); what changes under newly available or withdrawn evidence; what remains historically true; whether the underlying source rule itself changed; and which current actions follow.

Required discriminator: register a case with source attribution false, represented criterion present, practical-duty claim supported by its own applicable norm. Do not derive the third entry merely from the first two. Register a contrasting case where the actor's adopted criterion is present but the practical duty lacks a valid normative ground. These are application tests, not a request to invent a new theorem.

## Bounds

- No inference from source-law error to universal practical illegitimacy.
- No inference from blamelessness/reasonableness to duty, or from duty to correct source attribution.
- No inference from declaration or schema validity to genuine normativity.
- No diagnosis of any person's motive, culpability, or interior state from these formal records.
- No core edit, protected repository edit, external upload, or new mathematics.

