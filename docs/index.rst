dicolor Documentation
=======================

Directed Graph Analysis with Dichromatic Numbers and Dihomomorphisms

**dicolor** is a Python package for computing and analyzing properties of directed graphs,
including dichromatic coloring and dihomomorphism generation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   theory
   examples

Features
---------

- **Dichromatic Number**: Minimum colors for acyclic coloring of directed graphs
- **Dihomomorphisms**: Generate and analyze dihomomorphisms between digraphs
- **Graph Analysis**: Directed neighborhood complexes and topological properties
- **Batch Processing**: Analyze all non-isomorphic digraphs of given order
- **Command-line Tools**: CLI for analyzing digraph datasets

Getting Started
----------------

Installation::

    pip install dicolor

Quick example::

    import networkx as nx
    from dicolor import dichromatic_number
    
    # Create a directed cycle
    G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    print(dichromatic_number(G))  # Output: 2

API Reference
--------------

.. autosummary::
   :toctree: api

   dicolor.dihomomorphisms
   dicolor.digraph_analysis
   dicolor.dihom_cycle_analysis

Data
-----

Digraph data sourced from `Brendan McKay's database <https://users.cecs.anu.edu.au/~bdm/data/digraphs.html>`_.

Includes non-isomorphic digraphs up to order 6:

- Orders 1-5: Complete datasets
- Order 6: 1,547,860 digraphs (compressed format)

The data files are distributed with the package and automatically loaded when needed.

Indices and tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
