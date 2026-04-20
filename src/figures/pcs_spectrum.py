"""
pcs_spectrum.py — Figure: PCS completeness spectrum.

Produces ``pcs_completeness_spectrum.png`` — a visual taxonomy of
sentence classes showing which are grounded (decided by PCS) and which
are ungrounded (correctly classified as Undetermined).

This figure supports the argument in §7.3 and Theorem 8:
  ``The grounded class contains all of classical first-order arithmetic
  that is true over ℕ at Π₁ level, all of Euclidean geometry, all
  scientific laws expressible as grounded first-order sentences, and
  all programs on physical hardware.''

Also produces ``dcs_isomorphism_table.png`` — a schematic table of
the DCS parameter mapping across LP, HP, and GIT.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Figure 1 — PCS Completeness Spectrum
# ---------------------------------------------------------------------------

def plot_pcs_completeness_spectrum(figures_dir: Path) -> None:
    """Render the sentence-class spectrum for PCS."""
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=160)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # ---- Outer rectangle: all formal sentences ----
    outer = mpatches.FancyBboxPatch(
        (0.2, 0.3), 12.6, 6.4,
        boxstyle="round,pad=0.15",
        facecolor="#f8f9fa", edgecolor="#495057", linewidth=2,
    )
    ax.add_patch(outer)
    ax.text(6.5, 6.5, "All well-formed sentences of the enriched language $\\mathcal{L}^*$",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#343a40")

    # ---- Grounded region ----
    grounded_patch = mpatches.FancyBboxPatch(
        (0.5, 0.6), 8.2, 5.5,
        boxstyle="round,pad=0.12",
        facecolor="#ebfbee", edgecolor="#2f9e44", linewidth=1.8,
    )
    ax.add_patch(grounded_patch)
    ax.text(4.6, 5.85, "Grounded  $\\mathcal{G}(\\mathcal{L}^*)$ — PCS decides these",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#2f9e44")

    # ---- Grounded sub-regions ----
    sub_regions = [
        (0.7, 3.5, 3.8, 2.2, "#d3f9d8", "#2f9e44",
         "True $\\Pi_1$ arithmetic\n(Peano's true sentences)\nDecided via ω-rule",
         "Goldbach partial sums,\nCon(PA), …"),

        (0.7, 1.1, 3.8, 2.2, "#d3f9d8", "#2f9e44",
         "First-order empirical laws\n(physics, geometry, …)\nGrounded in base facts",
         "F=ma, Euclid V, …"),

        (4.8, 3.5, 3.7, 2.2, "#d3f9d8", "#2f9e44",
         "Bounded-domain computation\n(finite-state programs)\nDecided by bounded decider",
         "All physical hardware"),

        (4.8, 1.1, 3.7, 2.2, "#d3f9d8", "#2f9e44",
         "Original Gödel sentence G\n(true Π₁ arithmetic)\nNow proven in PCS",
         "True but PA-unprovable"),
    ]

    for x, y, w, h, fc, ec, title, example in sub_regions:
        p = mpatches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08",
            facecolor=fc, edgecolor=ec, linewidth=1.1,
        )
        ax.add_patch(p)
        ax.text(x + w/2, y + h*0.65, title,
                ha="center", va="center", fontsize=8, multialignment="center")
        ax.text(x + w/2, y + h*0.2, f"e.g. {example}",
                ha="center", va="center", fontsize=7, color="#555", style="italic")

    # ---- Ungrounded region ----
    ungrounded_patch = mpatches.FancyBboxPatch(
        (9.0, 0.6), 3.5, 5.5,
        boxstyle="round,pad=0.12",
        facecolor="#fff5f5", edgecolor="#c92a2a", linewidth=1.8,
    )
    ax.add_patch(ungrounded_patch)
    ax.text(10.75, 5.85, "Ungrounded\n→ Undetermined",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#c92a2a")

    ug_items = [
        (9.2, 3.8, 3.1, 1.9, "Liar sentence λ\n$\\lambda \\leftrightarrow \\neg\\text{Tr}(\\ulcorner\\lambda\\urcorner)$\n→ Undetermined"),
        (9.2, 1.7, 3.1, 1.9, "PCS-native diagonal $G^*$\n(self-ref. over truth layer)\n→ Undetermined"),
        (9.2, 0.75, 3.1, 0.85, "All Kripke-ungrounded cycles"),
    ]
    for x, y, w, h, text in ug_items:
        p = mpatches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.07",
            facecolor="#ffe3e3", edgecolor="#fa5252", linewidth=0.9,
        )
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text,
                ha="center", va="center", fontsize=7.8, multialignment="center")

    ax.set_title(
        "PCS Completeness Spectrum — What PCS Decides vs. Quarantines\n"
        "(Theorem 8: The Practically Complete System Theorem)",
        fontsize=12, fontweight="bold", pad=4,
    )
    fig.tight_layout()
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "pcs_completeness_spectrum.png", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2 — DCS Isomorphism Table
# ---------------------------------------------------------------------------

def plot_dcs_isomorphism_table(figures_dir: Path) -> None:
    """
    Render the DCS parameter mapping for LP, HP, and GIT as a visual table.
    """
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(13, 5.5), dpi=160)
    ax.axis("off")

    col_labels = ["Parameter", "$\\mathcal{S}_{LP}$ (Liar)", "$\\mathcal{S}_{HP}$ (Halting)", "$\\mathcal{S}_{GIT}$ (Gödel)"]
    rows_data = [
        ["System objects",        "Natural-language sentences",       "Turing machine programs",          "PA sentences"],
        ["Self-predicate $P$",    "Truth predicate $\\text{Tr}(x)$",  "Halts predicate $H(x,x)$",         "Provability $\\text{Prov}(x)$"],
        ["Diagonal sentence",     "Liar $\\lambda$: true iff false",  "Self-halting diagonal $D$",         "Gödel sentence $G$"],
        ["DC",                    "Quote operator $\\ulcorner\\cdot\\urcorner$",  "Quine / self-application",   "Gödel numbering + diag. lemma"],
        ["ST",                    "Bivalent natural language",        "Total oracle assumed",              "Standard model valuation"],
        ["UD",                    "All sentences in domain",          "All programs in domain",            "All arithmetic sentences"],
        ["DCS result",            "\\textbf{Paradox}",                "\\textbf{Undecidability}",           "\\textbf{Incompleteness}"],
        ["Negation-complete?",    "Yes → paradox (Thm 1)",           "Yes → undecidable (Thm 1)",         "No → unprovable (Remark 2.3)"],
    ]

    row_colours_bg = ["#f8f9fa", "#f1f3f5"] * 5
    col_widths = [0.22, 0.24, 0.27, 0.27]

    table = ax.table(
        cellText=rows_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.2)

    # Style header
    for c in range(4):
        table[0, c].set_facecolor("#364fc7")
        table[0, c].set_text_props(color="white", fontweight="bold")

    # Style last two rows for emphasis
    for c in range(4):
        table[len(rows_data) - 1, c].set_facecolor("#fff9db")
        table[len(rows_data), c].set_facecolor("#fff9db")

    # Alternating rows
    for r in range(1, len(rows_data) + 1):
        bg = "#f8f9fa" if r % 2 == 0 else "#ffffff"
        for c in range(4):
            if table[r, c].get_facecolor() == (1, 1, 1, 1) or True:
                pass  # let special rows keep their colour

    ax.set_title(
        "DCS Isomorphism: Parameter Mapping Across LP, HP, and GIT\n"
        "(Theorem 2 — Semantic cases; GIT positioned as limiting case)",
        fontsize=11, fontweight="bold", pad=12,
    )
    fig.tight_layout()
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / "dcs_isomorphism_table.png", bbox_inches="tight")
    plt.close(fig)
