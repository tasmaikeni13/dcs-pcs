#!/usr/bin/env python3
"""
run_light.py — Light mode runner (quick functional test).

Executes all four experiments with small parameter settings so the
entire suite completes in under 30 seconds on a modern laptop.
Intended for CI, local development, and first-time verification.

Usage
-----
    python scripts/run_light.py

Output
------
    results/   — CSV / JSON artefacts
    figures/   — PNG figures (8 files)

Parameters (light mode)
-----------------------
    Kripke sweep   : 9 probability levels, 50 nodes, 30 trials
    Halting        : states ∈ {4, 8, 12}, halt_prob ∈ {0.2, 0.5, 0.8}, 100 samples
    Depth scaling  : max depth = 20
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

# Allow running from the repo root without installing the package.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.experiments.liar_fixed_points import run_liar_experiment, run_deterministic_grounding
from src.experiments.kripke_sweep import run_kripke_sweep
from src.experiments.halting_validation import run_halting_validation
from src.experiments.depth_termination import run_depth_termination
from src.figures.architecture import plot_dcs_architecture, plot_bypass_lattice
from src.figures.grounding_curve import plot_grounding_curve
from src.figures.halting_heatmap import plot_bounded_halting
from src.figures.depth_scaling import plot_depth_scaling
from src.figures.pcs_spectrum import plot_pcs_completeness_spectrum, plot_dcs_isomorphism_table
from src.summary import write_summary_json, write_summary_latex

RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def banner(msg: str) -> None:
    width = 64
    print("\n" + "─" * width)
    print(f"  {msg}")
    print("─" * width)


def main() -> None:
    t0 = time.time()
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║   DCS / PCS Empirical Validation Suite — LIGHT MODE     ║")
    print("║   (quick functional test; ~30 s on a modern laptop)     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ------------------------------------------------------------------ #
    # Experiment 1 — Liar fixed-point analysis                            #
    # ------------------------------------------------------------------ #
    banner("Experiment 1 / 4 — Liar Fixed-Point Analysis")
    liar_df  = run_liar_experiment(RESULTS)
    det_df   = run_deterministic_grounding(RESULTS)

    biv_sat = liar_df[(liar_df["semantics"] == "bivalent") & liar_df["satisfies_G_iff_not_G"]].shape[0]
    tri_sat = liar_df[(liar_df["semantics"] == "trivalent") & liar_df["satisfies_G_iff_not_G"]].shape[0]
    print(f"  Bivalent satisfying assignments  : {biv_sat}/2  (expected 0)")
    print(f"  Trivalent satisfying assignments : {tri_sat}/3  (expected 1 — value U)")
    print(f"  Deterministic grounding (6 nodes): {det_df['grounded'].sum()}/6 grounded")

    # ------------------------------------------------------------------ #
    # Experiment 2 — Kripke grounding sweep                               #
    # ------------------------------------------------------------------ #
    banner("Experiment 2 / 4 — Kripke Grounding Sweep")
    probs = np.linspace(0.05, 0.85, 9)
    grounding_df = run_kripke_sweep(
        RESULTS, probs=probs, num_nodes=50, trials=30, seed=1234
    )
    print(f"  Base-prob range  : {probs[0]:.2f} – {probs[-1]:.2f}")
    print(f"  Grounded ratio   : {grounding_df['mean_grounded_ratio'].min():.3f} – "
          f"{grounding_df['mean_grounded_ratio'].max():.3f}")
    print(f"  Mean iterations  : {grounding_df['mean_iterations'].mean():.1f}")

    # ------------------------------------------------------------------ #
    # Experiment 3 — Bounded halting validation                           #
    # ------------------------------------------------------------------ #
    banner("Experiment 3 / 4 — Bounded Halting Validation")
    halting_df = run_halting_validation(
        RESULTS,
        state_grid=[4, 8, 12],
        halt_prob_grid=[0.2, 0.5, 0.8],
        samples=100,
        seed=7,
    )
    print(f"  Configurations tested : {len(halting_df)}")
    print(f"  Accuracy range        : {halting_df['accuracy'].min():.4f} – "
          f"{halting_df['accuracy'].max():.4f}  (expected 1.0000)")

    # ------------------------------------------------------------------ #
    # Experiment 4 — Finite-depth termination                             #
    # ------------------------------------------------------------------ #
    banner("Experiment 4 / 4 — Finite-Depth Termination Scaling")
    depth_df = run_depth_termination(RESULTS, max_depth=20)
    chain    = depth_df[depth_df["depth"] > 0]
    cycle    = depth_df[depth_df["depth"] == -1].iloc[0]
    print(f"  Max depth tested           : {chain['depth'].max()}")
    print(f"  All chains grounded        : {chain['grounded'].all()}")
    print(f"  Iterations = depth + 1     : {(chain['iterations_to_fixed_point'] == chain['depth'] + 1).all()}")
    print(f"  Liar cycle terminal value  : {cycle['terminal_value']}  (expected U)")

    # ------------------------------------------------------------------ #
    # Figures                                                             #
    # ------------------------------------------------------------------ #
    banner("Generating Figures")
    plot_dcs_architecture(FIGURES)
    print("  ✓ dcs_bypass_architecture.png")
    plot_bypass_lattice(FIGURES)
    print("  ✓ bypass_lattice_heatmap.png")
    plot_grounding_curve(grounding_df, FIGURES)
    print("  ✓ grounding_vs_base_probability.png")
    plot_bounded_halting(halting_df, FIGURES)
    print("  ✓ bounded_halting_empirics.png")
    plot_depth_scaling(depth_df, FIGURES)
    print("  ✓ finite_depth_termination.png")
    plot_pcs_completeness_spectrum(FIGURES)
    print("  ✓ pcs_completeness_spectrum.png")
    plot_dcs_isomorphism_table(FIGURES)
    print("  ✓ dcs_isomorphism_table.png")

    # ------------------------------------------------------------------ #
    # Summary artefacts                                                   #
    # ------------------------------------------------------------------ #
    banner("Writing Summary Artefacts")
    summary = write_summary_json(liar_df, grounding_df, halting_df, depth_df, RESULTS)
    write_summary_latex(liar_df, grounding_df, halting_df, depth_df, RESULTS)
    print(f"  ✓ results/validation_summary.json")
    print(f"  ✓ results/empirical_summary_table.tex")

    elapsed = time.time() - t0
    print(f"\n✅  Light mode complete in {elapsed:.1f} s")
    print(f"   results/ → {len(list(RESULTS.glob('*')))} files")
    print(f"   figures/ → {len(list(FIGURES.glob('*.png')))} PNG files\n")


if __name__ == "__main__":
    main()
