"""History-family enlargement following independent reviewer counterexamples.

The original finite family stays intact. Here raw action order and mission scope are
varied, and positive discrimination uses independently witnessed history or source
utterances. A record's own label never authenticates it.
"""
from itertools import permutations
from dataclasses import asdict
import json
import rivals as r


def old_projection(events,c=None):
    c=c or r.Constitution()
    return {'service':r.service_trace(),
            'vote_packet':tuple(e for e in events if e[1]=='vote'),
            'founding_text':('amendments_allowed',c.amendment_allowed,'quorum',c.quorum,'delay',c.publication_delay),
            'membership_history':tuple(e for e in events if e[1]=='founder_removes_member'),
            'publication_record':tuple(e for e in events if e[1]=='publish'),
            'appointment_record':tuple(e for e in events if e[1]=='appoint'),
            'technical_history':('independent_installation',0)}


def observed_case(events,c=None):
    c=c or r.Constitution()
    chronological=tuple(sorted(events,key=lambda event:event[0]))
    # Index is position in a witnessed chronological record, not a self-authenticating ID.
    minutes=tuple(enumerate(chronological))
    return {'events':events,'old_observations':old_projection(events,c),
            'ordered_minutes':minutes,'holder':r.run_constitution(c,events)['holder']}


def institution_history_cases():
    base=list(r.institution_case().events)
    missing=[e for e in base if e[1]!='propose']
    reordered=([e for e in base if e[1]=='propose']+[e for e in base if e[1]=='publish']+
               [e for e in base if e[1]=='vote']+[e for e in base if e[1]=='appoint'])
    return {k:observed_case(v) for k,v in [('base',base),('missing_proposal',missing),('publication_before_votes',reordered)]}


def enumerate_event_orders():
    # Fully disclosed distinct test class: all five events at one timestamp and
    # zero publication delay, so order itself has normative consequences.
    c=r.Constitution(publication_delay=0)
    base=[(1,'propose','allow_fresh_appointment'),(1,'vote','A','allow_fresh_appointment'),
          (1,'vote','B','allow_fresh_appointment'),(1,'publish','allow_fresh_appointment'),
          (1,'appoint',('A','C'),'N')]
    cases=[observed_case(list(p),c) for p in permutations(base)]
    old={};full={};collisions=[]
    for i,w in enumerate(cases):
        k=r.freeze(w['old_observations']);v=w['holder']
        if k in old and old[k][1]!=v:collisions.append((old[k][0],i))
        old.setdefault(k,(i,v))
        fk=(r.freeze(asdict(c)),r.freeze(w['ordered_minutes']))
        if fk in full:assert full[fk]==v
        full[fk]=v
    first=collisions[0] if collisions else None
    return {'permutations_checked':len(cases),'holder_N':sum(w['holder']=='N' for w in cases),
            'holder_P':sum(w['holder']=='P' for w in cases),
            'old_menu_collision':bool(collisions),'ordered_minutes_sufficient':True,
            'first_collision':[cases[i] for i in first] if first else [],
            'assumptions':'Same-time action order observed; zero publication delay supplied by this separate constitution.'}


def run_scoped_office(events):
    """Separate declared charter permits two-vote changes to mode or remit.

    No operation here purports to amend a sender's independently given words.
    """
    members={'A','B','C'};proposals={};votes={};pending=[]
    state={'mode':'predecessor_transfer','remit':'inventory','holder':'P'}
    audit=[]
    for time,kind,*args in sorted(events,key=lambda e:e[0]):
        ready=[x for x in pending if x[0]<=time]
        for _,field,value in ready:state[field]=value
        pending=[x for x in pending if x[0]>time]
        if kind=='propose':
            motion,field,value=args
            if field not in ['mode','remit']:raise ValueError('unamendable field')
            proposals[motion]=(field,value);votes[motion]=set()
        elif kind=='vote':
            voter,motion=args
            if voter in members and motion in proposals:votes[motion].add(voter)
        elif kind=='publish':
            motion=args[0]
            if motion in proposals and len(votes[motion])>=2:
                field,value=proposals[motion];pending.append((time+1,field,value))
                audit.append((time,'published',motion,field,value))
        elif kind=='appoint':
            voters,target=args
            if state['mode']=='board_appointment' and len(set(voters)&members)>=2:state['holder']=target
        elif kind=='report':
            bearer,domain,text=args
            audit.append((time,'report',bearer,domain,text,state['holder']==bearer and state['remit']==domain))
    return state,audit

FIXED='I adopt this office holder\'s inventory reports only. A later office amendment cannot enlarge this statement.'
DYNAMIC='I adopt reports within this office\'s remit as changed through its authorized amendment procedure.'


def adoption_after_amendment(mode,hazard=False):
    if mode not in ['fixed','dynamic']:raise ValueError(mode)
    source_statement=FIXED if mode=='fixed' else DYNAMIC
    # The source statement is retained from a separate earlier acquisition at time 0.
    events=[(1,'propose','m1','mode','board_appointment'),(2,'vote','A','m1'),(2,'vote','B','m1'),
            (2,'publish','m1'),(4,'appoint',('A','C'),'N'),
            (5,'propose','m2','remit','safety'),(6,'vote','A','m2'),(6,'vote','B','m2'),
            (6,'publish','m2'),(8,'report','N','safety','No hazard is present.')]
    state,audit=run_scoped_office(events)
    time,_,bearer,domain,text,within_current_remit=audit[-1]
    # Parse the controlled explicit source utterance. This is not a general NL parser.
    adopted_domains={'inventory'} if source_statement==FIXED else {state['remit']}
    owned=(within_current_remit and domain in adopted_domains)
    room={'hazards':['fault'] if hazard else []};report_true=(len(room['hazards'])==0)
    return {'holder':state['holder'],'new_domain':state['remit'],
            'received_rule':'The authorized office reports for P.',
            'independent_source_statement':source_statement,'source_statement_time':0,
            'events':events,'audit':audit,'source_owned':owned,'report_true':report_true,
            'finite_scoped_veracity':not owned or report_true,
            'scope':'Ordinary finite adoption analogue; constitution cannot rewrite independently acquired source words.'}


def run_all():
    return {'institution_history_cases':institution_history_cases(),
            'event_order_enumeration':enumerate_event_orders(),
            'adoption_cases':[adoption_after_amendment(m,h) for m in ['fixed','dynamic'] for h in [False,True]]}

if __name__=='__main__':print(json.dumps(run_all(),indent=2))
