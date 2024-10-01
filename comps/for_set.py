from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, Set, List, Tuple

def for_set(
    iterables: List[Tuple[str, Iterable]],
    generator_fn: Callable[..., Any]
) -> Set[Any]:
    """
    Equivalent to Racket's for/set.

    :param iterables: List of tuples (name, iterable) for iteration.
    :param generator_fn: Function that generates an item based on iterable variables.
    :return: Set of generated items.
    """
    # Define body function: take current 'result' and iterable variables, add generated item
    def body_add(result, **vars):
        item = generator_fn(**vars)
        return result | {item}

    # Run for_fold with single accumulator 'result'
    return for_fold(
        accumulators=[("result", set())],
        iterables=iterables,
        body=(body_add,),
        result="result"
    )

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 2, 3, 4, 4, 5]

    # Example 1: Create a set of unique numbers
    def identity(n):
        return n

    result = for_set(
        iterables=[("n", numbers)],
        generator_fn=identity
    )
    print(f"Example 1 Result: {result}")  # Output: Example 1 Result: {1, 2, 3, 4, 5}

    # Example 2: Create a set of squares
    def square(n):
        return n * n

    result2 = for_set(
        iterables=[("n", numbers)],
        generator_fn=square
    )
    print(f"Example 2 Result: {result2}")  # Output: Example 2 Result: {1, 4, 9, 16, 25}
