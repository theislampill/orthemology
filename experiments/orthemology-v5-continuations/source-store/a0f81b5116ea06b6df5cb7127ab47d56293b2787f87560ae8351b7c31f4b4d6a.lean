/- Exact separation of legal All self-instantiation from Girard-sensitive closure.
   New scoped specialisation of preserved no_self_product; UNCOMPILED. -/
import P01Examples
import HurkensBoundary
namespace P01D
open OrthemologyV2

/-- This is a metatheoretic decoding of the new PER proposal, not a term-level
    code evaluator and not canonical TypeCode interpretation. -/
def Realiser (P : PER) := {t : Term // P.dom t}

/-- AllPER returns a PER and all_self_eliminate permits that object as argument.
    This statement has no reification of all functions/sections as a conclusion. -/
theorem internal_all_self_instance (F : ParamFamily) (t u : Term)
    (h : (AllPER F).rel t u) : (F.obj (AllPER F)).rel t u :=
  all_self_eliminate h

/-- The excluded operation has an EXACT input type: every ambient section of
    GirardFamily, not merely finite tracked sections or admitted derivations.
    It is not supplied by internal_all_self_instance. -/
theorem no_same_level_Girard_retraction (P : PER)
    (pack : ((Q : PER) → OrthemologyV2Boundary.GirardFamily Realiser Q) → Realiser P)
    (unpack : Realiser P → (Q : PER) → OrthemologyV2Boundary.GirardFamily Realiser Q)
    (beta : ∀ (f : (Q : PER) → OrthemologyV2Boundary.GirardFamily Realiser Q) (Q : PER),
      unpack (pack f) Q = f Q) : False :=
  OrthemologyV2Boundary.no_self_product Realiser P pack unpack beta

end P01D
