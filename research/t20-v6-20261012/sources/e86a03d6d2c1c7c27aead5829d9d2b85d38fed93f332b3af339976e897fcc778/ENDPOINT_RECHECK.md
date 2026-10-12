# Recovered endpoint source and fresh execution checks

## Current evidence and interruption boundary

Two original fourth-tranche files have been recovered exactly from complete recorded tool output and matched to their pre-interruption SHA256 identities:

- `RepairTestingReduction.lean`: c86a552e28c596255b14bfaca8ef99c155ec5000a52301c127fbc12bc3e77de5
- `NATIVE_ENDPOINT.json`: a77d05474ebd510b30cf52b34828a407dadce962359c678701eba6a9ebda7c7b

The latter contains the literal 59-byte incremental P02 programme and both its natural-number index and the 105-byte prefix programme's index. Decoding the indices with the retained P02 codec recovers their actual source trees. That codec was recovered from the pre-existing checkpoint archive `user-checkpoints/Orthemology_P02_Measure_Research_Checkpoint_attempt-0002.zip`, member `code/prcodec.py`, with exact SHA256 dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c. It is the same identity referenced by the retained third-tranche semantic report.

The fourth-tranche endpoint Lean modules and their independent audit archive are currently unavailable. The historical JSON's sentence referring to separate Lean proofs is retained as part of its original bytes, not adopted as current recovered proof evidence. This packet does not restore that vanished kernel seal. The single recovered reduction source is not represented as a freshly compiled complete dependency closure.

## Actual decoded programmes

The incremental programme has arity one and output register 5. Starting with cache registers L=1 and R=1, it acquires one binary bit b in register 0 and executes exactly the following assignments, in order:

1. L := L times [b times 0 + (1 minus b) times 2]
2. R := R times [b times 1 + (1 minus b) times 1]
3. output := indicator(L+1 <= R)

Natural subtraction is truncated. The source contains two binary sequence nodes and three assignment nodes. The new `run_frame` adapter executes the decoded tree through an explicit task stack, invokes the retained expression evaluator, and returns the actual resulting frame. Its statement/repeat meter excludes expression-evaluation steps; expression work has a separate meter. The old `prcodec.run` function instead starts a new input frame and does not supply a carried cache. These APIs are not conflated.

The prefix programme has arity two: stage k and the sentinel word containing k+1 acquired bits. It initialises L=R=1, copies the word, loops k+1 times, multiplies by the same factors of the current low bit, divides the word by 2, then makes the same comparison. It therefore excludes the sentinel and reads no unacquired bit.

## Fresh ordinary argument

The following is a fresh ordinary proof about the displayed decoded programmes and stated adapter. It is not a new Lean theorem.

After m acquired bits, R=1 always. If any acquired bit was one, L=0. Otherwise L=2^m. This follows by induction from the fixed initial cache and the two update factors. Hence output is true exactly when a one has appeared. The prefix loop has the same invariant over its processed low-bit suffix. Multiplication order is irrelevant for these factors, and stripping exactly m bits removes no sentinel bit. Thus both actual decoded source trees compute the same seen-one predicate on every finite acquired prefix.

The controller has a distinct initial false action before any receipt. At action n it uses the first n receipts. The eager update output occurs after receipt n-1 and supplies action n, for n>=1. The pointwise output equality extends to every infinite input by equality at each finite opportunity; consequently every specified input measure has the same pushforward output law through the two adapters.

The incremental decoded tree requires exactly five statement tasks. With fewer than five tasks the new adapter stops before the stack is empty; with five it returns the same actual frame whose cache is subsequently threaded. The prefix tree has nine outside-loop statement tasks, m+1 repeat tasks, and five body statement tasks per iteration, totalling 6m+10. These counts exclude expression arithmetic, binary integer complexity, setup, input injection, codecs, rational readout and host wall time. The products can grow without bound.

## Actual Bernoulli source and literal report costs

Assume the supplied source/scoring weight is either 0 or 1/2, with independent identically distributed Bernoulli receipts. Fix disturbance 1/4 and read out report 1/2 for false and 5/8 for true. Substitution in the retained literal excess-loss expressions shows that the false report is good only in the first model and the true report only in the second. At weight zero all receipts are false almost surely, so the literal failure count is zero.

At weight one half, action n is wrong exactly when its n receipts are all false. This event has probability 2 to the power minus n. Tonelli's theorem and the geometric series therefore give total expected failures 2, including the initial action. The finite checks reproduce the partial sum 2047/1024 through action 10, but the infinite total follows from this ordinary argument rather than extrapolating tests.

The output streams are contained in the countable set consisting of all-zero forever and finite strings of zeros followed by ones forever. Thus the output law's nonatomic mass is zero under either actual model. This is an ordinary countable-support argument; the recovered third-tranche exact finite-observer solver provides retained mathematical context but this packet does not recreate the lost fourth-tranche Lean composition to it. Defect zero and literal correctness remain separate claims.

A two-state observer recording whether a one has appeared has the same behaviour. The raw integer implementation may grow on the all-zero input while this particular behaviour has a finite-state quotient. No general finite quotient for arbitrary rational candidate pairs is inferred.

## Fresh tests and failure controls

Run `python check_endpoint_recovery.py` in this directory. It first verifies the exact historical identity file and codec digests, decodes and re-encodes both programmes, and compares actual outputs on all 2,047 words of lengths zero through ten, covering 18,434 acquired-bit ticks. For each tick it checks the actual prefix interpreter, the carried-cache adapter, the seen-one value, the exact stated transition budgets and one-less-fuel failure. Every proper truncation of the 59-byte code and a wrong magic byte are rejected. The older arity-two indexed API defaults to zero on the arity-one cache source, as its contract specifies.

Cold zero cache, stale cache, pre-update output, wrong input bit and insufficient fuel are explicit failing alternatives. These are independent controls of a newly written finite checker, not recreated old mutation archive bytes or a universal Python-to-Lean refinement theorem.

The mathematical score/source contract is supplied. Receipt frequency does not establish normative authority, identify the forecast truth, authenticate a physical sensor or prove canonical adoption. This packet has author fresh checks; any independent review must be recorded separately.
