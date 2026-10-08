"""Independent synthetic-only parser, statistic and enclosure controls."""
import ast
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import tempfile
import unittest
import placement_core as core
import certified_exp as interval
from independent_oracles import (GAMMAS, adaptive_tail, descriptive_oracle,
    exp_negative_enclosure, fixture)

def decimal_token(x):
    if x is None: return ' \t '
    with localcontext() as ctx:
        ctx.prec=220
        return format(Decimal(x.numerator)/Decimal(x.denominator),'f')


def serialize(records):
    """Make stage CSV dictionaries from the independently chosen semantic fixture."""
    rosters={}
    people={}
    for row in records:
        rosters.setdefault(row['game'],set()).add(row['player'])
        people.setdefault((row['game'],row['player']),[]).append(row)
    output=[]
    for source in records:
        person=sorted(people[(source['game'],source['player'])],key=lambda x:x['round'])
        row={
            'gameId':source['game'], 'playerId':source['player'],'batchId':'synthetic-batch',
            'round.index':str(source['round']),
            'treatment.playerCount':str(len(rosters[source['game']])+1),
            'treatment.reward':'group',
            'round.data.ifp':repr({'willHappen':source['truth'],'globalAccurate':source['global_correct'],'synthetic_task':'task-'+str(source['round'])}),
            'player.data.roundLocalAccurate':repr([x['local_correct'] for x in person]),
            'player.data.roundLeftSide':repr(['local' if x['local_left'] else 'global' for x in person]),
            'player.data.roundSignals':repr([{'local':{'pro':0,'against':1},'global':{'pro':1,'against':0}} for _ in range(48)]),
            'player.data.localSource':'synthetic local source',
            'player.data.globalSource':'synthetic global source',
            'playerRound.data.value':decimal_token(source['forecast']),
            'playerRound.data.correct':'', 'playerRound.data.groupCorrect':'',
            'playerRound.data.groupVoteEmpty':'', 'playerRound.data.yesGroup':'',
            'playerRound.data.rewarded':'False','playerRound.data.knowledgeOfSubject':'2',
            'player.data.score':'0',
        }
        output.extend(dict(row,**{'stage.name':s}) for s in ['question','response','feedback'])
    return output


def summarize(records):return core.summarize(core.validate_rows(serialize(records)))


class IndependentImplementationControls(unittest.TestCase):
    def test_exact_parser_beyond_float_resolution(self):
        for token,expected in [('50.00000000000000000001',Q('50.00000000000000000001')),('1e-100',Q(1,10**100)),(' 5.000e+1 ',Q(50)),('100.000000000000000000000',Q(100)),('-0e10',Q(0)),(' \t\n',None)]:
            self.assertEqual(core.parse_forecast(token),expected)
        for token in ['NaN','Infinity','-Infinity','None','null','0x10','1_0','1/2','True','100.000000000000000000001','-0.000000000000000000001','５０',50,True]:
            with self.subTest(token=token),self.assertRaises(core.ValidationError):core.parse_forecast(token)

    def test_event_dictionary_ambiguity_fails_closed(self):
        for token in ["{'willHappen': True, 'globalAccurate': False, **{'willHappen': False}}", "{'willHappen': True, 'globalAccurate': False, ('will'+'Happen'): False}"]:
            with self.subTest(token=token),self.assertRaises(core.ValidationError):core.event_bits(token)

    def test_all_repeated_final_state_fields_gate(self):
        for field,value in [('playerRound.data.rewarded','True'),('playerRound.data.knowledgeOfSubject','3'),('player.data.score','1'),('round.data.ifp',repr({'willHappen':True,'globalAccurate':False,'synthetic_task':'changed'}))]:
            rows=serialize(fixture());rows[1][field]=value
            with self.subTest(field=field),self.assertRaises(core.ValidationError):core.validate_rows(rows)

    def test_truth_table(self):
        for h,lc,gc in product((False,True),repeat=3):
            self.assertEqual(core.cues(h,lc,gc),(h if lc else not h,h if gc else not h,lc!=gc))
        for bits in [(1,True,False),(True,0,False),(True,True,'False')]:
            with self.assertRaises(core.ValidationError):core.cues(*bits)

    def test_unequal_roster_statistic_against_independent_oracle(self):
        cases=[fixture()]
        for replacement in [None,Q(50),Q('50.00000000000000000001')]:
            r=fixture();r[0]['forecast']=replacement;cases.append(r)
        for r in cases:
            expected=descriptive_oracle(r);actual=summarize(r)
            for key in ['S','T','H','V']:self.assertEqual(actual[key],expected[key],key)
            self.assertEqual(actual['sum_abs_a'],expected['total_abs'])
            for short,long in [('plus','local_left'),('minus','global_left')]:
                for prefix in ['M','V','Q']:self.assertEqual(actual['sides'][long][prefix],expected[prefix+'_'+short])
            for short,long in [('present','valid'),('absent','absent'),('midpoint','exactly_50')]:
                self.assertEqual(actual['overall'][long],expected[short]);self.assertEqual(actual['disagreement'][long],expected['eligible_'+short])
            self.assertEqual(actual['S_R'],expected['V_plus']-expected['V_minus'])

    def test_zero_support_and_availability_rates(self):
        r=fixture()
        for row in r:
            if row['game']=='game-A':row['global_correct']=row['local_correct']
        actual=summarize(r)
        self.assertEqual(actual['games'],2);self.assertEqual(actual['H'],Q(1,2));self.assertEqual(actual['S'],Q(1,4))
        for row in r:row['local_left']=True
        actual=summarize(r)
        self.assertIsNone(actual['sides']['global_left']['availability_rate']);self.assertEqual(actual['sides']['global_left']['M'],0)
        self.assertIsNone(actual['availability_rate_difference'])
        for row in r:row['forecast']=None
        actual=summarize(r)
        self.assertEqual((actual['S'],actual['T'],actual['V']),(0,0,0));self.assertEqual(actual['games'],2)

    def test_full_population_failure_controls(self):
        base=serialize(fixture())
        cases=[base+[dict(base[0])],base[1:],base[3:]]
        for field,value in [('round.index','48'),('round.index','0.25'),('gameId',''),('playerId',''),('batchId',''),('batchId','other'),('treatment.playerCount','0'),('treatment.playerCount','9'),('treatment.reward','individual'),('player.data.localSource','changed'),('player.data.roundLocalAccurate',repr([True]*47)),('player.data.roundLocalAccurate',repr([1]*48)),('player.data.roundLeftSide',repr(['local']*49)),('player.data.roundLeftSide',repr(['left']*48)),('playerRound.data.value','49.99999999999999999999')]:
            rows=copy.deepcopy(base);rows[1][field]=value;cases.append(rows)
        for i,rows in enumerate(cases):
            with self.subTest(case=i),self.assertRaises(core.ValidationError):core.validate_rows(rows)
        with self.assertRaises(core.ValidationError):core.validate_rows(base,expected_counts={'opportunities':143})
        rows=copy.deepcopy(base)
        for row in rows:row['treatment.playerCount']='1'
        with self.assertRaises(core.ValidationError):core.validate_rows(rows)
        rows=copy.deepcopy(base)
        for row in rows:
            if row['gameId']=='game-B' and row['playerId']=='p2' and row['round.index']=='0':row['round.data.ifp']=repr({'willHappen':False,'globalAccurate':False})
        with self.assertRaises(core.ValidationError):core.validate_rows(rows)

    def test_projection_seven_fields_and_complete_keys(self):
        semantic=fixture();validated=core.validate_rows(serialize(semantic))
        projections=[]
        for row in semantic:
            projections.append({'gameId':row['game'],'playerId':row['player'],'roundIndex':str(row['round']),
                'forecast':decimal_token(row['forecast']),'accuracy':'','groupAccuracy':'',
                'expN':'2' if row['game']=='game-A' else '3',
                'globalAccuracy':str(int(row['global_correct'])),'localAccuracy':str(int(row['local_correct'])),
                'incentiveScheme':'group'})
        receipt=core.validate_projection(projections,validated)
        self.assertEqual(receipt['checks_passed'],7);self.assertEqual(receipt['rows'],144)
        cases=[projections[:-1],projections+[dict(projections[0])]]
        for field,value in [('forecast','99'),('accuracy','True'),('groupAccuracy','False'),('expN','9'),('globalAccuracy','True'),('localAccuracy','0'),('incentiveScheme','individual'),('playerId','other'),('roundIndex','48')]:
            mutant=copy.deepcopy(projections);mutant[0][field]=value;cases.append(mutant)
        for i,rows in enumerate(cases):
            with self.subTest(case=i),self.assertRaises(core.ValidationError):core.validate_projection(rows,validated)

    def test_semantic_repeats_and_missing_score_invariance(self):
        rows=serialize(fixture())
        for i,t in enumerate(['50','50.0','5e1']):rows[i]['playerRound.data.value']=t
        baseline=core.summarize(core.validate_rows(rows))
        for row in rows:row['playerRound.data.correct']='False'
        self.assertEqual(core.summarize(core.validate_rows(rows)),baseline)

    def test_order_preserves_bytes_and_full_coordinates(self):
        keys=[('é','a',0),('z','b',1),('A ','z',2),('A','z',2),('A','a',2),('A','z',1)]
        self.assertEqual(core.coordinate_order(keys),[('A','z',1),('A','a',2),('A','z',2),('A ','z',2),('z','b',1),('é','a',0)])
        v=core.validate_rows(serialize(fixture()))
        self.assertEqual(len(v.order),144)
        self.assertEqual(v.order[:3],[('game-A','p1',0),('game-A','p1',1),('game-A','p1',2)])
        self.assertEqual(v.order[48:52],[('game-B','p1',0),('game-B','p2',0),('game-B','p1',1),('game-B','p2',1)])

    def test_all_encoding_invariances(self):
        r=fixture();s=summarize(r)
        for row in r:row['local_left']=not row['local_left']
        self.assertEqual(summarize(r)['S'],-s['S']);self.assertEqual(summarize(r)['T'],s['T'])
        r=fixture()
        for row in r:
            row['local_correct'],row['global_correct']=row['global_correct'],row['local_correct']
            row['local_left']=not row['local_left']
        self.assertEqual(summarize(r)['S'],s['S'])
        r=fixture()
        for row in r:row['truth']=not row['truth'];row['forecast']=100-row['forecast']
        self.assertEqual(summarize(r)['S'],s['S'])
        r=fixture()
        for row in r:row['forecast']=Q(100 if row['local_left'] else 0)
        self.assertEqual(summarize(r)['S'],Q(3,4))

    def test_structural_receipt_has_no_relation_or_keys(self):
        import json
        v=core.validate_rows(serialize(fixture()))
        text=json.dumps(v.receipt)
        for forbidden in ['game-A','game-B','p1','p2','Q_plus','Q_minus','availability_rate','local_left','global_left','disagreement']:
            self.assertNotIn(forbidden,text)
        self.assertFalse(v.receipt['placement_forecast_relation_computed'])

    def test_synthetic_hash_change_does_not_touch_original(self):
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'synthetic-original';q=Path(d)/'synthetic-copy'
            p.write_bytes(b'synthetic source');original=p.read_bytes();digest=sha256(original).hexdigest()
            self.assertEqual(core.verify_file(p,digest,len(original))['sha256'],digest)
            q.write_bytes(original+b'!')
            with self.assertRaises(core.ValidationError):core.verify_file(q,digest,len(original))
            self.assertEqual(p.read_bytes(),original)

    def test_interval_independent_oracle_and_positive_underflow(self):
        for x in [Q(0),Q(1,10**100),Q(1,3),Q(1),Q(23,7),Q(100),Q(10000)]:
            lo,hi=interval.exp_neg_interval(x)
            olo,ohi=exp_negative_enclosure(x)
            self.assertLessEqual(lo,ohi);self.assertGreaterEqual(hi,olo)
            self.assertTrue(0<=lo<=hi<=1);self.assertGreater(hi,0)
            self.assertLessEqual(hi-lo,Q(1,10**12))
            with localcontext() as ctx:
                ctx.prec=220;point=(-(Decimal(x.numerator)/Decimal(x.denominator))).exp()
                self.assertLessEqual(Decimal(lo.numerator)/Decimal(lo.denominator),point)
                self.assertGreaterEqual(Decimal(hi.numerator)/Decimal(hi.denominator),point)

    def test_bound_direction_all_frozen_gammas(self):
        self.assertEqual(interval.GAMMAS,GAMMAS)
        for a in [[Q(1)],[Q(0)],[Q(1),Q(1)],[Q(1),Q(-2),Q(0)],[Q(1,3),Q(-2,7),Q(5,9)]]:
            aa=sum(map(abs,a),Q(0));v=sum((x*x for x in a),Q(0))
            for t in [Q(0),Q(1,3),Q(1),Q(2),Q(7)]:
                previous=None
                for g in GAMMAS:
                    result=interval.closed_bound(t,aa,v,g);lo,hi=result['interval']
                    self.assertEqual(result['D'],(g-1)*aa/(g+1))
                    self.assertGreaterEqual(hi,adaptive_tail(a,t,g));self.assertTrue(0<=lo<=hi<=1)
                    if previous:self.assertGreaterEqual(hi,previous[0])
                    previous=(lo,hi)

    def test_near_alpha_straddling_and_upward_render(self):
        with localcontext() as ctx:
            ctx.prec=160;x=Q(str(Decimal(40).ln().quantize(Decimal('1e-110'))))
        lo,hi=interval.exp_neg_interval(x)
        self.assertLessEqual(2*lo,Q(1,20));self.assertGreaterEqual(2*hi,Q(1,20))
        self.assertEqual(interval.alpha_relation(2*lo,2*hi),'unresolved_enclosure')
        for q in [Q(1,3),Q(1,10**100),Q(1,20),2*hi]:self.assertGreaterEqual(Q(interval.upward_decimal(q)),q)
        self.assertEqual(interval.alpha_relation(Q(0),Q(1,20)),'upper_bound_at_or_below_reference')

