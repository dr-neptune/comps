from typing import Iterable, Callable, Any, List, Tuple, Optional
import itertools

def for_last_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Optional[Any]:
    """
    Returns the last value returned by the body function that satisfies the when condition in nested iterations.
    """
    last_value = None
    found = False
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            last_value = body(**vars)
            found = True
    return last_value if found else None

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    chars = ['a', 'b']

    def create_pair(i, j):
        return (i, j)

    def condition(i, j):
        return True  # Accept all combinations

    last_pair = for_last_nest(
        iterables=[("i", nums), ("j", chars)],
        body=create_pair,
        when=condition
    )
    print(f"Last pair: {last_pair}")  # Output: Last pair: (2, 'b')
