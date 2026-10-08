# Portable reanalysis software

Python 3.12 is the verified runtime. Install the pinned dependencies in an isolated environment:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Use the equivalent interpreter path on Windows. Obtain the two required inputs separately from the official links in `INPUTS.json`. Supply local paths; the program neither downloads files nor executes archived programs. Input hashes are mandatory and checked before parsing. Do not add the input files to this package.

```sh
python -B reanalyse.py --decisions-zip /path/to/decisions.zip --summary-xlsx /path/to/summary.xlsx --output /path/to/aggregate.json
python -B validate.py --decisions-zip /path/to/decisions.zip --summary-xlsx /path/to/summary.xlsx
python -B -m unittest discover -s tests -v
```

Without `--output`, the analysis writes aggregate JSON to standard output. There is no record-level output option. The validator checks the bundled aggregate reference and independently implemented numerical fits. Synthetic tests require no source files. Runtime input parsing and the prior method-review scope are distinguished in `INPUTS.json`.

`fit_bfgs.py` and `fit_checked.py` preserve separately authored numerical implementations, adapted to a shared portable input/output wrapper. Packaging itself is not another independent implementation. `BINDING.json` records their provenance by hash. Original author programs and source documents are not included. Do not infer reuse permission for external inputs from this software package.

Verify package integrity from this directory:

```sh
sha256sum -c SHA256SUMS
```
