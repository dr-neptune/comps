from typing import Iterable, Callable, Any, List, Tuple

def for_and(
    iterables: List[Tuple[str, Iterable]],
    predicate: Callable[..., bool],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> bool:
    """
    Returns True if the predicate is True for all items, False otherwise.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in zip(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            if not predicate(**vars):
                return False
    return True

# Example usage
if __name__ == "__main__":
    numbers = [2, 4, 6, 8]

    def is_even(n):
        return n % 2 == 0

    all_even = for_and(
        iterables=[("n", numbers)],
        predicate=is_even
    )
    print(f"All numbers are even: {all_even}")  # Output: All numbers are even: True

    numbers_with_odd = [2, 3, 6, 8]
    all_even = for_and(
        iterables=[("n", numbers_with_odd)],
        predicate=is_even
    )
    print(f"All numbers are even: {all_even}")  # Output: All numbers are even: False
