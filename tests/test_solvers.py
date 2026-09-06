from dicolor.solvers import solve_example

def test_solve_example_empty():
    """Test that the solver handles empty input correctly."""
    assert solve_example([]) == []

def test_solve_example_data():
    """Test the solver with sample data."""
    data = [1, 2, 3]
    assert solve_example(data) == data
