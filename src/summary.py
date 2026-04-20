"""
summary.py — Aggregate results into JSON and LaTeX summary artefacts.

Reads the four experiment DataFrames and writes:
  results/validation_summary.json          — machine-readable summary
  results/empirical_summary_table.tex      — LaTeX table fragment for the paper
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def write_summary_json(
    liar_df: pd.DataFrame,
    grounding_df: pd.DataFrame,
    halting_df: pd.DataFrame,
    depth_df: pd.DataFrame,
    results_dir: Path,
) -> dict:
    """Serialise all key metrics to JSON."""
    payload = {
        "liar": {
            "bivalent_satisfying_assignments": int(
                liar_df[
                    (liar_df["semantics"] == "bivalent") & (liar_df["satisfies_G_iff_not_G"])
                ].shape[0]
            ),
            "trivalent_satisfying_assignments": int(
                liar_df[
                    (liar_df["semantics"] == "trivalent") & (liar_df["satisfies_G_iff_not_G"])
                ].shape[0]
            ),
        },
        "kripke_grounding": {
            "min_mean_grounded_ratio": float(grounding_df["mean_grounded_ratio"].min()),
            "max_mean_grounded_ratio": float(grounding_df["mean_grounded_ratio"].max()),
            "mean_iterations_avg": float(grounding_df["mean_iterations"].mean()),
        },
        "bounded_halting": {
            "min_accuracy": float(halting_df["accuracy"].min()),
            "max_accuracy": float(halting_df["accuracy"].max()),
            "mean_accuracy": float(halting_df["accuracy"].mean()),
            "configurations_tested": int(len(halting_df)),
        },
        "decision_termination": {
            "max_tested_depth": int(depth_df[depth_df["depth"] > 0]["depth"].max()),
            "all_grounded_chains_terminated": bool(
                depth_df[depth_df["depth"] > 0]["grounded"].all()
            ),
            "cycle_case_value": str(
                depth_df[depth_df["depth"] == -1]["terminal_value"].iloc[0]
            ),
        },
    }

    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "validation_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    return payload


def write_summary_latex(
    liar_df: pd.DataFrame,
    grounding_df: pd.DataFrame,
    halting_df: pd.DataFrame,
    depth_df: pd.DataFrame,
    results_dir: Path,
) -> None:
    """Write a LaTeX tabular fragment to results/empirical_summary_table.tex."""
    bivalent_sol = int(
        liar_df[
            (liar_df["semantics"] == "bivalent") & (liar_df["satisfies_G_iff_not_G"])
        ].shape[0]
    )
    trivalent_sol = int(
        liar_df[
            (liar_df["semantics"] == "trivalent") & (liar_df["satisfies_G_iff_not_G"])
        ].shape[0]
    )
    min_acc = float(halting_df["accuracy"].min())
    max_acc = float(halting_df["accuracy"].max())
    max_gr  = float(grounding_df["mean_grounded_ratio"].max())
    min_gr  = float(grounding_df["mean_grounded_ratio"].min())
    max_d   = int(depth_df[depth_df["depth"] > 0]["depth"].max())

    lines = [
        r"\begin{tabular}{p{9.5cm}p{5.2cm}}",
        r"\toprule",
        r"Empirical check & Result \\",
        r"\midrule",
        rf"Bivalent liar fixed-point $G \leftrightarrow \neg G$ "
        rf"& {bivalent_sol}/2 satisfying assignments \\",
        rf"Three-valued liar fixed-point "
        rf"& {trivalent_sol}/3 satisfying assignments (stable $U$) \\",
        rf"Bounded halting decider vs.\ simulation "
        rf"& accuracy in $[{min_acc:.3f},\ {max_acc:.3f}]$ \\",
        rf"Kripke grounding sweep (random dependency graphs) "
        rf"& grounded ratio in $[{min_gr:.3f},\ {max_gr:.3f}]$ \\",
        rf"Finite-depth decision termination stress test "
        rf"& converged for all depths up to {max_d} \\",
        r"\bottomrule",
        r"\end{tabular}",
    ]

    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "empirical_summary_table.tex").write_text(
        "\n".join(lines), encoding="utf-8"
    )
