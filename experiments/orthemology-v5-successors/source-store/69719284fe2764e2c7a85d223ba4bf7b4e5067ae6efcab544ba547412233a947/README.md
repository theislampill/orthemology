# Source-only reanalysis replay

This package contains independently written Python and synthetic tests. It contains no original data, author programs, or derived study records. Input provenance and publication-version limits are stated in the report’s single study account.

Use Python 3.12 and the versions in requirements.txt. Obtain the two inputs identified by INPUT_MANIFEST.json separately. Their hashes are checked before analysis. Nothing downloads automatically.

Run:

    python replay.py --raw-export /path/export_3.csv --author-responses /path/globalPref_LM_100.csv --output-root /path/new-output

The output directory must be new or empty. Reports and intermediate records are created there, locally. Do not redistribute those records. The code implements primary contrasts, explicitly posthoc block sensitivities, and recorded-cue checks. Consult the research report for the estimands and qualifications; computed p-values are diagnostics, not independent replication.

Synthetic tests need no study data:

    python -m unittest discover -p test_analysis_core.py -v
