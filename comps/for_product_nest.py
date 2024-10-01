from typing import Iterable, Callable, Any, List, Tuple
import itertools
from functools import reduce
import operator

def for_product_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Any:
    """
    Multiplies the values returned by the body function over nested iterations.
    """
    products = []
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    for values in itertools.product(*iterable_values):
        vars = dict(zip(iterable_names, values))
        if when(**vars):
            products.append(body(**vars))
    return reduce(operator.mul, products, 1)

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    exponents = [3, 4]

    def power(i, j):
        return i ** j

    total_product = for_product_nest(
        iterables=[("i", nums), ("j", exponents)],
        body=power
    )
    print(f"Total product: {total_product}")  # Output: Total product: 4096
