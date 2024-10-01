from typing import Iterable, Callable, Any, List, Tuple
import itertools

def for_and_nest(
    iterables: List[Tuple[str, Iterable]],
    predicate: Callable[..., bool],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> bool:
    """
    Returns True if the predicate is True for all combinations in nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars) and not predicate(**vars):
            return False
    return True

# Example usage
if __name__ == "__main__":
    nums = [2, 4]
    chars = ['a', 'b']

    def predicate(i, j):
        return i % 2 == 0  # Check if number is even (always true in this case)

    result = for_and_nest(
        iterables=[("i", nums), ("j", chars)],
        predicate=predicate
    )
    print(f"All combinations satisfy the predicate: {result}")  # Output: True
