#!/usr/bin/env python3
"""Check numerical agreement and the aggregate reference using local inputs."""
import argparse
import json
from pathlib import Path
import numpy as np
import reanalyse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decisions-zip', type=Path, required=True)
    parser.add_argument('--summary-xlsx', type=Path, required=True)
    args = parser.parse_args()
    aggregate, check = reanalyse.run(args.decisions_zip, args.summary_xlsx)
    expected = json.loads((Path(__file__).resolve().parent/'AGGREGATE.json').read_text())
    if set(aggregate) != set(expected):
        raise ValueError('Aggregate reference keys differ')
    for key, value in expected.items():
        if isinstance(value, bool):
            if aggregate[key] is not value:
                raise ValueError('Aggregate reference boolean differs')
        elif not np.allclose(aggregate[key], value, rtol=0., atol=1e-7):
            raise ValueError('Aggregate reference tolerance exceeded')
    print(json.dumps(dict(check, aggregate_reference='pass'), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
