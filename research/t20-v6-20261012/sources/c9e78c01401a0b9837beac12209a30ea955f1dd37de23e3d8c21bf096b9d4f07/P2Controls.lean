import PythonRunnerAPI
open P02.PythonExpr P02.PythonRunner
namespace RunnerAuthorControls
def empty : Program := ⟨0,0,(.seq .nil)⟩
example : callFuel true 80 empty [] (some 1) none = .ok (some (.traced 0 1 [])) := by rfl
example : callFuel false 80 empty [] (some 1) none = .ok (some (.value 0)) := by rfl
def singleton : Program := ⟨0,2,(.seq (.cons (.set 2 (.constant 0)) .nil))⟩
example : callFuel true 80 singleton [] (some 3) none = .ok (some (.traced 0 3 [(2,0)])) := by rfl
example : callFuel false 80 singleton [] (some 3) none = .ok (some (.value 0)) := by rfl
def sequence_updates : Program := ⟨0,0,(.seq (.cons (.set 0 (.constant 4)) (.cons (.set 0 (.binary .add (.reg 0) (.constant 1))) .nil)))⟩
example : callFuel true 80 sequence_updates [] (some 8) none = .ok (some (.traced 5 8 [(0,4),(0,5)])) := by rfl
example : callFuel false 80 sequence_updates [] (some 8) none = .ok (some (.value 5)) := by rfl
def zero_loop : Program := ⟨0,0,(.loop 0 (.constant 0) (.seq .nil))⟩
example : callFuel true 80 zero_loop [] (some 3) none = .ok (some (.traced 0 3 [])) := by rfl
example : callFuel false 80 zero_loop [] (some 3) none = .ok (some (.value 0)) := by rfl
def three_empty_iterations : Program := ⟨0,0,(.loop 0 (.constant 3) (.seq .nil))⟩
example : callFuel true 80 three_empty_iterations [] (some 9) none = .ok (some (.traced 2 9 [])) := by rfl
example : callFuel false 80 three_empty_iterations [] (some 9) none = .ok (some (.value 2)) := by rfl
def body_overwrites_loop_register : Program := ⟨0,0,(.loop 0 (.constant 2) (.set 0 (.constant 99)))⟩
example : callFuel true 80 body_overwrites_loop_register [] (some 9) none = .ok (some (.traced 99 9 [(0,99),(0,99)])) := by rfl
example : callFuel false 80 body_overwrites_loop_register [] (some 9) none = .ok (some (.value 99)) := by rfl
def captured_bound : Program := ⟨1,1,(.seq (.cons (.set 1 (.constant 0)) (.cons (.loop 2 (.reg 0) (.seq (.cons (.set 0 (.constant 0)) (.cons (.set 1 (.binary .add (.reg 1) (.constant 1))) .nil)))) .nil)))⟩
example : callFuel true 80 captured_bound [3] (some 33) none = .ok (some (.traced 3 33 [(1,0),(0,0),(1,1),(0,0),(1,2),(0,0),(1,3)])) := by rfl
example : callFuel false 80 captured_bound [3] (some 33) none = .ok (some (.value 3)) := by rfl
def nonzero_branch : Program := ⟨1,0,(.branch (.reg 0) (.seq .nil) (.set 0 (.constant 0)))⟩
example : callFuel true 80 nonzero_branch [17] (some 3) (some 0) = .ok (some (.traced 17 3 [])) := by rfl
example : callFuel false 80 nonzero_branch [17] (some 3) (some 0) = .ok (some (.value 17)) := by rfl
def zero_branch : Program := ⟨1,0,(.branch (.reg 0) (.set 0 (.constant 99)) (.set 0 (.constant 5)))⟩
example : callFuel true 80 zero_branch [0] (some 4) none = .ok (some (.traced 5 4 [(0,5)])) := by rfl
example : callFuel false 80 zero_branch [0] (some 4) none = .ok (some (.value 5)) := by rfl
def nested_loops : Program := ⟨0,3,(.seq (.cons (.set 3 (.constant 0)) (.cons (.loop 0 (.constant 2) (.loop 1 (.constant 2) (.set 3 (.binary .add (.reg 3) (.constant 1))))) .nil)))⟩
example : callFuel true 80 nested_loops [] (some 38) none = .ok (some (.traced 4 38 [(3,0),(3,1),(3,2),(3,3),(3,4)])) := by rfl
example : callFuel false 80 nested_loops [] (some 38) none = .ok (some (.value 4)) := by rfl
def unchecked_input_output : Program := ⟨1,0,(.seq .nil)⟩
example : callFuel true 80 unchecked_input_output [1267650600228229401496703205376] (some 1) (some 0) = .ok (some (.traced 1267650600228229401496703205376 1 [])) := by rfl
example : callFuel false 80 unchecked_input_output [1267650600228229401496703205376] (some 1) (some 0) = .ok (some (.value 1267650600228229401496703205376)) := by rfl
def unchecked_loop_index : Program := ⟨1,1,(.loop 1 (.reg 0) (.seq .nil))⟩
example : callFuel true 80 unchecked_loop_index [3] (some 9) (some 0) = .ok (some (.traced 2 9 [])) := by rfl
example : callFuel false 80 unchecked_loop_index [3] (some 9) (some 0) = .ok (some (.value 2)) := by rfl
end RunnerAuthorControls
