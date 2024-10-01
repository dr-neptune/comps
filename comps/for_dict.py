from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, Dict, Tuple, List

def for_dict(
    iterables: List[Tuple[str, Iterable]],
    body: Callable[..., Tuple[Any, Any]],
    *,
    when: Callable[..., bool] = lambda **kwargs: True
) -> Dict[Any, Any]:
    """
    Collects results into a dictionary.
    """
    def comprehension_body(result, **vars):
        key, value = body(**vars)
        result[key] = value
        return (result,)

    result = for_fold(
        accumulators=[("result", {})],
        iterables=iterables,
        body=comprehension_body,
        when=when,
        result=lambda result: result
    )
    return result

# Example usage
if __name__ == "__main__":
    words = ["apple", "banana", "cherry"]

    def word_length(word):
        return (word, len(word))

    word_lengths = for_dict(
        iterables=[("word", words)],
        body=word_length
    )
    print(f"Word lengths: {word_lengths}")  # Output: Word lengths: {'apple': 5, 'banana': 6, 'cherry': 6}

    # Example with numbers
    numbers = [1, 2, 3, 4, 5]

    def number_square(n):
        return (n, n * n)

    number_squares = for_dict(
        iterables=[("n", numbers)],
        body=number_square
    )
    print(f"Number squares: {number_squares}")  # Output: Number squares: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
