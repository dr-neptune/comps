from typing import Callable, Any, Iterable, List, Tuple
from functools import reduce
import itertools

def for_fold_nest(
    accumulators: List[Tuple[str, Any]],
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Tuple[Any, ...]],
    *,
    when: Callable[..., bool] = lambda **kwargs: True,
    result: Callable[..., Any] = None
) -> Any:
    """
    Nested version of for_fold, performing nested iterations over iterables.
    """
    env = {name: initial for name, initial in accumulators}
    accumulator_names = [name for name, _ in accumulators]
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        current_vars = {**env, **dict(zip(iterable_names, values))}

        if when(**current_vars):
            updated_values = body(**current_vars)
            if not isinstance(updated_values, tuple):
                raise TypeError("Body function must return a tuple of accumulator values.")
            if len(updated_values) != len(accumulator_names):
                raise ValueError("Body function must return a value for each accumulator.")
            for name, value in zip(accumulator_names, updated_values):
                env[name] = value
    if result:
        return result(**env)
    else:
        return {name: env[name] for name in accumulator_names}

# Example usage
if __name__ == "__main__":
    numbers = [1, 2]
    letters = ['a', 'b']

    def body(sum, i, j):
        return (sum + ord(j) * i,)

    result = for_fold_nest(
        accumulators=[("sum", 0)],
        iterables=[("i", numbers), ("j", letters)],
        body=body,
        result=lambda sum: sum
    )

    print(f"Resulting sum: {result}")  # Output: Resulting sum: 390
