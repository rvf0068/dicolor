"""Dicolor: Directed graph analysis and dihomomorphism computations.

This package provides tools for analyzing properties of directed graphs,
including dichromatic number computation and dihomomorphism generation.

Main modules:
- digraph_analysis: Compute dichromatic number and directed neighborhood complexes
- dihomomorphisms: Generate and analyze dihomomorphisms between directed graphs
- dihom_cycle_analysis: Analyze dihomomorphism graphs for cycle structures
"""

from .dihomomorphisms import dihomomorphisms, dihomomorphism_graph
from .digraph_analysis import dichromatic_number
from .digraph_utils import parse_digraph6, digraph_generator, list_digraphs

__version__ = "0.1.0"
__all__ = [
    "dihomomorphisms",
    "dihomomorphism_graph", 
    "dichromatic_number",
    "parse_digraph6",
    "digraph_generator",
    "list_digraphs",
]
