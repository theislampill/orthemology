# Actual source scoping is primitive recursive on the retained syntax codes

## Proved increment

`CodedScope.primrec_checkScope : Primrec₂ checkScope`

`CodedScope.checkScope_exact (n : Nat) (p : P01D.Poly) : checkScope n (Encodable.encode p) = decide (P01AC.Scoped n p)`

`CodedScope.computable_checkScope : Computable₂ checkScope`

These are genuine Mathlib primitive-recursiveness/computability theorems, not a claim inferred from executable Lean. The exactness theorem uses the existing EncodedCertificateSyntax instance. `Scoped` is the literal side condition used by `Rule.checkSide` for pi-introduction, conversion, pi-extensionality, and all-extensionality.

The proof exposes six arithmetic destructors for that exact encoding and proves their equations on actual constructors. It proves encoded application children are smaller than their parent code, then uses the existing Mathlib `Primrec.nat_strong_rec` theorem to justify the total recursive evaluator. No source `Primcodable` instance or decoder-computability assumption is added.

## Important limit

This evaluator is an extension of scoping to all natural inputs, **not a syntax validator**. A deliberate control proves `checkScope 1 0 = true`, while another proves that no source Poly encodes as zero. Thus the result must be composed with actual syntax validation/decoding before it can check untrusted source codes. The exactness theorem is restricted to genuine encoded source syntax.

## Remaining dependency graph and feasibility assessment

The endpoint remains r.e. of actual Joint/E certificate acceptance, followed by the source/semantic boundary. Four substantive pieces remain:

1. **Exact decoder/validity bridge.** Certify the actual derived encodings for Term, TypeCode, Poly, Ty, StepCert, RedCert, FiniteCert, LookupCert, Claim, Rule, and mutually recursive SerialCert/SerialCertList, plus the explicit PolyCert tree codec. It is enough to prove primitive-recursive code-level decoder/re-encoder behavior; plain Encodable roundtrip is insufficient. Every constructor uses finite tags/payload chains, and natural/tree/list subcodes decrease. The retained Term has six constructors, TypeCode four, Poly three, Ty seven. No theoretical obstruction was found. A sorted natural-code validator/normalizer using existing `nat_strong_rec` or `nat_omega_rec'` is a credible common recursion engine. It still needs exact correspondence to each actual decoder, including malformed payload/terminator rejection and cross-type fields. This is not proved here.

2. **Actual source transformations.** Certify the operations appearing in Rule.conclusion, Rule.premises, and checkSide: `abstract`, `pren`, `inst`, `tinst`, `tsubst (typeImages τ)`, `fin`, `finSupport`, `twkTel`, `theta`, `motiveAt`, and the concrete branch/induction templates. `TyScoped` is still open. Most are finite constructor recursion/composition. The principal nontrivial transport is binder-changing substitution: actual `mixed` takes functional environments and changes them under pi/sigma/all. A bare first-order fold on source code does not certify an arbitrary Nat→Poly/Ty function. The actual checker uses only specific finitely presented environments, so the needed theorem should specialize to finite environment codes plus binder counters and prove exactness to those uses. Do not assert computability for arbitrary functional substitutions.

3. **Five auxiliary checkers and 63 rule payload cases.** `checkStep`, `checkRed`, `checkFinite`, `checkPoly`, `checkLookup` are finite certificate recursion plus exact equality and the certified syntax operations. All constructor cases must be connected to the actual payload coding; the executable proofs alone do not provide this. This is substantial but finite, predominantly mechanical work after (1)-(2).

4. **Serialized certificate tree recursion and existential closure.** Prove actual `checkSerialized`/`checkCode` computable, or a total natural-code checker exactly equivalent to it. The explicit SerialCert/SerialCertList presentation eliminates nested datatypes, and recursive children decrease in code. Existing `nat_omega_rec'` already supplies the recursion engine; no giant new general computability theory is needed. Compose the real checker with the now-proved actual programType family map, then apply Mathlib existential/r.e. closure and the established certificate soundness/completeness. This last composition must wait for the actual checker theorem.

Conclusion: a uniform **recursion engine** exists in Mathlib and the Scoped proof validates its use on the exact codec. There is no existing one-line transport making arbitrary derived Encodable syntax and arbitrary recursive Lean code primitive recursive. The remaining work is genuinely a sizeable, finite formalization of codec validity, binder-sensitive syntax transformations, and rule cases. It is not another arithmetic optimization task and not a new foundational impossibility.

## Evidence paths

- Actual side conditions: `hase-joint-certificate-checker-20261010/CertificateRules.lean`, checkSide lines 206-269
- Actual rule syntax transformations: same file, conclusion/premises lines 76-203
- Actual auxiliary recursion: `hase-joint-certificate-auxiliary-20261010/AuxiliaryCertificates.lean`
- Actual encoded certificate grammar: `hase-joint-certificate-codec-20261010/{EncodedCertificateSyntax,EncodedCertificatePayloads,PolyCertificateEncoding,SerializedCertificateCodec}.lean`
- Library recursion combinators: retained Mathlib/Computability/Primrec.lean, nat_strong_rec around line 983 and nat_omega_rec' around line 1011
- Inspector logs preserve the exact source type constructors and binder-changing `mixed`/substitution definitions

## Verification and preserved diagnostics

Run `python hase-coded-scope-computability-20261010/verify.py`. It replays the exact upstream FamilyComputability source and three new modules in fresh output with Lean 4.19 `--trust=0`, under the final codec object pins. No full-baseline rebuild is performed. Positive controls exercise both variable-bound outcomes, atoms, both application branches, a larger valid bound, and the malformed-input limitation. Two false controls must fail: accepting a variable at the bound and ignoring an out-of-scope right child.

The central axioms are restricted to propext, Classical.choice, and Quot.sound. No custom axioms, admitted proofs, protected edits, source adoption, integration, or T20 closure are claimed.

All earlier attempts remain under diagnostics. Attempt 01 produced only linter warnings for names used solely in termination proofs; these were made explicitly unused. Attempt 02 exposed dependent-if simplification and an incorrect `decide_and` lemma-name guess; the final proof uses ordinary simplification with explicit child bounds. InspectSyntax/InspectMixed retain failed name/import probes as diagnostics, not accepted proof inputs.
