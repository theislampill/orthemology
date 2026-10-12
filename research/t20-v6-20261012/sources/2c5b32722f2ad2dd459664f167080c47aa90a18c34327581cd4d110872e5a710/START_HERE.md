# Start here: T20 whole-corpus guide and cross-front synthesis

The principal documents are:

1. [Full T20 field guide](../aca4b8bf8dfda4c11ce279ed46dfe7bb7b807ca350c883e63b6de46725caee3e/FULL_T20_FIELD_GUIDE.md): the research stories in intuitive terms, with their distinctions and source families.
2. [Cross-front mathematical synthesis](../8aad39f6fb030620059edd4e0639f58078537a10181836b64089f6d82dbe10f4/whole.md): eight explicit deductions, proofs and concrete controls.
3. [Foundational crosswalk](../253fba48ba3485fcf05ec81b8d4a70f0a97dc7470d3c58b261c022c1befa142f/FOUNDATIONS_CROSSWALK.md): how these results bear on the twelve programmes and the affirmative philosophical arguments.
4. [Message for Dot](../76d8a3e1004dab1f7569c5ac682dd6712bc27a2353ca7e237d1ab70872d7d12d/DOT_MESSAGE.md): a focused handoff, not a new research campaign.

Use [the corpus register](../../PUBLIC_BOUNDARIES.md#recovered-reference-039) to locate every recursively inventoried ZIP object. [The source report index](../../PUBLIC_BOUNDARIES.md#recovered-reference-040) links unchanged selected reports to their original archive/member identities. The original ZIPs are not redundantly embedded in this derivative packet.

**Read the [coverage and limits](../b06b0d487b5842a8364e3bb5bacaa307f2b091a7e59de664abb603941e5aaab8/COVERAGE_AND_LIMITS.md).** The resumed execution lost tool-result visibility. The generated receipts and scripts are provided for visible readback; the assistant does not claim to have independently observed a final verification seal or freshly read every proof in the corpus.

## Replay

From a freshly extracted package root:

```sh
python3 -B verification/verify_packet.py .
python3 -B -m unittest discover -s research -p 'test_contracts.py' -v
python3 -O -B -m unittest discover -s research -p 'test_contracts.py' -v
python3 -B research/exhaustive_oracle.py
```

Only the Python standard library is required. The commands do not modify the original research repositories, access a network, install dependencies or replay the inherited Lean corpus. Run them in a disposable extraction.

Search the preserved source reports with:

```sh
python3 -B verification/search_sources.py 'rigidity' --limit 20
```

## Main takeaway

A representation can preserve present answers without preserving future evidence, costs, admissibility, computation or proof. The synthesis gives a finite positive construction for retaining exactly the distinctions required by a declared joint future contract, and a compatible condition for its smooth geometric component.

**T20 remains open.** This is a private research handoff. Selected reports may contain private source or review context and should not be published wholesale without review.
