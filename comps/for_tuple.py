from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, Tuple, List

def for_tuple(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Tuple[Any, ...]:
    """
    Collects results into a tuple.
    """
    def comprehension_body(result, **vars):
        item = body(**vars)
        return (result + (item,),)

    result = for_fold(
        accumulators=[("result", ())],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda result: result
    )
    return result

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3]

    def cube(n):
        return n ** 3

    cubes = for_tuple(
        iterables=[("n", numbers)],
        body=cube
    )
    print(f"Cubes: {cubes}")  # Output: Cubes: (1, 8, 27)
