from typing import Iterable, Callable, Any, Generator, Tuple, List

def for_generator(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Any],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Generator[Any, None, None]:
    """
    Returns a generator that yields results.
    """
    iterable_names = [name for name, _ in iterables]
    iterable_values = [iterable for _, iterable in iterables]

    def generator():
        for values in zip(*iterable_values):
            vars = dict(zip(iterable_names, values))
            if when(**vars):
                yield body(**vars)

    return generator()

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    def is_even(n):
        return n % 2 == 0

    def double(n):
        return n * 2

    even_doubles = for_generator(
        iterables=[("n", numbers)],
        body=double,
        when=is_even
    )

    print(f"Even doubles: {list(even_doubles)}")  # Output: Even doubles: [4, 8]
