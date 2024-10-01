from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, Set, Tuple, List

def for_set(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Set[Any]:
    """
    Collects results into a set.
    """
    def comprehension_body(result, **vars):
        item = body(**vars)
        return (result | {item},)

    result = for_fold(
        accumulators=[("result", set())],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda result: result
    )
    return result

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 2, 3, 4, 4, 5]

    def identity(n):
        return n

    unique_numbers = for_set(
        iterables=[("n", numbers)],
        body=identity
    )
    print(f"Unique numbers: {unique_numbers}")  # Output: Unique numbers: {1, 2, 3, 4, 5}

    # Example with squares
    def square(n):
        return n * n

    unique_squares = for_set(
        iterables=[("n", numbers)],
        body=square
    )
    print(f"Unique squares: {unique_squares}")  # Output: Unique squares: {1, 4, 9, 16, 25}
