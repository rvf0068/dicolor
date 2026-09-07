# dicolor

**Directed graph analysis with dichromatic numbers and dihomomorphisms**

A Python package for computing and analyzing properties of directed graphs, including dichromatic coloring and dihomomorphism generation.

## Features

- **Dichromatic Number**: Compute the minimum number of colors needed for an acyclic coloring of directed graphs
- **Dihomomorphisms**: Generate all dihomomorphisms between two directed graphs
- **Dihomomorphism Graph**: Build and analyze the graph of dihomomorphisms with adjacency conditions
- **Directed Neighborhood Complex**: Analyze topological properties of directed graphs
- **Comprehensive Analysis**: Batch process all non-isomorphic digraphs of a given order

## Installation

```bash
pip install dicolor
```

For development:

```bash
pip install -e ".[dev,test,docs]"
```

## Quick Start

### Dichromatic Number

```python
import networkx as nx
from dicolor import dichromatic_number

# Create a directed cycle
G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
chi_d = dichromatic_number(G)
print(f"Dichromatic number: {chi_d}")  # Output: 2
```

### Dihomomorphisms

```python
import networkx as nx
from dicolor import dihomomorphisms

# Create source and target graphs
D = nx.DiGraph([(0, 1)])  # Single arc
E = nx.DiGraph([(0, 1)])  # Single arc

# Generate all dihomomorphisms
for f in dihomomorphisms(D, E):
    print(f)
# Output:
# {0: 0, 1: 0}
# {0: 0, 1: 1}
# {0: 1, 1: 1}
```

### Dihomomorphism Graph

```python
import networkx as nx
from dicolor import dihomomorphism_graph

D = nx.DiGraph([(0, 1)])
E = nx.DiGraph([(0, 1), (1, 0)])  # Digon (2-cycle)

# Build the dihomomorphism graph
G = dihomomorphism_graph(D, E)
print(f"Vertices: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
```

## API Reference

### Main Functions

#### `dichromatic_number(G, allow_digons=True)`
Compute the dichromatic number of a directed graph.

**Parameters:**
- `G` (networkx.DiGraph): The input directed graph
- `allow_digons` (bool): If True, 2-cycles are not forbidden; if False, all cycles are forbidden

**Returns:** int - The dichromatic number

#### `dihomomorphisms(D, E)`
Generate all dihomomorphisms from source graph D to target graph E.

**Parameters:**
- `D` (networkx.DiGraph): Source directed graph
- `E` (networkx.DiGraph): Target directed graph

**Yields:** dict - Each dihomomorphism as a mapping of vertices

#### `dihomomorphism_graph(D, E)`
Build the undirected graph of dihomomorphisms between D and E.

**Parameters:**
- `D` (networkx.DiGraph): Source directed graph
- `E` (networkx.DiGraph): Target directed graph

**Returns:** networkx.Graph - Graph where vertices are dihomomorphisms and edges represent adjacency

## Command-Line Tools

### digraph_analysis

Analyze all non-isomorphic digraphs of a given order:

```bash
python -m dicolor.digraph_analysis 3 --format csv --out results.csv
```

Options:
- `order`: Number of vertices (1-6)
- `--format`: Output format (csv or org) 
- `--out`: Output file
- `--allow-digons`: Allow 2-cycles (default: True)

### dihom_cycle_analysis

Analyze dihomomorphisms from directed cycles to target digraphs:

```bash
python -m dicolor.dihom_cycle_analysis 3 --domain cycle --format org
```

Options:
- `order`: Number of vertices
- `--domain`: Source domain (cycle or arc)
- `--cycle-order`: Length of source cycle (default: same as order)
- `--format`: Output format (csv or org)
- `--out`: Output file

## Theory

### Dichromatic Number

The **dichromatic number** $\chi_d(G)$ of a directed graph $G$ is the minimum number of colors needed for an acyclic coloring—a coloring where each color class induces an acyclic subgraph (contains no directed cycles).

This is equivalent to partitioning the vertices into the minimum number of directed acyclic subgraphs.

### Dihomomorphisms

A **dihomomorphism** $f: D \to E$ between directed graphs is a vertex map satisfying:

1. **Arc condition**: For every arc $u \to v$ in $D$, either $f(u) \to f(v)$ is an arc in $E$, or $f(u) = f(v)$
2. **Acyclicity condition**: For every vertex $w$ in $E$, the subgraph of $D$ induced by the preimage $f^{-1}(w)$ is acyclic

Dihomomorphisms generalize homomorphisms in undirected graphs and capture the structure of directed graph mappings that respect both arc and acyclicity constraints.

## Data

Digraph data is sourced from [Brendan McKay's database](https://users.cecs.anu.edu.au/~bdm/data/digraphs.html).

Digraphs up to order 6 are included:
- Order 1-5: Complete datasets
- Order 6: 1547860 non-isomorphic digraphs (compressed)

## Testing

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=dicolor tests/
```

## Documentation

Build the Sphinx documentation:

```bash
cd docs
make html
```

## License

MIT License - See LICENSE file for details

## References

- McKay, B. D. (2011). "Digraphs." <https://users.cecs.anu.edu.au/~bdm/data/digraphs.html>
- Related work on directed graph colorings and homomorphisms

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
