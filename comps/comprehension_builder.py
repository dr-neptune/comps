from comps.operations import AddAccumulator, AddIterable, SetFilter, SetResult, SetBody
from typing import Callable, Any, Iterable
from dataclasses import dataclass

@dataclass
class ComprehensionBuilder:
    accumulators: list = None
    iterables: list = None
    filter_function: Callable[..., bool] = None
    result_name: str = None
    body_functions: list = None

    def __post_init__(self):
        self.accumulators = []
        self.iterables = []
        self.filter_function = lambda **kwargs: True  # Default filter: always True
        self.result_name = None
        self.body_functions = []

    def __rshift__(self, other):
        match other:
            case AddAccumulator(name=name, initial_value=initial_value):
                self.accumulators.append((name, initial_value))
            case AddIterable(name=name, iterable=iterable):
                self.iterables.append((name, iterable))
            case SetFilter(filter_function=filter_function):
                self.filter_function = filter_function
            case SetResult(result_name=result_name):
                self.result_name = result_name
            case SetBody(body_function=body_function):
                self.body_functions.append(body_function)
            case _:
                raise ValueError(f"Unsupported operation: {other}")
        return self

    def run(self):
        if not self.body_functions:
            raise ValueError("Body function must be set before running the comprehension.")

        if self.result_name is None:
            # Default result: return all accumulator values as a dictionary
            def default_result(**kwargs):
                return {name: kwargs[name] for name, _ in self.accumulators}
        else:
            # Custom result: return the specified accumulator
            def default_result(**kwargs):
                return kwargs[self.result_name]

        # Initialize the environment with accumulators
        env = {name: value for name, value in self.accumulators}

        # Prepare iterators for the iterables
        iterators = [iterable for _, iterable in self.iterables]
        iterable_names = [name for name, _ in self.iterables]
        accumulator_names = [name for name, _ in self.accumulators]

        # Iterate over the zipped iterables
        for values in zip(*iterators):
            # Current variables include accumulators and iterables
            current_vars = {**env, **dict(zip(iterable_names, values))}

            # Apply the filter function
            if not self.filter_function(**current_vars):
                continue  # Skip this iteration if filter condition is not met

            # Apply each body function and collect updates
            updates = []
            for body_fn in self.body_functions:
                updated_value = body_fn(**current_vars)
                updates.append(updated_value)

            # Update the accumulators in order
            for i, value in enumerate(updates):
                acc_name = accumulator_names[i]
                env[acc_name] = value

        # Prepare final variables for the result function
        final_vars = {**env, **{name: None for name in iterable_names}}

        # Return the result using the result function
        return default_result(**final_vars)
