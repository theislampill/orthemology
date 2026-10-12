import sys, unittest, importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
class Availability(unittest.TestCase):
    def test_codec_and_compiler_exist(self):
        self.assertIsNotNone(importlib.util.find_spec('prcodec'), 'Concrete PR codec/compiler not implemented yet')
    def test_rational_flow_solver_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('flow_solver'), 'Exact rational flow solver not implemented yet')

from itertools import product
from fractions import Fraction as Q
from prcodec import *
import flow_solver as fs

def words(n):return product((0,1),repeat=n)
def ref_candidate(fn,e,i,u):
    return next((s for s in range(u+1) if all(fn(e,i,s,t) for t in range(u+1))),u+1)
def ref_sigma(fn,e,bits):
    out=[]
    for u,bit in enumerate(bits):
        r=ref_candidate(fn,e,0,u);old=ref_candidate(fn,e,0,u-1) if u else 0
        out.append(bit if r!=old else 0)
    return tuple(out)
def ref_pi(fn,e,bits):
    i=next((i for i,b in enumerate(bits) if b==0),len(bits))
    if i==len(bits):return tuple(bits)
    out=list(bits[:i+1])
    for u,bit in enumerate(bits[i+1:]):
        r=ref_candidate(fn,e,i,u);old=ref_candidate(fn,e,i,u-1) if u else 0
        out.append(bit if r!=old else 0)
    return tuple(out)
def ref_shift(base,bits,q):
    v=0
    for j,bit in enumerate(bits,1):
        v=2*v+bit
        if Q(v+1,2**j)<=q:return tuple(bits)
        if Q(v,2**j)>=q:return tuple(bits[:j])+output_prefix(base,bits[j:])
    return tuple(bits)

class CodecTests(unittest.TestCase):
    def test_roundtrip_and_canonical(self):
        ps=[pr_zero(2),pr_succ(),pr_proj(4,2),Program(2,2,Loop(3,V(0),Set(2,E('add',V(2),C(1)))))]
        for p in ps:
            self.assertEqual(decode(encode(p)),p);self.assertEqual(decode_bytes(encode_bytes(p)),p)
            data=encode_bytes(p)
            for n in range(len(data)):self.assertIsNone(decode_bytes(data[:n]))
            self.assertIsNone(decode_bytes(data+b'\0'))
        self.assertIsNone(decode_bytes(MAGIC+b'\x82\x00\x02\x11\x00'))
    def test_invalid_is_zero_resource_is_not(self):
        for e in (0,1,17,255,256,65535):self.assertEqual(evaluate_index(e,7,255),0)
        p=Program(2,2,Loop(3,V(0),Set(2,E('add',V(2),C(1)))))
        with self.assertRaises(ResourceLimit):evaluate_index(encode(p),100,255,step_limit=3)
        huge=Program(2,2,Set(2,E('pow2',V(0))))
        with self.assertRaises(ResourceLimit):run(huge,(100,1),max_bits=10)
    def test_snapshot_bound(self):
        p=Program(1,1,Loop(2,V(0),Seq(Set(0,C(99)),Set(1,E('add',V(1),C(1))))))
        self.assertEqual(run(p,(3,)),3)
    def test_primitive_recursive_closure(self):
        f=Program(2,2,Set(2,E('add',V(0),V(1))))
        p=compose(f,[pr_succ(),pr_proj(1,0)],1)
        for n in range(20):self.assertEqual(run(p,(n,)),2*n+1)
        # g(x)=x, h(x,t,y)=succ(y) gives addition.
        h=Program(3,3,Set(3,E('add',V(2),C(1))))
        a=prim_rec(pr_proj(1,0),h)
        for x in range(8):
            for y in range(8):self.assertEqual(run(a,(x,y)),x+y)
    def test_local_reset_on_repeated_inline(self):
        p=Program(4,4,Seq(Set(5,E('add',V(5),C(1))),Set(4,E('eq',V(5),C(1)))))
        observer=compile_pi3(p,0)
        for bits in words(6):
            self.assertEqual(output_prefix(observer,bits),ref_pi(lambda e,i,s,t:True,0,bits))
    def test_noninjectivity(self):
        a=pr_zero(2);b=Program(2,2,Seq(Set(2,C(0)),Set(3,C(7))))
        self.assertNotEqual(encode(a),encode(b))
        for bits in words(5):self.assertEqual(output_prefix(a,bits),output_prefix(b,bits))
    def test_expression_primitives(self):
        for op,expect in [('add',8),('sub',2),('mul',15),('div',1),('mod',2),('eq',0),('le',0)]:
            self.assertEqual(run(Program(0,0,Set(0,E(op,C(5),C(3)))),()),expect)
        self.assertEqual(run(Program(0,0,Set(0,E('div',C(5),C(0)))),()),0)
        self.assertEqual(run(Program(0,0,Set(0,E('mod',C(5),C(0)))),()),5)

class CompilerTests(unittest.TestCase):
    def test_sigma2_compilation(self):
        pairs=[(Program(3,3,Set(3,E('le',V(0),V(1)))),lambda e,i,s,t:s>=e),
               (Program(3,3,Set(3,E('le',V(2),V(1)))),lambda e,i,s,t:t<=s)]
        for source,fn in pairs:
            for e in range(3):
                p=decode(encode(compile_sigma2(source,e)))
                for bits in words(6):self.assertEqual(output_prefix(p,bits),ref_sigma(fn,e,bits))
    def test_pi3_compilation(self):
        pairs=[(Program(4,4,Set(4,E('le',E('add',V(1),C(1)),V(0)))),lambda e,i,s,t:i<e),
               (Program(4,4,Set(4,E('le',V(1),V(2)))),lambda e,i,s,t:i<=s),
               (Program(4,4,Set(4,E('le',V(3),V(2)))),lambda e,i,s,t:t<=s)]
        for source,fn in pairs:
            for e in range(3):
                p=decode(encode(compile_pi3(source,e)))
                for bits in words(6):self.assertEqual(output_prefix(p,bits),ref_pi(fn,e,bits))
    def test_rational_shift_compilation(self):
        sources=[pr_zero(2),Program(2,2,Set(2,E('mod',V(1),C(2)))),
                 Program(2,2,Set(2,E('mod',E('div',V(1),E('pow2',V(0))),C(2)))),
                 Program(2,2,Set(2,E('mod',V(0),C(2)))),
                 Program(2,2,Set(2,E('eq',E('div',V(1),E('pow2',E('add',V(0),C(1)))),C(1))))]
        for source in sources:
            for q in [Q(0),Q(1,3),Q(1,2),Q(2,3),Q(1)]:
                p=decode(encode(compile_shift(source,q.numerator,q.denominator)))
                for bits in words(6):self.assertEqual(output_prefix(p,bits),ref_shift(source,bits,q))
    def test_q8_bounded_machine_compiler(self):
        machines=[([('H',)],0),([('I',0,1),('H',)],1),([('I',0,1),('D',0,2,1),('H',)],3)]
        for machine,halt_at in machines:
            p=decode(encode(compile_q8(machine)))
            for bits in words(6):self.assertEqual(output_prefix(p,bits),tuple(0 if n<halt_at else b for n,b in enumerate(bits)))
        p=compile_q8([('I',0,0)])
        for bits in words(5):self.assertEqual(output_prefix(p,bits),(0,)*5)
    def test_prefix_causality(self):
        p=compile_pi3(Program(4,4,Set(4,E('le',V(1),V(2)))),0)
        for b in words(4):
            ans=output_prefix(p,b)
            for tail in words(2):self.assertEqual(output_prefix(p,b+tail)[:4],ans)
    def test_compiler_refusals(self):
        with self.assertRaises(ValueError):compile_pi3(pr_zero(3),0)
        with self.assertRaises(ValueError):compile_sigma2(pr_zero(4),0)
        with self.assertRaises(ValueError):compile_shift(pr_zero(2),1,0)
        with self.assertRaises(ValueError):compile_q8([('I',0,8)])
        with self.assertRaises(ValueError):compile_q8([])

class FlowTests(unittest.TestCase):
    def test_interval_correspondence(self):
        rows=[[( (Q(0),Q(1)),Q(1,2)),((Q(0),Q(-1)),Q(-1,4))],
              [((Q(0),Q(1)),Q(3,4)),((Q(0),Q(-1)),Q(-1,2))]]
        r=fs.solve(rows);self.assertTrue(fs.verify(r));self.assertTrue(Q(1,3)<=r['probabilities'][1]<=Q(2,3))
    def test_periodic_swap(self):
        rows=[[((Q(1),Q(0)),Q(0))],[((Q(0),Q(1)),Q(0))]]
        r=fs.solve(rows);self.assertEqual(r['probabilities'],(Q(1,2),Q(1,2)))
    def test_empty_zero_weight_row_refused(self):
        with self.assertRaises(ValueError):fs.solve([[],[((Q(1),Q(1)),Q(-1))]])
    def test_zero_weight_row_keeps_valid_witness(self):
        r=fs.solve([[((Q(0),Q(1)),Q(0))],[]]);self.assertTrue(fs.verify(r))
    def test_three_state_cycle(self):
        rows=[]
        for i in range(3):
            rows.append([(tuple(Q(int(j==k)) for j in range(3)),Q(0)) for k in range(3) if k!=(i+1)%3])
        r=fs.solve(rows);self.assertEqual(r['probabilities'],(Q(1,3),)*3)
    def test_exact_data_and_infeasibility(self):
        with self.assertRaises(TypeError):fs.solve([[((0.0,),Q(1))]])
        self.assertIsNone(fs.vertex(1,[],[((Q(1),),Q(0)),((Q(-1),),Q(-1))]))
        self.assertFalse(fs.verify({'probabilities':(Q(1,2),Q(1,2)),'flow':((Q(1),Q(0)),(Q(0),Q(0))),'rows':((Q(1),Q(0)),(Q(0),Q(1))),'input_rows':((),())}))

class VerifierBoundaryTests(unittest.TestCase):
    def test_external_input_binding(self):
        import inspect
        self.assertGreaterEqual(len(inspect.signature(fs.verify).parameters),2)
        good=fs.solve([[],[]])
        self.assertTrue(fs.verify(good,[[],[]]))
        self.assertFalse(fs.verify(good,[[((1,1),-1)],[]]))
    def test_schema_exactness(self):
        good=fs.solve([[],[]])
        for bad in [None,{},dict(good,probabilities=(1.0,0)),
                    dict(good,probabilities=(True,0)),dict(good,flow=((1,0,9),(0,0,9))),
                    dict(good,rows=((1,),(0,1))),dict(good,input_rows=([],)),
                    dict(good,input_rows=([((1,),0)],[]))]:
            try:answer=fs.verify(bad)
            except (TypeError,KeyError,IndexError,ValueError):self.fail('Malformed result must be refused, not interpreted')
            self.assertFalse(answer)

class BoundaryRegressionTests(unittest.TestCase):
    def test_malformed_counter_instruction(self):
        for machine in [[()], [['H']], [('I',True,0)], [('D',0,0,False)]]:
            with self.assertRaises(ValueError):compile_q8(machine)
    def test_direct_execution_discovers_full_suite(self):
        text=Path(__file__).read_text()
        lines=text.splitlines()
        self.assertGreater(next(i for i,line in enumerate(lines) if line.startswith("if __name__==")),next(i for i,line in enumerate(lines) if line.startswith("class BoundaryRegressionTests")))

if __name__=='__main__':unittest.main()
