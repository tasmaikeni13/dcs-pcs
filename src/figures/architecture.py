"""
architecture.py — Figure: DCS bypass architecture and bypass lattice.

Produces two publication-quality figures:

1. ``dcs_bypass_architecture.png``
   Flow diagram showing how the three DCS assumptions (DC, ST, UD),
   their canonical bypass operators, and the PCS construction relate.

2. ``bypass_lattice_heatmap.png``
   A 3×2 heatmap of the complete bypass taxonomy (Theorem 4),
   colour-coded by which DCS assumption each bypass targets.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Figure 1 — DCS Bypass Architecture
# ---------------------------------------------------------------------------

def plot_dcs_architecture(figures_dir: Path) -> None:
    """Render the structural synthesis diagram (DC → bypass → PCS)."""
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=160)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Colour palette
    C_ASSUMPTION = {"DC": "#d0ebff", "ST": "#d3f9d8", "UD": "#ffe8cc"}
    C_BYPASS     = {"DC": "#a5d8ff", "ST": "#b2f2bb", "UD": "#ffd8a8"}
    C_PCS        = "#f3f0ff"
    C_EDGE       = "#343a40"

    def rounded_box(x, y, w, h, text, facecolor, fontsize=10, bold=False):
        fancy = mpatches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            facecolor=facecolor,
            edgecolor=C_EDGE,
            linewidth=1.4,
        )
        ax.add_patch(fancy)
        weight = "bold" if bold else "normal"
        ax.text(
            x + w / 2, y + h / 2, text,
            ha="center", va="center",
            fontsize=fontsize, fontweight=weight,
            wrap=True, multialignment="center",
        )

    # Row 1 – DCS assumptions
    assumptions = [("DC\nDiagonal Closure", 0.4, "DC"),
                   ("ST\nSemantic Totality", 4.4, "ST"),
                   ("UD\nUniversal Domain", 8.4, "UD")]
    for label, x, key in assumptions:
        rounded_box(x, 5.0, 3.2, 1.3, label, C_ASSUMPTION[key], fontsize=10, bold=True)

    # Row 2 – bypass operators
    bypasses = [
        ("$B_{DC}^1$ — Tarski\nHierarchical stratification\nblocks same-level self-application", 0.4, "DC"),
        ("$B_{ST}^1$ — Kripke\nThree-valued semantics\ngaps instead of contradictions", 4.4, "ST"),
        ("$B_{UD}^2$ — Meta-ascent\nRestricted ω-rule decides\nall true Π₁ sentences", 8.4, "UD"),
    ]
    for label, x, key in bypasses:
        rounded_box(x, 2.8, 3.2, 1.8, label, C_BYPASS[key], fontsize=8.5)

    # Row 3 – PCS synthesis
    rounded_box(2.8, 0.5, 6.4, 1.6,
                "PCS — Practically Complete System\n"
                "Consistency   ·   Grounded Completeness   ·   Partial Decidability\n"
                "Gödel-consistent (new diagonals → Undetermined)",
                C_PCS, fontsize=9, bold=True)

    # Arrows: assumption → bypass
    arrow_kw = dict(arrowstyle="-|>", color=C_EDGE, lw=1.5)
    for x_centre in [2.0, 6.0, 10.0]:
        ax.annotate("", xy=(x_centre, 4.6), xytext=(x_centre, 5.0), arrowprops=arrow_kw)

    # Arrows: bypass → PCS
    bypass_centres = [2.0, 6.0, 10.0]
    pcs_top_y = 2.1
    for xc in bypass_centres:
        ax.annotate("", xy=(6.0, pcs_top_y), xytext=(xc, 2.8), arrowprops=arrow_kw)

    ax.set_title(
        "DCS Bypass Architecture → PCS Synthesis",
        fontsize=14, fontweight="bold", pad=8,
    )
    fig.tight_layout()
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "dcs_bypass_architecture.png", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2 — Bypass Lattice Heatmap
# ---------------------------------------------------------------------------

def plot_bypass_lattice(figures_dir: Path) -> None:
    """
    Render the complete bypass taxonomy as an annotated 3×2 matrix.

    Rows = DCS assumptions; columns = bypass index (B^1, B^2).
    Cell colour encodes which assumption is targeted.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 5), dpi=160)

    row_labels = ["DC  (Diagonal Closure)", "ST  (Semantic Totality)", "UD  (Universal Domain)"]
    col_labels = ["Bypass $B^1$", "Bypass $B^2$"]

    cell_text = [
        [
            "$B_{DC}^1$ — Tarski stratification\n"
            "Type-level separation prevents\nsame-level self-application.",
            "$B_{DC}^2$ — Domain restriction\n"
            "Remove resources needed for\ndiagonal construction (e.g. Presburger).",
        ],
        [
            "$B_{ST}^1$ — Kripke fixed-point\n"
            "Allow truth-value gaps via\n{T, F, ⊥}; minimal fixed point.",
            "$B_{ST}^2$ — Paraconsistent semantics\n"
            "Allow truth-value gluts;\nblock explosion (Priest LP).",
        ],
        [
            "$B_{UD}^1$ — Bounded domain\n"
            "Restrict to finite-state / bounded-\nmodel (decidable halting).",
            "$B_{UD}^2$ — Meta-language ascent\n"
            "Restricted ω-rule; evaluate with\nstronger meta-principles.",
        ],
    ]

    pcs_mark = [(0, 0), (1, 0), (2, 1)]  # cells used by PCS: B_DC^1, B_ST^1, B_UD^2

    colours = [
        ["#a5d8ff", "#dde9f0"],
        ["#b2f2bb", "#ddf0e4"],
        ["#ffd8a8", "#f0e8d8"],
    ]

    n_rows, n_cols = 3, 2
    cell_w, cell_h = 5.0, 1.5

    for r in range(n_rows):
        for c in range(n_cols):
            x0 = c * cell_w
            y0 = (n_rows - 1 - r) * cell_h
            rect = plt.Rectangle(
                (x0, y0), cell_w, cell_h,
                facecolor=colours[r][c],
                edgecolor="#495057",
                linewidth=1.2,
            )
            ax.add_patch(rect)

            # PCS badge
            if (r, c) in pcs_mark:
                badge = plt.Rectangle(
                    (x0 + cell_w - 0.55, y0 + cell_h - 0.32), 0.48, 0.26,
                    facecolor="#7048e8", edgecolor="none",
                )
                ax.add_patch(badge)
                ax.text(
                    x0 + cell_w - 0.31, y0 + cell_h - 0.19,
                    "PCS", color="white", fontsize=6, ha="center", va="center",
                    fontweight="bold",
                )

            ax.text(
                x0 + cell_w / 2, y0 + cell_h / 2,
                cell_text[r][c],
                ha="center", va="center", fontsize=8,
                multialignment="center",
            )

    ax.set_xlim(0, n_cols * cell_w)
    ax.set_ylim(0, n_rows * cell_h)
    ax.set_xticks([i * cell_w + cell_w / 2 for i in range(n_cols)])
    ax.set_xticklabels(col_labels, fontsize=11, fontweight="bold")
    ax.set_yticks([(n_rows - 1 - r) * cell_h + cell_h / 2 for r in range(n_rows)])
    ax.set_yticklabels(row_labels, fontsize=10, fontweight="bold")
    ax.tick_params(length=0)
    ax.set_title(
        "Complete Bypass Taxonomy (Theorem 4)\n"
        "Purple badges mark bypasses used in PCS",
        fontsize=12, fontweight="bold", pad=10,
    )
    fig.tight_layout()
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "bypass_lattice_heatmap.png", bbox_inches="tight")
    plt.close(fig)
