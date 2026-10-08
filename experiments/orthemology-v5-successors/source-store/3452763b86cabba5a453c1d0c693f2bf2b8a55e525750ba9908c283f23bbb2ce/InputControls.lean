import CertificateData
open OrthemicCertificate
private def interp : Interpretation := ⟨["m"], ["s"], ["a"], "r1", "o", "s", "a"⟩
private def good : Input 1 1 1 := ⟨#[1], #[2], [⟨[0],0,[0]⟩], interp⟩
#guard good.inputCheck
#guard !( {good with rows := #[-1]} : Input 1 1 1).inputCheck
#guard !( {good with rows := #[2]} : Input 1 1 1).inputCheck
#guard !( {good with rows := #[]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[0],0,[0]⟩,⟨[0],0,[0]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[1],0,[0]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[0],1,[0]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[0],0,[1]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[0,0],0,[0]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with menus := [⟨[0],0,[0,0]⟩]} : Input 1 1 1).inputCheck
#guard !( {good with interpretation := {interp with authority := "changed"}} : Input 1 1 1).sameInput good
-- These malformed binary dimensions must reject before enumerating any Fin universe.
private def huge : Input (2^100) (2^100) (2^100) := ⟨#[],#[],[],interp⟩
#guard !huge.inputCheck
private def zeroHuge : Input 0 (2^100) (2^100) := ⟨#[],#[],[],interp⟩
#guard !zeroHuge.inputCheck
#eval good.inputCheck
private def zeroStateHuge : Input (2^100) 0 (2^100) := ⟨#[],#[],[],interp⟩
#guard !zeroStateHuge.inputCheck
private def zeroActionHuge : Input (2^100) (2^100) 0 := ⟨#[],#[],[],interp⟩
#guard !zeroActionHuge.inputCheck
