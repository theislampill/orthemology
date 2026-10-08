#!/usr/bin/env python3
"""Check public locator identities; optionally verify externally supplied authoritative DOCX bodies."""
from pathlib import Path
import argparse, hashlib, json, zipfile
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--reports',type=Path,help='Read-only directory containing the six named authoritative DOCX files')
a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=json.loads((P/'SOURCE_PACKAGE.json').read_text())
for r in manifest['files']:
 f=P/r['path'];assert f.is_file() and sha(f.read_bytes())==r['sha256'] and f.stat().st_size==r['bytes'],r['path']
graph=json.loads((P/'DEPENDENCY_DAG.json').read_text())
locators=json.loads((P/'SOURCE_LOCATORS.json').read_text())['passages']
assert all(b['passage_id'] in locators for n in graph['nodes'] for b in n['bindings'])
checked=0
if a.reports:
 docs={}
 for name,r in graph['sources'].items():
  f=a.reports/Path(r['original_path']).name
  assert sha(f.read_bytes())==r['original_sha256'],name
  with zipfile.ZipFile(f) as z:xml=z.read('word/document.xml')
  assert sha(xml)==r['document_xml_sha256'],name
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  texts=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in ET.fromstring(xml).findall('.//w:body/w:p',ns)]
  assert len(texts)==r['paragraph_count'],name
  docs[name]=texts
 for key,r in locators.items():
  name,para=key.split(':');text=docs[name][int(para[1:])]
  assert sha(text.encode())==r['text_sha256'] and len(text.encode())==r['text_utf8_bytes'],key
  checked+=1
print(json.dumps({'status':'PASS','nodes':len(graph['nodes']),'typed_edges':len(graph['edges']),'source_body_check':'PASS' if a.reports else 'NOT_RUN','external_body_paragraphs_checked':checked,'proof_replay':False}))
