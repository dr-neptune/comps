from typing import Iterable, Callable, Any, Generator, List, Tuple

def for_generator(
    iterables: List[Tuple[str, Iterable]],
    generator_fn: Callable[..., Any]
) -> Generator[Any, None, None]:
    """
    Equivalent to Racket's for/generator, returning a generator object.

    :param iterables: List of tuples (name, iterable) for iteration.
    :param generator_fn: Function that generates an item based on iterable variables.
    :return: Generator object that yields generated items lazily.
    """
    # Generator function that yields results
    def generator():
        for values in zip(*[it[1] for it in iterables]):
            vars = {name: value for (name, _), value in zip(iterables, values)}
            yield generator_fn(**vars)

    return generator()

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Example 1: Create a generator of squares
    def square(n):
        return n * n

    gen = for_generator(
        iterables=[("n", numbers)],
        generator_fn=square
    )
    print(f"Example 1 Result: {list(gen)}")  # Output: Example 1 Result: [1, 4, 9, 16, 25]

    # Example 2: Create a generator of (a, b) pairs
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]

    def make_tuple(a, b):
        return (a, b)

    gen2 = for_generator(
        iterables=[("a", list1), ("b", list2)],
        generator_fn=make_tuple
    )
    print(f"Example 2 Result: {list(gen2)}")  # Output: Example 2 Result: [(1, 10), (2, 20), (3, 30)]
