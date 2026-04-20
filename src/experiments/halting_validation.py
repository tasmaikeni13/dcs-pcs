"""
halting_validation.py — Experiment 3: Bounded halting validation.

Validates the DCS prediction that on finite-state machines (bounded
domain, Bypass B_UD^1) the halting problem is fully decidable.

For each combination of machine size and halting-transition probability,
we sample *samples* random FSMs and compare the bounded decider's output
against direct simulation.  Expected result: 100 % agreement.

The experiment also records observed halting rates and mean step counts,
providing a concrete picture of the Turing machine landscape restricted
to finite-state realizations.

References
----------
Turing, A. (1937). On computable numbers. *PLMS*, 42, 230–265.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from ..core.halting import run_halting_experiment


def run_halting_validation(
    results_dir: Path,
    state_grid: Iterable[int],
    halt_prob_grid: Iterable[float],
    samples: int = 500,
    seed: int = 7,
) -> pd.DataFrame:
    """
    Run the bounded halting validation experiment.

    Parameters
    ----------
    results_dir :
        Directory to write CSV output.
    state_grid :
        Machine sizes (number of states) to test.
    halt_prob_grid :
        Halting-transition probabilities to test.
    samples :
        Number of random machines per (n_states, halt_prob) pair.
    seed :
        RNG seed.

    Returns
    -------
    pd.DataFrame
        Columns: n_states, halt_prob, accuracy, observed_halting_rate,
        mean_steps_until_stop_or_loop.
    """
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float]] = []

    for n_states in state_grid:
        for halt_prob in halt_prob_grid:
            result = run_halting_experiment(
                n_states=n_states,
                halt_prob=halt_prob,
                samples=samples,
                rng=rng,
            )
            rows.append(result)

    df = pd.DataFrame(rows)
    results_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(results_dir / "bounded_halting_validation.csv", index=False)
    return df
