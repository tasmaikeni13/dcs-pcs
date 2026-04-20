"""
dcs_pcs.experiments — Individual experiment runners.

Each module corresponds to one class of empirical test from §8 of the paper.

Submodules
----------
liar_fixed_points   Experiment 1 – bivalent / trivalent Liar fixed-point.
kripke_sweep        Experiment 2 – Kripke grounding sweep over random theories.
halting_validation  Experiment 3 – Bounded halting decider validation.
depth_termination   Experiment 4 – Finite-depth termination scaling.
"""

from .liar_fixed_points import run_liar_experiment, run_deterministic_grounding, summarise_liar
from .kripke_sweep import run_kripke_sweep
from .halting_validation import run_halting_validation
from .depth_termination import run_depth_termination

__all__ = [
    "run_liar_experiment",
    "run_deterministic_grounding",
    "summarise_liar",
    "run_kripke_sweep",
    "run_halting_validation",
    "run_depth_termination",
]
