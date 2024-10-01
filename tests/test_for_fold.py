import pytest
from comps.for_fold import for_fold

# Test Example 1: One Accumulator over One Iterable
def test_single_accumulator():
    numbers = [1, 2, 3, 4, 5]

    # Happy Path: Sum the numbers
    def body(sum, n):
        return {"sum": sum + n}

    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=body,
        result=lambda **kwargs: kwargs["sum"]  # Extract sum from accumulators
    )
    assert result == 15, "Single accumulator happy path failed."

    # Failure Path: Body function returns an invalid accumulator name
    def invalid_body(sum, n):
        return {"total": sum + n}  # 'total' is not a valid accumulator

    with pytest.raises(ValueError, match="Invalid accumulator name in updates: total"):
        for_fold(
            accumulators=[("sum", 0)],
            iterables=[("n", numbers)],
            body=invalid_body,
            result=lambda **kwargs: kwargs["sum"]
        )

# Test Example 2: Two Accumulators over Two Iterables
def test_multiple_accumulators():
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    # Happy Path: Sum1 and Sum2
    def body(sum1, sum2, a, b):
        return {"sum1": sum1 + a, "sum2": sum2 + b}

    result = for_fold(
        accumulators=[("sum1", 0), ("sum2", 0)],
        iterables=[("a", list1), ("b", list2)],
        body=body,
        result=lambda **kwargs: (kwargs["sum1"], kwargs["sum2"])
    )
    assert result == (6, 60), "Multiple accumulators happy path failed."

    # Failure Path: Body function returns invalid accumulator names
    def invalid_body(sum1, sum2, a, b):
        return {"total1": sum1 + a, "total2": sum2 + b}  # 'total1' and 'total2' are invalid

    with pytest.raises(ValueError, match="Invalid accumulator name in updates: total1"):
        for_fold(
            accumulators=[("sum1", 0), ("sum2", 0)],
            iterables=[("a", list1), ("b", list2)],
            body=invalid_body,
            result=lambda **kwargs: (kwargs["sum1"], kwargs["sum2"])
        )

# Test Example 3: Filter with `when` Clause
def test_filter_with_when():
    numbers = [1, 2, 3, 4, 5]

    # Happy Path: Sum only even numbers
    def body(sum, n):
        return {"sum": sum + n}

    def when(**kwargs):
        return kwargs["n"] % 2 == 0  # Include only even numbers

    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=body,
        when=when,
        result=lambda **kwargs: kwargs["sum"]
    )
    assert result == 6, "Filter with when clause happy path failed."

    # Failure Path: Filter function refers to an undefined variable
    def invalid_when(**kwargs):
        return kwargs["n"] % 2 == 0 and kwargs["undefined_var"] > 0  # 'undefined_var' does not exist

    with pytest.raises(KeyError, match="undefined_var"):
        for_fold(
            accumulators=[("sum", 0)],
            iterables=[("n", numbers)],
            body=body,
            when=invalid_when,
            result=lambda **kwargs: kwargs["sum"]
        )

# Test Example 4: Custom Result
def test_custom_result():
    numbers = [1, 2, 3, 4]

    # Happy Path: Calculate sum and product
    def body(sum, product, n):
        return {"sum": sum + n, "product": product * n}

    def custom_result(**kwargs):
        return f"Sum: {kwargs['sum']}, Product: {kwargs['product']}"

    result = for_fold(
        accumulators=[("sum", 0), ("product", 1)],
        iterables=[("n", numbers)],
        body=body,
        result=custom_result
    )
    assert result == "Sum: 10, Product: 24", "Custom result happy path failed."

    # Failure Path: Result function accesses a non-existent accumulator
    def invalid_result(**kwargs):
        return kwargs["non_existent"]  # 'non_existent' does not exist

    with pytest.raises(KeyError, match="non_existent"):
        for_fold(
            accumulators=[("sum", 0), ("product", 1)],
            iterables=[("n", numbers)],
            body=body,
            result=invalid_result
        )
