import pytest
from comps.for_fold import for_fold  # Assuming for_fold is defined in for_fold.py

# Example 1: One accumulator over one iterable
def test_example_1(subtests):
    numbers = [1, 2, 3, 4, 5]

    with subtests.test("One accumulator over one iterable"):
        result = for_fold(
            accumulators=[("sum", 0)],
            iterables=[("n", numbers)],
            body=lambda env: {"sum": env["sum"] + env["n"]},
            result=lambda env: env["sum"]
        )
        assert result == 15  # 1 + 2 + 3 + 4 + 5 = 15

# Example 2: Two accumulators over two iterables
def test_example_2(subtests):
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    with subtests.test("Two accumulators over two iterables"):
        result = for_fold(
            accumulators=[("sum1", 0), ("sum2", 0)],
            iterables=[("a", list1), ("b", list2)],
            body=lambda env: {"sum1": env["sum1"] + env["a"], "sum2": env["sum2"] + env["b"]},
            result=lambda env: (env["sum1"], env["sum2"])
        )
        assert result == (6, 60)  # 1 + 2 + 3 = 6, 10 + 20 + 30 = 60

# Example 3: Filter with 'when' (only sum even numbers)
def test_example_3(subtests):
    numbers = [1, 2, 3, 4, 5]

    with subtests.test("Filter even numbers"):
        result = for_fold(
            accumulators=[("sum", 0)],
            iterables=[("n", numbers)],
            body=lambda env: {"sum": env["sum"] + env["n"]},
            when=lambda env: env["n"] % 2 == 0,  # Filter to only include even numbers
            result=lambda env: env["sum"]
        )
        assert result == 6  # Only 2 and 4 are summed

# Example 4: Custom result (sum and product of numbers)
def test_example_4(subtests):
    numbers = [1, 2, 3, 4]

    with subtests.test("Custom result with sum and product"):
        result = for_fold(
            accumulators=[("sum", 0), ("product", 1)],
            iterables=[("n", numbers)],
            body=lambda env: {"sum": env["sum"] + env["n"], "product": env["product"] * env["n"]},
            result=lambda env: f"Sum: {env['sum']}, Product: {env['product']}"
        )
        assert result == "Sum: 10, Product: 24"  # 1 + 2 + 3 + 4 = 10, 1 * 2 * 3 * 4 = 24
