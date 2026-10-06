"""Explicit-input replay. No downloads, external writes or packaged observations."""
import argparse,json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-export',required=True,type=Path)
    parser.add_argument('--author-responses',required=True,type=Path)
    parser.add_argument('--output-root',required=True,type=Path,
                        help='New or empty directory for locally generated reports and intermediate records')
    args=parser.parse_args()
    for source in [args.raw_export,args.author_responses]:
        if not source.is_file():parser.error('Input file is missing: '+str(source))
    out=args.output_root.resolve()
    if out.exists() and any(out.iterdir()):parser.error('Output directory must be new or empty.')
    out.mkdir(parents=True,exist_ok=True)
    (out/'verification').mkdir();(out/'private-source').mkdir()
    import run_reanalysis as raw
    raw.HERE=out
    raw.INPUT_PATHS={'export_3.csv':args.raw_export.resolve(),'globalPref_LM_100.csv':args.author_responses.resolve()}
    d,author=raw.load();r=raw.build_rounds(d)
    (out/'verification'/'reconstruction_audit.json').write_text(json.dumps(raw.clean_json(raw.audit(d,r,author)),indent=2))
    import estimate_contrasts
    estimate_contrasts.main()
    import batch_sensitivity
    batch_sensitivity.main()
    import manipulation_checks
    manipulation_checks.main()
    print('Replay finished. Locally generated reports:',out/'verification')
    print('Intermediate study records are local only:',out/'private-source')

if __name__=='__main__':main()
