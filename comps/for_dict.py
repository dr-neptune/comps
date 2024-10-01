from comps.for_fold import for_fold
from typing import Iterable, Callable, Any, Dict, List, Tuple

def for_dict(
    iterables: List[Tuple[str, Iterable]],
    key_fn: Callable[..., Any],
    value_fn: Callable[..., Any]
) -> Dict[Any, Any]:
    """
    Equivalent to Racket's for/dict.

    :param iterables: List of tuples (name, iterable) for iteration.
    :param key_fn: Function that generates the key based on iterable variables.
    :param value_fn: Function that generates the value based on iterable variables.
    :return: Dictionary of generated key-value pairs.
    """
    # Define body function: take current 'result' and iterable variables, add key-value pair
    def body_add(result, **vars):
        key = key_fn(**vars)
        value = value_fn(**vars)
        return {**result, key: value}

    # Run for_fold with single accumulator 'result'
    return for_fold(
        accumulators=[("result", {})],
        iterables=iterables,
        body=(body_add,),
        result="result"
    )

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Example 1: Create a dict mapping numbers to their squares
    def key_fn(n):
        return n

    def value_fn(n):
        return n * n

    result = for_dict(
        iterables=[("n", numbers)],
        key_fn=key_fn,
        value_fn=value_fn
    )
    print(f"Example 1 Result: {result}")  # Output: Example 1 Result: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

    # Example 2: Create a dict mapping numbers to their string representations
    def key_fn_str(n):
        return n

    def value_fn_str(n):
        return str(n)

    result2 = for_dict(
        iterables=[("n", numbers)],
        key_fn=key_fn_str,
        value_fn=value_fn_str
    )
    print(f"Example 2 Result: {result2}")  # Output: Example 2 Result: {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}

    # Example 3: Mapping numbers to their factorial (using a simple factorial function)
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result

    def key_fn_fact(n):
        return n

    def value_fn_fact(n):
        return factorial(n)

    result3 = for_dict(
        iterables=[("n", numbers)],
        key_fn=key_fn_fact,
        value_fn=value_fn_fact
    )
    print(f"Example 3 Result: {result3}")  # Output: Example 3 Result: {1: 1, 2: 2, 3: 6, 4: 24, 5: 120}
