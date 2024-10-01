from typing import Iterable, Callable, Any, List, Tuple
import itertools

def for_or_nest(
    iterables: List[Tuple[str, Iterable]],
    predicate: Callable[..., bool],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> bool:
    """
    Returns True if the predicate is True for any combination in nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars) and predicate(**vars):
            return True
    return False

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    chars = ['a', 'b']

    def predicate(i, j):
        return i == 2 and j == 'b'

    result = for_or_nest(
        iterables=[("i", nums), ("j", chars)],
        predicate=predicate
    )
    print(f"Any combination satisfies the predicate: {result}")  # Output: True
