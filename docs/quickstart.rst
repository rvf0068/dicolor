Quick Start Guide
==================

This guide will get you up and running with dicolor in just a few minutes.

Basic Concepts
---------------

**Directed Graph**: A graph where edges have a direction, typically represented as an arc from one vertex to another.

**Dichromatic Number**: The minimum number of colors needed to color the vertices such that each color class forms an acyclic subgraph (contains no directed cycles).

**Dihomomorphism**: A vertex map between directed graphs that respects both arc structure and acyclicity constraints.

Computing Dichromatic Number
------------------------------

The dichromatic number is the minimum number of colors for acyclic coloring:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    
    # Create a directed 3-cycle
    G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    
    # Compute dichromatic number
    chi_d = dichromatic_number(G)
    print(f"Dichromatic number: {chi_d}")  # Output: 2
    
    # Digons (2-cycles) can be handled differently
    G_digon = nx.DiGraph([(0, 1), (1, 0)])
    
    # Allow digons (default)
    chi_allow = dichromatic_number(G_digon, allow_digons=True)
    print(f"With allow_digons=True: {chi_allow}")  # Output: 1
    
    # Forbid digons
    chi_forbid = dichromatic_number(G_digon, allow_digons=False)
    print(f"With allow_digons=False: {chi_forbid}")  # Output: 2

Generating Dihomomorphisms
----------------------------

Generate all dihomomorphisms between two directed graphs:

.. code-block:: python

    import networkx as nx
    from dicolor import dihomomorphisms
    
    # Source and target graphs (both single arcs)
    D = nx.DiGraph([(0, 1)])
    E = nx.DiGraph([(0, 1)])
    
    # Generate all dihomomorphisms
    all_maps = list(dihomomorphisms(D, E))
    print(f"Number of dihomomorphisms: {len(all_maps)}")  # Output: 3
    
    for f in all_maps:
        print(f"Mapping: {f}")
    
    # Output:
    # Mapping: {0: 0, 1: 0}
    # Mapping: {0: 0, 1: 1}
    # Mapping: {0: 1, 1: 1}

Analyzing Dihomomorphism Graphs
---------------------------------

Build and analyze the graph structure of dihomomorphisms:

.. code-block:: python

    import networkx as nx
    from dicolor import dihomomorphism_graph
    
    # Single arc source
    D = nx.DiGraph([(0, 1)])
    
    # Digon (2-cycle) target
    E = nx.DiGraph([(0, 1), (1, 0)])
    
    # Build dihomomorphism graph
    G = dihomomorphism_graph(D, E)
    
    print(f"Vertices: {G.number_of_nodes()}")  # 3 dihomomorphisms
    print(f"Edges: {G.number_of_edges()}")     # Adjacency structure
    
    # Access dihomomorphism mappings
    for node in G.nodes():
        mapping = G.nodes[node]['map']
        print(f"Dihomomorphism: {node} -> {mapping}")

Working with Larger Graphs
----------------------------

The package includes digraph data for orders 1-6 from McKay's database:

.. code-block:: python

    import networkx as nx
    from dicolor import parse_digraph6, digraph_generator
    
    # Generate all non-isomorphic digraphs of order 3
    for G in digraph_generator(3):
        print(f"Digraph with {G.number_of_nodes()} vertices, {G.number_of_edges()} arcs")
    
    # Parse digraph6 string
    d6_string = "&AO"  # Single arc as digraph6
    G = parse_digraph6(d6_string)
    print(f"Vertices: {G.nodes()}, Arcs: {G.edges()}")

Command-Line Usage
-------------------

Analyze all digraphs of a given order:

.. code-block:: bash

    # Compute dichromatic numbers for order 3
    python -m dicolor.digraph_analysis 3 --format csv --out results.csv
    
    # Analyze dihomomorphisms from cycles
    python -m dicolor.dihom_cycle_analysis 3 --domain cycle --format org
    
    # Analyze dihomomorphisms from single arc
    python -m dicolor.dihom_cycle_analysis 3 --domain arc --format csv

Common Patterns
----------------

**Checking if a graph is a DAG**:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    
    G = nx.DiGraph([(0, 1), (1, 2)])  # Path graph (DAG)
    
    if dichromatic_number(G) == 1:
        print("Graph is acyclic (DAG)")
    else:
        print("Graph contains cycles")

**Finding vertex colorings**:

.. code-block:: python

    from dicolor.digraph_analysis import _acyclic_coloring
    import networkx as nx
    
    G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    
    # Get first acyclic 2-coloring
    coloring = next(_acyclic_coloring(G, 2))
    print(f"2-coloring: {coloring}")

**Batch processing digraphs**:

.. code-block:: python

    from dicolor import dichromatic_number, digraph_generator
    
    results = {}
    for idx, G in enumerate(digraph_generator(4)):
        chi_d = dichromatic_number(G)
        results[idx] = chi_d
    
    print(f"Processed {len(results)} digraphs of order 4")

Next Steps
-----------

- Read the :doc:`theory` section for mathematical background
- Explore the :doc:`api/index` for detailed function documentation
- Check out :doc:`examples` for more advanced usage
- Run the tests to ensure everything works: ``pytest tests/``
