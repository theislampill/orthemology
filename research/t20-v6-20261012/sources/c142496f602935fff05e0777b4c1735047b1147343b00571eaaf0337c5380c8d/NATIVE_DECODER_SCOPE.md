# Validated native-tree decoder extension

## Result and actual semantic boundary

A new decoder now connects a generic finite native-tree representation to the independently evaluated seven-rule SourceProof model. It does not consume byte strings and is not a verified UTF-8/JSON implementation or a verified semantics for CPython. It does not model mutable capture, cycles, foreign objects, subclasses, callbacks, host memory/stack failures or arbitrary native APIs.

WireValue represents nonnegative integers, strictly negative integers (`negative n` means `-(n+1)`), exact booleans, null, Unicode strings, arrays and object field lists with string keys. Arrays identify native list/tuple presentation. Objects retain order and duplicates rather than silently converting field lists to maps. Non-string dictionary keys and unsupported native scalar classes have no representation; the concrete ingress rejects them separately.

The decoder has explicit fuel and the native entry enforces the declared full-tree node/height/integer guards. Every actual proof/type/term constructor is parsed from its exact literal tag and arity. Objects require an exact key multiset and no duplicates. Missing, extra or duplicate fields, wrong scalar kinds, unknown tags and malformed type/term/trace structures refuse. Semantic scope and explicit trace correctness remain in the source checker, so an empty trace can decode syntactically and still be refused semantically.

## Noncircular grammar and proofs

NativeProofRep is an independently stated inductive grammar. For each of the seven rules it states exact key-multiset permutation, actual field-value membership, exact type/term trees, and recursive child grammar. It does not mention decoder acceptance or target-checker acceptance.

- decodeType_sound / decodeTerm_sound / decodeTrace_sound prove successful parsing preserves the exact represented type/term/trace tree
- decodeProof_sound proves every parsed proof satisfies NativeProofRep
- NativeProofRep.decode_complete proves every grammar-valid field ordering parses with enough depth; canonical dictionary order is not required
- NativeProofRep.deterministic proves each represented native tree has a unique SourceProof meaning
- decodeNativeProof_roundtrip establishes the guarded canonical encoding round-trip
- nativeCheck_representation_equivalence proves equality of the entire native-model/source-model outcome, including refusal, for bounded native representations
- native_checker_constructor_erasure_square and native_checker_sound compose native decoding with the independently proved source checker/Cert correspondence and semantic soundness
- native_check_rejects_duplicate_fields is a universal duplicate-field rejection theorem
- native_checker_partial_export_square retains explicit source-check and separate partial-constructor-export success; it does not claim that every accepted proof passes text exporter limits

These are kernel-checked model-level theorems. They are not assertions that the actual Python/JSON runtime has been extracted or proved equivalent.

## Axiom accounting

The older constructor-square main results retain propext/Quot.sound. The new grammar/permutation proofs additionally use Classical.choice through Lean's existing List.isPerm_iff library theorem. The native semantic soundness corollary itself still has only propext/Quot.sound. No user-defined axiom, sorryAx, admitted proof or native_decide is used.

## Duplicate-field policy and concrete tests

Python dictionaries cannot retain duplicate equal keys. The WireValue field-list form deliberately can. Duplicate cases are therefore compared to the actual strict raw-JSON interface before map construction, never by first applying Python dict(fields), which would erase the counterexample. Ordinary unique-key cases are checked against both reference.check on native values and reference.check_json on actual bytes.

The separate native-cross-language-final test run, now passing all 188 cases (54 accepted / 134 refused), varies all seven root field orders, missing/extra fields, same/conflicting duplicate fields, nested duplicates, wrong rule kind/name, malformed type indices/arities, malformed and invalid traces, and wrong root/child shapes. These are finite independent execution checks of the source map, not substitutes for the universal model proofs.

## Evidence

fresh-build-3/RECEIPT.json records a new empty native build of all 24 source modules, 24 nonempty objects and 30 target type/axiom readbacks. NativeDecoderAudit.stdout contains definitions and expected-type restatements. The earlier fresh-build-2 generation remains preserved with its independent review; this native extension is a distinct later generation pending separate review.

The original supplied P03 checkpoint, all canonical source owners, historical obligation statuses and P02 dependency map are unchanged. This work is a separate research/proposal qualification.

The first concrete-test generator emitted one unparenthesized top-level Bool constructor. That Lean syntax failure is preserved under native-cross-language/rejected-harness. Corrected generation passed unchanged model sources; no semantic condition was weakened.
