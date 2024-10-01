from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, List, Tuple

def for_tuple(
    iterables: List[Tuple[str, Iterable]],
    generator_fn: Callable[..., Any]
) -> Tuple[Any, ...]:
    """
    Equivalent to Racket's for/list but returning a tuple instead.

    :param iterables: List of tuples (name, iterable) for iteration.
    :param generator_fn: Function that generates an item based on iterable variables.
    :return: Tuple of generated items.
    """
    # Define body function: take current 'result' and iterable variables, append generated item
    def body_append(result, **vars):
        item = generator_fn(**vars)
        return result + (item,)

    # Run for_fold with single accumulator 'result'
    return for_fold(
        accumulators=[("result", ())],  # Initialize an empty tuple
        iterables=iterables,
        body=(body_append,),
        result="result"
    )

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Example 1: Create a tuple of squares
    def square(n):
        return n * n

    result = for_tuple(
        iterables=[("n", numbers)],
        generator_fn=square
    )
    print(f"Example 1 Result: {result}")  # Output: Example 1 Result: (1, 4, 9, 16, 25)

    # Example 2: Create a tuple of (a, b) pairs
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    def make_tuple(a, b):
        return (a, b)

    result2 = for_tuple(
        iterables=[("a", list1), ("b", list2)],
        generator_fn=make_tuple
    )
    print(f"Example 2 Result: {result2}")  # Output: Example 2 Result: ((1, 10), (2, 20), (3, 30))
