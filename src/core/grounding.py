"""
grounding.py — Grounding analysis and random theory generation.

A sentence φ is *grounded* in a formal system if its truth or falsity
can be established by a well-founded chain that bottoms out in
non-self-referential base facts.  Ungrounded sentences (Liar, mutual
cycles, etc.) receive the value Undetermined in PCS.

This module provides:
  - ``random_theory``: sample a random dependency graph.
  - ``grounding_depth``: compute grounding depth for each node.
  - Analysis helpers used by the Kripke sweep experiment.

References
----------
Kripke, S. (1975). Outline of a theory of truth. *Journal of Philosophy*, 72(19), 690–716.
"""

from __future__ import annotations

import numpy as np

from .kripke import Node
from .semantics import TruthValue


# ---------------------------------------------------------------------------
# Random theory generator
# ---------------------------------------------------------------------------

def random_theory(
    num_nodes: int,
    base_prob: float,
    rng: np.random.Generator,
) -> list[Node]:
    """
    Sample a random dependency graph.

    Each node is independently either a base node (with probability
    *base_prob*) or a neg-node pointing to a uniformly random other node.

    Parameters
    ----------
    num_nodes :
        Total number of sentences in the theory.
    base_prob :
        Probability that each sentence is a grounded base fact.
    rng :
        NumPy random generator.

    Returns
    -------
    list[Node]
        The sampled dependency graph.
    """
    nodes: list[Node] = []
    for _ in range(num_nodes):
        if rng.random() < base_prob:
            base_val: TruthValue = "T" if rng.random() < 0.5 else "F"
            nodes.append(Node("base", base_value=base_val))
        else:
            dep = int(rng.integers(0, num_nodes))
            nodes.append(Node("neg", dep=dep))
    return nodes


# ---------------------------------------------------------------------------
# Structural grounding depth
# ---------------------------------------------------------------------------

def grounding_depth(nodes: list[Node]) -> list[int | None]:
    """
    Compute the *structural* grounding depth for each node.

    - Base nodes have depth 0.
    - A neg-node has depth = depth(dep) + 1 if dep is grounded; else None.
    - Nodes in cycles have depth None (ungrounded).

    This is a static structural measure; it agrees with the Kripke
    fixed-point result for simple chains but differs for complex cycles
    where the dynamic fixed point must be used.

    Returns
    -------
    list[int | None]
        Grounding depth per node (None = ungrounded).
    """
    depths: list[int | None] = [None] * len(nodes)

    # Seed base nodes.
    for i, node in enumerate(nodes):
        if node.kind == "base":
            depths[i] = 0

    # Propagate in passes (up to n passes suffices for acyclic chains).
    changed = True
    while changed:
        changed = False
        for i, node in enumerate(nodes):
            if depths[i] is not None:
                continue
            if node.kind == "neg" and node.dep is not None:
                dep_depth = depths[node.dep]
                if dep_depth is not None:
                    depths[i] = dep_depth + 1
                    changed = True

    return depths


# ---------------------------------------------------------------------------
# Grounding statistics
# ---------------------------------------------------------------------------

def grounding_stats(nodes: list[Node]) -> dict[str, float | int]:
    """
    Return a summary of the grounding structure of a theory.
    """
    depths = grounding_depth(nodes)
    grounded = [d for d in depths if d is not None]
    ungrounded_count = depths.count(None)
    return {
        "total": len(nodes),
        "grounded_count": len(grounded),
        "ungrounded_count": ungrounded_count,
        "grounded_fraction": len(grounded) / max(len(nodes), 1),
        "max_depth": max(grounded, default=0),
        "mean_depth": float(np.mean(grounded)) if grounded else 0.0,
    }
