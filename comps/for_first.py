from typing import Iterable, Callable, Any, List, Tuple, Optional

def for_first(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Optional[Any]:
    """
    Returns the first value returned by the body function that satisfies the when condition.
    If no item satisfies the condition, returns None.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in zip(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            return body(**vars)
    return None

# Example usage
if __name__ == "__main__":
    numbers = [1, 3, 5, 6, 7]

    def square(n):
        return n * n

    def is_even(n):
        return n % 2 == 0

    first_even_square = for_first(
        iterables=[("n", numbers)],
        body=square,
        when=is_even
    )
    print(f"First even square: {first_even_square}")  # Output: First even square: 36
