from typing import Iterable, Callable, Any, List, Tuple, Optional
import itertools

def for_first_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Optional[Any]:
    """
    Returns the first value returned by the body function that satisfies the when condition in nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            return body(**vars)
    return None

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    chars = ['a', 'b']

    def create_pair(i, j):
        return (i, j)

    def condition(i, j):
        return i == 2 and j == 'b'

    first_match = for_first_nest(
        iterables=[("i", nums), ("j", chars)],
        body=create_pair,
        when=condition
    )
    print(f"First matching pair: {first_match}")  # Output: First matching pair: (2, 'b')
