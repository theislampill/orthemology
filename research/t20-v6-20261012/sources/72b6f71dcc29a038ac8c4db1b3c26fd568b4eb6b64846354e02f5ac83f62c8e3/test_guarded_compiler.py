"""Bounded deterministic tests, not a sampling or performance campaign."""
from fractions import Fraction as F
from itertools import combinations, product
import unittest
from guarded_compiler import Rule, Tree, compile_exact, exact_step, tree_value, prune_exact

METRICS = {}

def powerset(items):
    return tuple(frozenset(c) for n in range(len(items)+1) for c in combinations(items,n))

def R(name, head, premises=(), support=(), cost=0, allowed=None):
    return Rule(name,head,tuple(premises),frozenset(support),F(cost),allowed)

def prices(table):
    return {q:{s:row[0] for s,row in rows.items()} for q,rows in table.items()}

def allow(evidence, arity, predicate):
    return frozenset(ss for ss in product(powerset(evidence),repeat=arity) if predicate(ss))

# Token identity, proposition version, report role and recorded source ancestry.
# These are declared fixture metadata, not measurements of truth or independence.
META = {
 'a': ('P@v1','corroborating_report','root-A'),
 'b': ('P@v1','corroborating_report','root-B'),
 'copy_a': ('P@v1','corroborating_report','root-A'),
 'unrelated': ('Q@v1','corroborating_report','root-C'),
 'admin': ('P@v1','receipt_only','root-D'),
 'old': ('P@v0','corroborating_report','root-E'),
}

def corroborates(ss):
    roots={META[e][2] for e in ss[0]
           if META[e][:2] == ('P@v1','corroborating_report')}
    return len(roots)>=2


def source_fixture():
    E=('a','b')
    rules=(R('first_report','packet',support=('a',),cost=1),
           R('adjoin_corroborating_report','packet',('packet',),('b',),1),
           R('two_root_licence','licensed',('packet',),cost=1,
             allowed=allow(E,1,corroborates)))
    return ('packet','licensed'),E,rules


def unpruned_oracle(judgements, rules, rounds):
    """Independently enumerate EVERY support/price pair up to a height bound."""
    old={q:set() for q in judgements}
    for _ in range(rounds):
        new={q:set(old[q]) for q in judgements}
        for r in rules:
            for children in product(*(old[q] for q in r.premises)):
                ss=tuple(s for s,c in children)
                if r.allowed is not None and ss not in r.allowed:
                    continue
                s=set(r.support); c=r.cost
                for cs,cc in children:
                    s.update(cs); c+=cc
                new[r.head].add((frozenset(s),c))
        old=new
    return {q:{s:min(c for t,c in pairs if t==s) for s,_ in pairs}
            for q,pairs in old.items()}


class GuardedCompilerTests(unittest.TestCase):
    def test_larger_corroborating_support_is_retained_for_guard(self):
        J,E,rules=source_fixture()
        got,history=compile_exact(J,E,rules)
        self.assertEqual(prices(got),{'packet':{frozenset('a'):F(1),frozenset('ab'):F(2)},
                                     'licensed':{frozenset('ab'):F(3)}})
        # The source-sensitive proof needs three nodes despite only two judgements.
        self.assertEqual(len(history),len(J)*(len(E)+1)+1)
        self.assertFalse(history[2]['licensed'])
        self.assertEqual(tree_value(got['licensed'][frozenset('ab')][1],rules)[3],3)

    def test_copies_incidental_roles_and_wrong_versions_do_not_corroborate(self):
        self.assertTrue(corroborates((frozenset(('a','b')),)))
        for e in ('copy_a','unrelated','admin','old'):
            self.assertFalse(corroborates((frozenset(('a',e)),)),e)
        self.assertFalse(corroborates((frozenset(META)-{'b'},)))

    def test_ordered_disjoint_source_guard_can_be_nonmonotone(self):
        E=('a','b')
        # Two separately selected report packages must have disjoint roots.
        guard=allow(E,2,lambda ss:bool(ss[0]) and bool(ss[1]) and ss[0].isdisjoint(ss[1]))
        self.assertIn((frozenset('a'),frozenset('b')),guard)
        self.assertNotIn((frozenset('ab'),frozenset('b')),guard)
        rules=(R('a','p',support='a',cost=2),R('b','p',support='b',cost=3),
               R('ab','p',support='ab',cost=0),R('independent','t',('p','p'),cost=1,allowed=guard))
        result,_=compile_exact(('p','t'),E,rules)
        self.assertEqual(prices(result)['t'],{frozenset('ab'):F(6)})

    def test_unsupported_cycles_and_zero_cost_cycles(self):
        loop=R('loop','p',('p',))
        empty,_=compile_exact(('p',),('e',),(loop,))
        self.assertEqual(empty,{'p':{}})
        base=R('base','p',support='e',cost=F(1,3))
        result,_=compile_exact(('p',),('e',),(base,loop))
        self.assertEqual(prices(result),{'p':{frozenset('e'):F(1,3)}})
        self.assertEqual(tree_value(result['p'][frozenset('e')][1],(base,loop))[3],1)

    def test_equal_support_pruning_preserves_external_guard_and_exact_support(self):
        J,E,rules=source_fixture()
        first,add,target=rules
        noop=R('recheck','packet',('packet',),cost=0)
        rules+= (noop,)
        p=Tree(add,(Tree(first,()),))
        long=Tree(target,(Tree(noop,(Tree(noop,(p,)),)),))
        reduced=prune_exact(long,rules)
        before=tree_value(long,rules); after=tree_value(reduced,rules)
        self.assertIsNotNone(before); self.assertIsNotNone(after)
        self.assertEqual(before[:2],after[:2]); self.assertLessEqual(after[2],before[2])
        self.assertEqual(after[3],3); self.assertLess(after[4],before[4])
        # Replacing packet {a,b} with the cheaper packet {a} violates the licence.
        with self.assertRaises(ValueError):
            tree_value(Tree(target,(Tree(first,()),)),rules)

    def test_repeated_premises_pay_twice_and_rational_cost_is_exact(self):
        base=R('base','p',support='e',cost=F(1,3))
        combine=R('twice','t',('p','p'),cost=F(1,5))
        result,_=compile_exact(('p','t'),('e',),(base,combine))
        self.assertEqual(prices(result)['t'],{frozenset('e'):F(13,15)})

    def test_contract_rejects_unknown_evidence_and_negative_prices(self):
        for rule in (R('outside','p',support='x'),R('negative','p',cost=-1),
                     R('unknown_premise','p',('q',)),
                     R('bad_guard','p',('p',),allowed=frozenset({(frozenset('x'),)}))):
            with self.assertRaises(ValueError):
                compile_exact(('p',),('e',),(rule,))

    def test_mutable_rule_fields_are_rejected_before_witness_construction(self):
        malformed=(Rule('list_premises','p',[],frozenset('e'),F(0)),
                   Rule('set_support','p',(),set('e'),F(0)),
                   Rule('guard_shape','p',('p',),frozenset(),F(0),frozenset({frozenset('e')})))
        for rule in malformed:
            with self.assertRaises(ValueError,msg=rule.name):
                compile_exact(('p',),('e',),(rule,))

    def test_all_unary_guard_truth_tables_against_unpruned_oracle(self):
        E=('a','b'); J=('p','t'); supports=powerset(E)
        count=witnesses=0
        # Every one-premise Boolean guard on all four supports, with each local
        # support. Fixed zero/positive-cost bases and an enriching cycle are used.
        for mask in range(16):
            allowed=frozenset((supports[i],) for i in range(4) if mask&(1<<i))
            for local in supports:
                rules=(R('empty','p',cost=3),R('a','p',support='a',cost=1),
                       R('enrich','p',('p',),support='b',cost=1),
                       R('guarded','t',('p',),local,1,allowed))
                table,history=compile_exact(J,E,rules)
                bound=len(J)*(len(E)+1)
                self.assertEqual(prices(table),unpruned_oracle(J,rules,bound+2))
                self.assertEqual(prices(table),prices(exact_step(J,rules,table)))
                for q,rows in table.items():
                    for s,(cost,t) in rows.items():
                        val=tree_value(t,rules)
                        self.assertEqual(val[:3],(q,s,cost)); self.assertLessEqual(val[3],bound)
                        witnesses+=1
                count+=1
        METRICS['all_unary_guard_truth_tables_cases']=count
        METRICS['compiled_witnesses_checked']=witnesses

if __name__=='__main__':
    unittest.main(verbosity=2)
