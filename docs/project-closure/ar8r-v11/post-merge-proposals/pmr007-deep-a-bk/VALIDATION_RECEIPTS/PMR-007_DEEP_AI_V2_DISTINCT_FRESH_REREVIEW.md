# PMR-007 Deep Round AI V2 — distinct fresh rereview

```text
candidate: PMR-007-NMIB-1 V2
review relation: distinct three-host symbolic SAT and exact source-anchor implementation in the same Pro program
external independence: false
disposition: PASS_WITH_NONBLOCKING_SOURCE_RECONSTRUCTION_AND_H7_PREMISE_NOTES
```

The rereview verified all eight frozen hashes, the Asfahani translation hash,
the El-Tobgui dissertation snapshot hash, and nine exact source anchors.  It
then reconstructed the candidate with three potential mental hosts using
SymPy's symbolic satisfiability engine rather than the primary two-host brute
force enumeration.

```text
frozen hash rows:                                      8
frozen hash mismatches:                                0
source anchors checked:                                9
source anchor failures:                                0
symbolic host count:                                   3
NM-HOST violation satisfiable:                         false
structure/underived with no host satisfiable:           true
notional/underived with no constitutive ground:         true
H7a+b+d without H7c and no underived host:              true
full H7a–H7d failure of exactly one underived host:     false
full bridge with no personal subject:                   true
unique constitutive host with multiple representers:   true
```

The distinct SAT model therefore confirms the exact boundary:

```text
notional representation -> some mental host
```

under `NM-HOST`, while the following remain independent:

```text
structure -> intrinsic notion;
representation -> constitutive grounding;
underivability transfer;
unique constitutive host;
personal subjecthood;
agency;
Wisdom.
```

The full conditional result holds only because H7a–H7d are explicitly assumed.
It is a bridge specification and premise-minimality result, not evidence that
those hard premises are true.
