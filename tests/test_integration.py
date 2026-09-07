"""Integration tests for the dicolor package."""

import pytest
import networkx as nx

from dicolor.digraph_analysis import dichromatic_number


class TestIntegration:
    """Integration tests combining multiple modules."""

    def test_dichromatic_and_dihomomorphism(self):
        """Test dichromatic number matches acyclic coloring constraint."""
        G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
        chi_d = dichromatic_number(G)
        # Cycle requires 2 colors
        assert chi_d == 2

    def test_dag_properties(self):
        """Test that DAGs have dichromatic number 1."""
        # Create a DAG
        G = nx.DiGraph([(0, 1), (0, 2), (1, 3), (2, 3)])
        assert nx.is_directed_acyclic_graph(G)
        assert dichromatic_number(G) == 1
