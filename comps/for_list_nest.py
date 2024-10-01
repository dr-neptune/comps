from typing import Iterable, Callable, Any, List, Tuple
import itertools

def for_list_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> List[Any]:
    """
    Collects results into a list using nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]
    result = []

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            item = body(**vars)
            result.append(item)
    return result

# Example usage
if __name__ == "__main__":
    numbers = [1, 2]
    letters = ['a', 'b']

    def make_pair(i, j):
        return (i, j)

    pairs = for_list_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=make_pair
    )
    print(f"Nested pairs: {pairs}")  # Output: Nested pairs: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
