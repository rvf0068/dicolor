"""Utilities for parsing and generating directed graphs in digraph6 format.

This module provides functions to parse digraph6 strings (Brendan McKay's
compact ASCII encoding for directed graphs) and access digraph datasets
from McKay's database of non-isomorphic directed graphs on 1-6 vertices.

References:
    Digraph6 format: https://users.cecs.anu.edu.au/~bdm/data/digraphs.html
"""

import gzip
from collections.abc import Iterator
from importlib import resources

import networkx as nx

# Package name for accessing digraph data files
DATA_PACKAGE = "dicolor.data"

# Non-isomorphic directed graphs from Brendan McKay's database
_dict_digraphs = {
    1: "dig1.d6",
    2: "dig2.d6",
    3: "dig3.d6",
    4: "dig4.d6",
    5: "dig5.d6",
    6: "dig6.d6.gz",
}


def _get_data_file_path(filename: str) -> resources.abc.Traversable:
    """Helper function to resolve the path to a digraph data file.

    Args:
        filename: Name of the data file (e.g., 'dig3.d6').

    Returns:
        A Traversable object representing the file path.
    """
    return resources.files(DATA_PACKAGE).joinpath(filename)


def parse_digraph6(d6_str: str) -> nx.DiGraph:
    """Parse a digraph6 string into a NetworkX DiGraph.

    Digraph6 is a compact ASCII encoding for directed graphs defined by
    Brendan McKay. Each string encodes the number of vertices followed
    by the adjacency matrix in row-major order using 6-bit ASCII characters.

    Args:
        d6_str: A digraph6 string, optionally prefixed with ``>>digraph6<<``.
            Valid strings must start with ``&`` (after the optional prefix).

    Returns:
        The directed graph encoded by the string.

    Raises:
        ValueError: If the string does not start with ``&`` (after stripping
            the optional ``>>digraph6<<`` header), or if the string is too
            short to represent all edges.

    Examples:
        >>> g = parse_digraph6("&A?")
        >>> g.number_of_nodes(), g.number_of_edges()
        (2, 0)
        >>> g = parse_digraph6("&AO")
        >>> list(g.edges())
        [(0, 1)]
    """
    d6_str = d6_str.strip()
    if d6_str.startswith(">>digraph6<<"):
        d6_str = d6_str[12:]

    if not d6_str.startswith("&"):
        raise ValueError("Valid digraph6 strings must start with '&'")
    d6_str = d6_str[1:]

    data = [ord(c) - 63 for c in d6_str]

    if data[0] <= 62:
        n = data[0]
        data = data[1:]
    elif data[1] <= 62:
        n = (data[1] << 12) | (data[2] << 6) | data[3]
        data = data[4:]
    else:
        n = (
            (data[2] << 30)
            | (data[3] << 24)
            | (data[4] << 18)
            | (data[5] << 12)
            | (data[6] << 6)
            | data[7]
        )
        data = data[8:]

    bits = [int(b) for val in data for b in format(val, "06b")]

    if len(bits) < n * n:
        raise ValueError("String is too short to represent all edges")

    g: nx.DiGraph = nx.DiGraph()
    g.add_nodes_from(range(n))

    idx = 0
    for i in range(n):
        for j in range(n):
            if bits[idx] == 1:
                g.add_edge(i, j)
            idx += 1

    return g


def digraph_generator(n: int) -> Iterator[nx.DiGraph]:
    """Yield all non-isomorphic directed graphs on *n* vertices.

    Data obtained from Brendan McKay's digraph data page:
    https://users.cecs.anu.edu.au/~bdm/data/digraphs.html

    Args:
        n: Number of vertices. Available values: 1 to 6.

    Yields:
        A directed graph with ``n`` vertices.

    Raises:
        ValueError: If ``n`` is not in the available range (1--6).

    Examples:
        >>> gen = digraph_generator(1)
        >>> g = next(gen)
        >>> g.number_of_nodes(), g.number_of_edges()
        (1, 0)
        >>> sum(1 for _ in digraph_generator(3))
        7
    """
    if n not in _dict_digraphs:
        msg = f"Digraph data for n={n} is not available."
        raise ValueError(msg)

    filename = _dict_digraphs[n]
    file_path = _get_data_file_path(filename)

    if filename.endswith(".gz"):
        with file_path.open("rb") as raw_file:
            with gzip.open(raw_file, "rt", encoding="utf-8") as graph_file:
                for line in graph_file:
                    line = line.strip()
                    if line:
                        yield parse_digraph6(line)
    else:
        with file_path.open("r", encoding="utf-8") as graph_file:
            for line in graph_file:
                line = line.strip()
                if line:
                    yield parse_digraph6(line)


def list_digraphs(n: int) -> list[nx.DiGraph]:
    """List all non-isomorphic directed graphs on *n* vertices.

    Data obtained from Brendan McKay's digraph data page:
    https://users.cecs.anu.edu.au/~bdm/data/digraphs.html

    Args:
        n: Number of vertices. Available values: 1 to 6.

    Returns:
        All non-isomorphic directed graphs on ``n`` vertices.

    Examples:
        >>> len(list_digraphs(2))
        3
        >>> len(list_digraphs(4))
        218
    """
    return list(digraph_generator(n))
