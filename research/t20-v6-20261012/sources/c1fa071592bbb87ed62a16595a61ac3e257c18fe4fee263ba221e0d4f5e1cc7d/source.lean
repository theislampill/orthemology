import PythonExprSafety
import CodecStmt

/-! Well-formed variadic source syntax for prcodec.py:161–183. The mutual list
is a finite-list representation of a Seq tuple's children, not binary lowering.
The P1 source/frontend/primitive/host assumptions remain explicit.
-/
namespace P02.PythonRunner
open P02.PythonExpr

mutual
inductive Command where
  | set : ℕ → PyExpr → Command
  | seq : Commands → Command
  | loop : ℕ → PyExpr → Command → Command
  | branch : PyExpr → Command → Command → Command
inductive Commands where
  | nil : Commands
  | cons : Command → Commands → Commands
end

mutual
def lowerCommand : Command → P02A2.ObserverCore.Stmt
  | .set r e => .set r (lower e)
  | .seq ss => P02.Codec.sequenceList (lowerCommands ss)
  | .loop r e s => .loop r (lower e) (lowerCommand s)
  | .branch e s t => .branch (lower e) (lowerCommand s) (lowerCommand t)
def lowerCommands : Commands → List P02A2.ObserverCore.Stmt
  | .nil => []
  | .cons s ss => lowerCommand s :: lowerCommands ss
end

def commandList : Commands → List Command
  | .nil => []
  | .cons s ss => s :: commandList ss

inductive Task where
  | stmt : Command → Task
  | repeat : ℕ → ℕ → ℕ → Command → Task

/-- Head-top order is the reverse of Python's list-end representation. -/
def schedule (ss : Commands) (tail : List Task) : List Task :=
  (commandList ss).map Task.stmt ++ tail

/-- Pure ideal summary, not a practical preflight resource estimator. -/
structure Summary where
  store : Dictionary
  events : List (ℕ × ℕ)
  pops : ℕ
  ticks : ℕ
  bits : ℕ

def unchanged (d : Dictionary) : Summary := ⟨d,[],0,0,0⟩

def follow (a : Summary) (f : Dictionary → Summary) : Summary :=
  let b := f a.store
  ⟨b.store,a.events++b.events,a.pops+b.pops,a.ticks+b.ticks,max a.bits b.bits⟩

/-- Charge one outer task pop, plus its entire expression cost when applicable. -/
def charge (ticks bits : ℕ) (a : Summary) : Summary :=
  {a with pops := a.pops+1, ticks := ticks+a.ticks, bits := max bits a.bits}

/-- n is the captured remaining count. The terminal repeat task still ticks. -/
def repeatSummary (body : Dictionary → Summary) (r : ℕ) : ℕ → ℕ → Dictionary → Summary
  | _, 0, d => ⟨d,[],1,1,0⟩
  | k, n+1, d => charge 1 0
      (follow (body (dictionaryWrite d r k)) (repeatSummary body r (k+1) n))

mutual
def commandSummary (trace : Bool) : Command → Dictionary → Summary
  | .set r e, d =>
      let v := value e (dictionaryRead d)
      ⟨dictionaryWrite d r v, if trace then [(r,v)] else [], 1, 1+cost e, neededBits d e⟩
  | .seq ss, d => charge 1 0 (commandsSummary trace ss d)
  | .loop r e s, d => charge (1+cost e) (neededBits d e)
      (repeatSummary (fun d => commandSummary trace s d) r 0 (value e (dictionaryRead d)) d)
  | .branch e s t, d => charge (1+cost e) (neededBits d e)
      (if value e (dictionaryRead d) = 0 then commandSummary trace t d else commandSummary trace s d)
def commandsSummary (trace : Bool) : Commands → Dictionary → Summary
  | .nil, d => unchanged d
  | .cons s ss, d => follow (commandSummary trace s d) (commandsSummary trace ss)
end

def taskSummary (trace : Bool) : Task → Dictionary → Summary
  | .stmt s, d => commandSummary trace s d
  | .repeat r count k s, d => repeatSummary (commandSummary trace s) r k (count-k) d

def tasksSummary (trace : Bool) : List Task → Dictionary → Summary
  | [], d => unchanged d
  | t::ts, d => follow (taskSummary trace t d) (tasksSummary trace ts)

@[simp] theorem follow_unchanged (a : Summary) : follow a unchanged = a := by
  cases a
  simp [follow, unchanged]

@[simp] theorem unchanged_follow (d : Dictionary) (f : Dictionary → Summary) :
    follow (unchanged d) f = f d := by
  simp [follow, unchanged]

/-- Associativity retains chronological events and additive ticks/pops; widths
compose by maximum. No source storage bound on all dictionary entries occurs. -/
theorem follow_assoc (a : Summary) (f g : Dictionary → Summary) :
    follow (follow a f) g = follow a (fun d => follow (f d) g) := by
  simp [follow, List.append_assoc, Nat.add_assoc, Nat.max_assoc]

theorem follow_charge (ticks bits : ℕ) (a : Summary) (f : Dictionary → Summary) :
    follow (charge ticks bits a) f = charge ticks bits (follow a f) := by
  simp [follow, charge, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm, Nat.max_assoc]

theorem tasksSummary_append (trace : Bool) (as bs : List Task) (d : Dictionary) :
    tasksSummary trace (as++bs) d = follow (tasksSummary trace as d) (tasksSummary trace bs) := by
  induction as generalizing d with
  | nil => simp [tasksSummary]
  | cons a as ih => simp [tasksSummary, ih, follow_assoc]

theorem scheduled_summary (trace : Bool) (ss : Commands) (tail : List Task) (d : Dictionary) :
    tasksSummary trace (schedule ss tail) d = follow (commandsSummary trace ss d) (tasksSummary trace tail) := by
  cases ss with
  | nil => simp [schedule, commandList, commandsSummary]
  | cons s ss =>
      simpa [schedule, commandList, tasksSummary, taskSummary, commandsSummary, follow_assoc] using
        congrArg (follow (commandSummary trace s d))
          (funext (fun d => scheduled_summary trace ss tail d))
termination_by sizeOf ss


end P02.PythonRunner
