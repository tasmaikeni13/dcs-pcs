"""
dcs_pcs.figures — Publication-quality figure generators.

Each module produces one or two PNG files in the ``figures/`` directory.

Submodules
----------
architecture        dcs_bypass_architecture.png + bypass_lattice_heatmap.png
grounding_curve     grounding_vs_base_probability.png
halting_heatmap     bounded_halting_empirics.png
depth_scaling       finite_depth_termination.png
pcs_spectrum        pcs_completeness_spectrum.png + dcs_isomorphism_table.png
"""

from .architecture import plot_dcs_architecture, plot_bypass_lattice
from .grounding_curve import plot_grounding_curve
from .halting_heatmap import plot_bounded_halting
from .depth_scaling import plot_depth_scaling
from .pcs_spectrum import plot_pcs_completeness_spectrum, plot_dcs_isomorphism_table

__all__ = [
    "plot_dcs_architecture",
    "plot_bypass_lattice",
    "plot_grounding_curve",
    "plot_bounded_halting",
    "plot_depth_scaling",
    "plot_pcs_completeness_spectrum",
    "plot_dcs_isomorphism_table",
]
