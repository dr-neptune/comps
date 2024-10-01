from typing import Iterable, Callable, Any, Tuple, List
import itertools

def for_tuple_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Tuple[Any, ...]:
    """
    Collects results into a tuple using nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]
    result = []

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            item = body(**vars)
            result.append(item)
    return tuple(result)

# Example usage
if __name__ == "__main__":
    numbers = [1, 2]
    letters = ['a', 'b']

    def combine(i, j):
        return f"{i}{j}"

    combined = for_tuple_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=combine
    )
    print(f"Nested combined tuple: {combined}")
    # Output: Nested combined tuple: ('1a', '1b', '2a', '2b')
