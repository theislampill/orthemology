# PMR-007 Deep AV V2 distinct fresh rereview

```text
disposition: PASS_WITH_NONBLOCKING_LOGIC_AND_VOCABULARY_NOTES
candidate: PMR-007-NBIF-1 V2
primary method: one-neutral-variable bit-table enumeration
rereview method: two-neutral-variable set projection and interval enumeration
external independence: NOT CLAIMED
```

## Frozen custody

```text
frozen files checked: 6
hash mismatches: 0
```

## Distinct checks

```text
exhaustive X=1 bit, N=2 bits, Y=1 bit table pairs: 65,536
entailed pairs: 2,401
criterion failures: 0
interpolant-count failures: 0
uniqueness failures: 0

random X,N,Y four-valuation cases: 20,000
random failures: 0
```

The set-projection implementation independently confirmed:

```text
A entails C iff S_A is a subset of T_C;
interpolants are exactly the sets I with S_A subset I subset T_C;
number of interpolants is 2^(|T_C minus S_A|);
uniqueness holds exactly when S_A=T_C.
```

## Scope notes

1. The finite theorem is constructive propositional interpolation.
2. Craig's first-order theorem remains prior art and was not re-proved.
3. The theorem cannot certify that the declared shared vocabulary is neutral;
   target import must be audited independently.
4. Satisfiability, source truth, translation, referent identity, model-class
   completeness, and actual-world selection remain separate.
5. An interpolant need not be natural, explanatory, computationally tractable,
   or implementation-ready.

```text
fresh rereview:
PASS_WITH_NONBLOCKING_LOGIC_AND_VOCABULARY_NOTES
```
