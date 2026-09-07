"""Tests for the digraph_analysis module."""

import pytest
import networkx as nx

from dicolor.digraph_analysis import dichromatic_number, _acyclic_coloring


class TestDichromaticNumber:
    """Test suite for dichromatic number computation."""

    def test_dichromatic_empty_graph(self):
        """Test dichromatic number of empty graph."""
        G = nx.DiGraph()
        assert dichromatic_number(G) == 0

    def test_dichromatic_single_vertex(self):
        """Test dichromatic number of single vertex."""
        G = nx.DiGraph()
        G.add_node(0)
        assert dichromatic_number(G) == 1

    def test_dichromatic_path(self):
        """Test dichromatic number of directed path."""
        G = nx.DiGraph([(0, 1), (1, 2), (2, 3)])
        assert dichromatic_number(G) == 1

    def test_dichromatic_cycle(self):
        """Test dichromatic number of directed cycle."""
        G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
        assert dichromatic_number(G) == 2

    def test_dichromatic_digon(self):
        """Test dichromatic number of digon (2-cycle)."""
        G = nx.DiGraph([(0, 1), (1, 0)])
        # With allow_digons=True, digon needs only 1 color
        assert dichromatic_number(G, allow_digons=True) == 1
        # With allow_digons=False, digon needs 2 colors
        assert dichromatic_number(G, allow_digons=False) == 2

    def test_dichromatic_tournament(self):
        """Test dichromatic number of tournament."""
        G = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
        assert dichromatic_number(G) == 1

    def test_acyclic_coloring_single_vertex(self):
        """Test acyclic coloring of single vertex."""
        G = nx.DiGraph()
        G.add_node(0)
        colorings = list(_acyclic_coloring(G, 1))
        assert len(colorings) == 1
        assert colorings[0] == {0: 1}

    def test_acyclic_coloring_path(self):
        """Test acyclic coloring of directed path."""
        G = nx.DiGraph([(0, 1), (1, 2)])
        colorings = list(_acyclic_coloring(G, 1))
        assert len(colorings) == 1
        for coloring in colorings:
            assert all(v in coloring for v in [0, 1, 2])
