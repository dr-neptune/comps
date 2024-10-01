from typing import Iterable, Callable, Any, Dict, Tuple, List
import itertools

def for_dict_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Tuple[Any, Any]],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Dict[Any, Any]:
    """
    Collects results into a dictionary using nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]
    result = {}

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            key, value = body(**vars)
            result[key] = value
    return result

# Example usage
if __name__ == "__main__":
    keys = ['x', 'y']
    values = [10, 20]

    def make_entry(k, v):
        return (k, v)

    dictionary = for_dict_nest(
        iterables=[("k", keys), ("v", values)],
        body=make_entry
    )
    print(f"Nested dictionary: {dictionary}")
    # Output: Nested dictionary: {'x': 20, 'y': 20}
