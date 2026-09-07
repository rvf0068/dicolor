#!/usr/bin/env python3
"""Generate all dihomomorphisms between two directed graphs.

A *dihomomorphism* f: D -> E is a map on vertices such that:

  1. **Arc condition**: for every arc u->v in D, either f(u)->f(v) is an arc
     in E, or f(u) = f(v).
  2. **Acyclicity condition**: for every vertex w in E, the subgraph of D
     induced by the preimage f^{-1}(w) is acyclic (contains no directed
     cycle).

Usage
-----
    uv run python -m dicolor.dihomomorphisms <d6_source> <d6_target>

where ``d6_source`` and ``d6_target`` are digraph6 strings (as produced by
McKay's utilities or the :func:`parse_digraph6` function).  By default all
dihomomorphisms are printed; use ``--count`` to display only their number.

Example
-------
Single arc 0->1 as both source and target (digraph6 ``"&AO"``)::

    uv run python -m dicolor.dihomomorphisms "&AO" "&AO"
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Hashable, Iterator

import networkx as nx

from .digraph_utils import parse_digraph6


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------


def dihomomorphisms(
    D: nx.DiGraph,
    E: nx.DiGraph,
) -> Iterator[dict[Hashable, Hashable]]:
    """Generate all dihomomorphisms from *D* to *E*.

    A dihomomorphism f: D -> E is a vertex map satisfying two conditions:

    1. **Arc condition** — for every arc u->v in *D*, either f(u)->f(v) is an
       arc in *E*, or f(u) = f(v).
    2. **Acyclicity condition** — for every vertex w in *E*, the subgraph of
       *D* induced by the preimage f^{-1}(w) is acyclic.

    The function uses backtracking: vertices of *D* are assigned images in *E*
    one at a time (in the order returned by ``D.nodes()``).  At each step the
    arc condition is checked against all already-assigned neighbours, and the
    acyclicity condition is checked incrementally on the growing preimage.

    .. rubric:: Parameters

    D : networkx.DiGraph
        Source directed graph.
    E : networkx.DiGraph
        Target directed graph.

    .. rubric:: Yields

    dict
        Each yielded mapping is a ``dict`` from every vertex of *D* to a
        vertex of *E* that satisfies both conditions.

    .. rubric:: Notes

    * If *D* contains a self-loop, no dihomomorphism exists (a singleton
      preimage with a self-loop is already cyclic).
    * If *D* is empty (no vertices), the unique empty map is yielded.
    * If *E* is empty (no vertices) and *D* is non-empty, no map exists.

    .. rubric:: Examples

    >>> import networkx as nx
    >>> D = nx.DiGraph([(0, 1)])
    >>> E = nx.DiGraph([(0, 1)])
    >>> list(dihomomorphisms(D, E))
    [{0: 0, 1: 0}, {0: 0, 1: 1}, {0: 1, 1: 1}]

    A directed 3-cycle cannot be mapped to a single vertex (the full preimage
    would be cyclic):

    >>> C3 = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    >>> pt = nx.DiGraph()
    >>> pt.add_node(0)
    >>> list(dihomomorphisms(C3, pt))
    []

    A tournament on 3 vertices (a DAG) can be collapsed to a single point:

    >>> T3 = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
    >>> list(dihomomorphisms(T3, pt))
    [{0: 0, 1: 0, 2: 0}]
    """
    d_nodes = list(D.nodes())
    e_nodes = list(E.nodes())

    if not d_nodes:
        yield {}
        return
    if not e_nodes:
        return

    # preimages[w]: list of D-vertices currently assigned to w (mutable stack).
    preimages: dict[Hashable, list[Hashable]] = {w: [] for w in e_nodes}
    # Partial assignment built up during backtracking.
    assignment: dict[Hashable, Hashable] = {}

    def _backtrack(idx: int) -> Iterator[dict[Hashable, Hashable]]:
        if idx == len(d_nodes):
            yield dict(assignment)
            return

        u = d_nodes[idx]

        # A self-loop on u makes any preimage containing u cyclic.
        if D.has_edge(u, u):
            return

        # Neighbours in D whose images are already fixed.
        assigned_preds = [p for p in D.predecessors(u) if p in assignment]
        assigned_succs = [s for s in D.successors(u) if s in assignment]

        for w in e_nodes:
            # ------------------------------------------------------------------
            # Arc condition: check against already-assigned predecessors/succs.
            # ------------------------------------------------------------------
            valid = True

            # p -> u in D  =>  f(p) -> f(u) in E  or  f(p) = f(u)
            for p in assigned_preds:
                fp = assignment[p]
                if fp != w and not E.has_edge(fp, w):
                    valid = False
                    break
            if not valid:
                continue

            # u -> s in D  =>  f(u) -> f(s) in E  or  f(u) = f(s)
            for s in assigned_succs:
                fs = assignment[s]
                if w != fs and not E.has_edge(w, fs):
                    valid = False
                    break
            if not valid:
                continue

            # ------------------------------------------------------------------
            # Acyclicity condition: check that preimage(w) ∪ {u} is still a DAG.
            # ------------------------------------------------------------------
            preimages[w].append(u)
            acyclic = (
                len(preimages[w]) < 2
                or nx.is_directed_acyclic_graph(D.subgraph(preimages[w]))
            )

            if acyclic:
                assignment[u] = w
                yield from _backtrack(idx + 1)
                del assignment[u]

            preimages[w].pop()

    yield from _backtrack(0)


def dihomomorphism_graph(
    D: nx.DiGraph,
    E: nx.DiGraph,
) -> nx.Graph:
    """Return the undirected graph of dihomomorphisms from *D* to *E*.

    Vertices of the returned graph are all dihomomorphisms from *D* to *E*,
    each represented as a tuple of image values in the order of
    ``list(D.nodes())``.  Two dihomomorphisms f and h are adjacent when, for
    every arc x->y in *D*, both f(x)->h(y) and h(x)->f(y) are arcs in *E*.

    Each node carries the corresponding dihomomorphism as the node attribute
    ``"map"`` (a ``dict`` mapping D-vertices to E-vertices).

    .. rubric:: Parameters

    D : networkx.DiGraph
        Source directed graph.
    E : networkx.DiGraph
        Target directed graph.

    .. rubric:: Returns

    networkx.Graph
        Undirected graph whose vertices are dihomomorphisms from *D* to *E*
        and whose edges encode the adjacency relation described above.

    .. rubric:: Notes

    When *D* has no arcs the adjacency condition is vacuously satisfied, so
    the result is the complete graph on all dihomomorphisms.

    .. rubric:: Examples

    Source and target are both a single arc 0->1; the condition requires
    arrows *crossing* between two maps, which the single arc cannot support:

    >>> import networkx as nx
    >>> D = nx.DiGraph([(0, 1)])
    >>> E = nx.DiGraph([(0, 1), (1, 0)])  # digon
    >>> G = dihomomorphism_graph(D, E)
    >>> G.number_of_nodes(), G.number_of_edges()
    (4, 1)

    When *D* has no arcs the result is a complete graph:

    >>> D0 = nx.DiGraph()
    >>> D0.add_nodes_from([0, 1])
    >>> G0 = dihomomorphism_graph(D0, E)
    >>> G0.number_of_nodes() == 4 and nx.is_isomorphic(G0, nx.complete_graph(4))
    True
    """
    d_nodes = list(D.nodes())
    d_edges = list(D.edges())
    maps = list(dihomomorphisms(D, E))

    def _key(f: dict[Hashable, Hashable]) -> tuple[Hashable, ...]:
        return tuple(f[v] for v in d_nodes)

    G: nx.Graph = nx.Graph()
    for f in maps:
        G.add_node(_key(f), map=f)

    for i in range(len(maps)):
        for j in range(i + 1, len(maps)):
            f, h = maps[i], maps[j]
            if all(
                E.has_edge(f[x], h[y]) and E.has_edge(h[x], f[y])
                for x, y in d_edges
            ):
                G.add_edge(_key(f), _key(h))

    return G


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate all dihomomorphisms between two directed graphs given "
            "as digraph6 strings."
        )
    )
    parser.add_argument(
        "source",
        metavar="D",
        help="Digraph6 string for the source graph D.",
    )
    parser.add_argument(
        "target",
        metavar="E",
        help="Digraph6 string for the target graph E.",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Print only the number of dihomomorphisms.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Stop after printing N dihomomorphisms (ignored with --count or --graph).",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Print the dihomomorphism graph (vertices and edges).",
    )
    args = parser.parse_args()

    D = parse_digraph6(args.source)
    E = parse_digraph6(args.target)

    print(
        f"Source: {D.number_of_nodes()} vertices, {D.number_of_edges()} arcs  "
        f"(d6: {args.source})"
    )
    print(
        f"Target: {E.number_of_nodes()} vertices, {E.number_of_edges()} arcs  "
        f"(d6: {args.target})"
    )

    if args.graph:
        G = dihomomorphism_graph(D, E)
        print(f"Dihomomorphism graph: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
        for node in G.nodes():
            print(f"  {node}  map={G.nodes[node]['map']}")
        if G.number_of_edges():
            print("Edges:")
            for u, v in G.edges():
                print(f"  {u} -- {v}")
        return

    gen = dihomomorphisms(D, E)

    if args.count:
        total = sum(1 for _ in gen)
        print(f"Number of dihomomorphisms: {total}")
    else:
        shown = 0
        for f in gen:
            print(f)
            shown += 1
            if args.limit is not None and shown >= args.limit:
                remaining = sum(1 for _ in gen)
                print(
                    f"... (stopped after {shown}; "
                    f"{remaining} more dihomomorphisms exist)"
                )
                break
        else:
            print(f"Total: {shown} dihomomorphism(s).")


if __name__ == "__main__":
    sys.exit(main())
