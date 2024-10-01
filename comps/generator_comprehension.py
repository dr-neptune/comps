from typing import Callable, Any, Iterable, List, Tuple, Dict

class GeneratorComprehension:
    def __init__(
        self,
        iterables: List[Tuple[str, Iterable]],
        accumulators: List[Tuple[str, Any]],
        body: Callable[..., Tuple[Any, ...]],
        when: Callable[..., bool] = lambda **kwargs: True,
        result: Callable[..., Any] = None
    ):
        self.iterables = iterables
        self.accumulators = accumulators
        self.body = body
        self.when = when
        self.result = result

    def run(self) -> Any:
        # Initialize accumulators
        env = {name: initial for name, initial in self.accumulators}
        accumulator_names = [name for name, _ in self.accumulators]
        iterable_names = [name for name, _ in self.iterables]
        iterables = [iterable for _, iterable in self.iterables]

        # Iterate over the iterables
        for values in zip(*iterables):
            # Update the environment with current iterable values
            current_vars = {**env, **dict(zip(iterable_names, values))}

            # Apply the filter
            if not self.when(**current_vars):
                continue

            # Call the body function
            updated_values = self.body(**current_vars)

            if not isinstance(updated_values, tuple):
                raise TypeError("Body function must return a tuple of accumulator values.")

            if len(updated_values) != len(accumulator_names):
                raise ValueError("Body function must return a value for each accumulator.")

            # Update accumulators
            for name, value in zip(accumulator_names, updated_values):
                env[name] = value

        # Apply the result function if provided
        if self.result:
            return self.result(**env)
        else:
            # Default result is to return the accumulators as a dictionary
            return {name: env[name] for name in accumulator_names}
