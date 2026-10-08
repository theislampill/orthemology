# Grounded testimony and continuation after source identification

This T20 component connects occurrence-sensitive testimony to finite grounded support analysis. It is a new scoped formal component and application, not a claim to have invented Horn logic, provenance semirings, hitting sets or the earlier programme's copied-root results.

## Exact result

A conclusion has a surviving grounded derivation after support removal exactly when at least one of its inclusion-minimal support sets survives. Multiple proof paths are alternatives; keeping their union as if every root were jointly necessary is too restrictive.

For a finite family of complete carrier-label supports, the full family of inclusion-minimal label cuts can be archived before the actual carrier-to-source-root map is learned. For every later supplied fixed map, mapping those cuts and inclusion-minimising the images recovers exactly the minimal actual-root cuts. The theorem does not discover or authenticate the map.

Keeping only cardinality-cheapest label cuts is insufficient. In the four-label family {a1}, {a2,b}, {a3,b}, suppose a1, a2 and a3 are aliases of one actual root a. The unique cheapest label cut is {a1,b}, which maps to two roots. The discarded inclusion-minimal cut {a1,a2,a3} maps to the actual optimum {a}, one root. Thus even retaining every cheapest label cut can make later source-root diagnosis report the wrong resilience. A K3,2 support family supplies a second control.

## Truth and authority scope

“Derivable” means that the specified calculus contains a finite grounded derivation. Losing every represented support does not make a historical conclusion false. A true claim may also be known through a route not represented in this calculus. The least-grounded rule excludes unanchored finite self-certification; it does not say that every truth must have a Horn derivation.

Source truth follows only under the separate theorem's explicit hypotheses: available primitive claims are true and every rule preserves the chosen truth interpretation. No data field proves its own source, interpretation or normative authority.

The occurrence fixture distinguishes:

- authenticated source ownership of a duty at time 0 and applicable source veracity
- an actually issued directive and legitimate standing at that past time
- current prospective standing to issue the next directive
- applicability of the old duty to the present occasion
- an available concrete implementation

The source-owned truthful-duty route does not demand a second jurisdiction proof of that same duty. “Owns duty 0” is already a resolved occurrence/content attribution, not an arbitrary string claiming authenticity. Actual authentication and competent uptake remain external premises. Prospective revocation removes only the live grant; it preserves historical evidence. Evidence invalidation is a different operator and cannot silently remove the live grant. Missing present applicability blocks the current action conclusion without erasing the past duty. The model does not implement any real obligation or physical action.

T17's ordinary defeasible entitlement remains a separate positive route. This calculus does not impose exceptional-source certification on every ordinary report.

## What was checked

The author run uses official Lean 4.19.0, with existing pinned Mathlib dependency objects reused read-only. Six isolated modules cover grounded derivability, exact retraction, carrier/root quotient transport, exact minimal-cut archive transport, occurrence controls and constructive bad-rule mutation controls. Finite four-label and K3,2 statements use ordinary kernel-reduced decide proofs, not native_decide. Exact declaration types and axiom dependencies are recorded separately. No custom axiom or sorry is used.

The Python antichain analyser was compared with a separately written direct-closure/subset-enumeration baseline on 2,325 positive rule systems and all 9,300 availability profiles. A tiny alias search covered 2,589 support-antichain/partition cases through four labels: no strict cost error below four labels and 40 at four. The search also checked full inclusion-minimal-cut transport in every case. These finite checks are not a general Python-to-Lean refinement theorem. The antichain implementation's general correctness remains the written proof unless separately formalised.

The bad-rule controls are constructive: adding an authorship-only inference creates a duty which the baseline excludes; dropping current applicability creates an action which the baseline excludes; dropping the live grant creates prospective issuing power which the baseline excludes. These are successful proofs about explicitly different rule systems, not failed compilations claimed as semantic evidence.

## Scholarly source-to-model locators

This concise mapping is our analytical application of classical Arabic passages; it is not a translated quotation or a claim that the sources supplied the algorithm.

- Asbahani main389–391: original speech, conveyance and carrier act; maps to carrier/root typing in GroundedQuotient.
- Asbahani main608–615,725–728: scoped uptake of unfamiliar testimony; maps to source-owned duty in OccurrenceControls.
- Asbahani main677–680: reliability and particular error remain distinct; maps to GroundedSupport's true-root and sound-rule hypotheses.
- Al-Da main25–26: transfer retains relevant conditions; maps to applicability/live-grant premises and MutationControls.
- Al-Da main475: act, consequence and attribution differ; productive support does not alone establish assertoric ownership.

The companion written lane owns the selected-page rereading; the formal supplement adds no further page-reading credit. The complete original exposition is retained separately, unchanged.

## Prior ownership and contribution ceiling

T6 already used support hypergraphs, a common-gate transversal, copied-root minimax and root-bound synchronisation. T7 already proved exact alias-image, fault-budget, threshold and fixed-family cost results. T8 already distinguished shared actual stores from genuine label replies. T9 already combined occurrence, authority, compatible realisers and next-service support, with relational composition and information bounds. T16 already preserves whole source-relative rows and separates fixture acceptance from interpretation truth.

The added component derives support alternatives from grounded inference, proves exact later retraction/quotient behaviour, and exposes the specific premature cheapest-cut summarisation error. The general mathematical methods are established prior art. SecPAL and provenance-semiring sources are identified in the written proof. No general novel hypergraph theorem, actual source truth, necessary-bearer/common-source existence, rightful authority, personal identity, indefinite continuation, empirical validation or repository adoption is inferred.

## Files and reproduction

- EXACT_PROBLEM_AND_WRITTEN_PROOF.md gives the complete mathematical definitions, proofs, source comparison and written small-size lower boundary.
- lean/ contains six mathematical modules plus a generated type/axiom readback file.
- grounded_support.py and test_grounded_support.py supply the finite analyser and tests.
- search_cut_order.py reproduces CUT_ORDER_SEARCH.json.
- validation/ contains the scoped build/readback receipts and source/import hashes.

Run Python tests with python -m unittest -v in this directory, then python search_cut_order.py. For Lean, use the recorded Lean4.19 environment and compile the six modules in the order recorded in validation; never modify or rebuild the shared dependency setup. A portable recipient must supply the same supported imports or requalify a changed environment. No candidate repository file was changed.
