# Fresh independent review of recovered endpoint bytecode

**PASS_SCOPED: source-bound ordinary argument and finite execution checks.** No gap was found in the stated initialized-cache, binary-input, nonnegative-integer-fuel contract. This does not restore the unavailable fourth-tranche Lean closures or their former seals.

## Exact reviewed material

The author ZIP `Endpoint_Source_Recovery_20261001.zip` has SHA256 `b86ebec4ba4cc5c6aa15e713de975d62269c83d0bdddc564dd5240075936d1e2`. All seven manifest-listed payloads were hash-verified after extraction. The historical identity file is exact: `NATIVE_ENDPOINT.json` SHA256 `a77d05474ebd510b30cf52b34828a407dadce962359c678701eba6a9ebda7c7b`. The retained codec is `prcodec.py`, SHA256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`.

The historical JSON's reference to separate Lean proofs is preserved only as historical source text. The present review does not adopt it as recovered kernel evidence. The separately recovered `RepairTestingReduction.lean` is not represented as a freshly compiled dependency closure and is not needed for this endpoint execution argument.

The author checker was replayed in a copied area and reproduced its receipt byte-identically. A separately written parser and recursive interpreter then checked the actual natural-number indices, rather than accepting a desired output stream as a premise.

## Decoded source and adapter boundary

The 59-byte cache program has arity one and output register 5. Its two sequence nodes and three assignments perform, in order, for input bit b:

1. register 2: L := L × (b×0 + (1−b)×2)
2. register 4: R := R × (b×1 + (1−b)×1)
3. register 5: output := indicator(L+1≤R)

Subtraction is natural truncated subtraction. The declared stateful adapter initializes `(L,R)=(1,1)`, injects each acquired bit as the natural 0 or 1, executes the source, and carries registers 2 and 4 to the next call. Its output is read after both updates.

The 105-byte prefix program has arity two: stage k and the sentinel encoding of exactly k+1 acquired bits. It resets L and R to one, copies the word, executes k+1 low-bit updates while dividing the word by two, and applies the same final comparison. It excludes the sentinel. Both complete decoded trees are retained in this packet.

The source programs produce decisions after receipts. The full report policy additionally prepends one false action before receiving any bit and maps false to q=1/2 and true to q=5/8. These initial-action, readout and carried-frame conventions are part of the stated adapter. They are not silently inferred from a standalone bytecode index.

The original arity-two indexed evaluator returns its documented zero value on the arity-one cache code. Conversely, calling the prefix code with a cache-style frame supplies neither its stage/word interface nor its initialization semantics. The two programs are extensionally equal only through their specified adapters, not through arbitrary interchange of APIs.

## Ordinary pointwise proof

For every finite binary input prefix of length m, induction on the cache update gives R=1 and:

- L=2^m if all acquired bits are zero
- L=0 if any acquired bit is one

Therefore L+1≤R holds exactly in the second case. In the prefix program, after j loop iterations the same assertion holds for the processed low-bit suffix, and the word register has been divided by 2^j. The multiplication factors commute, so reverse processing order does not change whether a one is present. After exactly m iterations the remaining word is the sentinel 1. Thus both decoded programs compute the seen-one predicate for every finite valid prefix.

The full action at index n uses exactly the first n receipts; index zero is the separate initial false action. Equality at every finite index gives equality of the infinite streams for every binary input. Each coordinate depends on a finite prefix, so the maps are measurable and have equal pushforwards under any specified input measure. This is an ordinary induction/law argument, not a recovered universal Lean refinement theorem.

## Literal source/scoring connection and costs

The retained third-tranche `BernoulliPrefixLaw.lean` defines `auditSourceLaw alpha` as the infinite product of its Bernoulli coin measures. `AuditContractBinding.lean` binds that same selector distribution to the weighted expected charge. Both reference files were independently compared to the retained third-tranche master manifest before copying; their identities are recorded in `evidence/SOURCE_LAW_REFERENCES.json`.

For disturbance 1/4, the exact two all-truth excesses are:

| Source/scoring weight | Report | Zero-truth excess | One-truth excess |
|---|---:|---:|---:|
| 0 | 1/2 | 0 | 0 |
| 0 | 5/8 | 9/64 | −7/64 |
| 1/2 | 1/2 | −5/32 | 3/32 |
| 1/2 | 5/8 | −1/64 | −1/64 |

Hence, within these two literal report actions, false is weakly correct exactly at weight zero, and true is strictly correct at weight one half. The counted failure is failure of the prescribed expected-score inequalities for some truth, not a guarantee that every realized selector draw improves its individual loss.

At weight zero, every receipt is zero almost surely, so all reports are false and the total failure count is zero. At weight one half, action n fails exactly when its n receipts are all zero. The probability is 2^(−n), including probability one for the initial action. Tonelli and the geometric series give total expected failures

    sum over n≥0 of 2^(−n) = 2.

Thus the actual supplied source/scoring fixture has ordinary expected costs `(0,2)`. The finite execution check gives `2047/1024` through action ten; it does not infer the infinite total by extrapolation. Omitting the initial action changes the limiting count to one and is a rejected alternative convention.

## Countable output and computation-clock scope

Every output stream is all false forever, or consists of finitely many false actions followed by true actions forever. This is a countable image. Its measurable pushforward is therefore supported on countably many singletons under either actual source law, and its nonatomic mass is zero. This ordinary argument separates output-law defect from literal repair; it does not restore a lost fourth-tranche formal composition.

The cache tree takes exactly five statement tasks. The prefix tree has nine outside-loop tasks, m+1 repeat tasks and five body tasks per iteration, totaling 6m+10 for m≥1 acquired bits. These follow from the decoded tree structure and are corroborated by both interpreters. Fuel claims concern nonnegative integer fuel and natural-number register frames. The generic research `run_frame` helper is not a validated arbitrary-Python-object API.

These task counts exclude expression evaluation, bit complexity, input injection, initialization, codecs, report readout and wall time. In particular, the raw cache grows as 2^m along the all-zero input even though its seen-one behavior has a two-state quotient. Zero expected report failures does not imply bounded raw storage or finite lifetime runtime.

## Fresh independent controls

The new checker independently parsed and reinterpreted both encoded programs, matching the retained decoder and execution on all 2,047 words of lengths zero through ten and all 18,434 acquired-bit ticks. It additionally checked 578 arbitrary natural cache frames against the literal update equation, the four exact loss pairs, and every finite error sum through action ten.

Named negative controls reject cold zero cache, stale cache, output read before updating, use of the wrong API in either direction, an extra loop iteration that consumes the sentinel, and omission of the initial action. The author's separately replayed checks supply the one-less-fuel and malformed-code controls. These are finite execution checks and ordinary source inspection, not a fresh kernel proof or a proof of general compiler correctness.

No empirical-source authentication, normative authority, canonical adoption, generalized finite-state quotient for arbitrary rational models, or expected restoration-time theorem is claimed here.
