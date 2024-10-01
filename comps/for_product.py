from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, List, Tuple

def for_product(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Any:
    """
    Multiplies the values returned by the body function over the iterables.
    """
    def comprehension_body(product, **vars):
        return (product * body(**vars),)

    result = for_fold(
        accumulators=[("product", 1)],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda product: product
    )
    return result

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4]

    def identity(n):
        return n

    total_product = for_product(
        iterables=[("n", numbers)],
        body=identity
    )
    print(f"Product of numbers: {total_product}")  # Output: Product of numbers: 24

    # Product of squares
    def square(n):
        return n * n

    product_squares = for_product(
        iterables=[("n", numbers)],
        body=square
    )
    print(f"Product of squares: {product_squares}")  # Output: Product of squares: 576
