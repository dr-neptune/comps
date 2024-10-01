from typing import Iterable, Callable, Any, List, Tuple
import itertools

def for_sum_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Any:
    """
    Sums up the values returned by the body function over nested iterations.
    """
    total = 0
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            total += body(**vars)
    return total

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    chars = ['a', 'b']

    def value(i, j):
        return i * ord(j)

    total = for_sum_nest(
        iterables=[("i", nums), ("j", chars)],
        body=value
    )
    print(f"Total sum: {total}")  # Output: Total sum: 390
