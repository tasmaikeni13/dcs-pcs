"""
grounding_curve.py — Figure: Kripke grounding ratio vs base-fact probability.

Produces ``grounding_vs_base_probability.png`` showing how the fraction
of grounded sentences at the Kripke fixed point rises with the density
of non-self-referential base facts in a random theory.

This figure directly validates the prediction from Theorem 5 (P2): as
the theory contains more empirically anchored base facts, the grounded
(PCS-decidable) fraction approaches 1.0.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_grounding_curve(df: pd.DataFrame, figures_dir: Path) -> None:
    """
    Plot grounded-ratio vs base-fact probability with ±1 std-dev band.

    Parameters
    ----------
    df :
        Output of :func:`~dcs_pcs.experiments.kripke_sweep.run_kripke_sweep`.
    figures_dir :
        Directory to save the PNG.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8, 5), dpi=160)

    x = df["base_probability"].to_numpy()
    y = df["mean_grounded_ratio"].to_numpy()
    yerr = df["std_grounded_ratio"].to_numpy()

    ax.plot(
        x, y,
        marker="o", linewidth=2.2,
        color="#0b7285",
        label="Mean grounded ratio",
        zorder=3,
    )
    ax.fill_between(
        x,
        np.maximum(0.0, y - yerr),
        np.minimum(1.0, y + yerr),
        alpha=0.20, color="#0b7285",
        label="±1 standard deviation",
    )

    # Annotate endpoints
    ax.annotate(
        f"{y[0]:.2f}",
        xy=(x[0], y[0]),
        xytext=(x[0] + 0.03, y[0] + 0.06),
        fontsize=8.5, color="#0b7285",
    )
    ax.annotate(
        f"{y[-1]:.2f}",
        xy=(x[-1], y[-1]),
        xytext=(x[-1] - 0.10, y[-1] - 0.07),
        fontsize=8.5, color="#0b7285",
    )

    ax.set_ylim(-0.02, 1.05)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Base-fact probability $p_{\\mathrm{base}}$", fontsize=12)
    ax.set_ylabel("Grounded ratio at fixed point", fontsize=12)
    ax.set_title(
        "Kripke Grounding Increases with Base-Fact Density\n"
        "(Empirical support for PCS Grounded Completeness, Theorem 5 P2)",
        fontsize=11,
    )
    ax.legend(frameon=True, fontsize=10)
    fig.tight_layout()
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "grounding_vs_base_probability.png", bbox_inches="tight")
    plt.close(fig)
