# Executability and concrete-evidence clarification

The independently accepted shared progress core and fixed-controller sharpness
modules are mathematical Lean reference definitions in noncomputable/classical
sections. They include classical decisions over service-guard propositions and
Finset.toList choices. Their theorems are kernel-checked, but the whole 21-path
shared controller/interpreter has not been extracted, code-generated or
natively evaluated. An explicit finite public request schedule and a verified
mathematical trace witness are supplied. These are not a native implementation.

The unchanged executable source localStep/attempt definitions occur literally
inside those proofs. The local source-window fixture checks reduce those source
definitions. That does not turn the new classical shared-state interpreter into
the source's native four-path runBatch or a natively evaluated 21-path successor.

Concrete shared fixture: source bytes [65,66,67] (ASCII ABC), length 3,
SHA256 b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78.
Starting draft [65,66,67,10] (ABC+LF), length 4. The source action installs the
exact acceptance rule, increments ruleVersion 3→4 and leaves the draft unchanged.
It is one installation and zero repairs, not completed source-text recovery.
The generic theorem permits arbitrary applicable source plants/actions under
its explicit premises. This fixture is distinct from the separately verified
3013-byte label-local actual-batch witness.
