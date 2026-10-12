from pathlib import Path
import re,json
R=Path(__file__).resolve().parent; W=R.parent
src=(W/'hase-imported-compiler-transport-20261010/sources/ExtensionalRepairSyntax.lean').read_text()
main=src.split('mutual',1)[1].split('\nend',1)[0]
grammar={}
for name in ['CtxE','FormE','HasE']:
    body=main.split('inductive '+name,1)[1].split('  inductive ',1)[0]
    grammar[name]=re.findall(r'^\s*\|\s+(\w+)\s*:',body,re.M)
expected=sum(grammar.values(),[]); ports=[]
for file,thm in [('HasEStructuralBase.lean','form_trename'),('HasEStructuralRename.lean','form_rename')]:
    txt=(R/'sources'/file).read_text().split('theorem '+thm,1)[1].split('\ntheorem ',1)[0]
    branches=re.findall(r'^\s*\|\s*@?(\w+)',txt,re.M)
    assert set(expected)<=set(branches),(file,set(expected)-set(branches))
    ports.append({'file':file,'theorem':thm,'constructors_covered':expected,'branch_labels':branches,'omitted':[]})
(R/'SOURCE_CONSTRUCTOR_COVERAGE.json').write_text(json.dumps({'status':'PASS','actual_grammar':grammar,'ports':ports},indent=2)+'\n')
print('PASS actual 2/7/20 mutual constructor source coverage.')
