from comps.comprehension_builder import ComprehensionBuilder
from comps.operations import AddAccumulator, AddIterable, SetFilter, SetResult, SetBody
from typing import Callable, Any, Iterable


def for_fold(
    accumulators: list[tuple[str, Any]],
    iterables: list[tuple[str, Iterable]],
    body: Callable[..., dict],
    *,
    when: Callable[..., bool] = lambda **kwargs: True,
    result: Callable[..., Any] = None
) -> Any:
    """
    Simplified for_fold function using ComprehensionBuilder.
    """
    builder = ComprehensionBuilder()

    # Add accumulators
    for name, value in accumulators:
        builder >> AddAccumulator(name, value)

    # Add iterables
    for name, iterable in iterables:
        builder >> AddIterable(name, iterable)

    # Set the body, filter, and result
    builder >> SetBody(body)
    builder >> SetFilter(when)

    if result:
        builder >> SetResult(result)

    return builder.run()

if __name__ == '__main__':
    # Example 1: One Accumulator over One Iterable
    numbers = [1, 2, 3, 4, 5]

    def body(sum, n):
        return {"sum": sum + n}

    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=body,
        result=lambda **kwargs: kwargs["sum"]
    )
    print(f"Example 1 Result: {result}")  # Output: Example 1 Result: 15


    # Example 2: Two Accumulators over Two Iterables
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    def body(sum1, sum2, a, b):
        return {"sum1": sum1 + a, "sum2": sum2 + b}

    result = for_fold(
        accumulators=[("sum1", 0), ("sum2", 0)],
        iterables=[("a", list1), ("b", list2)],
        body=body,
        result=lambda **kwargs: (kwargs["sum1"], kwargs["sum2"])
    )
    print(f"Example 2 Result: {result}")  # Output: Example 2 Result: (6, 60)


    # Example 3: Filter with `when` Clause (Sum only even numbers)
    def body(sum, n):
        return {"sum": sum + n}

    def when(**kwargs):
        return kwargs["n"] % 2 == 0

    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=body,
        when=when,
        result=lambda **kwargs: kwargs["sum"]
    )
    print(f"Example 3 Result: {result}")  # Output: Example 3 Result: 6


    # Example 4: Custom Result with Sum and Product
    numbers = [1, 2, 3, 4]

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
    print(f"Example 4 Result: {result}")  # Output: Example 4 Result: Sum: 10, Product: 2
