"""
dcs_pcs.core — Core engines for DCS/PCS empirical validation.

Submodules
----------
semantics   Truth-value algebras (bivalent, Kleene trivalent).
kripke      Kripke minimal fixed-point construction and node types.
halting     Bounded halting decider for finite-state machines.
grounding   Grounding depth analysis and random theory generation.
"""

from .semantics import TruthValue, tri_not, biv_not, liar_fixed_point_table
from .kripke import Node, kripke_fixed_point, liar_node, linear_chain, mutual_cycle, mixed_theory
from .halting import generate_random_machine, bounded_decider, bounded_simulation, run_halting_experiment
from .grounding import random_theory, grounding_depth, grounding_stats

__all__ = [
    "TruthValue", "tri_not", "biv_not", "liar_fixed_point_table",
    "Node", "kripke_fixed_point", "liar_node", "linear_chain", "mutual_cycle", "mixed_theory",
    "generate_random_machine", "bounded_decider", "bounded_simulation", "run_halting_experiment",
    "random_theory", "grounding_depth", "grounding_stats",
]
