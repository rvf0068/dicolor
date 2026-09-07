#!/usr/bin/env python3
"""Compute dichromatic number and homotopy type of the directed neighborhood
complex for each non-isomorphic digraph of a given order.

Usage
-----
    uv run python -m dicolor.digraph_analysis <order> [--format {org,csv}]

where *order* is an integer between 1 and 6.  Results are written to
``digraph_analysis_<order>.org`` (default) or ``.csv`` in the current
directory.

The digraphs are indexed starting from 0, matching the position in
the digraph6 data files.

Data source
-----------
Digraph data obtained from Brendan McKay's page:
https://users.cecs.anu.edu.au/~bdm/data/digraphs.html
"""

from __future__ import annotations

import argparse
import csv
import gzip
import sys
from importlib import resources

import networkx as nx

from pycombtop import directed_neighborhood_complex
from pycombtop.homotopy_type import homotopy_type_sc_with_verdict

from .digraph_utils import parse_digraph6, _dict_digraphs, _get_data_file_path

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _iter_digraph6_pairs(n: int):
    """Yield ``(d6_string, DiGraph)`` pairs for all digraphs of order *n*."""
    if n not in _dict_digraphs:
        raise ValueError(
            f"No data for order {n}. Available orders: {sorted(_dict_digraphs)}"
        )
    filename = _dict_digraphs[n]
    file_path = _get_data_file_path(filename)

    if filename.endswith(".gz"):
        with file_path.open("rb") as raw_file:
            with gzip.open(raw_file, "rt", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        yield line, parse_digraph6(line)
    else:
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line, parse_digraph6(line)


# ---------------------------------------------------------------------------
# Acyclic coloring
# ---------------------------------------------------------------------------


def _get_safe_colors(
    G: nx.DiGraph,
    nodes: list,
    node_to_idx: dict,
    colors_list: list[int],
    k: int,
    allow_digons: bool = True,
) -> list[int]:
    """Return all valid colors for the next uncolored node.

    A color *c* is valid if assigning it to the current node does not create
    a monochromatic directed cycle in the color-*c* subgraph.  When
    *allow_digons* is ``True``, a 2-cycle (digon) between two nodes of the
    same color is not considered a forbidden cycle.
    """
    u = nodes[len(colors_list)]
    safe_colors: list[int] = []

    # A self-loop forms a 1-cycle: the node can never be safely colored.
    if G.has_edge(u, u):
        return []

    for c in range(1, k + 1):
        # Seed DFS with already-colored successors of u that share color c.
        # Stack stores (node, depth); depth=1 means a direct successor of u.
        initial = [
            v
            for v in G.successors(u)
            if node_to_idx[v] < len(colors_list)
            and colors_list[node_to_idx[v]] == c
        ]
        stack = [(v, 1) for v in initial]
        visited: set = set(initial)
        creates_cycle = False

        # DFS restricted to nodes already assigned color c.
        while stack:
            curr, depth = stack.pop()
            # If a color-c node reaches u, we would close a monochromatic cycle.
            # When allow_digons is True, a 2-cycle (digon, depth=1) is permitted.
            if G.has_edge(curr, u) and (depth > 1 or not allow_digons):
                creates_cycle = True
                break
            for neighbor in G.successors(curr):
                n_idx = node_to_idx[neighbor]
                if (
                    n_idx < len(colors_list)
                    and colors_list[n_idx] == c
                    and neighbor not in visited
                ):
                    visited.add(neighbor)
                    stack.append((neighbor, depth + 1))

        if not creates_cycle:
            safe_colors.append(c)

    return safe_colors


def _acyclic_coloring(
    G: nx.DiGraph,
    k: int,
    nodes: list | None = None,
    node_to_idx: dict | None = None,
    colors_list: list[int] | None = None,
    allow_digons: bool = True,
):
    """Generate all acyclic *k*-colorings of *G* via backtracking."""
    if colors_list is None:
        colors_list = []
        nodes = list(G.nodes())
        node_to_idx = {node: i for i, node in enumerate(nodes)}

    if len(colors_list) == len(nodes):
        yield {nodes[i]: colors_list[i] for i in range(len(nodes))}
    else:
        for choice in _get_safe_colors(G, nodes, node_to_idx, colors_list, k, allow_digons):
            colors_list.append(choice)
            yield from _acyclic_coloring(G, k, nodes, node_to_idx, colors_list, allow_digons)
            colors_list.pop()


def dichromatic_number(G: nx.DiGraph, allow_digons: bool = True) -> int:
    """Return the dichromatic number of *G*.

    The dichromatic number is the minimum number of colors needed for an
    acyclic coloring: a coloring such that each monochromatic subgraph
    contains no directed cycle.  When *allow_digons* is ``True``, a directed
    cycle must have at least 3 vertices to be forbidden (digons are ignored).
    """
    n = G.number_of_nodes()
    if n == 0:
        return 0
    for k in range(1, n + 1):
        if next(_acyclic_coloring(G, k, allow_digons=allow_digons), None) is not None:
            return k
    return n


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _homotopy_str(verdict) -> str:
    """Return a plain-text representation of a homotopy verdict."""
    ht = verdict.verdict
    if not verdict.is_exact:
        ht += " [approx]"
    return ht


def _write_csv(
    n: int,
    rows: list[tuple[int, int, int, str]],
    output_file: str,
) -> None:
    """Write results as a CSV file to *output_file*."""
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "edges", "chi_d", "homotopy_type_dnc"])
        writer.writerows(rows)


def _write_org_table(
    n: int,
    rows: list[tuple[int, int, int, str]],
    output_file: str,
) -> None:
    """Write an org-mode table to *output_file*."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"#+TITLE: Digraph analysis for order {n}\n")
        f.write("#+AUTHOR: Generated by digraph_analysis.py\n\n")
        f.write(
            "Data from Brendan McKay's page: "
            "https://users.cecs.anu.edu.au/~bdm/data/digraphs.html\n\n"
        )
        f.write("| # | Edges | chi_d | Homotopy type of DNC |\n")
        f.write("|---+-------+-------+----------------------|\n")
        for idx, edges, chi_d, ht in rows:
            f.write(f"| {idx} | {edges} | {chi_d} | {ht} |\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Compute dichromatic number and homotopy type of the directed "
            "neighborhood complex for all non-isomorphic digraphs of a given order."
        )
    )
    parser.add_argument(
        "order",
        type=int,
        help=f"Number of vertices. Available: {sorted(_DIGRAPH_FILES)}.",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "org"],
        default="org",
        help="Output format (default: org).",
    )
    parser.add_argument(
        "--out",
        metavar="FILE",
        help="Output file (default: digraph_analysis_<order>.<fmt>).",
    )
    parser.add_argument(
        "--allow-digons",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Allow digons (2-cycles) in monochromatic subgraphs, i.e. a "
            "directed cycle must have at least 3 vertices to be forbidden "
            "(default: True). Use --no-allow-digons to forbid digons."
        ),
    )
    args = parser.parse_args()

    n = args.order
    fmt = args.format
    output_file = args.out or f"digraph_analysis_{n}.{fmt}"

    print(f"Processing digraphs of order {n}...", flush=True)

    rows: list[tuple[int, int, int, str]] = []
    for idx, (d6_str, G) in enumerate(_iter_digraph6_pairs(n)):
        chi_d = dichromatic_number(G, allow_digons=args.allow_digons)
        dnc = directed_neighborhood_complex(G)
        ht = _homotopy_str(homotopy_type_sc_with_verdict(dnc))
        rows.append((idx, G.number_of_edges(), chi_d, ht))

        if idx > 0 and idx % 500 == 0:
            print(f"  {idx} digraphs processed...", flush=True)

    if fmt == "csv":
        _write_csv(n, rows, output_file)
    else:
        _write_org_table(n, rows, output_file)
    print(f"Done. {len(rows)} digraphs written to: {output_file}")


if __name__ == "__main__":
    sys.exit(main())
