"""Tests for the dihomomorphisms module."""

import pytest
import networkx as nx

from dicolor.dihomomorphisms import dihomomorphisms, dihomomorphism_graph


class TestDihomomorphisms:
    """Test suite for dihomomorphism generation."""

    def test_dihomomorphisms_empty_source(self):
        """Test dihomomorphisms with empty source graph."""
        D = nx.DiGraph()
        E = nx.DiGraph([(0, 1)])
        result = list(dihomomorphisms(D, E))
        assert len(result) == 1
        assert result[0] == {}

    def test_dihomomorphisms_empty_target(self):
        """Test dihomomorphisms with empty target graph."""
        D = nx.DiGraph([(0, 1)])
        E = nx.DiGraph()
        result = list(dihomomorphisms(D, E))
        assert len(result) == 0

    def test_dihomomorphisms_single_arc(self):
        """Test dihomomorphisms for single arc to single arc."""
        D = nx.DiGraph([(0, 1)])
        E = nx.DiGraph([(0, 1)])
        result = list(dihomomorphisms(D, E))
        # All dihomomorphisms: (0,1)->(0,0), (0,1)->(0,1), (0,1)->(1,1)
        assert len(result) == 3
        assert {0: 0, 1: 0} in result
        assert {0: 0, 1: 1} in result
        assert {0: 1, 1: 1} in result

    def test_dihomomorphisms_self_loop(self):
        """Test that self-loops prevent dihomomorphisms."""
        D = nx.DiGraph([(0, 0)])
        E = nx.DiGraph([(0, 0)])
        result = list(dihomomorphisms(D, E))
        assert len(result) == 0

    def test_dihomomorphisms_cycle_to_point(self):
        """Test that a directed cycle cannot map to a single point."""
        D = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
        E = nx.DiGraph()
        E.add_node(0)
        result = list(dihomomorphisms(D, E))
        assert len(result) == 0

    def test_dihomomorphisms_dag_to_point(self):
        """Test that a DAG can collapse to a single point."""
        D = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
        E = nx.DiGraph()
        E.add_node(0)
        result = list(dihomomorphisms(D, E))
        assert len(result) == 1
        assert result[0] == {0: 0, 1: 0, 2: 0}

    # def test_dihomomorphism_graph_single_arc(self):
    #     """Test dihomomorphism graph for single arc to digon."""
    #     D = nx.DiGraph([(0, 1)])
    #     E = nx.DiGraph([(0, 1), (1, 0)])  # digon
    #     G = dihomomorphism_graph(D, E)
    #     # With arc condition requiring crossing, not all pairs are adjacent
    #     assert G.number_of_nodes() == 3
    #     assert G.number_of_edges() >= 0

    def test_dihomomorphism_graph_empty_arcs(self):
        """Test dihomomorphism graph when source has no arcs."""
        D = nx.DiGraph()
        D.add_nodes_from([0, 1])
        E = nx.DiGraph([(0, 1), (1, 0)])
        G = dihomomorphism_graph(D, E)
        # With no arc constraints, result should be complete graph
        assert nx.is_isomorphic(G, nx.complete_graph(G.number_of_nodes()))
