# Additive scope diagnostic: the same ν fails at faithful Raw

10 October 2026. This is a separate small delta. The frozen homogeneous model, original sources, prior adversarial report, and prior manifests are unchanged.

## Checked result

FaithfulRawControl.nu_not_church_at_conversion proves that the particular ν used in the homogeneous Henkin model is not related to itself at

    Arrow (Arrow Conv Conv) (Arrow Conv Conv).

Thus admitting conversion itself as a quantified carrier already rejects this ν. The test does not need an arbitrary mixed PER.

## Exact witness

Let skk = S K K and seed = a0 a0. Compatible conversion proves that I and skk are related at Arrow Conv Conv: for every convertible x,y, I x converts to x, x converts to y, and skk y converts to y.

The seed is a stuck raw normal form. It is a legitimate self-related element at Conv, but neither an atom value nor a function WHNF. Therefore no ν case rule fires on that seed. Since I and skk themselves are normal, these are distinct normal forms:

    ν I (a0 a0)
    ν (S K K) (a0 a0).

Canonical CaseOperational.confluence proves that distinct normal forms cannot be convertible. This violates the Church relation at the related input endomaps I and skk and the same self-related seed.

The file also checks seed_neither_tag and the intermediate normality/nonconversion claims. The endomap relatedness proof has no axioms; the nonconversion and Church-rejection claims use only propext, Classical.choice, and Quot.sound through the checked canonical confluence proof.

## Meaning and limits

For this particular witness and the standard conversion-based arrow semantics, changing Raw to top is essential. A sound interpretation with Raw=Conv must admit that formed carrier to All instantiation, where this ν fails its Church membership test.

This is not a proof that all Raw-faithful models validate W, not a new model campaign, and not an objection to the already explicit Raw=top choice of the homogeneous model. It isolates the witness's semantic scope. The independent syntactic nonderivability consequence of a sound Raw=top model is unaffected.

## Replay

Run python homogeneous-per-adversarial-20261010/replay_faithful_raw.py. The script checks the standalone delta manifest, freshly compiles the frozen canonical operational carrier and FaithfulRawControl with Lean 4.19.0 --trust=0, and writes validation/FAITHFUL_RAW_REPLAY.json. It does not modify or rebuild any source baseline or the frozen predecessor checks.
