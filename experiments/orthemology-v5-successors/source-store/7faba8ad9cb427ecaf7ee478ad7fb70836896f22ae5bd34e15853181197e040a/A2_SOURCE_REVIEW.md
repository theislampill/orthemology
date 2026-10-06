# Independent cold source review of A2

A2 source manifest: `83f7bef7b6c6b354aca11cd0ebb9b7603b541d960f8b0f2eb57d8c4c4117f7f1`.
Approved specification: `68d6d80a484a35e6127d4aa08bef605e63144c95f9d027cb9c14b336ff625ba3`.

## Verdict

PASS for the exact derived-domain and semantic-transport claims. No mathematical source gap was found. The three frozen modules passed independent compilation, all 72 declaration axiom checks passed, and all 20 independent reviewer theorems passed. The A1 packet and its raw-input negative controls remain unchanged.

## Real call boundaries

The new reversePrefix is exactly the raw compiler's reverse call at private start 22, with destination 1. foldStart then executes the unchanged initialStmt. The proof obtains the original code and reversed remaining history from call_frame and call_value, followed by the inherited exact reverse-source theorem. This is tied to the actual rawPolicyProgram syntax by a reviewer reflexivity theorem; it is not an unrelated abstract evaluator.

The inherited loop invariant gives the represented semantic history after every number of fold iterations. The new matches_loop_index_update separately accounts for the actual interpreter write of register 2 immediately before a body call. The reviewer checks the exact runLoop successor equation against that store. Initial values and the actual step derive the invariant; arbitrary raw-store validity is not assumed in the final endpoints.

For each prefix of the actual `List.finRange 18`, collection preserves registers below 21 because scratch begins at 39 and result buffers occupy 21 through 38. Step arguments read only registers below 21. The new ordered-prefix theorem therefore covers all actual components, after the register-2 write; no duplicate-free-order hypothesis escapes the final endpoint. A reviewer strengthens this to equality of the entire argument vector before and after every prefix.

At exhaustion, the encoded empty-history sentinel is 1. The guard `4 ≤ register 1` is false, so the source body executes skip. The new theorem includes the clock-updated actual entry store. Independent controls additionally show that any below-four guard value skips any supplied step. Loop padding does not fabricate a receipt or execute a selector call.

The actual final readout arguments equal `rep` of the complete original acquired history. This uses the original code as loop bound, its length lower bound, and chronological reversal. It is stronger than asserting some unnamed bounded state exists.

## Selector ranges

The source state contains supportCode of a finite Boolean support, bitNat of a Boolean state, and retainedCode of an optional finite pair set. Thus support is below 4, state below 2, and retained code at most 16. The step adds genuine Boolean action and receipt slots. Phase and visit counts need no finite bound because cycle selection reduces the index modulo two.

The source-computed candidate is proved to be bitNat of the retained phase candidate. Both cycle and target addresses are consequently below 16. Active pairs are an actual finite pair mask below 16; the state-specific action row is exactly supportCode of retainedActions. Its cycle address is also below 16. The proofs use the inherited exact source components and actual represented inputs, rather than postulating bounds for arbitrary raw natural inputs.

The A1 malformed support-4 witness remains valid and untouched. A2 never strengthens it into raw component extensionality.

## Source transport

normalizeConfig changes only selector data. Kernel, rational coefficients, tolerances, initial support/state and fallbacks remain definitionally unchanged; the reviewer checks every nonselector field explicitly. The full original Certificate is preserved by A1 normalization. The new constructor commutes with withComputedTolerance.

The retained semantic policy and represented state do not depend on table representation, so both are definitionally unchanged. Exact source decisions then agree for every encoded finite acquired history by the two original source-correctness instances. The proof does not claim equality on malformed natural history codes.

## Physical output and decoder roles

The generic runtime theorem takes two programs with their own implementation certificates and agreement of their executed policies only on encoded acquired histories. That agreement makes historyStep and historyObservation identical. The inherited all-tape four-bit frame theorem then gives matching frames. Division by four and the finite remainder cover every output coordinate, producing function equality, not only almost-sure equality.

The uniform fuel schedule remains program-specific. Scheduled output equality does not imply the two uniform fuel values or finite success thresholds agree. No code-size, instruction-count, meter or wall-time equality is asserted.

Decoder policies are separate parameters. Their agreement is proved within the decoder pair, independently of the execution pair. The common canonical output-only decoder is definitionally composed with physical runtime output, including total receipt extraction on noncompletion tapes. This yields exact mixed decoded-history equality while allowing execution and decoding configurations to have different tolerances, kernels, menus and priorities.

The reviewer separately checks proposal and total receipt-path equality on every tape and specializes physical output equality to the all-one forever-rejection tape. No completion assumption or almost-everywhere exception enters the transport.

## Laws, events and meaningful negative control

Since the decoded-history functions are identical, their pushforwards under every input measure coincide. The old-execution/computed-decoder failure sets are literally equal, so equality of their measure values and equivalence of positivity need no extra measurability premise. This does not assert that arbitrary events are measurable; it rewrites the same set.

The reviewer instantiates the result with the exact inherited oldConfig and its original certificate. Positive-measure mixed failure is preserved. The matching computed/computed positive control is also preserved. Combining these two accepted facts proves the normalized mixed decoded-history function is different from the normalized matching decoded-history function. Thus the transport cannot be read as silently replacing the decoder or changing which program executed.

## No dropped environment-correctness premise

A2 compares two instances of the same existing Boolean fixture runtime wrapper. This equality statement is meaningful without assuming a supplied Config kernel equals that environment or its initial state is false. It is not a theorem that an arbitrary Config kernel is implemented by that wrapper, nor a new parity-success result. The original kernel/state/winningness/model-membership requirements remain in the inherited correctness and counterexample results when those are invoked. The reviewer's instantiated positive and negative controls use those already established inherited endpoints.

## Replay and limits

A2 now verifies exact 167-core and five-A1 object censuses, source/object hashes, A1/core receipt lineage and absence of symlinks. This independent invocation reuses only the reviewer's own previously rebuilt objects and starts a new A2 output. The pinned external official dependency cache remains trusted.

The exact frozen census helper additionally passes a positive fixture and rejects extra objects, missing objects, symlinks, wrong object digests and wrong source digests. These are isolated helper tests with non-executable fixtures; the separate successful full replay tests the real 167+5 trees.

All 72 author declarations and 20 reviewer theorem closures use only propext, Classical.choice, Quot.sound, or an empty/subset closure. No A2 Lean proof failure or resource-limited outcome occurred in this independent review. The author's empty-axiom audit parsing diagnostic is preserved as a postprocessing issue, not a failed proof. No historical failed mutant, interrupted denotation or optional comparison probe was rerun. No native Python/CPython refinement or arbitrary-kernel executable selector extraction is claimed.
