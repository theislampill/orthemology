"""Finite source-motivated rival histories; no empirical authentication oracle.

Observation functions project independently inspectable actions/records, not target
truth labels. Their fidelity and availability are application premises. Conventional
validity is evaluated against a supplied founding convention, never identified with
ethical legitimacy, numerical identity, revelation, or actual-world authenticity.
"""
from dataclasses import dataclass, asdict
from itertools import combinations, product
import json

@dataclass
class Case:
    name: str
    observations: dict
    target: dict
    events: tuple = ()

TOKEN_KINDS=('attest','repair','seal','theft','found','coerced','arrival_only','conditional_then_theft')
INVENTORY='Upon my voluntary handover of this ring, E may report inventory for me until Tuesday.'
ARRIVAL='Take this ring only to show the household that I sent you; no inventory report is commissioned.'

def interpret_token(events):
    """Small action interpreter: ownership, actual sending and commission differ."""
    holder='P'; instructions={}; sent=False; commission=False
    for e in events:
        if e[0]=='says': instructions[e[1]]=e[2]
        elif e[0]=='give':
            _,actor,recipient=e
            if holder != actor: raise ValueError('giver does not hold token')
            holder=recipient
            if actor=='P' and recipient=='E':
                sent=True
                commission=instructions.get('P')==INVENTORY
        elif e[0]=='drop':
            if holder!=e[1]: raise ValueError('dropper does not hold token')
            holder='ground'
        elif e[0]=='pick_up':
            if holder!='ground': raise ValueError('token not on ground')
            holder=e[1]
        elif e[0] in ('take','force_take'):
            if holder!=e[1]: raise ValueError('wrong victim')
            holder=e[2]
    return holder,sent,commission

def token_case(kind,fact=True,sincere=True):
    if kind not in TOKEN_KINDS: raise ValueError(kind)
    instruction={
        'attest':INVENTORY,'repair':'Take this ring to repair its broken setting.',
        'seal':'Take this ring to seal the equipment crate.', 'arrival_only':ARRIVAL,
        'conditional_then_theft':INVENTORY
    }.get(kind,'No instruction to E.')
    events=[('says','P',instruction)]
    if kind in ['attest','repair','seal','arrival_only']:
        events += [('give','P','E')]
    elif kind=='found': events += [('drop','P'),('pick_up','E')]
    elif kind=='coerced': events += [('force_take','P','E')]
    else: events += [('take','P','E')]
    # The carrier's displayed packet has identical content in every rival world.
    events += [('says','E','P sent me. Inventory is one.')]
    holder,sent,commission=interpret_token(events)
    inventory=['unit'] if fact else []
    report_true=(len(inventory)==1)
    obs={
        'received':('P-ring','E','P sent me. Inventory is one.'),
        'transfer':tuple(e for e in events if e[0] in ['give','take','force_take','drop','pick_up']),
        'prior_instruction':tuple(e for e in events if e[0]=='says' and e[1]=='P'),
        'employment_record':('E works in P laboratory',),
    }
    return Case(f'token:{kind}:fact={fact}:sincere={sincere}',obs,
                {'holder':holder,'sent':sent,'commission':commission,'report_true':report_true,
                 'sincere':sincere,'scoped_veracity':not commission or report_true},tuple(events))

CHALLENGE_KINDS=('envoy','maintenance','fixed_replay','adaptive_counterfeit','stolen_access','aborted_envoy','diverted_to_other')

def challenge_case(kind,nonce):
    if kind not in CHALLENGE_KINDS or nonce not in range(4): raise ValueError((kind,nonce))
    events=[('recipient_challenge',nonce)]
    instruction='Report inventory for me using this response.'
    if kind in ['envoy','diverted_to_other']:
        recipient='E' if kind=='envoy' else 'X'
        events += [('P_direct_instruction',instruction),
                   ('P_delivers_access','E'),('E_requests',nonce),('P_terminal_emits',nonce),
                   ('P_dispatches_response',recipient)]
        if recipient=='X':events += [('E_appropriates_response','X')]
    elif kind=='aborted_envoy':
        events += [('P_direct_instruction',instruction),('P_withholds_access','E'),
                   ('E_fabricates',nonce),('E_self_supplies','E')]
    elif kind=='maintenance':
        events += [('P_direct_instruction','Test and repair the terminal; do not report inventory for me.'),
                   ('P_delivers_access','E'),('E_requests',nonce),('P_terminal_emits',nonce),
                   ('P_dispatches_response','E')]
    elif kind=='stolen_access':
        events += [('E_steals_access','P'),('E_requests',nonce),('P_terminal_emits',nonce),
                   ('E_self_supplies','E')]
    elif kind=='fixed_replay':events += [('E_replays_old',0),('E_self_supplies','E')]
    else:events += [('E_observes_challenge',nonce),('E_fabricates',nonce),('E_self_supplies','E')]
    source_action=tuple(e for e in events if e[0] in ['P_terminal_emits','E_replays_old','E_fabricates'])
    output=source_action[-1][1]
    origin=any(e[0]=='P_terminal_emits' for e in events)
    mission=(('P_direct_instruction',instruction) in events and origin
             and ('P_dispatches_response','E') in events)
    # Mission here means this response was purposefully supplied to E for this
    # reporting mission. Prior commissioning is a distinguishable earlier fact.
    obs={'received':('apparent-source-mark','E claims inventory mission'),
         'challenge':(nonce,output), 'source_action':source_action,
         'original_instruction':tuple(e for e in events if e[0]=='P_direct_instruction'),
         'access_history':tuple(e for e in events if e[0] in ['P_delivers_access','E_steals_access','P_withholds_access']),
         'dispatch_record':tuple(e for e in events if e[0] in ['P_dispatches_response','E_self_supplies'])}
    return Case(f'challenge:{kind}:n={nonce}',obs,
                {'origin':origin,'mission':mission,'prior_commission':('P_direct_instruction',instruction) in events,
                 'challenge_matches':nonce==output},tuple(events))

@dataclass(frozen=True)
class Constitution:
    amendment_allowed: bool=True
    members: tuple=('A','B','C')
    quorum: int=2
    publication_delay: int=1


def run_constitution(c,events):
    members=set(c.members); regime='predecessor_transfer'; holder='P'
    proposal=None; votes=set(); valid_amendment=False; publication=None; effective=None
    decisions=[]
    for time,kind,*args in sorted(events,key=lambda e:e[0]):
        if effective is not None and time>=effective: regime='board_appointment'
        if kind=='founder_removes_member': members.discard(args[0])
        elif kind=='propose': proposal=args[0]; votes=set()
        elif kind=='vote':
            voter,motion=args
            if motion==proposal and voter in members: votes.add(voter)
        elif kind=='publish':
            motion=args[0]
            if (c.amendment_allowed and proposal==motion=='allow_fresh_appointment'
                    and len(votes)>=c.quorum):
                valid_amendment=True; publication=time; effective=time+c.publication_delay
        elif kind=='appoint':
            appointing,target=args
            # This case's appointment uses the board, with A and C current and independent
            # of the earlier constitutional vote. B's earlier vote may have been stale.
            permitted=(regime=='board_appointment' and len(set(appointing)&members)>=c.quorum)
            if permitted: holder=target
            decisions.append((time,'appoint',target,permitted,regime))
    return {'holder':holder,'amendment':valid_amendment,'publication':publication,
            'effective':effective,'decisions':tuple(decisions),'regime':regime}


def service_trace(initial=0):
    bit=initial; out=[]
    for command in ('read','toggle','read','intruder-toggle','read'):
        if command=='toggle':bit=1-bit;out.append(('ok',bit))
        elif command=='intruder-toggle':out.append(('denied',bit))
        else:out.append(('read',bit))
    return tuple(out)


def institution_case(mutable=True,remove_voter=False,publish=True,appoint_time=4,
                     descent=False,operational=True):
    c=Constitution(amendment_allowed=mutable)
    events=[]
    if remove_voter: events.append((0,'founder_removes_member','B'))
    events += [(1,'propose','allow_fresh_appointment'),
               (2,'vote','A','allow_fresh_appointment'),(2,'vote','B','allow_fresh_appointment')]
    if publish: events += [(2,'publish','allow_fresh_appointment')]
    events += [(appoint_time,'appoint',('A','C'),'N')]
    execution=run_constitution(c,events)
    # Actual technical construction is separately simulated. It neither sends a vote
    # nor confers an office. P need not have ordered a transfer of that office.
    parent={'bit':0}; new={'bit':parent['bit'] if descent else 0}
    technical=('copied_from_P',parent['bit']) if descent else ('independent_installation',0)
    outputs=service_trace(new['bit']) if operational else ('unavailable',)
    obs={'service':outputs,
         'vote_packet':tuple(e for e in events if e[1]=='vote'),
         'founding_text':('amendments_allowed',c.amendment_allowed,'quorum',c.quorum,'delay',c.publication_delay),
         'membership_history':tuple(e for e in events if e[1]=='founder_removes_member'),
         'publication_record':tuple(e for e in events if e[1]=='publish'),
         'appointment_record':tuple(e for e in events if e[1]=='appoint'),
         'technical_history':technical}
    target={**execution,'descent':descent,'operational':operational}
    name=f'institution:m={mutable}:remove={remove_voter}:pub={publish}:at={appoint_time}:desc={descent}:up={operational}'
    return Case(name,obs,target,tuple(events))

# Discourse syntax is compositional but deliberately tiny. Context resolving the
# embedded I/here/now belongs to the embedded speaker, not the present carrier.
@dataclass(frozen=True)
class Context:
    speaker: str
    time: int
    place: str='lab'

def resolve_atom(context): return ('at',context.speaker,context.place,context.time)
def translation_a_to_b(words):
    if words!=('I','am','here','now'):raise ValueError(words)
    return ('HERE','NOW','SELF','located')

def proposition_b(words,context):
    if words!=('HERE','NOW','SELF','located'):raise ValueError(words)
    return resolve_atom(context)

def discourse_case(kind,speaker,time):
    if kind not in ['assert','quote','report'] or speaker not in ['P','Q'] or time not in [0,1]:
        raise ValueError((kind,speaker,time))
    context=Context(speaker,time); atom=resolve_atom(context)
    leaf=('I','am','here','now')
    if kind=='assert':
        tree=('assert',speaker,('atom',atom)); frame='My own factual statement follows:'
    elif kind=='quote':
        tree=('mention',speaker,('atom',atom)); frame='The following words are an example, which I do not assert:'
    else:
        # Q/P really said the sentence; a narrator reports that act accurately.
        # This assertion concerns an occurrence, not its embedded location claim.
        tree=('assert','Narrator',('said',speaker,('atom',atom)))
        frame='I report that the embedded speaker uttered these words; I do not endorse them:'
    uttered={(speaker,atom)}
    true_atoms={('at','P','lab',0)}
    if tree[0]=='mention': outer_true=None
    elif tree[2][0]=='said':outer_true=(tree[2][1],tree[2][2][1]) in uttered
    else:outer_true=tree[2][1] in true_atoms
    # Export omits discourse framing and context. Every world emits identical bytes.
    translated=translation_a_to_b(leaf)
    obs={'received':translated,
         'full_frame':frame,
         'context_record':(context.speaker,context.time,context.place),
         'carrier_record':('Archivist','quotes retained fragment',10)}
    target={'asserts_p0':tree==('assert','P',('atom',('at','P','lab',0))),
            'embedded_true':atom in true_atoms,'outer_true':outer_true,
            'source_act':tree,'translation_preserves_embedded':proposition_b(translated,context)==atom}
    return Case(f'discourse:{kind}:{speaker}:{time}',obs,target,(tree,))


def freeze(x):
    if isinstance(x,dict):return tuple(sorted((k,freeze(v)) for k,v in x.items()))
    if isinstance(x,(list,tuple)):return tuple(freeze(v) for v in x)
    return x


def sufficient(worlds,target,observations):
    seen={}
    for w in worlds:
        key=tuple(freeze(w.observations[x]) for x in observations)
        val=freeze(w.target[target])
        if key in seen and seen[key]!=val:return False
        seen[key]=val
    return True


def minimal_discriminators(worlds,target):
    if not worlds:raise ValueError('no world set')
    names=sorted(worlds[0].observations)
    if any(set(w.observations)!=set(names) for w in worlds):raise ValueError('different menus')
    minimal=[]
    for size in range(len(names)+1):
        for subset in combinations(names,size):
            if any(set(old)<=set(subset) for old in minimal):continue
            if sufficient(worlds,target,subset):minimal.append(subset)
    return minimal


def survivors(worlds,actual,observations):
    return [w.name for w in worlds if all(w.observations[x]==actual.observations[x] for x in observations)]


def run_all():
    tokens=[token_case(k,fact,sincere) for k,fact,sincere in product(TOKEN_KINDS,[False,True],[False,True])]
    challenges=[challenge_case(k,n) for k,n in product(CHALLENGE_KINDS,range(4))]
    institutions=[institution_case(*args) for args in product([False,True],[False,True],[False,True],[2,4],[False,True],[False,True])]
    discourse=[discourse_case(k,s,t) for k,s,t in product(['assert','quote','report'],['P','Q'],[0,1])]
    a=challenge_case('envoy',2)
    return {
      'scope':'finite stipulated research models, Python execution only; no revelation or real authority authentication',
      'counts':{'tokens':len(tokens),'challenges':len(challenges),'institutions':len(institutions),'discourse':len(discourse)},
      'minimal_discriminators':{
        'token_commission':minimal_discriminators(tokens,'commission'),
        'token_report_truth':minimal_discriminators(tokens,'report_true'),
        'token_private_sincerity':minimal_discriminators(tokens,'sincere'),
        'challenge_origin':minimal_discriminators(challenges,'origin'),
        'challenge_mission':minimal_discriminators(challenges,'mission'),
        'institution_holder':minimal_discriminators(institutions,'holder'),
        'discourse_source_assertion_p0':minimal_discriminators(discourse,'asserts_p0')},
      'challenge_survivors_at_nonce_2':{
        'received_only':survivors(challenges,a,['received']),
        'fresh_challenge':survivors(challenges,a,['received','challenge']),
        'plus_source_action':survivors(challenges,a,['received','challenge','source_action']),
        'plus_original_instruction':survivors(challenges,a,['received','challenge','source_action','original_instruction']),
        'plus_actual_dispatch':survivors(challenges,a,['received','challenge','source_action','original_instruction','dispatch_record'])},
      'cases':[asdict(w) for w in tokens+challenges+institutions+discourse]}

if __name__=='__main__':print(json.dumps(run_all(),indent=2))
