# Replay the P01 successor

1. Rebuild or materialize the repaired P01 parent project using its separate qualified-shadow bundle. Its 31 compiled artifact hashes must match its successful strict-0004 receipt. Keep the exact nine locked dependency revisions and tracked-clean source.
2. Use Lean 4.19.0, commit 6caaee842e94, with Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b.
3. Extract this successor bundle without changing sources. Select a new absent work-directory name; previous receipts must not be overwritten.
4. Run the exact qualification script. The local defaults reproduce the original workspace. Other layouts can set the parent and compiler paths explicitly:

```sh
export P01_PARENT_PROJECT=/absolute/path/to/qualified-parent/project
export P01_PARENT_RECEIPT=/absolute/path/to/qualified-parent/QUALIFICATION.json
export P01_LEAN=/absolute/path/to/lean-4.19.0-linux/bin/lean
export PYTHONPATH="$PWD/handoff${PYTHONPATH:+:$PYTHONPATH}"
python3 -B qualify.py fresh-replay \
  P01RecursiveModel P01RecursiveAssertions P01CurryParametricity P01ModelWitnesses \
  P01EffectSeeds P01FiniteCoupling P01EffectMass P01CouplingWitness
```

The script first checks the selected imported parent artifact bytes, verifies all locked dependency revisions and tracked cleanliness, and checks the exact compiler identity. It compiles all successor modules in a fresh output directory, creates the complete declaration/type/axiom audit, checks the actual exit status, rejects proof placeholders and nonstandard axioms, parses every required target, and binds the output to unchanged source bytes.

The import-path defaults identify the previously qualified parent helper scripts in the original workspace. On another machine the bundled handoff directory supplied through PYTHONPATH provides those same helpers; canonical_gate.py is unchanged from the qualified checkpoint.

A successful replay must report KERNEL_VERIFIED_SCOPED_P01_SUCCESSOR and kernel_credit=true for all 151 targets. Module compilation alone, a historical receipt, or partial audit output is not equivalent to this result. Keep the exact readbacks and failed runs if repair is necessary.

No external expert review, repository integration, owner adoption or generalization beyond REMAINING_OBLIGATIONS.md follows from replay success.
