"""
semantics.py — Truth-value algebras for DCS/PCS experiments.

Defines the two-valued (bivalent) and three-valued (Kleene / Kripke)
semantics used throughout the empirical validation suite.

References
----------
Kripke, S. (1975). Outline of a theory of truth. *Journal of Philosophy*, 72(19), 690–716.
Priest, G. (1979). The logic of paradox. *Journal of Philosophical Logic*, 8(1), 219–241.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal


# ---------------------------------------------------------------------------
# Truth-value type
# ---------------------------------------------------------------------------

TruthValue = Literal["T", "F", "U"]
"""A sentence may be True (T), False (F), or Undetermined (U)."""

BIVALENT_DOMAIN: tuple[TruthValue, ...] = ("T", "F")
TRIVALENT_DOMAIN: tuple[TruthValue, ...] = ("T", "F", "U")


# ---------------------------------------------------------------------------
# Negation tables
# ---------------------------------------------------------------------------

#: Classical (bivalent) strong negation: ¬T = F, ¬F = T.
BIVALENT_NOT: dict[TruthValue, TruthValue] = {"T": "F", "F": "T"}

#: Kleene strong three-valued negation: ¬T = F, ¬F = T, ¬U = U.
#: This is the negation used in Kripke's minimal fixed-point construction.
TRIVALENT_NOT: dict[TruthValue, TruthValue] = {"T": "F", "F": "T", "U": "U"}

#: Priest paraconsistent negation (same table; explosion is blocked externally).
PARACONSISTENT_NOT: dict[TruthValue, TruthValue] = {"T": "F", "F": "T", "U": "U"}


def tri_not(value: TruthValue) -> TruthValue:
    """Apply Kleene strong three-valued negation."""
    return TRIVALENT_NOT[value]


def biv_not(value: TruthValue) -> TruthValue:
    """Apply classical bivalent negation.  Raises for 'U'."""
    if value not in BIVALENT_NOT:
        raise ValueError(f"Bivalent negation undefined for value '{value}'.")
    return BIVALENT_NOT[value]


# ---------------------------------------------------------------------------
# Fixed-point checks
# ---------------------------------------------------------------------------

def is_liar_fixed_point(value: TruthValue, semantics: Literal["bivalent", "trivalent"]) -> bool:
    """
    Return True iff *value* satisfies the equation  G ↔ ¬G
    in the given semantics.

    In bivalent semantics (T/F only) this has no solution — the DCS
    instability is witnessed directly.  In Kripke's three-valued semantics
    the Undetermined value U is a stable fixed point: ¬U = U, so U = ¬U.
    """
    if semantics == "bivalent":
        if value not in BIVALENT_DOMAIN:
            return False
        return value == biv_not(value)          # impossible for T or F
    else:  # trivalent
        return value == tri_not(value)           # True only for U


def liar_fixed_point_table(semantics: Literal["bivalent", "trivalent"]) -> list[dict]:
    """Return a list of rows describing all candidate values and whether they satisfy G ↔ ¬G."""
    domain = BIVALENT_DOMAIN if semantics == "bivalent" else TRIVALENT_DOMAIN
    return [
        {
            "semantics": semantics,
            "candidate_value": v,
            "satisfies_G_iff_not_G": is_liar_fixed_point(v, semantics),
        }
        for v in domain
    ]


# ---------------------------------------------------------------------------
# Conjunction / disjunction (for richer PCS experiments)
# ---------------------------------------------------------------------------

_AND: dict[tuple[TruthValue, TruthValue], TruthValue] = {
    ("T", "T"): "T", ("T", "F"): "F", ("T", "U"): "U",
    ("F", "T"): "F", ("F", "F"): "F", ("F", "U"): "F",
    ("U", "T"): "U", ("U", "F"): "F", ("U", "U"): "U",
}

_OR: dict[tuple[TruthValue, TruthValue], TruthValue] = {
    ("T", "T"): "T", ("T", "F"): "T", ("T", "U"): "T",
    ("F", "T"): "T", ("F", "F"): "F", ("F", "U"): "U",
    ("U", "T"): "T", ("U", "F"): "U", ("U", "U"): "U",
}


def tri_and(a: TruthValue, b: TruthValue) -> TruthValue:
    """Kleene strong three-valued conjunction."""
    return _AND[(a, b)]


def tri_or(a: TruthValue, b: TruthValue) -> TruthValue:
    """Kleene strong three-valued disjunction."""
    return _OR[(a, b)]
