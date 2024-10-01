from cytoolz import reduce, sliding_window
from typing import Any, Callable, Dict, List, Tuple

def for_fold(
    accumulators: List[Tuple[str, Any]],
    iterables: List[Tuple[str, Any]],
    body: Callable,
    *,
    when: Callable[[Dict[str, Any]], bool] = lambda env: True,
    result: Callable[[Dict[str, Any]], Any] = lambda env: [env[name] for name, _ in accumulators]
) -> Any:
    """
    A Python implementation of Racket's for/fold.

    :param accumulators: List of tuples (name, initial_value) for accumulators.
    :param iterables: List of tuples (name, iterable) for iteration.
    :param body: Function that updates accumulators.
    :param when: Optional filter function.
    :param result: Function to compute the final result.
    :return: The result computed by the result function.
    """
    # Initialize the environment with accumulators
    env = {name: value for name, value in accumulators}
    # Prepare the iterators
    iterators = [iterable for _, iterable in iterables]
    names = [name for name, _ in iterables]
    # Zip the iterators to loop over them simultaneously
    for values in zip(*iterators):
        # Update the environment with the current values
        env.update(dict(zip(names, values)))
        # Apply the filter
        if not when(env):
            continue
        # Update the accumulators using the body function
        updates = body(env)
        env.update(updates)
    # Compute the final result
    return result(env)


if __name__ == '__main__':
    # Example 1: One accumulator over one iterable
    numbers = [1, 2, 3, 4, 5]
    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=lambda env: {"sum": env["sum"] + env["n"]},
        result=lambda env: env["sum"]
    )
    print(f"Example 1 Result: {result}")

    # Example 2: Two accumulators over two iterables
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]
    result = for_fold(
        accumulators=[("sum1", 0), ("sum2", 0)],
        iterables=[("a", list1), ("b", list2)],
        body=lambda env: {"sum1": env["sum1"] + env["a"], "sum2": env["sum2"] + env["b"]},
        result=lambda env: (env["sum1"], env["sum2"])
    )
    print(f"Example 2 Result: {result}")  # Should print (6, 60)

    # Example 3: Filter with 'when' (only sum even numbers)
    numbers = [1, 2, 3, 4, 5]
    result = for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=lambda env: {"sum": env["sum"] + env["n"]},
        when=lambda env: env["n"] % 2 == 0,  # Filter to only include even numbers
        result=lambda env: env["sum"]
    )
    print(f"Example 3 Result: {result}")  # Should print 6 (2 + 4)

    # Example 4: Custom result (sum and product of numbers)
    numbers = [1, 2, 3, 4]
    result = for_fold(
        accumulators=[("sum", 0), ("product", 1)],
        iterables=[("n", numbers)],
        body=lambda env: {"sum": env["sum"] + env["n"], "product": env["product"] * env["n"]},
        result=lambda env: f"Sum: {env['sum']}, Product: {env['product']}"
    )
    print(f"Example 4 Result: {result}")  # Should print "Sum: 10, Product: 24"
