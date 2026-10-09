# Independent review: reason, exclusion and original causation

8 October 2026 UTC. Review of the exact `reason-causation-bridge/MANIFEST.json` with SHA-256 `504ef228406a1e9d9e38979df9dfa58f0f3fab4a7551ed944177a2a3e5d29794`. No author files were edited. This is a bounded research review, not owner acceptance, final integration, or T20 closure.

## Verdict

**No unresolved material defect found at the frozen stage's stated ceiling.** The implementation supports a restricted compatibility claim; it does not refute the chapter's stronger argument by demonstrating modus ponens. The failed direct T20 transport is substantively correct. One important precision issue, property-level exclusion despite token identity, was raised during review and explicitly incorporated before freeze (`EXCLUSION_TRANSPORT.md:25`).

The positive result is a discrimination among implementation, understanding, input truth and warrant. It is not a naturalistic explanation of reason. The assessment's negative appraisal of the stronger argument remains a philosophical judgement about the inspected bridges, not a computer-verified anti-naturalist no-go refutation.

## 1. The implemented distinctions survive inspection

`model/check_bridge.py:18–48` implements an injective, unchanged codebook for four literals; acceptance requires both availability bits and antecedent-code equality. The microstep does not call the truth evaluator. `:60–75` checks implementation correspondence and conditional soundness separately; `:78–122` supplies formula interventions and faulty-mechanism/source-error controls.

My independent checker enumerates raw nine-bit packets rather than using the author's packet generator, and uses a separately written literal truth table. Fresh results:

- All 512 packets agree with the declared bit equations and abstraction.
- All 2,048 conditional cases pass. There are 1,344 true-input cases, 128 accepted cases, and only 32 cases combining acceptance with true input.
- Removing matching yields 64 true-input/false-output cases; ignoring the first availability flag yields 32.
- Each formula-register/availability bit can change the accepted derivation; the noise bit cannot. Changes to an unaccepted conclusion register are separately excluded from this meaningful-response count.
- Calling the author's `run()` without its file-writing entrypoint reproduces the saved JSON. All 19 payload hashes still agree afterward; all 13 predecessor bindings agree.

These checks establish more than accidental success or an acceptance-only AND gate. The fixed semantic condition can falsify an implementation. Nevertheless, matching is syntactic, the calculus is only a four-literal one-step rule, and withholding one derivation is neither a falsehood judgement nor a complete consequence procedure. The final text makes these limits explicit (`MODEL_AND_TRANSPORT.md:18–32`).

The bad-source control is also legitimate: the same local packet and rule coexist with different external values and an explicit upstream error (`:36–40`). It does not vary meaning while fixing the complete world, violate a perfect sensor equation, or demonstrate that an otherwise competent human inference is unwarranted. This is a software-equation check, not experimental verification of physically closed hardware.

## 2. The chapter's actual challenge is preserved

Decisive visual source checks support the stage's reading. Ameri pp.255–256 requires understanding and causal relevance of logical laws; p.270 expressly treats computers as derivative instruments of designers/users. The p.262 note permits God-created matter to produce consciousness while opposing its naturalistic origin. Page252 separates epistemic reliance on reason from ontological dependence. These passages defeat any reading of the chapter as merely denying correct material computation. [Publisher source](https://almobadarah.com/uploads/books/5f6ae0298582cce21002cbe4.pdf).

The implementation therefore answers a genuinely weaker proposition. Its origin, supplied interpretation and absence of a subject mean it does not instantiate the full antecedent needed for the ambitious counterexample. `INDEPENDENT_ASSESSMENT.md:35–59` correctly retains this obstacle while criticizing particular exclusion steps.

The targeted Reppert paper explicitly rejects the simplest atom-motion argument (displayed p.11), distinguishes explanatory levels (pp.11–18), and later presses content-sensitive causation and apprehension of necessity (pp.23–25). [Primary paper](https://www.theistic.net/papers/V.Reppert/ReppertAFR.pdf). The assessment's structural/conventional criticism is relevant: realization in different materials need not mean freedom from all organizational constraints. Its necessity distinction is also valid: entailment's necessity does not entail a token mechanism's infallibility. Neither observation yet explains a subject's grasp of necessary truth. The frozen assessment retains that separate question at lines49 and101 rather than treating it as answered.

## 3. The original-peer import fails for definite reasons

The decisive T20 source distinctions are real, not terminological repairs invented for this review:

- Majmu20 item2031 L007–010 separates solo sufficiency from simultaneous exclusive attribution; item2032 L002 and L006–008 adds unchanged efficacy and augmented work to the argument. [Item2031](https://islamweb.net/ar/library/content/22/2031/), [item2032](https://islamweb.net/ar/library/content/22/2032/).
- Majmu8 item805 L305–309 distinguishes incomplete created conditions from independent complete efficacy; L313–318 positively retains created means. [Item805](https://www.islamweb.net/ar/library/content/22/805/).
- Bayan5 item962 L004–007 distinguishes finite willing/causal assistance from unreceived divine willing. [Item962](https://www.islamweb.net/ar/library/content/415/962/).

Numerically different explanatory descriptions do not establish numerically different original producers. Dependently realized properties do not acquire original self-sufficiency from a locally sufficient transition law. Conversely, compatible descriptions of one event supply no example of two original bearers retaining whole-work efficacy together. The report correctly keeps both directions of the failed map visible.

Important retained qualification: dependence or token identity alone does not solve the mental-property causal-relevance problem. That issue can survive without original peers. The inserted paragraph at `EXCLUSION_TRANSPORT.md:25` resolves the ambiguity identified during review. Read its conclusion as failure of the inspected direct import, not a universal theorem prohibiting every future reformulation or analogy.

The comparison with nonabsorption is appropriately methodological: response sensitivity does not itself authenticate the stronger kind of production. It neither identifies derivative size with intentional causation nor withdraws the separate common-source warrant appraisal.

## 4. No unearned worldview or reliability conclusion

No probability model for cognition is defined. The 32 nonvacuous successes and mutant failure counts are coverage counts, not empirical frequencies or priors over naturalistic worlds. Balfour's printed pp.279–282 adds a truth-bias/probability premise, beyond physical ancestry; his p.285 note gives a separate exclusion route. [1906 printing](https://archive.org/details/foundationsofbeln00balf/page/279/mode/1up). Plantinga's inspected manuscript preserves both poorly grounded low estimates and an inscrutability route, then separately discusses defeat and warrant. [1994 manuscript mirror](https://static1.1.sqspcdn.com/static/f/38692/383655/1263300179793/Naturalism%2BDefeated.pdf).

The stage properly treats these as distinct burdens. Lack of exact numerical estimates alone would not defeat every qualitative, defeasible argument; equally, possible adaptive falsehood does not establish low global reliability. The report does not infer consciousness, proper function, knowledge, naturalism, theism, equal worldview credibility, or a blanket genetic fallacy from its program. It also distinguishes a real interpreted mathematical proof from the additional evidence needed for its physical/metaphysical application.

## Verification limits and reproducibility

Run `PYTHONDONTWRITEBYTECODE=1 python3 independent_checks.py` in this review directory. `INDEPENDENT_CHECKS.json` records the fresh results. `REVIEW_RECEIPT.json` binds the reviewed freeze, source returns, reviewer files and scope.

I inspected the actual code and all three principal arguments, the targeted primary receipt/provenance, and relevant predecessor arguments and primary passages. My Ameri reading was a targeted visual return to fifteen pages, not another continuous chapter reading or whole-book reading. The author's broader continuous-reading claim is supported by its recorded provenance, not independently repeated here. I did not verify the cited 1918 Balfour printing, Reppert's 2003 pp.73/85, Plantinga's 2011 p.329, or Lewis's book pages. No fresh full Lean build or kernel replay was performed by this reviewer; I inspected the inherited theorem boundary and the frozen new check logs. No source bodies are included in this review deliverable.
