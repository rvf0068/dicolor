Installation Guide
====================

Requirements
-------------

- Python 3.8 or later
- pip or other package installer

Installation from PyPI
----------------------

Install the latest stable release::

    pip install dicolor

Installation for Development
-----------------------------

Clone the repository and install in development mode::

    git clone https://github.com/user/dicolor.git
    cd dicolor
    pip install -e ".[dev,test,docs]"

This installs the package in editable mode with all optional dependencies:

- `dev`: Development tools (linting, type checking)
- `test`: Testing tools (pytest, coverage)
- `docs`: Documentation tools (Sphinx, themes)

Dependencies
------------

Core dependencies:

- `networkx <https://networkx.org/>`_: Graph data structure and algorithms
- `pycombtop <https://github.com/user/pycombtop>`_: Computational topology

Optional dependencies:

.. code-block:: text

    [test] pytest, pytest-cov
    [docs] sphinx, sphinx-rtd-theme, sphinx-autodoc-typehints
    [dev] ruff, mypy

Verifying Installation
----------------------

Test that the package is correctly installed::

    python -c "import dicolor; print(dicolor.__version__)"

Run the test suite::

    pytest tests/

Build documentation locally::

    cd docs
    make html
    # Open docs/_build/html/index.html in a browser

Troubleshooting
---------------

**ImportError: No module named 'dicolor'**
    Ensure the package is installed and the Python path is correct.

**Missing dependency error**
    Install missing dependencies with::

        pip install [missing-package]

**Tests fail**
    Ensure all test dependencies are installed::

        pip install -e ".[test]"

**Documentation build fails**
    Install documentation dependencies::

        pip install -e ".[docs]"
        cd docs
        make clean html
