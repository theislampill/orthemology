"""Supplementary cross-implementation regression; not a theorem about Python source."""
import csv, importlib.util, json, pathlib
from fractions import Fraction
spec=importlib.util.spec_from_file_location('predecessor_probe','private-locator:71d899355bd9e81c1732')
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
rows=list(csv.reader(open('solver-small-results.csv')))
assert len(rows)==260
counts={1:0,2:0}
for m,code,num,den in rows:
    m,code=int(m),int(code)
    table=[]
    for q in range(m):
        edges=[]
        for b in (False,True):
            e=(code//((2*m)**(2*q+int(b))))%(2*m)
            edges.append((e//2,e%2))
        table.append(tuple(edges))
    actual=Fraction(int(num),int(den))
    expected=reference.defect(table)[0]
    assert actual==expected,(m,code,actual,expected)
    counts[m]+=1
out={'lean_source':'SolverProbe.lean','lean_solver':'MealySolver.solveDefect','compared_against':'private-locator:71d899355bd9e81c1732 defect','checked_machines_by_states':counts,'all_match':True,'interpretation':'Executable regression evidence only; the Lean theorem proves Lean solver correctness independently, and this finite test does not prove Python source correspondence.'}
pathlib.Path('solver-small-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
