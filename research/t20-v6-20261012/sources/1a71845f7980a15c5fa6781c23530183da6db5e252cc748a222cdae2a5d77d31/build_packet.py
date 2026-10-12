#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,re,os,time,sys
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def save(name,obj):(BASE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

sources=[
 ('OWNER','tranche20/owner-instructions/Pasted text(20261007-075932).txt','Complete owner computational objective',None),
 ('SARG','tranche20/cooperation-reassessment/SOURCE_ARGUMENT.md','Complete current reconstruction; §§3–7 especially',None),
 ('PMAP','tranche20/cooperation-reassessment/PREMISE_MAP.json','Complete premise map and countermodel_test_scope',None),
 ('MAUD','tranche20/cooperation-reassessment/MODEL_AUDIT.md','Complete current relevance audit, including reconciled upstream/downstream scope',None),
 ('ROOT','tranche20/cooperation-reassessment/ROOT_REASSESSMENT.md','Complete current judgement; preserved not revised',None),
 ('IWAR','tranche20/cooperation-reassessment/independent-warrant-review/REVIEW.md','Complete review; §§3–6 especially',None),
 ('T17','tranche20/recovered-inputs/text/Orthemology_Seventeenth_Research_Final_v1_20261005.txt','Direct P54–83 and P99–112; relevant P65–68, P74–81, P108–112',None),
 ('MF','tranche20/targeted-final-loci/causal-action/web/mf_extended.txt','Complete unique Arabic web L906–928; relevant L908, L912–913, L917–921','https://islamweb.net/ar/library/content/22/2032/'),
 ('M2A','tranche20/cooperation-reassessment/islamweb-vol2.txt','Arabic lines8–24,38–41; pp2:168–172 and 178–180','https://www.islamweb.net/ar/library/content/108/156/'),
 ('M2B','tranche20/cooperation-reassessment/islamweb-item157.txt','Complete four lines, pp2:180–182','https://www.islamweb.net/ar/library/content/108/157/'),
 ('M2C','tranche20/cooperation-reassessment/islamweb-item158.txt','Arabic lines1–5, pp2:182–184; used perfection continuation1–2','https://www.islamweb.net/ar/library/content/108/158/'),
 ('SFGEN','tranche20/targeted-final-loci/causal-action/receipts/saf2-L0574-L0636.txt','Direct retained Arabic L0623–0627 genus/token control',None),
 ('SFACT','tranche20/targeted-final-loci/causal-action/web/salim145.txt','Direct Arabic labelled web L2254–2257 (2:142) and L2272–2273 (2:145)','https://islamhouse.com/read/ar/الصفدية-272837'),
 ('SID','tranche20/targeted-final-loci/causal-action/SOURCE_IDENTITY.json','Complete source and edition identity controls',None),
 ('SPAGE','tranche20/targeted-final-loci/causal-action/PAGE_CORRESPONDENCE.json','Complete correspondence map; preserved electronic/scan distinctions',None),
 ('SEDGE','tranche20/targeted-final-loci/causal-action/PREMISE_EDGES.json','Complete existing source-bridge map',None),
]
bindings=[dict(id=i,path=p,sha256=sha(ROOT/p),bytes=(ROOT/p).stat().st_size,read_scope=s,url=u,status='READ_ONLY_RETAINED_INPUT') for i,p,s,u in sources]
save('SOURCE_BINDINGS.json',{'captured_utc':now(),'sources':bindings,'reading_method':'Direct retained local text and maps; no fresh network or scan claim','action_typing_preserved':{'particular_act':'Salim2:145','global_inactivity_argument':'Salim2:142'}})

rows=[]
def row(i,clause,loc,role,add,sat,con,res):
 rows.append(dict(id=i,clause=clause,source=loc,role_in_test=role,additive=add,saturation=sat,concordant_profiles=con,residual=res))
row('U_EXIST','Same actual necessary essentially unreceived bearers','T17 P54–61; SARG StageA','RETAINED_UPSTREAM','Rigid root identifiers and no incoming efficient origin in every represented context','Same','Same','Finite constant-domain and root-graph interpretation does not certify full metaphysical intrinsic necessity; actual-world application remains unproved')
row('P1','Action uses possessed power','PMAP P1; T17 P63','RETAINED_UPSTREAM','Command membership and executable issue checked','All four binary commands executable','Same intrinsic command set under restriction','No power=True qualification used')
row('P2a','Intrinsic unreceived capacity and will','PMAP P2a; M2A lines8–24','RETAINED_UPSTREAM','Typed root/constitutive/efficient graph; no peer-to-intrinsic path','Same','No efficient edge between matching private reason evaluators','Shared abstract reason content is not itself an efficient donor; its ultimate explanatory adequacy remains unestablished')
row('P3','No efficient-priority capacity/will circle','PMAP P3; M2A lines19–24','RETAINED_UPSTREAM','Finite DAG checked; mutation cycle rejected','Same','Concord does not add an efficient edge','Finite DAG does not validate every real causal/metaphysical interpretation')
row('P4_CND','Same numerical contribution, same original productive respect, nonduplication','PMAP P4; MAUD §1; MF L906,L912–913','RETAINED_UPSTREAM_AT_FIXED_RESPECT','Primitive differentiated contribution relation permits duplicates then checks CND','Emission CND true; sufficient-as-whole gives whole-e CND false; exhaustive-input-as-whole gives vacuous whole-e CND','Same ambiguity','No silent transport from emission tokens to entire same numerical effect; faithful requisite/provenance interpretation missing')
row('P5_EQUAL','Equal relevant eligible capacities persist in coexistence','PMAP P5; T17 P65–68','RETAINED_UPSTREAM','Identical explicit command interpreters; standing witnesses with idle peer; all-Nat constructive extension','All four executable vector commands for each agent','All commands remain available; actual profile admissibility restricted separately','Operational availability is represented; robust control over arbitrary rival commands is stronger and not obtained for every target')
row('ELIGIBLE_PURE','Genuinely feasible added ability without need, contradiction, borrowing or impairment','T17 P65–67','RETAINED_UPSTREAM_PHILOSOPHICAL_GRANT','Fixed target constructible for either; generic same-bearer sum command concentrates all additive vectors','No target removed by Eligible=false; saturation has target-control constraints','Wisdom compatibility distinct from executable eligibility','Algebraic construction is not universal source-warranted metaphysical feasibility or all pure perfection')
row('P6_OUTCOME','Complete power plus complete determinate will entails exact specified outcome','PMAP P6; MF L912; T17 P108–112','RETAINED_UPSTREAM_WITH_CONTENT_FIXED','Actual whole intended target occurs; independent deletion-robust determinant fails; bare P6 not refuted merely by diagnostic deletion','Actual target11 robustly occurs at unchanged command against all Boolean rivals','Each diagonal target occurs; full P6 context domain needs justified admissibility','Do not insert solo-original-provision or arbitrary rectangular compossibility into P6; missing context/completion interpretation is explicit')
row('FIXED_STATE','Keep surviving agent actual state, will, command and target fixed','MF L908,L912; PMAP fixed_background','RETAINED_COMPARISON_REQUIREMENT','Same object command11 under peer suppression; fails q22; command22 repair rejected','Same command11 under suppression; output vector unchanged','Actual same policy/command fixed in target comparison','Surgical intervention is not automatically metaphysically admissible world; rigid e identity is stipulated, not source-defended')
row('GENUINE_CONTRIBUTION','Differentiated original work on same target','MAUD §1; MF L908–909','RETAINED_UPSTREAM_REQUIRING_FAITHFUL_INTERPRETATION','Both positive inputs indispensable to both output coordinates','Different actual emission paths; neither indispensable to saturated output','Same as chosen production law','Causal relevance somewhere is weaker than indispensable actual contribution; source L908 contribution-sensitivity must not be silently dropped')
row('B5_U','Concentration of jointly productive powers in one bearer','MF L917–919; IWAR §5','BRIDGE_STEP_TESTED','Finite set union insufficient in general: joint44 outside finite bound. New unbounded sum-command concentration theorem supplies witness','Binary saturation output executable by each','No third actual source added','Constructive concentration is family-relative; abstract union is not itself source U')
row('B5_R','Each same rigid bearer eligible for concentrated power','MF L919; T17 P65–67','DISPUTED_DOWNSTREAM_NOT_ASSUMED','Either same g executes a+b in unbounded interpreter; not transferred from a new individual','Either executes fixed binary target','Same','Source-level no-cost/pure applicability of this model still needs philosophical warrant')
row('B5_F','Missing capacity is genuine constitutive perfection','MF L920–921; M2B line4; M2C lines1–2','DISPUTED_DOWNSTREAM_NOT_ASSUMED','No missing standing operation for fixed q or unbounded additive union. Frozen partial exercise insufficient','No missing binary command, but whole-effect authorship/control incomplete','Same','Not possessing exclusive actual provenance is not proved to be missing constitutive capacity; classification remains open')
row('B5_I_N','Cannot self-complete missing intrinsic perfection, hence external receipt incompatible with self-necessity','MF L920–921; IWAR §5.3','DISPUTED_TRANSFER_WITH_INTRINSIC_RECEIPT_EXCLUSION_RETAINED','No intrinsic completion event instantiated by split exercise','Same','Same','The accepted exclusion of received constitutive perfection does not manufacture its receipt antecedent')
row('B6','Outcome determination to entire original provision to exclusivity','MF L912–913; IWAR §4','DISPUTED_DOWNSTREAM_NOT_ASSUMED','No counterexample under deletion-robust determinant reading; no conclusion about bare P6 alone','Checked outcome/provenance separation only at emission signature; whole-target CND and identity unresolved','Same with admissibility burden','No full antecedent-preserving B6 countermodel; no universal B6 derivation')
row('M1_P2b','Joint-effect completion becomes received intrinsic productive perfection','M2A line41; MF L920–921','DISPUTED_DOWNSTREAM_NOT_ASSUMED','External result depends on two unchanged acts; intrinsic graph unchanged','Redundant output paths undermine premise of needed completion','Same','No faithful full-profile model or derived intrinsic-receipt bridge; actual exercise norm not settled')
row('B2','Necessary concord entails reciprocal efficient conditioning or a third cause','PMAP B2; T17 P74–81','DISPUTED_DOWNSTREAM_NOT_ASSUMED','Not a demonstrated necessary-concord theory','Equal intrinsic scores give matching choices without efficient cross-edge','Nonrectangular diagonal is explicitly stipulated','Algorithmic absence of cycle does not establish source-worthy necessary wisdom or matching reason explanation')
row('P7','Contingent coalescence has efficient explanation without independent third original','PMAP P7; SARG StageE','RETAINED_BUT_REPRESENTATION_INCOMPLETE','Two emitted inputs computed through addition','OR is a semantic operator; physical apparatus reading could require unrepresented original provision','Same','No third agent symbol is not a proof of complete original-resource accounting; law-versus-mechanism interpretation unresolved')
row('O1','Relevant actual created field genuinely connected','PMAP O1; T17 P74','RETAINED_APPLICATION_PREMISE_NOT_COSMOLOGICALLY_TESTED','Both agents feed both coordinates of a bounded unified output','Shared output circuit','Same','No empirical entire-actual-field applicability result')
row('ACTION_TYPES','Standing capacity, genus, act token and created effect stay distinct','SFGEN L0623–0627; SFACT2:142,2:145','RETAINED_TYPING_CONTROL','Typed graph; no temporal empty-extension claim','Same','Same','No new divine-action/cessation theorem')
save('PREMISE_MATRIX.json',{'schema':'cooperation-preservation-v1','conclusion':'NO_FULL_COUNTERMODEL; FAMILY_SCOPED_OBSTRUCTION_AND_WEAK_SEPARATION','rows':rows})

lean=ROOT/'tranche20/hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux/bin/lean'
receipts=[]
def run(name,cmd,env=None,expected=0):
 start=now(); t=time.monotonic()
 p=subprocess.run(cmd,cwd=BASE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 elapsed=time.monotonic()-t; end=now()
 path=BASE/'receipts'/name;path.write_text(p.stdout)
 receipts.append(dict(name=name,command=[str(x) for x in cmd],cwd=str(BASE),started_utc=start,ended_utc=end,elapsed_seconds=elapsed,exit_code=p.returncode,expected_exit_code=expected,log=str(path.relative_to(BASE)),log_sha256=sha(path),classification='VERIFICATION'))
 if p.returncode!=expected: print(p.stdout);raise SystemExit(f'{name}: unexpected exit {p.returncode}')
 return p.stdout
run('lean-version-final.log',[str(lean),'--version'])
run('python-search-final.log',[sys.executable,str(BASE/'src/search.py')])
run('python-tests-final.log',[sys.executable,str(BASE/'src/test_search.py')])
(BASE/'build').mkdir(exist_ok=True)
run('lean-kernel-final.log',[str(lean),'-o',str(BASE/'build/FixedTarget.olean'),str(BASE/'src/FixedTarget.lean')])
names=re.findall(r'^theorem\s+(\w+)',(BASE/'src/FixedTarget.lean').read_text(),re.M)
readback='import FixedTarget\n'+''.join(f'#check FixedTarget.{n}\n#print axioms FixedTarget.{n}\n' for n in names)
(BASE/'src/Readback.lean').write_text(readback)
env=os.environ.copy(); env['LEAN_PATH']=str(BASE/'build')
axioms=run('lean-readback-final.log',[str(lean),str(BASE/'src/Readback.lean')],env)
assert 'sorryAx' not in axioms
assert not re.search(r'\b(sorry|axiom|admit)\b', re.sub(r'/\-.*?\-/|--[^\n]*','',(BASE/'src/FixedTarget.lean').read_text(),flags=re.S))
assert all(sha(ROOT/e['path'])==e['sha256'] for e in bindings)
save('DECLARATIONS.json',{'theorems':names,'count':len(names),'axiom_readback':'receipts/lean-readback-final.log','custom_metaphysical_axioms':[],'sorry_or_admit':False})
save('VERIFICATION.json',{'completed_utc':now(),'toolchain':{'path':str(lean),'sha256':sha(lean),'version':'4.19.0'},'commands':receipts,'input_hashes_unchanged':True,'scope':'Fresh new packet only; no historical scientific packages, repository or delivered archive replayed'})
print(json.dumps({'status':'PASS','theorems':len(names),'commands':len(receipts),'completed_utc':now()},indent=2))
