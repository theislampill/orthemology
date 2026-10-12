# Read-only packet verification

Use Python 3.10 or later. No third-party dependencies are needed.

```sh
python -B tools/verify_packet.py .
python -B -O tools/verify_packet.py .
python -B tools/verify_packet.py /path/to/Orthemology_Comprehensive_Research_Handoff_20261009.zip
```

The verifier checks every top-level packet payload, original input identity and the complete 2,067-file publication Git tree. It does not extract the ZIP, execute embedded research, install dependencies, contact services, or modify source files. Nested original ZIPs are verified as retained bytes; their recursively checked member inventory is separately preserved, not silently executed.

The manifest is a consistency check, not self-authentication against a maliciously replaced manifest. Check the separately delivered ZIP SHA-256 against your transfer anchor. All rejection checks use unconditional runtime checks rather than Python `assert`.

Tests:

```sh
python -B -m unittest discover -s tools -p test_verify_packet.py -v
python -B -O -m unittest discover -s tools -p test_verify_packet.py -v
```

The 15 test methods include real normal/optimised child-process acceptance and tamper rejection. Test-only temporary files do not modify the retained payload. Final evidence logs are under `review/evidence/`. Running without `-B` can create `__pycache__`, which the strict exact-file-set verifier correctly reports as an unexpected extra file. Keep generated test/replay output outside the packet.
