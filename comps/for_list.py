from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, List, Tuple

def for_list(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> List[Any]:
    """
    Collects results into a list.
    """
    def comprehension_body(result, **vars):
        item = body(**vars)
        return (result + [item],)

    # Use a different variable name to store the result
    final_result = for_fold(
        accumulators=[("result", [])],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda result: result
    )
    return final_result


# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    def square(n):
        return n * n

    # Again, use a different variable name
    squares = for_list(
        iterables=[("n", numbers)],
        body=square
    )
    print(f"Squares: {squares}")  # Output: Squares: [1, 4, 9, 16, 25]
