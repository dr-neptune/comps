from comps.generator_comprehension import GeneratorComprehension
from typing import Callable, Any, Iterable, List, Tuple

def for_fold(
    accumulators: List[Tuple[str, Any]],
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Tuple[Any, ...]],
    *,
    when: Callable[..., bool] = lambda **kwargs: True,
    result: Callable[..., Any] = None
) -> Any:
    """
    Simplified for_fold function using GeneratorComprehension.
    """
    comprehension = GeneratorComprehension(
        iterables=iterables,
        accumulators=accumulators,
        body=body,
        when=when,
        result=result
    )
    return comprehension.run()

# Ensure the following code is properly indented and within the if __name__ == "__main__" block
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Example: Sum and Product
    def body(sum, product, n):
        return (sum + n, product * n)

    # Use a different variable name to avoid conflict
    final_result = for_fold(
        accumulators=[("sum", 0), ("product", 1)],
        iterables=[("n", numbers)],
        body=body,
        result=lambda sum, product: (sum, product)
    )

    print(f"Sum: {final_result[0]}, Product: {final_result[1]}")  # Output: Sum: 15, Product: 120
