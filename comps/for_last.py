from typing import Iterable, Callable, Any, List, Tuple, Optional

def for_last(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Optional[Any]:
    """
    Returns the last value returned by the body function that satisfies the when condition.
    If no item satisfies the condition, returns None.
    """
    last_value = None
    found = False
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in zip(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            last_value = body(**vars)
            found = True
    return last_value if found else None

# Example usage
if __name__ == "__main__":
    numbers = [2, 4, 5, 7, 8]

    def cube(n):
        return n ** 3

    def is_odd(n):
        return n % 2 == 1

    last_odd_cube = for_last(
        iterables=[("n", numbers)],
        body=cube,
        when=is_odd
    )
    print(f"Last odd cube: {last_odd_cube}")  # Output: Last odd cube: 343
