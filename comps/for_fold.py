from comps.comprehension_builder import ComprehensionBuilder
from comps.operations import AddAccumulator, AddIterable, SetFilter, SetResult, SetBody
from typing import Callable, Any, Iterable, Tuple


def for_fold(
    accumulators: list[Tuple[str, Any]],
    iterables: list[Tuple[str, Iterable]],
    body: Tuple[Callable[..., Any], ...],
    result: str = None,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Any:
    """
    Simplified for_fold function using ComprehensionBuilder with filtering.

    :param accumulators: List of tuples (name, initial_value) for accumulators.
    :param iterables: List of tuples (name, iterable) for iteration.
    :param body: Tuple of functions, each corresponding to an accumulator.
                 Each function should return the updated value for its accumulator.
    :param result: The name of the accumulator to return as the final result.
                   If None, returns all accumulators as a dictionary.
    :param when: A filter function that takes keyword arguments and returns a boolean.
                 If False, the current iteration is skipped.
    :return: The result as specified by the 'result' parameter.
    """
    builder = ComprehensionBuilder()

    # Add accumulators
    for name, value in accumulators:
        builder >> AddAccumulator(name, value)

    # Add iterables
    for name, iterable in iterables:
        builder >> AddIterable(name, iterable)

    # Add body functions
    for body_fn in body:
        builder >> SetBody(body_fn)

    # Set the filter
    if when:
        builder >> SetFilter(when)

    # Set the result
    if result:
        builder >> SetResult(result)

    return builder.run()


# Example usage in the if __name__ == "__main__" block
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Example 1: One Accumulator over One Iterable
    def body_sum(sum, n):
        return sum + n

    result1 = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=(body_sum,),
        result="sum"
    )
    print(f"Example 1 Result: {result1}")  # Output: Example 1 Result: 15

    # Example 2: Two Accumulators over Two Iterables
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    def body_sum1(sum1, sum2, a, b):
        return sum1 + a

    def body_sum2(sum1, sum2, a, b):
        return sum2 + b

    result2 = for_fold(
        accumulators=[("sum1", 0), ("sum2", 0)],
        iterables=[("a", list1), ("b", list2)],
        body=(body_sum1, body_sum2),
        result="sum2"
    )
    print(f"Example 2 Result: {result2}")  # Output: Example 2 Result: 60

    # Example 3: Filter with `when` Clause (Sum only even numbers)
    def body_sum_even(sum, n):
        return sum + n

    def when_even(**kwargs):
        return kwargs["n"] % 2 == 0  # Include only even numbers

    result3 = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=(body_sum_even,),
        result="sum",
        when=when_even
    )
    print(f"Example 3 Result: {result3}")  # Output: Example 3 Result: 6

    # Example 4: Custom Result with Sum and Product
    numbers_prod = [1, 2, 3, 4]

    def body_sum_prod_sum(sum, product, n):
        return sum + n

    def body_sum_prod_prod(sum, product, n):
        return product * n

    def custom_result(**kwargs):
        return f"Sum: {kwargs['sum']}, Product: {kwargs['product']}"

    result4 = for_fold(
        accumulators=[("sum", 0), ("product", 1)],
        iterables=[("n", numbers_prod)],
        body=(body_sum_prod_sum, body_sum_prod_prod),
        result="product"  # Alternatively, set to "sum" or any other accumulator
    )
    print(f"Example 4 Result: {result4}")  # Output: Example 4 Result: 24

    # Example 5: Custom Result Function
    result5 = for_fold(
        accumulators=[("sum", 0), ("product", 1)],
        iterables=[("n", numbers_prod)],
        body=(body_sum_prod_sum, body_sum_prod_prod),
        result="product"  # Or set a custom result function if needed
    )
    print(f"Example 5 Result: {result5}")  # Output: Example 5 Result: 24
