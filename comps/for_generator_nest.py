from typing import Iterable, Callable, Any, Generator, Tuple, List
import itertools

def for_generator_nest(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Generator[Any, None, None]:
    """
    Returns a generator that yields results using nested iterations.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    def generator():
        for values in itertools.product(*iterable_values):
            vars = dict(zip(iterable_names, values))
            if when(**vars):
                yield body(**vars)
    return generator()

# Example usage
if __name__ == "__main__":
    nums = [1, 2]
    chars = ['a', 'b']

    def create_pair(i, j):
        return (i, j)

    gen = for_generator_nest(
        iterables=[("i", nums), ("j", chars)],
        body=create_pair
    )
    print("Generated pairs:")
    for item in gen:
        print(item)
    # Output:
    # Generated pairs:
    # (1, 'a')
    # (1, 'b')
    # (2, 'a')
    # (2, 'b')
