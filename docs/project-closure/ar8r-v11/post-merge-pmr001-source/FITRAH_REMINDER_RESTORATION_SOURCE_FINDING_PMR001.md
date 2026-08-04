# PMR-001 source finding — fiṭrah, impairment, reminder, and restoration

## Authority classes

```text
al-ʿUjayrī:
  contemporary Atharī synthesis with explicit Ibn Taymiyyah locators

El-Tobgui:
  secondary scholarly reconstruction of the Darʾ

current orthemology/daee files:
  implementation correspondence and honesty boundary

Arabic-primary verification:
  NOT PERFORMED IN THIS TRANCHE
```

## Exact source findings

### 1. Latent normative disposition is not identical to presently manifested recognition

Al-ʿUjayrī presents recognition of the Creator as innate while also allowing the disposition to be corrupted, obscured, or inactive. His Chapter 1 states that analysis and proof can be required to **remind** a person of the original predisposition rather than create it from nothing. See the attached Markdown snapshot at lines 188–225, especially 190, 200, 202, 210, and 223.

This yields a typed distinction:

```text
latent normative disposition
≠ present occurrent recognition
≠ articulated proposition
≠ inferential proof
≠ behavioral assent
```

### 2. Impairment and restoration are state-sensitive, not merely output-sensitive

Al-ʿUjayrī compares corruption of the disposition to illness that makes the sweet appear sour or produces double vision. The relevant remedy removes the impairment; a correct verbal answer alone does not show that this condition changed.

El-Tobgui reconstructs fiṭrah as an “original normative disposition,” not merely one isolated logical axiom. He describes sound fiṭrah as helping judge premises and arguments and explains that doctrinal habituation, whim, interest, faulty supposition, and other defects can pervert it. He also states that a corrupted fiṭrah may be resuscitated through sound reasoning, spiritual purification, or other means, after which it may recognize truth in a healthy way. See the attached dissertation snapshot at lines 4395–4417 and 4806–4832.

This supports the following source-relative transition vocabulary:

```text
original normative disposition
→ impairment/occlusion
→ reminder or corrective means
→ rehabilitation to a healthy condition
→ renewed recognition
```

It does not establish that every real human state can be observed or mechanically diagnosed.

### 3. Reason, report, sense, and fiṭrah are not interchangeable

El-Tobgui's reconstruction distinguishes ḥiss, khabar, and ʿaql, with fiṭrah underlying and normatively conditioning their proper function. Al-ʿUjayrī likewise allows reasoning to remind or deepen while assigning revelation a further role in detailed knowledge of the divine attributes.

Therefore a daee or orthemology implementation must not reduce the target to:

```text
one scalar confidence;
one propositional output;
one route score;
one metaortheme;
or one transcript-level signature.
```

## Current-main implementation correspondence

At repository authority `cc91f41fec364ea3910b80d57252bb1e0a050278`, current main already preserves several correct boundaries:

- `applications/daee-epistemics/DAEE-ORTHEMOLOGY-CROSSWALK.yaml` distinguishes inferred profile, actual interior condition, runtime closure, rendered response, and actual uptake/restoration.
- `applications/daee-epistemics/NOETIC-FIELD-DYNAMICS.yaml` states that runtime improvement does not entail result truth or human restoration and that fiṭrah is not measured from discourse.
- `applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md` describes fiṭrah as a normative orientation/proper-function ground rather than a measurable coordinate.
- `applications/daee-epistemics/CORRECTIVE-TRANSITION-FIXTURES.yaml` includes hostile fixtures rejecting closure-as-restoration.

The post-merge source finding therefore does **not** overturn the current repository. It strengthens the interpretation of why those separations are required.

## Status delta

```text
surface S25 daee target/kernel/source-target:
  PREMISE_SET_ENRICHED

surface S27 burden landing/reread/causality:
  INTERPRETATION_STRENGTHENED

surface S28 meta-noetic restoration:
  INTERPRETATION_STRENGTHENED

whole-stack daee disposition:
  UNCHANGED — PARTIAL_CROSS_LAYER_BINDING
```

The whole-stack disposition remains unchanged because no fresh file-level audit of the exact later daee snapshot, no proxy validation, and no causal intervention study was performed.

## New formal burden exposed

A future stable-restoration theorem must type at least:

```text
TargetDisposition(q)
LatentOrActivated(q)
ImpairmentSet(q)
ReminderIntervention(i)
StateTransition(q,i,q')
RecognitionOutcome(q')
SourceCompatibility(q')
CausalLanding(i,q,q')
RereadClosure(q')
```

It must not infer `StateTransition` merely from a correct output. This burden feeds PMR-002/PMR-003 stable-restoration work.

## What this finding establishes

- source support for distinguishing latent disposition, impairment, reminder, rehabilitation, and recognition;
- a stronger source rationale for current daee honesty boundaries;
- a dependency for future restoration formalization.

## What it does not establish

- Arabic-primary wording;
- a neutral psychological theory of all humans;
- an observable proxy for fiṭrah;
- causal efficacy of any daee operation;
- held-out learned-system restoration;
- a world-directed theological conclusion.
