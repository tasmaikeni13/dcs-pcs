"""
depth_termination.py — Experiment 4: Finite-depth termination scaling.

Validates Theorem 5 P3: for sentences with finite grounding depth d,
the Kripke fixed-point algorithm terminates in exactly d+1 iterations.
This provides computational evidence that grounded sentences have a
well-defined, finite decision procedure.

Conversely, purely self-referential (cyclic) sentences are tested to
confirm they remain Undetermined (U) at the fixed point — consistent
with PCS correctly classifying them as ``Undetermined'' rather than
paradoxical.

The experiment sweeps depth from 1 to *max_depth* on linear chains
and records iterations and terminal values.  It also runs the cycle
control (Liar node) as a negative-control comparison.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..core.kripke import kripke_fixed_point, linear_chain, liar_node


def run_depth_termination(
    results_dir: Path,
    max_depth: int = 40,
) -> pd.DataFrame:
    """
    Run the finite-depth termination scaling experiment.

    For depths 1 … *max_depth*, build a linear chain of that depth,
    run the Kripke engine, and record iterations and terminal value.
    Also add a cycle-control row (depth = -1) for the Liar sentence.

    Returns
    -------
    pd.DataFrame
        Columns: depth, iterations_to_fixed_point, terminal_value, grounded.
        depth == -1 encodes the cycle (Liar) control case.
    """
    rows: list[dict] = []

    for depth in range(1, max_depth + 1):
        chain = linear_chain(depth=depth, base_value="T")
        values, iterations, _ = kripke_fixed_point(chain)
        terminal = values[-1]
        rows.append(
            {
                "depth": depth,
                "iterations_to_fixed_point": iterations,
                "terminal_value": terminal,
                "grounded": terminal != "U",
            }
        )

    # Cycle control: the Liar node (self-negating) — should remain U.
    liar = liar_node()
    values_cycle, iters_cycle, _ = kripke_fixed_point(liar)
    rows.append(
        {
            "depth": -1,   # sentinel: cycle case
            "iterations_to_fixed_point": iters_cycle,
            "terminal_value": values_cycle[0],
            "grounded": values_cycle[0] != "U",
        }
    )

    df = pd.DataFrame(rows)
    results_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(results_dir / "finite_depth_termination.csv", index=False)
    return df
