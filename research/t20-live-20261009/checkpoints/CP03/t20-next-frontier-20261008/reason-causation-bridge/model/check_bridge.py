#!/usr/bin/env python3
"""Exhaustive finite implementation test, not a cognition or metaphysics test."""
from itertools import product
import json
from pathlib import Path

LITERALS = ("p", "not_p", "q", "not_q")
CODES = tuple(range(4))
BITS = (False, True)

def decode(code):
    return LITERALS[code]

def valuation(literal, world):
    p, q = world
    return {"p":p, "not_p":not p, "q":q, "not_q":not q}[literal]

def encode_packet(A, B, C, first, second, noise):
    return (A & 1, (A >> 1) & 1, B & 1, (B >> 1) & 1,
            C & 1, (C >> 1) & 1, int(first), int(second), int(noise))

def abstraction(bits):
    A = bits[0] + 2 * bits[1]
    B = bits[2] + 2 * bits[3]
    C = bits[4] + 2 * bits[5]
    return decode(A), decode(B), decode(C), bool(bits[6]), bool(bits[7])

def microstep(bits, *, drop_match=False, drop_first=False):
    # Bit equality and Boolean gates; no semantic evaluator is called.
    match = (bits[0] == bits[2]) and (bits[1] == bits[3])
    accepted = (bool(bits[6]) or drop_first) and bool(bits[7]) and (match or drop_match)
    return int(accepted), bits[4], bits[5]

def decode_output(bits):
    return bool(bits[0]), decode(bits[1] + 2 * bits[2])

def macrostep(packet):
    A, B, C, first, second = packet
    return first and second and A == B, C

def input_correct(packet, world):
    A, B, C, first, second = packet
    return ((not first) or valuation(A, world)) and ((not second) or
            ((not valuation(B, world)) or valuation(C, world)))

def output_correct(output, world):
    accepted, literal = output
    return (not accepted) or valuation(literal, world)

def as_record(packet, world, output):
    return {"packet":packet, "world":{"p":world[0],"q":world[1]},
            "output":output, "input_correct":input_correct(packet,world),
            "output_correct":output_correct(output,world)}

def run():
    packets = list(product(CODES, CODES, CODES, BITS, BITS, BITS))
    worlds = list(product(BITS, BITS))
    checks = 0
    mutant_witnesses = {}
    for A,B,C,first,second,noise in packets:
        bits = encode_packet(A,B,C,first,second,noise)
        packet = abstraction(bits)
        output = decode_output(microstep(bits))
        assert output == macrostep(packet)
        # Irrelevant micro-level variation does not alter the interpreted response.
        other_noise = encode_packet(A,B,C,first,second,not noise)
        assert microstep(bits) == microstep(other_noise)
        for world in worlds:
            assert not input_correct(packet,world) or output_correct(output,world)
            checks += 1
            for key,kwargs in (("drop_formula_match",{"drop_match":True}),
                               ("drop_first_premise",{"drop_first":True})):
                bad_output = decode_output(microstep(bits,**kwargs))
                if input_correct(packet,world) and not output_correct(bad_output,world):
                    mutant_witnesses.setdefault(key,as_record(packet,world,bad_output))
    assert len(mutant_witnesses) == 2

    base = encode_packet(0,0,2,True,True,False)  # p, p→q; conclude q.
    interventions = {
      "base":base,
      "withdraw_first":encode_packet(0,0,2,False,True,False),
      "withdraw_second":encode_packet(0,0,2,True,False,False),
      "change_first_formula_only":encode_packet(2,0,2,True,True,False),
      "change_implication_antecedent_only":encode_packet(0,2,2,True,True,False),
      "change_consequent_only":encode_packet(0,0,3,True,True,False),
    }
    outcomes = {key:decode_output(microstep(bits)) for key,bits in interventions.items()}
    assert outcomes["base"] == (True,"q")
    for key in ("withdraw_first","withdraw_second","change_first_formula_only",
                "change_implication_antecedent_only"):
        assert outcomes[key][0] is False
    assert outcomes["change_consequent_only"] == (True,"not_q")

    # Same input, program and compositional content map, different external q.
    packet = abstraction(base)
    output = decode_output(microstep(base))
    good = as_record(packet,(True,True),output)
    bad = as_record(packet,(True,False),output)
    assert good["input_correct"] and good["output_correct"]
    assert not bad["input_correct"] and not bad["output_correct"]

    # Explicit upstream equations for a physical-model version of the input control.
    # a=p; b=(not p or q) or error. Same equation/codebook in both cases.
    # Local packet can coincide while external q and error differ.
    coupled = []
    for p,q,error in ((True,True,False),(True,False,True)):
        local = encode_packet(0,0,2,p,(not p or q) or error,False)
        coupled.append({"world":{"p":p,"q":q}, "source_error":error,
                        "local_bits":local,
                        "record":as_record(abstraction(local),(p,q),decode_output(microstep(local)))})
    assert coupled[0]["local_bits"] == coupled[1]["local_bits"]
    assert coupled[0]["record"]["output_correct"]
    assert not coupled[1]["record"]["output_correct"]

    # A concrete mutation witness, not a probability or frequency estimate.
    specific = encode_packet(0,2,1,True,True,False) # p, q→¬p.
    specific_packet = abstraction(specific)
    specific_world = (True,False)
    mutant = decode_output(microstep(specific,drop_match=True))
    assert input_correct(specific_packet,specific_world)
    assert not output_correct(mutant,specific_world)
    assert decode_output(microstep(specific))[0] is False

    return {
      "scope":"Finite bit-level/formula-level compatibility only",
      "formula_codes":dict(enumerate(LITERALS)),
      "input_packets":len(packets), "world_valuations":len(worlds),
      "truth_preservation_checks":checks,
      "commuting_abstraction_checks":len(packets),
      "noise_invariance_checks":len(packets),
      "interventions":outcomes,
      "fixed_content_external_world_control":{"good":good,"bad":bad},
      "explicit_upstream_error_control":coupled,
      "mutation_witnesses":mutant_witnesses,
      "specific_formula_matching_mutation":as_record(specific_packet,specific_world,mutant),
      "established":["finite commuting abstraction","formula-code-sensitive acceptance",
         "conditional propositional truth preservation","faulty match mutation rejected",
         "valid execution does not authenticate external premise truth"],
      "not_established":["actual mental content","subjective understanding","human belief",
         "naturalised normativity or proper function","warrant or knowledge",
         "metaphysical naturalism","theism","evolutionary origin",
         "any reliability probability"]}

if __name__ == "__main__":
    result=run()
    rendered=json.dumps(result,indent=2,sort_keys=True)+"\n"
    (Path(__file__).parent/"RESULTS.json").write_text(rendered)
    print(rendered,end="")
