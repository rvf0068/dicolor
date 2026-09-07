Theoretical Background
======================

Dichromatic Number
-------------------

Definition
~~~~~~~~~~

The **dichromatic number** :math:`\chi_d(G)` of a directed graph :math:`G = (V, E)` is defined as:

.. math::

   \chi_d(G) = \min\{k : V \text{ can be partitioned into } k \text{ acyclic subgraphs}\}

In other words, it is the minimum number of colors needed to color the vertices of :math:`G` such that each color class induces a directed acyclic subgraph (DAG).

Properties
~~~~~~~~~~

1. **Bounds**: For a directed graph :math:`G` on :math:`n` vertices:
   
   .. math::
   
      1 \leq \chi_d(G) \leq n
   
   - :math:`\chi_d(G) = 1` if and only if :math:`G` is acyclic (is a DAG)
   - :math:`\chi_d(G) = n` only for very specific graph structures

2. **Relationship to Chromatic Number**: For undirected graphs, the chromatic number and dichromatic number have different meanings:
   
   - Undirected chromatic number counts proper vertex colorings
   - Dichromatic number requires acyclicity in color classes

3. **Cycle Relation**: Every directed cycle requires at least 2 colors:
   
   - A 3-cycle :math:`0 \to 1 \to 2 \to 0` has :math:`\chi_d = 2`
   - A :math:`k`-cycle with :math:`k \geq 3` has :math:`\chi_d = 2`

4. **Digons**: 2-cycles (digons) between vertices can be treated specially:
   
   - With `allow_digons=True`: Digons are colored with 1 color
   - With `allow_digons=False`: Digons require 2 colors

Algorithms
~~~~~~~~~~

This package uses backtracking to compute acyclic colorings:

1. Order vertices of :math:`G`
2. For each vertex, determine which colors are safe
3. A color is safe if assigning it doesn't create a monochromatic directed cycle
4. Use DFS to check for cycles within each color class
5. Backtrack if no safe color exists for a vertex

Time Complexity
~~~~~~~~~~~~~~~

- Enumerating all acyclic :math:`k`-colorings: Exponential in worst case
- Computing dichromatic number: :math:`O(n \cdot T(k))` where :math:`T(k)` is time to check all :math:`k`-colorings

Dihomomorphisms
----------------

Definition
~~~~~~~~~~

A **dihomomorphism** from directed graph :math:`D` to directed graph :math:`E` is a vertex map :math:`f: V(D) \to V(E)` satisfying:

1. **Arc Condition**: For every arc :math:`u \to v` in :math:`D`:
   
   .. math::
   
      f(u) \to f(v) \in E \quad \text{or} \quad f(u) = f(v)

2. **Acyclicity Condition**: For every vertex :math:`w \in V(E)`, the induced subgraph:
   
   .. math::
   
      D[f^{-1}(w)] \text{ is acyclic}

Key Properties
~~~~~~~~~~~~~~

1. **Self-loops Forbidden**: If :math:`D` has a self-loop, no dihomomorphism exists (the preimage would be cyclic)

2. **DAGs Map to DAGs**: If :math:`D` is acyclic, then :math:`D` can always map to any target graph :math:`E` with vertices

3. **Existence Conditions**:
   - If :math:`D` is empty, exactly one dihomomorphism exists (empty map)
   - If :math:`E` is empty and :math:`D` non-empty, no dihomomorphism exists
   - Cycles in :math:`D` severely restrict possible mappings

4. **Complete Mapping Space**: All dihomomorphisms from :math:`D` to :math:`E` form a discrete set

Examples
~~~~~~~~

**Single Arc to Single Arc**:

Source: :math:`D = 0 \to 1`, Target: :math:`E = 0 \to 1`

Dihomomorphisms:

- :math:`f_1: \{0 \mapsto 0, 1 \mapsto 0\}` (both vertices map to 0)
- :math:`f_2: \{0 \mapsto 0, 1 \mapsto 1\}` (preserving arc)
- :math:`f_3: \{0 \mapsto 1, 1 \mapsto 1\}` (both vertices map to 1)

All three satisfy:

- Arc condition: Each preserves the arc structure
- Acyclicity: Each preimage (single vertex or two vertices with arc) is acyclic

**3-Cycle Cannot Map to Point**:

Source: :math:`D = 0 \to 1 \to 2 \to 0`, Target: :math:`E = \{w\}` (single vertex)

If all vertices map to :math:`w`, the preimage :math:`f^{-1}(w) = \{0, 1, 2\}` contains the 3-cycle, violating acyclicity.

**DAG Can Collapse**:

Source: :math:`D = 0 \to 1 \to 2` (path, acyclic), Target: :math:`E = \{w\}`

The map :math:`f: \{0 \mapsto w, 1 \mapsto w, 2 \mapsto w\}` works because :math:`f^{-1}(w) = D` is acyclic.

Dihomomorphism Graph
---------------------

Given digraphs :math:`D` and :math:`E`, the **dihomomorphism graph** :math:`G` is defined as:

- **Vertices**: All dihomomorphisms from :math:`D` to :math:`E`
- **Edges**: Two dihomomorphisms :math:`f, h` are adjacent if for every arc :math:`x \to y` in :math:`D`:
  
  .. math::
  
     f(x) \to h(y) \in E \quad \text{and} \quad h(x) \to f(y) \in E

This adjacency condition captures the structure of "compatible" dihomomorphisms and enables topological analysis of the mapping space.

Applications
~~~~~~~~~~~~

The dihomomorphism graph is used to study:
- Homotopy type of mapping spaces
- Clique complexes of dihomomorphism graphs
- Topological properties of directed graph structures

References
-----------

1. Lovász, L. (2010). "Large networks and graph limits." 
   American Mathematical Society.

2. Bollobás, B. (1998). "Modern Graph Theory." 
   Springer-Verlag.

3. McKay, B. D. (2011). "Digraphs."
   https://users.cecs.anu.edu.au/~bdm/data/digraphs.html

4. Diestel, R. (2017). "Graph Theory (5th Edition)."
   Springer-Verlag.
