"""
kripke_sweep.py — Experiment 2: Kripke grounding sweep over random theories.

Sweeps base-fact probability from near-zero to near-one, sampling
multiple random dependency graphs at each probability level and
recording the fraction of sentences that are grounded at the fixed point.

Prediction (Theorem 5, P2)
--------------------------
Grounding fraction increases monotonically with base-fact density.
At probability 1.0 all nodes are base nodes (trivially grounded).
At probability 0.0 all nodes are neg-nodes; cycles are guaranteed and
all nodes remain Undetermined.  The intermediate regime shows a smooth
transition that is consistent with the theoretical grounding guarantee.

The sweep also records mean iterations-to-convergence, which should
remain bounded (finite grounding depth → finite termination, Theorem 5 P3).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from ..core.kripke import kripke_fixed_point
from ..core.grounding import random_theory


def run_kripke_sweep(
    results_dir: Path,
    probs: Iterable[float],
    num_nodes: int = 250,
    trials: int = 150,
    seed: int = 1234,
) -> pd.DataFrame:
    """
    Sweep base-fact probability and record grounding statistics.

    Parameters
    ----------
    results_dir :
        Directory to write CSV output.
    probs :
        Iterable of base-fact probabilities to sweep.
    num_nodes :
        Number of sentences per random theory.
    trials :
        Number of independent random theories per probability level.
    seed :
        RNG seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Columns: base_probability, mean_grounded_ratio, std_grounded_ratio,
        mean_iterations, min_grounded_ratio, max_grounded_ratio.
    """
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float]] = []

    for p_base in probs:
        ratios: list[float] = []
        iters: list[int] = []

        for _ in range(trials):
            nodes = random_theory(num_nodes=num_nodes, base_prob=p_base, rng=rng)
            _, iteration_count, grounded_ratio = kripke_fixed_point(nodes)
            ratios.append(grounded_ratio)
            iters.append(iteration_count)

        rows.append(
            {
                "base_probability": float(p_base),
                "mean_grounded_ratio": float(np.mean(ratios)),
                "std_grounded_ratio": float(np.std(ratios)),
                "min_grounded_ratio": float(np.min(ratios)),
                "max_grounded_ratio": float(np.max(ratios)),
                "mean_iterations": float(np.mean(iters)),
                "max_iterations": float(np.max(iters)),
            }
        )

    df = pd.DataFrame(rows)
    results_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(results_dir / "kripke_grounding_sweep.csv", index=False)
    return df
