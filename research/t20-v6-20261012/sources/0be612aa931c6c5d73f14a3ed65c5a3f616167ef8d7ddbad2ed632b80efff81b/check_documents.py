#!/usr/bin/env python3
"""Bounded editorial-preservation and PDF checks, not a semantic proof."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
import fitz

NAME='information-composition-and-self-revision-v5'
BASE='information-composition-and-self-revision-v4'
TITLE='Information, Composition, and Self-Revision: Local Descriptions and Operative Access'

def require(value, message):
    if not value:
        raise AssertionError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def results(text):
    return re.findall(r'\\begin\{(?:theorem|proposition)\}.*?\\end\{proof\}', text, re.S)

def displays(text):
    return re.findall(r'\\begin\{(?:equation|align)\}.*?\\end\{(?:equation|align)\}|\\\[.*?\\\]', text, re.S)

def bibliography(text):
    body=text.split(r'\begin{thebibliography}{99}',1)[1].split(r'\end{thebibliography}',1)[0]
    return {m.group(1):m.group(2) for m in re.finditer(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\Z)',body,re.S)}

def read_labels(text):
    return {m.group(1):{'number':m.group(2),'page':int(m.group(3))}
            for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',text)}

def source_preserved(old,new,contract):
    expected=old
    for edit in contract['replacements']:
        require(expected.count(edit['before'])==1,'Non-unique preimage '+edit['id'])
        expected=expected.replace(edit['before'],edit['after'],1)
    expected=expected.replace(r'\end{thebibliography}',contract['added_bibliography']+'\n'+r'\end{thebibliography}',1)
    return expected==new

def inspect_pdf(path):
    with fitz.open(path) as doc:
        texts=[];pages=[]
        for i,page in enumerate(doc):
            text=page.get_text();require(bool(text.strip()),'Blank page')
            require('\ufffd' not in text,'Replacement glyph')
            spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b
                   for line in b['lines'] for s in line['spans'] if s['text'].strip()]
            for span in spans:
                x0,y0,x1,y1=span['bbox']
                require(x0>=-.5 and y0>=-.5 and x1<=page.rect.width+.5 and y1<=page.rect.height+.5,
                        f'Out of page: {path.name}:{i+1}:{span["text"]}')
            pages.append({'page':i+1,'text_characters':len(text),'spans':len(spans)})
            texts.append(text)
        return {'file':path.name,'sha256':digest(path),'pages':len(doc),
                'metadata':doc.metadata,'page_checks':pages},' '.join(' '.join(texts).split())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();p=args.root
    old=(p/'comparison-baseline'/f'{BASE}.tex').read_text();new=(p/f'{NAME}.tex').read_text()
    contract=json.loads((p/'assessment/edit-contract.json').read_text())
    require(len(contract['replacements'])==5,'Unexpected edit population')
    require(source_preserved(old,new,contract),'Source differs outside exact edit contract')
    ob,nb=results(old),results(new)
    require(len(nb)==8 and ob==nb,'Numbered statement/proof changed')
    require(displays(old)==displays(new),'Displayed mathematics changed')
    b0,b1=bibliography(old),bibliography(new)
    require(len(b0)==19 and len(b1)==20 and all(b1.get(k)==v for k,v in b0.items()),'Inherited bibliography changed')
    require(set(b1)-set(b0)=={'herlihywing'},'Unexpected bibliography addition')
    # Negative controls ensure a claimed preservation check really detects drift.
    bad=new.replace('Put $G=J\\cap P$.','Put $G=J\\cup P$.',1)
    require(bad!=new and not source_preserved(old,bad,contract) and results(bad)!=ob,
            'Proof-mutation control did not discriminate')
    bad=new.replace('the model\'s premises','all possible premises',1)
    require(bad!=new and not source_preserved(old,bad,contract),'Out-of-scope edit control failed')
    loc=read_labels((p/'build'/f'{NAME}.aux').read_text())
    oldlabels=re.findall(r'\\label\{([^}]+)\}',old);newlabels=re.findall(r'\\label\{([^}]+)\}',new)
    require(oldlabels==newlabels and len(newlabels)==len(set(newlabels)),'Labels changed or duplicated')
    require(set(newlabels)<=set(loc),'Unresolved label')
    refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',new));require(refs<=set(loc),'Unresolved reference')
    cited={k for chunk in re.findall(r'\\cite\{([^}]+)\}',new) for k in chunk.split(',')}
    require(cited<=set(b1),'Missing cited source')
    for i,b in enumerate(nb,1):
        label=re.search(r'\\label\{([^}]+)\}',b).group(1)
        require(loc[label]['number']==str(i),'Result renumbered')
    oldloc=json.loads((p/'comparison-baseline/resolved-labels.json').read_text())
    require(all(loc[k]['number']==v['number'] for k,v in oldloc.items() if k in set(oldlabels)),
            'An inherited number changed')
    sm=json.loads((p/'assessment/semantic-preservation.json').read_text())
    require(sm['count']==len(sm['rows'])==115 and len({r['id'] for r in sm['rows']})==115,'Inherited denominator changed')
    for r in sm['rows']:
        label=r['destination_label'];require(label in loc and r['destination_pdf_page']==loc[label]['page'],'Stale preservation locator')
    extra=json.loads((p/'assessment/inherited-workflow-obligations.json').read_text())
    require(extra['count']==len(extra['rows'])==12,'Workflow obligation denominator changed')
    for r in extra['rows']:
        require(r['label'] in loc and r['page']==loc[r['label']]['page'],'Stale workflow locator')
    scripts=json.loads((p/'assessment/checker-preservation.json').read_text())
    require(len(scripts)==6,'Wrong inherited checker count')
    for item in scripts:
        path=p/'verification'/item['file']
        require(digest(path)==item['sha256'] and path.stat().st_size==item['bytes'],'Inherited checker changed')
    pdfs=[]
    for file in (f'{NAME}.pdf','review-and-preservation.pdf'):
        info,text=inspect_pdf(p/'build'/file)
        if file.startswith(NAME):
            require(info['metadata'].get('title')==TITLE and not info['metadata'].get('author'),'Title/author metadata drift')
            # Source-edition identifiers in the bibliography are not labels of
            # this manuscript. The exact edit contract separately fixes headers.
            body=text.split('References',1)[0]
            version_pattern=r'\b(?:Version\s*\d+|v[1-9]\d*)\b'
            require(not re.search(version_pattern,body,re.I),'Visible manuscript-version label')
            require(re.search(version_pattern,body+' Version 5',re.I) is not None,
                    'Manuscript-label negative control failed')
            require(re.search(version_pattern,body+' v5',re.I) is not None,
                    'Short manuscript-label negative control failed')
            require('online version 5.0.0' in text, 'Inherited source-edition detail lost')
            for forbidden in ('dogfood','changelog','IMPLEMENTAUDIT','Nobel','Gettier','reviewer','sidecar','change what is true'):
                require(forbidden.lower() not in text.lower(),'Editorial/project material in manuscript: '+forbidden)
            require('All guard-relevant state' in text and 'Linearizability supplies' in text,'Missing clarified boundary')
        pdfs.append(info)
    for file in (f'{NAME}.log','review-and-preservation.log'):
        require(not re.search(r'Overfull|undefined|multiply defined',(p/'build'/file).read_text()),'Layout/reference warning')
    outcome={'status':'PASS','source_edit_contract_exact':True,'prose_replacements':5,
             'numbered_statements_and_proofs_byte_identical':len(nb),
             'displayed_mathematical_blocks_byte_identical':len(displays(new)),
             'inherited_bibliography_entries_byte_identical':19,'new_bibliography_entries':1,
             'preserved_labels':len(newlabels),'preservation_obligations':115,'inherited_workflow_obligations':12,
             'inherited_mathematical_checkers_unchanged':6,'negative_document_controls':2,
             'source_sha256':digest(p/f'{NAME}.tex'),'pdfs':pdfs,
             'limits':'Structural comparison and PDF text geometry. Not a semantic proof, visual review, peer review, historical-priority investigation or implementation verification.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(outcome,indent=2)+'\n')
    print(json.dumps({'status':'PASS','proofs':8,'displays':outcome['displayed_mathematical_blocks_byte_identical'],'pages':[x['pages'] for x in pdfs]}))
if __name__=='__main__':main()
