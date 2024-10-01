from typing import Iterable, Callable, Any, List, Tuple

def for_or(
    iterables: List[Tuple[str, Iterable]],
    predicate: Callable[..., bool],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> bool:
    """
    Returns True if the predicate is True for any item, False otherwise.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in zip(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            if predicate(**vars):
                return True
    return False

# Example usage
if __name__ == "__main__":
    numbers = [1, 3, 5, 7]

    def is_even(n):
        return n % 2 == 0

    any_even = for_or(
        iterables=[("n", numbers)],
        predicate=is_even
    )
    print(f"Any number is even: {any_even}")  # Output: Any number is even: False

    numbers_with_even = [1, 3, 4, 7]
    any_even = for_or(
        iterables=[("n", numbers_with_even)],
        predicate=is_even
    )
    print(f"Any number is even: {any_even}")  # Output: Any number is even: True
