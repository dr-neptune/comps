from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, List, Tuple

def for_sum(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Any:
    """
    Sums up the values returned by the body function over the iterables.
    """
    def comprehension_body(sum, **vars):
        return (sum + body(**vars),)

    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda sum: sum
    )
    return result

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    def identity(n):
        return n

    total = for_sum(
        iterables=[("n", numbers)],
        body=identity
    )
    print(f"Sum of numbers: {total}")  # Output: Sum of numbers: 15

    # Sum of squares
    def square(n):
        return n * n

    total_squares = for_sum(
        iterables=[("n", numbers)],
        body=square
    )
    print(f"Sum of squares: {total_squares}")  # Output: Sum of squares: 55
