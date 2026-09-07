Examples
=========

This section provides practical examples of using the dicolor package.

Basic Dichromatic Number Computation
--------------------------------------

Compute the dichromatic number for various graph types:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    
    # Directed Acyclic Graph (DAG)
    dag = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
    print(f"DAG dichromatic number: {dichromatic_number(dag)}")  # 1
    
    # Directed 3-cycle
    cycle3 = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    print(f"3-cycle dichromatic number: {dichromatic_number(cycle3)}")  # 2
    
    # Directed 4-cycle
    cycle4 = nx.DiGraph([(0, 1), (1, 2), (2, 3), (3, 0)])
    print(f"4-cycle dichromatic number: {dichromatic_number(cycle4)}")  # 2
    
    # Tournament (complete directed graph)
    tournament = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
    print(f"Tournament dichromatic number: {dichromatic_number(tournament)}")  # 1

Understanding Digons
---------------------

Explore how digons (2-cycles) are treated:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    
    # Create a digon (0 <-> 1)
    digon = nx.DiGraph([(0, 1), (1, 0)])
    
    # With digons allowed (default)
    chi_allow = dichromatic_number(digon, allow_digons=True)
    print(f"Digon with allow_digons=True: {chi_allow}")  # 1
    
    # Without allowing digons
    chi_forbid = dichromatic_number(digon, allow_digons=False)
    print(f"Digon with allow_digons=False: {chi_forbid}")  # 2
    
    # Digon is an edge-contraction of 3-cycle at one vertex
    # but differs in cycle length requirements

Generating Vertex Colorings
-----------------------------

Generate all valid acyclic colorings:

.. code-block:: python

    import networkx as nx
    from dicolor.digraph_analysis import _acyclic_coloring
    
    # Simple directed path
    G = nx.DiGraph([(0, 1), (1, 2)])
    
    # Get all 1-colorings (should be just one for a path)
    colorings_1 = list(_acyclic_coloring(G, 1))
    print(f"Number of 1-colorings: {len(colorings_1)}")
    for coloring in colorings_1:
        print(f"  Coloring: {coloring}")
    
    # For 2-colorings (should be many more options)
    colorings_2 = list(_acyclic_coloring(G, 2))
    print(f"Number of 2-colorings: {len(colorings_2)}")

Working with Dihomomorphisms
------------------------------

Generate and explore dihomomorphisms:

.. code-block:: python

    import networkx as nx
    from dicolor import dihomomorphisms, dihomomorphism_graph
    
    # Example 1: Simple arc
    print("=== Example 1: Arc to Arc ===")
    D = nx.DiGraph([(0, 1)])
    E = nx.DiGraph([(0, 1)])
    
    maps = list(dihomomorphisms(D, E))
    print(f"Found {len(maps)} dihomomorphisms")
    for i, f in enumerate(maps):
        print(f"  f_{i}: {f}")
    
    # Example 2: Path to single vertex
    print("\n=== Example 2: Path to Point ===")
    D2 = nx.DiGraph([(0, 1), (1, 2)])
    E2 = nx.DiGraph()
    E2.add_node(0)
    
    maps2 = list(dihomomorphisms(D2, E2))
    print(f"Found {len(maps2)} dihomomorphisms")
    for f in maps2:
        print(f"  {f}")
    
    # Example 3: Dihomomorphism graph structure
    print("\n=== Example 3: Dihomomorphism Graph ===")
    D3 = nx.DiGraph([(0, 1)])
    E3 = nx.DiGraph([(0, 1), (1, 0)])  # Digon
    
    G = dihomomorphism_graph(D3, E3)
    print(f"Graph: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
    print("Adjacency:")
    for u, v in G.edges():
        print(f"  {u} -- {v}")

Advanced Example: Custom Graph Construction
---------------------------------------------

Build and analyze custom directed graphs:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number, dihomomorphisms
    
    # Create a tournament (complete directed graph with one direction per edge)
    n = 4
    tournament = nx.DiGraph()
    tournament.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            tournament.add_edge(i, j)  # Always i -> j
    
    chi_d = dichromatic_number(tournament)
    print(f"Tournament on {n} vertices: dichromatic number = {chi_d}")
    
    # Create a "butterfly" graph (two triangles sharing a vertex)
    butterfly = nx.DiGraph()
    butterfly.add_edges_from([
        (0, 1), (1, 2), (2, 0),      # Triangle 1
        (0, 3), (3, 4), (4, 0),      # Triangle 2
    ])
    
    chi_butterfly = dichromatic_number(butterfly)
    print(f"Butterfly graph: dichromatic number = {chi_butterfly}")
    
    # Find dihomomorphisms from path to butterfly
    path = nx.DiGraph([(0, 1), (1, 2)])
    maps = list(dihomomorphisms(path, butterfly))
    print(f"Dihomomorphisms from path to butterfly: {len(maps)}")

Batch Processing Digraphs
--------------------------

Analyze all small non-isomorphic digraphs:

.. code-block:: python

    from dicolor import dichromatic_number, digraph_generator
    
    # Analyze all digraphs of order 3
    print("=== Digraphs of order 3 ===")
    stats = {}
    for idx, G in enumerate(digraph_generator(3)):
        chi_d = dichromatic_number(G)
        edges = G.number_of_edges()
        if chi_d not in stats:
            stats[chi_d] = []
        stats[chi_d].append((idx, edges))
    
    for chi_d in sorted(stats.keys()):
        graphs = stats[chi_d]
        print(f"chi_d = {chi_d}: {len(graphs)} digraphs")
        for idx, edges in graphs[:3]:  # Show first 3
            print(f"  Graph {idx}: {edges} arcs")

Real-world Pattern: Graph Coloring Verification
---------------------------------------------------

Verify if a coloring is valid:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    from dicolor.digraph_analysis import _acyclic_coloring
    
    def verify_coloring(G, coloring):
        """Verify that a coloring is acyclic."""
        for color in set(coloring.values()):
            # Get vertices of this color
            vertices = [v for v, c in coloring.items() if c == color]
            subgraph = G.subgraph(vertices)
            # Check if acyclic
            if not nx.is_directed_acyclic_graph(subgraph):
                return False
        return True
    
    # Example: Verify a manual coloring
    G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    
    # Try coloring
    coloring = {0: 1, 1: 1, 2: 2}
    is_valid = verify_coloring(G, coloring)
    print(f"Coloring {coloring} is valid: {is_valid}")
    
    # Get actual minimum coloring
    chi_d = dichromatic_number(G)
    actual_coloring = next(_acyclic_coloring(G, chi_d))
    print(f"Minimum coloring: {actual_coloring}")
    print(f"Is valid: {verify_coloring(G, actual_coloring)}")

Performance Analysis
---------------------

Analyze performance on larger graphs:

.. code-block:: python

    import time
    import networkx as nx
    from dicolor import dichromatic_number, digraph_generator
    
    # Time dichromatic computation for increasing orders
    for order in range(1, 5):
        start = time.time()
        count = 0
        for G in digraph_generator(order):
            chi_d = dichromatic_number(G)
            count += 1
        elapsed = time.time() - start
        print(f"Order {order}: {count} digraphs in {elapsed:.2f}s")

Integration with NetworkX
--------------------------

Combine dicolor with NetworkX utilities:

.. code-block:: python

    import networkx as nx
    from dicolor import dichromatic_number
    
    # Create a random directed graph
    G = nx.erdos_renyi_graph(5, 0.3, directed=True)
    
    # Convert to directed graph
    if not isinstance(G, nx.DiGraph):
        G = G.to_directed()
    
    # Analyze
    chi_d = dichromatic_number(G)
    print(f"Random graph dichromatic number: {chi_d}")
    
    # Check connectivity
    print(f"Strongly connected: {nx.is_strongly_connected(G)}")
    print(f"Number of SCCs: {nx.number_strongly_connected_components(G)}")
