"""Literal deterministic history policy with exact tests and unbounded counters.

Incremental Memory inputs must come from these routines with the same validated
model/body, or be deliberately constructed test states. action_for_history is the
public total-policy boundary on arbitrary finite histories. It validates syntax
before indexing and uses persistent lawful fallback off the certified policy.
"""
from dataclasses import dataclass, replace
from fractions import Fraction
from certificates import check_positive
from finite import used
from model import natural, validate_model


@dataclass(frozen=True)
class Memory:
    phase: int
    known1: bool
    retained: int | None
    departures: tuple
    uses: tuple
    receipts: tuple
    fallback: bool
    prepared_state: int | None
    prepared_action: int | None


def initial_memory(model, positive):
    model = validate_model(model)
    if check_positive(model, positive) is None:
        raise ValueError('controller requires an accepted positive body')
    return Memory(0, False, None, (0,) * model.n_states,
                  tuple((0,) * model.n_actions for _ in range(model.n_states)),
                  tuple(tuple((0,) * model.n_states for _ in range(model.n_actions))
                        for _ in range(model.n_states)), False, None, None)


def threshold(model):
    differences = [abs(p0 - p1) for states0, states1 in zip(model.rows[0], model.rows[1])
                   for row0, row1 in zip(states0, states1) for p0, p1 in zip(row0, row1) if p0 != p1]
    return min(differences) / 2 if differences else Fraction(1)


def rejection(model, memory):
    delta, theta = threshold(model), memory.phase % 2
    for s in range(model.n_states):
        for a in range(model.n_actions):
            count = memory.uses[s][a]
            if count > memory.phase:
                for y in range(model.n_states):
                    if abs(Fraction(memory.receipts[s][a][y], count) - model.rows[theta][s][a][y]) >= delta:
                        return True
    return False


def choose(model, positive, memory, state):
    natural(state, model.n_states)
    region = positive.K if memory.known1 else positive.W
    if memory.fallback or state not in region:
        action = model.menus[state][0]
        return action, replace(memory, fallback=True, retained=None, prepared_state=state, prepared_action=action)
    components = positive.known_components if memory.known1 else positive.uncertain_components[memory.phase % 2]
    retained = memory.retained
    if retained is None:
        retained = next((i for i, c in enumerate(components) if state in used(c)), None)
    pairs = (positive.D1 if memory.known1 else positive.D) if retained is None else components[retained]
    actions = tuple(a for s, a in pairs if s == state)
    if not actions:
        action = model.menus[state][0]
        return action, replace(memory, fallback=True, retained=None, prepared_state=state, prepared_action=action)
    action = actions[memory.departures[state] % len(actions)]
    return action, replace(memory, retained=retained, prepared_state=state, prepared_action=action)


def observe(model, positive, prepared_memory, state, action, receipt):
    natural(state, model.n_states); natural(action, model.n_actions); natural(receipt, model.n_states)
    if action not in model.menus[state]:
        raise ValueError('historical action is unlawful')
    memory = prepared_memory
    if memory.prepared_state is None or memory.prepared_action is None:
        raise ValueError('observe must follow choose')
    departures = list(memory.departures); departures[state] += 1
    uses = [list(row) for row in memory.uses]; uses[state][action] += 1
    receipts = [[list(row) for row in source] for source in memory.receipts]
    receipts[state][action][receipt] += 1
    updated = replace(memory, departures=tuple(departures), uses=tuple(map(tuple, uses)),
                      receipts=tuple(tuple(map(tuple, source)) for source in receipts),
                      prepared_state=None, prepared_action=None)
    impossible = (not model.rows[1][state][action][receipt] if memory.known1 else
                  not (model.rows[0][state][action][receipt] or model.rows[1][state][action][receipt]))
    if (memory.fallback or memory.prepared_state != state or memory.prepared_action != action or impossible):
        return replace(updated, fallback=True, retained=None)
    # Revelation owns precedence over both empirical rejection and component exit.
    if not memory.known1 and not model.rows[0][state][action][receipt]:
        return replace(updated, known1=True, retained=None, fallback=receipt not in positive.K)
    if memory.known1:
        return replace(updated, fallback=receipt not in positive.K)
    if receipt not in positive.W:
        return replace(updated, fallback=True, retained=None)
    components = positive.uncertain_components[memory.phase % 2]
    exited = memory.retained is not None and receipt not in used(components[memory.retained])
    if rejection(model, updated) or exited:
        return replace(updated, phase=memory.phase + 1, retained=None)
    return updated


def action_for_history(model, positive, history):
    model = validate_model(model)
    if type(history) not in (tuple, list) or not history or len(history) % 2 != 1:
        raise ValueError('history must be a nonempty odd-length state/action sequence')
    # Complete syntax validation precedes replay or any indexing by history data.
    for index, value in enumerate(history):
        natural(value, model.n_states if index % 2 == 0 else model.n_actions)
    for index in range(1, len(history), 2):
        if history[index] not in model.menus[history[index - 1]]:
            raise ValueError('history contains an unlawful action')
    positive = check_positive(model, positive)
    if positive is None:
        raise ValueError('controller requires an accepted positive body')
    memory = initial_memory(model, positive)
    if history[0] != model.initial:
        memory = replace(memory, fallback=True)
    for index in range(0, len(history) - 1, 2):
        _, prepared = choose(model, positive, memory, history[index])
        memory = observe(model, positive, prepared, history[index], history[index + 1], history[index + 2])
    return choose(model, positive, memory, history[-1])[0]
