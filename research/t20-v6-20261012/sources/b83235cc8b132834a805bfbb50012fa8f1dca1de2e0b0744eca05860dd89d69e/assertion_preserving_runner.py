"""Additive assertion-preserving execution adapter; original scripts remain unchanged.
Transforms `assert predicate, message` into `if not predicate: raise AssertionError(message)`
before compilation, so Python -O cannot remove checks. No extra mathematical credit.
"""
import ast,sys
from pathlib import Path
class KeepAssertions(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[] if node.msg is None else [node.msg],keywords=[]),cause=None)],orelse=[]),node)
def compile_preserving(source,filename):
    tree=ast.parse(source,filename);tree=KeepAssertions().visit(tree);ast.fix_missing_locations(tree)
    return compile(tree,filename,'exec',optimize=0)
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: assertion_preserving_runner.py SCRIPT | --self-test')
    if sys.argv[1]=='--self-test':
        try:exec(compile_preserving("assert False, 'sentinel'",'<sentinel>'),{})
        except AssertionError as e:
            if str(e)!='sentinel':raise RuntimeError('Wrong sentinel message')
            print('PASS: false assertion raises even under optimized execution')
        else:raise RuntimeError('False assertion was erased')
    else:
        script=Path(sys.argv[1]).resolve();exec(compile_preserving(script.read_text(),str(script)),{'__name__':'__main__','__file__':str(script),'__builtins__':__builtins__})
