"""
halting_heatmap.py — Figure: Bounded halting experiment results.

Produces ``bounded_halting_empirics.png`` — a two-panel figure:
  Left  — Decider accuracy heatmap (n_states × halt_prob).
  Right — Observed halting rate vs n_states, one line per halt_prob.

Both panels empirically validate the DCS prediction that on finite-state
machines (Bypass B_UD^1 operative) the bounded decider achieves
100 % agreement with direct simulation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_bounded_halting(df: pd.DataFrame, figures_dir: Path) -> None:
    """
    Render the bounded halting empirics figure.

    Parameters
    ----------
    df :
        Output of :func:`~dcs_pcs.experiments.halting_validation.run_halting_validation`.
    figures_dir :
        Directory to save the PNG.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=160)

    # ----- Left panel: accuracy heatmap -----
    pivot_acc = df.pivot(index="n_states", columns="halt_prob", values="accuracy")
    im = axes[0].imshow(
        pivot_acc.to_numpy(),
        aspect="auto",
        cmap="YlGn",
        vmin=0.98,
        vmax=1.0,
    )
    axes[0].set_xticks(range(len(pivot_acc.columns)))
    axes[0].set_xticklabels([f"{p:.2f}" for p in pivot_acc.columns], fontsize=9)
    axes[0].set_yticks(range(len(pivot_acc.index)))
    axes[0].set_yticklabels([str(s) for s in pivot_acc.index], fontsize=9)
    axes[0].set_xlabel("Halt-transition probability", fontsize=11)
    axes[0].set_ylabel("Number of states", fontsize=11)
    axes[0].set_title("Bounded Decider Accuracy\n(expected: 1.000 across all cells)", fontsize=10)
    cb = fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)
    cb.ax.set_ylabel("Accuracy", fontsize=9)

    # Annotate each cell with the accuracy value.
    data_arr = pivot_acc.to_numpy()
    for ri in range(data_arr.shape[0]):
        for ci in range(data_arr.shape[1]):
            axes[0].text(
                ci, ri, f"{data_arr[ri, ci]:.4f}",
                ha="center", va="center", fontsize=7.5, color="black",
            )

    # ----- Right panel: halting rate vs n_states -----
    cmap = plt.cm.get_cmap("tab10")
    halt_probs = sorted(df["halt_prob"].unique())
    for idx, prob in enumerate(halt_probs):
        sub = df[df["halt_prob"] == prob].sort_values("n_states")
        axes[1].plot(
            sub["n_states"],
            sub["observed_halting_rate"],
            marker="o",
            linewidth=1.9,
            color=cmap(idx),
            label=f"halt p = {prob:.2f}",
        )

    axes[1].set_ylim(-0.02, 1.05)
    axes[1].set_xlabel("Number of states", fontsize=11)
    axes[1].set_ylabel("Observed halting rate", fontsize=11)
    axes[1].set_title("Halting Frequency on Bounded Machines", fontsize=10)
    axes[1].legend(fontsize=8, frameon=True)

    fig.suptitle(
        "Bounded-Domain Halting Experiments\n"
        "(Bypass $B_{UD}^1$ restores full decidability on finite-state machines)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "bounded_halting_empirics.png", bbox_inches="tight")
    plt.close(fig)
