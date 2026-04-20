"""
kripke.py — Kripke-style fixed-point grounding engine.

Implements the minimal fixed-point construction that underlies the
Bypass B_ST^1 (Semantic Totality bypass) in the PCS architecture.
Nodes are truth-bearers in a dependency graph; base nodes carry an
explicit truth value and negation nodes inherit their value via ¬.

The engine iterates in the style of Kripke's strong Kleene construction:
  1. Every node starts Undetermined (U).
  2. Base nodes are immediately assigned their given value.
  3. In each round, any neg-node whose dependency has stabilised
     is updated; the rest remain U.
  4. Iteration continues until no change occurs (fixed point reached).

Sentences that remain U at the fixed point are *ungrounded* — they
either participate in a self-referential cycle (like the Liar) or
depend on an ungrounded ancestor.

References
----------
Kripke, S. (1975). Outline of a theory of truth. *Journal of Philosophy*, 72(19), 690–716.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .semantics import TruthValue, tri_not


# ---------------------------------------------------------------------------
# Node definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Node:
    """
    A node in a truth-dependency graph.

    Parameters
    ----------
    kind : str
        Either ``"base"`` (carries an intrinsic truth value) or
        ``"neg"`` (its truth value is the negation of its dependency's value).
    base_value : TruthValue or None
        For ``kind="base"`` nodes, the intrinsic value ("T" or "F").
        Ignored for neg-nodes.
    dep : int or None
        For ``kind="neg"`` nodes, the index of the node whose value is negated.
        Ignored for base-nodes.
    """

    kind: str                           # "base" | "neg"
    base_value: Optional[TruthValue] = None
    dep: Optional[int] = None

    def __post_init__(self) -> None:
        if self.kind not in ("base", "neg"):
            raise ValueError(f"Node kind must be 'base' or 'neg', got '{self.kind}'.")
        if self.kind == "neg" and self.dep is None:
            raise ValueError("Neg-nodes must specify a dependency index.")


# ---------------------------------------------------------------------------
# Fixed-point engine
# ---------------------------------------------------------------------------

def kripke_fixed_point(
    nodes: list[Node],
    max_iter: int = 10_000,
) -> tuple[list[TruthValue], int, float]:
    """
    Run the Kripke minimal fixed-point construction on a node list.

    Parameters
    ----------
    nodes :
        The dependency graph described as an ordered list of :class:`Node`.
    max_iter :
        Hard iteration ceiling (avoids infinite loops during experiments).

    Returns
    -------
    values : list[TruthValue]
        Final truth assignment at the fixed point.
    iterations : int
        Number of rounds executed before convergence (or hitting *max_iter*).
    grounded_ratio : float
        Fraction of nodes that received a definite (T or F) value.
    """
    # Step 1 – initialise everything to U.
    values: list[TruthValue] = ["U"] * len(nodes)

    # Step 2 – immediately fix base nodes.
    for i, node in enumerate(nodes):
        if node.kind == "base" and node.base_value is not None:
            values[i] = node.base_value

    # Step 3 – iterate until fixed point.
    iterations = 0
    while iterations < max_iter:
        iterations += 1
        changed = False
        new_values = values.copy()

        for i, node in enumerate(nodes):
            if node.kind == "neg" and node.dep is not None:
                dep_val = values[node.dep]
                # Only propagate if the dependency is already grounded.
                candidate: TruthValue = tri_not(dep_val) if dep_val != "U" else "U"
                if candidate != new_values[i]:
                    new_values[i] = candidate
                    changed = True

        values = new_values
        if not changed:
            break

    n = max(len(nodes), 1)
    grounded_ratio = sum(v != "U" for v in values) / n
    return values, iterations, grounded_ratio


# ---------------------------------------------------------------------------
# Utility constructors
# ---------------------------------------------------------------------------

def liar_node() -> list[Node]:
    """Return a single-node graph whose only node is the Liar sentence (self-negating)."""
    return [Node("neg", dep=0)]


def linear_chain(depth: int, base_value: TruthValue = "T") -> list[Node]:
    """
    Build a linear chain:  base → neg(base) → neg(neg(base)) → … (depth levels).

    The grounding depth of the last node equals *depth*.
    """
    chain: list[Node] = [Node("base", base_value=base_value)]
    for i in range(depth):
        chain.append(Node("neg", dep=i))
    return chain


def mutual_cycle(size: int = 2) -> list[Node]:
    """
    Build a mutual-negation cycle of *size* nodes:
        node[0] negates node[size-1], node[i] negates node[i-1].
    All nodes remain U at the fixed point.
    """
    nodes: list[Node] = []
    for i in range(size):
        nodes.append(Node("neg", dep=(i - 1) % size))
    return nodes


def mixed_theory() -> list[Node]:
    """
    Reference theory used in the deterministic grounding experiment:
        0: base T
        1: neg(0) → F
        2: neg(1) → T
        3: neg(3) → U  (pure Liar)
        4: neg(5)  ⎫ mutual cycle → both U
        5: neg(4)  ⎭
    """
    return [
        Node("base", base_value="T"),   # 0
        Node("neg", dep=0),              # 1
        Node("neg", dep=1),              # 2
        Node("neg", dep=3),              # 3  ← self-referential
        Node("neg", dep=5),              # 4  ⎫ mutual cycle
        Node("neg", dep=4),              # 5  ⎭
    ]
