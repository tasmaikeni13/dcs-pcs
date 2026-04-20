"""
liar_fixed_points.py — Experiment 1: Liar fixed-point analysis.

Validates the core DCS Instability theorem (Theorem 1) by exhaustively
checking whether the equation  G ↔ ¬G  has a satisfying assignment in
bivalent vs. three-valued semantics.

Predictions
-----------
- Bivalent: 0 satisfying assignments.  G=T → ¬G=F → contradiction;
  G=F → ¬G=T → contradiction.  DCS instability is exhibited directly.
- Trivalent (Kripke): exactly 1 satisfying assignment (G=U).
  ¬U = U, so U = ¬U holds.  Bypass B_ST^1 is operative.

Also runs the deterministic mixed-theory grounding example that
verifies grounded nodes propagate correctly while cyclic nodes stay U.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ..core.semantics import liar_fixed_point_table, BIVALENT_DOMAIN, TRIVALENT_DOMAIN
from ..core.kripke import kripke_fixed_point, mixed_theory


def run_liar_experiment(results_dir: Path) -> pd.DataFrame:
    """
    Enumerate all candidate values for G ↔ ¬G in both semantics.

    Returns a DataFrame with columns:
        semantics, candidate_value, satisfies_G_iff_not_G
    """
    rows: list[dict] = []
    rows.extend(liar_fixed_point_table("bivalent"))
    rows.extend(liar_fixed_point_table("trivalent"))

    df = pd.DataFrame(rows)
    results_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(results_dir / "liar_fixed_points.csv", index=False)
    return df


def run_deterministic_grounding(results_dir: Path) -> pd.DataFrame:
    """
    Run the deterministic mixed-theory grounding example.

    Theory layout:
        0: base T
        1: neg(0) → F
        2: neg(1) → T
        3: neg(3) → U  [Liar]
        4: neg(5)  ⎫ mutual cycle → both U
        5: neg(4)  ⎭
    """
    nodes = mixed_theory()
    values, iterations, grounded_ratio = kripke_fixed_point(nodes)

    df = pd.DataFrame(
        {
            "sentence_id": list(range(len(nodes))),
            "kind": [n.kind for n in nodes],
            "dependency": [n.dep if n.dep is not None else -1 for n in nodes],
            "fixed_point_value": values,
            "grounded": [v != "U" for v in values],
        }
    )
    results_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(results_dir / "deterministic_grounding_example.csv", index=False)

    summary = {
        "iterations": iterations,
        "grounded_ratio": grounded_ratio,
        "grounded_count": int(sum(v != "U" for v in values)),
        "total": len(values),
    }
    (results_dir / "deterministic_grounding_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    return df


def summarise_liar(df: pd.DataFrame) -> dict[str, int]:
    """Return a dict of satisfying-assignment counts per semantics."""
    return {
        "bivalent_satisfying": int(
            df[(df["semantics"] == "bivalent") & (df["satisfies_G_iff_not_G"])].shape[0]
        ),
        "trivalent_satisfying": int(
            df[(df["semantics"] == "trivalent") & (df["satisfies_G_iff_not_G"])].shape[0]
        ),
    }
