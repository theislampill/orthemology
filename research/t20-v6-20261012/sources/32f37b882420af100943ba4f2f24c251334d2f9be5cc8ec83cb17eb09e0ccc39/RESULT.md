# Canonical certificate-domain validity

## Exact scope

`CertificateCodeValidity.certValid : Nat → Nat → Bool` is primitive recursive. Its kernel-checked image theorem establishes exactly the existing `Encodable.encode` image for each of these 15 code sorts:

0 Term; 1 TypeCode; 2 Poly; 3 Ty; 4 Nat; 5 Tel; 6 StepCert; 7 RedCert; 8 FiniteCert; 9 PolyCert; 10 LookupCert; 11 Claim; 12 Rule; 13 SerialCert; 14 SerialCertList.

The new descriptor instantiations cover 96 retained certificate/payload constructors: StepCert 5, RedCert 2, FiniteCert 7, PolyCert 8, LookupCert 2, Claim 6, Rule 63, SerialCert 1, SerialCertList 2. These are not 96 logical rules or 15 judgment families. The retained six source judgment families remain unchanged. Main Rule plus auxiliary logical constructors total 63 + 24 = 87. The previously frozen core has 20 source syntax constructors (6 Term, 4 TypeCode, 3 Poly, 7 Ty); Nat and Tel are separate code auxiliaries.

## Construction and retained representation

The finite descriptor table records each retained constructor tag, exact payload arity, external field leaf wrapper, and child sort. Every one of the 96 constructor equations is proved against the unchanged source encoding, not an alternate encoding. Local shape reconstructs and compares the entire payload, including final terminator. Sorted recursive children then establish actual child image membership. Both SerialCertList.cons children are traversed. Core syntax and Tel invoke their already verified canonical validators; Nat's unchanged standard encoding has the full natural image.

The generic well-founded evaluator rejects a recursive child unless its code strictly decreases. Exactness needs child-decrease only on canonical parents, proved from actual constructor fields. This matters because a shape-correct malformed input need not itself satisfy those decrease hypotheses. The algorithm is total on all naturals and the primitive-recursive theorem has no computability premise.

The target is canonical encoded image membership. No claim is made that ordinary source `Encodable.decode` has identical behavior on arbitrary malformed/noncanonical inputs. No source `Primcodable` assumption or new global source instance is introduced. These image results provide the certificate-domain premise for a separately assembled canonical semantic checker; this package alone does not prove source derivability RE, compute the entire semantic checker, adopt source changes, or close T20.

## Verification status

`verify.py --init` creates immutable input pins and recompiles the complete selected additive dependency chain in a fresh output directory. Subsequent `verify.py` replays check those same pins before and after compilation. The successful `validation/AUTHOR_REPLAY.json` is the authoritative completion record: it records every source/object/log, exact retained import-object closure, axiom audits, all 96 runtime constructor witnesses, eight malformed runtime witnesses, and five semantic false-theorem rejections. `validation/FINAL_FREEZE.json` then pins the delivered sources, replay receipt and selected outputs. Frozen descriptor identities are separately checked against `validation/DESCRIPTION_FREEZE.json`; core and telescope packages remain independently frozen and accepted. Lean uses `--trust=0 -s 65536`, explicitly recorded in the receipt. No baseline rebuild is performed.

## Diagnostic preservation

`diagnostics/` retains unsuccessful proof elaboration and control attempts, including the superseded monolithic 63-Rule proof, broad unsupported-sort simplifier attempt, and control stack investigation. Final Rule correspondence is split into per-constructor helpers, all proved against the same frozen descriptor. The 15-sort support lemma uses explicit excluded equalities, avoiding a large simplifier split tree. No axioms or admitted goals replace these proofs.

The initial control stack failure came from concrete kernel reduction of malformed payload arithmetic. The final wrapper control uses symbolic `Nat.pair_eq_pair` reconstruction; no native-decision axiom is used. The larger recorded stack allowance is a resource setting only.
