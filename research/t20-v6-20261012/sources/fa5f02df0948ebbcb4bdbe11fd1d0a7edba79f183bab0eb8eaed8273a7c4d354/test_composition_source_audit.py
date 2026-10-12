"""Additive source-alignment checks; old models are imported without editing.
These diagnose representation contracts, not metaphysical actual production.
"""
from pathlib import Path
from fractions import Fraction
from dataclasses import fields
import sys,unittest,json
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
FRONT=HERE.parents[2]
sys.path.insert(0,str(FRONT/'coalescence-composition/src'))
import composition as m


def leaves(t):
    return [t] if isinstance(t,m.Leaf) else leaves(t.left)+leaves(t.right)

def token_audit(t):
    """Necessary registry conditions IF Leaf.token is to name one actual act.
    This does not change tree evaluation or assert all causal DAGs forbid reuse.
    """
    by_id={};conflicts=[];duplicate_refs=[]
    for leaf in leaves(t):
        signature=(leaf.bearer,leaf.setting)
        if leaf.token in by_id:
            if by_id[leaf.token]!=signature:conflicts.append(leaf.token)
            else:duplicate_refs.append(leaf.token)
        else:by_id[leaf.token]=signature
    return {'ids':sorted(by_id),'conflicting_same_id':conflicts,'repeated_reference':duplicate_refs}


class SourceAlignmentChecks(unittest.TestCase):
    def test_map_one_id_cannot_belong_to_two_bearers(self):
        with self.assertRaises(ValueError):
            m.merge({'alpha':m.Act('A',0,0)},{'alpha':m.Act('B',0,0)})
    def test_distinct_keys_not_record_values_determine_act_count(self):
        value=m.Act('A',0,0)
        one={'alpha':value};two={'alpha':value,'alpha2':value}
        self.assertIs(two['alpha'],two['alpha2'])
        self.assertEqual((m.summary(one)[1],m.summary(two)[1]),(1,2))
        self.assertEqual(m.merge(one,one),one)
        # Two keys assert two actual occurrences; the program cannot certify that assertion.
    def test_bare_tree_does_not_validate_numerical_token_owner(self):
        t=m.Branch(m.Leaf('shared','A',0),m.Leaf('shared','B',0))
        self.assertEqual(m.evaluate(t),0)
        self.assertEqual(token_audit(t)['conflicting_same_id'],['shared'])
    def test_same_leaf_reference_is_syntax_reuse_not_new_actual_act(self):
        a=m.Leaf('alpha','A',0);b=m.Leaf('beta','B',1)
        ordinary=m.Branch(a,b);reused=m.Branch(a,m.Branch(a,b))
        self.assertEqual((m.evaluate(ordinary),m.evaluate(reused)),(2,1))
        self.assertEqual(token_audit(ordinary)['ids'],token_audit(reused)['ids'])
        self.assertEqual(token_audit(reused)['repeated_reference'],['alpha'])
        self.assertNotEqual(m.flatten(ordinary),m.flatten(reused))
    def test_owner_summary_not_numerically_one_intrinsic_act(self):
        original={'alpha1':m.Act('A',0,1),'alpha2':m.Act('A',1,1),'beta':m.Act('B',0,1)}
        replacement={'alpha_star':m.Act('A',2,1),'beta':m.Act('B',0,1)}
        self.assertEqual(m.owner_group_Z3_mean(original),1)
        self.assertEqual(m.owner_group_Z3_mean(original),m.owner_group_Z3_mean(replacement))
        self.assertNotEqual(set(original),set(replacement))
        self.assertEqual((len(original),len(replacement)),(3,2))
        self.assertEqual(m.support(original),m.support(replacement))
        self.assertIsInstance(m.owner_group_Z3_mean(original),int)
    def test_owner_decoder_is_not_the_rational_intention_interpreter(self):
        state={'alpha1':m.Act('A',0,0),'alpha2':m.Act('A',1,0),'beta':m.Act('B',1,0)}
        self.assertEqual(m.owner_group_Z3_mean(state),0)
        self.assertEqual(m.visible(state),Fraction(2,3))
        self.assertFalse(m.own_end(state,'A',0))
        changed_goals={k:m.Act(a.bearer,a.setting,1) for k,a in state.items()}
        self.assertEqual(m.owner_group_Z3_mean(state),m.owner_group_Z3_mean(changed_goals))
    def test_rational_contextual_success_changes_the_selected_exercise(self):
        p0={'beta':m.Act('B',0,1)};p2={'beta':m.Act('B',2,1)}
        r0=m.issue_response(p0,'A','alpha0',1);r2=m.issue_response(p2,'A','alpha2',1)
        self.assertEqual((r0['alpha0'].goal,r2['alpha2'].goal),(1,1))
        self.assertEqual((r0['alpha0'].setting,r2['alpha2'].setting),(2,0))
        self.assertEqual(m.visible(m.merge(p0,r0)),1)
        self.assertEqual(m.visible(m.merge(p2,r2)),1)
        self.assertNotEqual(m.visible(r0),1);self.assertNotEqual(m.visible(r2),1)
    def test_diagonal_suppression_reuses_A_record_not_complete_state(self):
        act=m.Act('A',0,0);solo={'alpha':act};joint=m.merge(solo,{'beta':m.Act('B',0,0)})
        suppressed=m.suppress(joint,'beta')
        self.assertIs(suppressed['alpha'],act)
        self.assertEqual(m.created_output(joint),m.created_output(suppressed))
        self.assertTrue(m.own_end(joint,'A',0));self.assertTrue(m.own_end(suppressed,'A',0))
        self.assertNotEqual(joint,suppressed)
        self.assertEqual((m.support(joint),m.support(suppressed)),(frozenset({'A','B'}),frozenset({'A'})))
    def test_actual_schema_limits_are_exposed(self):
        self.assertEqual([f.name for f in fields(m.Act)],['bearer','setting','goal'])
        self.assertEqual([f.name for f in fields(m.Leaf)],['token','bearer','setting'])
        self.assertEqual(m.created_output({'alpha':m.Act('A',0,0)}),frozenset({('created-profile',Fraction(0))}))
        self.assertFalse(hasattr(m.Act('A',0,0),'power_token'))
        self.assertFalse(hasattr(m,'entire_provider'))

if __name__=='__main__':unittest.main(verbosity=2)
