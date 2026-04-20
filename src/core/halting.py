"""
halting.py — Bounded halting decider for finite-state machines.

Models the computational aspect of the DCS: the Halting Problem is
an instance of DCS Instability in S_HP (Turing-complete programs over
a Universal Turing Machine).  On *finite-state* machines, however,
halting is always decidable — the bounded decider visits each state at
most once and correctly determines whether the machine halts.

This module implements:
  - ``generate_random_machine``: random FSM generator for experiments.
  - ``bounded_decider``: the polynomial-time halting decider for FSMs.
  - ``bounded_simulation``: direct simulation for ground-truth comparison.

The agreement between decider and simulation across thousands of
randomly generated machines empirically validates the DCS prediction
that Bypass B_UD^1 (bounded domain) recovers decidability.

References
----------
Turing, A. (1937). On computable numbers. *PLMS*, 42, 230–265.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Machine type
# ---------------------------------------------------------------------------

#: A finite-state machine is a list of transitions.
#: ``transitions[s] == -1`` means state *s* is a halting state.
#: ``transitions[s] == j`` means the machine moves from *s* to *j*.
FSM = list[int]


# ---------------------------------------------------------------------------
# Random machine generation
# ---------------------------------------------------------------------------

def generate_random_machine(
    n_states: int,
    halt_prob: float,
    rng: np.random.Generator,
) -> FSM:
    """
    Sample a random finite-state machine.

    Parameters
    ----------
    n_states :
        Number of distinct non-halting states.
    halt_prob :
        Probability that any given state is a halting state (transition = -1).
    rng :
        NumPy random generator for reproducibility.

    Returns
    -------
    FSM
        A list of length *n_states* where each entry is either -1 (halt)
        or an integer in [0, n_states) (next state).
    """
    transitions: FSM = []
    for _ in range(n_states):
        if rng.random() < halt_prob:
            transitions.append(-1)
        else:
            transitions.append(int(rng.integers(0, n_states)))
    return transitions


# ---------------------------------------------------------------------------
# Bounded decider
# ---------------------------------------------------------------------------

def bounded_decider(transitions: FSM, start_state: int = 0) -> bool:
    """
    Decide whether the FSM halts starting from *start_state*.

    On finite-state machines the halting problem is decidable: simply
    track visited states.  If a state is revisited, the machine is in
    an infinite loop.  If transition -1 is reached, the machine halts.

    Time complexity: O(|states|).

    Parameters
    ----------
    transitions :
        The FSM transition table.
    start_state :
        Index of the initial state.

    Returns
    -------
    bool
        True if the machine halts; False if it loops.
    """
    seen: set[int] = set()
    current = start_state
    while current not in seen:
        nxt = transitions[current]
        if nxt == -1:
            return True          # reached a halting state
        seen.add(current)
        current = nxt
    return False                 # revisited a state → infinite loop


# ---------------------------------------------------------------------------
# Direct simulation (ground truth)
# ---------------------------------------------------------------------------

def bounded_simulation(
    transitions: FSM,
    start_state: int = 0,
) -> tuple[bool, int]:
    """
    Simulate the FSM for at most ``len(transitions) + 1`` steps.

    On a machine with *n* states, if it has not halted after *n* steps
    it will never halt (pigeonhole principle).

    Parameters
    ----------
    transitions :
        The FSM transition table.
    start_state :
        Index of the initial state.

    Returns
    -------
    halted : bool
        Whether a halt transition was reached within the step budget.
    steps : int
        Number of steps executed.
    """
    current = start_state
    step_limit = len(transitions) + 1
    for step in range(1, step_limit + 1):
        nxt = transitions[current]
        if nxt == -1:
            return True, step
        current = nxt
    return False, step_limit


# ---------------------------------------------------------------------------
# Batch experiment helper
# ---------------------------------------------------------------------------

def run_halting_experiment(
    n_states: int,
    halt_prob: float,
    samples: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """
    Run *samples* halting experiments for the given parameters.

    Returns a summary dict with accuracy, observed halting rate, and mean steps.
    """
    matches = 0
    halting_count = 0
    step_list: list[int] = []

    for _ in range(samples):
        machine = generate_random_machine(n_states, halt_prob, rng)
        dec = bounded_decider(machine)
        obs, steps = bounded_simulation(machine)
        if dec == obs:
            matches += 1
        if obs:
            halting_count += 1
        step_list.append(steps)

    return {
        "n_states": n_states,
        "halt_prob": halt_prob,
        "accuracy": matches / samples,
        "observed_halting_rate": halting_count / samples,
        "mean_steps_until_stop_or_loop": float(np.mean(step_list)),
    }
