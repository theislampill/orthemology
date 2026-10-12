"""Locate exact included source bytes without reproducing an author's workspace."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('locator',help='Original locator, SHA-256, source ID, or supplementary source path');p.add_argument('--document',help='Optional original binding document, relative to delivery root');args=p.parse_args()
 data=json.loads((ROOT/'historical_coverage/SOURCE_PATH_RESOLVER.json').read_text());out=[]
 for row in data['routes']+data['exceptions']:
  if args.document and row['binding_document']!=args.document:continue
  if args.locator in [row.get('original_locator'),row.get('workspace_alias'),row.get('sha256'),row.get('included_path'),row.get('owner',{}).get('id'),row.get('owner',{}).get('source_id')]:out.append(row)
 if not out:raise SystemExit('No declared exact route found; do not infer a missing source from an approximate filename.')
 print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
