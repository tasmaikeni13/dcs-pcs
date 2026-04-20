"""
depth_scaling.py — Figure: Finite grounding depth implies finite termination.

Produces ``finite_depth_termination.png`` showing the linear relationship
between grounding depth and Kripke fixed-point iterations.

Theorem 5 P3 predicts that a sentence with grounding depth d requires
exactly d+1 Kripke iterations to stabilise.  This figure validates that
prediction computationally across all tested depths.

A second sub-panel distinguishes grounded (T/F) terminal values from the
cycle-control (U) case.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_depth_scaling(df: pd.DataFrame, figures_dir: Path) -> None:
    """
    Render the finite-depth termination scaling figure.

    Parameters
    ----------
    df :
        Output of :func:`~dcs_pcs.experiments.depth_termination.run_depth_termination`.
    figures_dir :
        Directory to save the PNG.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=160)

    # ----- Left panel: iterations vs depth -----
    chain = df[df["depth"] > 0].copy()

    axes[0].plot(
        chain["depth"],
        chain["iterations_to_fixed_point"],
        marker="o",
        linewidth=2.1,
        color="#ae3ec9",
        label="Observed iterations",
        zorder=3,
    )
    axes[0].plot(
        chain["depth"],
        chain["depth"] + 1,
        linestyle="--",
        linewidth=1.5,
        color="#495057",
        label="depth + 1 (theory prediction)",
    )
    axes[0].set_xlabel("Grounding depth $d$", fontsize=12)
    axes[0].set_ylabel("Iterations to fixed point", fontsize=12)
    axes[0].set_title(
        "Finite Grounding Depth → Finite Termination\n"
        "(Theorem 5 P3: iterations = depth + 1)",
        fontsize=10,
    )
    axes[0].legend(frameon=True, fontsize=10)

    # ----- Right panel: terminal value distribution -----
    value_map = {"T": "#2f9e44", "F": "#e03131", "U": "#868e96"}
    counts = chain["terminal_value"].value_counts()
    bars = axes[1].bar(
        counts.index,
        counts.values,
        color=[value_map.get(v, "#adb5bd") for v in counts.index],
        edgecolor="#343a40",
        linewidth=1.0,
    )
    for bar, count in zip(bars, counts.values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            str(count),
            ha="center", va="bottom", fontsize=11,
        )

    # Add cycle-control annotation
    cycle_row = df[df["depth"] == -1].iloc[0]
    axes[1].axhline(0, color="none")  # spacing trick
    axes[1].text(
        0.97, 0.97,
        f"Liar cycle (control):\nterminal value = {cycle_row['terminal_value']}\n"
        f"(grounded = {cycle_row['grounded']})",
        transform=axes[1].transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3bf", edgecolor="#f59f00"),
    )

    axes[1].set_xlabel("Terminal truth value", fontsize=12)
    axes[1].set_ylabel("Number of chain depths with this value", fontsize=11)
    axes[1].set_title(
        "Terminal Values Across All Tested Depths\n"
        "(Green = T, Red = F, Grey = U; cycle control in box)",
        fontsize=10,
    )

    fig.suptitle(
        "PCS Decision Procedure: Depth Scaling Validation (Experiment 4)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "finite_depth_termination.png", bbox_inches="tight")
    plt.close(fig)
