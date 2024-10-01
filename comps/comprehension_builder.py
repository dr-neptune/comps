from comps.operations import AddAccumulator, AddIterable, SetFilter, SetResult, SetBody
from typing import Callable, Any, Iterable
from dataclasses import dataclass


@dataclass
class ComprehensionBuilder:
    accumulators: list = None
    iterables: list = None
    filter_function: Callable = None
    result_function: Callable = None
    body_function: Callable = None

    def __post_init__(self):
        self.accumulators = []
        self.iterables = []
        self.filter_function = lambda **kwargs: True
        self.result_function = None
        self.body_function = None

    def __rshift__(self, other):
        match other:
            case AddAccumulator(name=name, initial_value=initial_value):
                self.accumulators.append((name, initial_value))
            case AddIterable(name=name, iterable=iterable):
                self.iterables.append((name, iterable))
            case SetFilter(filter_function=filter_function):
                self.filter_function = filter_function
            case SetResult(result_function=result_function):
                self.result_function = result_function
            case SetBody(body_function=body_function):
                self.body_function = body_function
            case _:
                raise ValueError(f"Unsupported operation: {other}")
        return self
    def run(self):
        if self.body_function is None:
            raise ValueError("Body function must be set before running the comprehension.")
        if self.result_function is None:
            # Default result: return all accumulator values
            self.result_function = lambda **kwargs: [kwargs[name] for name, _ in self.accumulators]

        # Initialize the environment with accumulators
        env = {name: value for name, value in self.accumulators}

        # Prepare the iterators for the iterables
        iterators = [iterable for _, iterable in self.iterables]
        iterable_names = [name for name, _ in self.iterables]
        accumulator_names = [name for name, _ in self.accumulators]

        # Zip the iterators and iterate over them simultaneously
        for values in zip(*iterators):
            # Create a dict of current variables (accumulators + iterables)
            current_vars = {**env, **dict(zip(iterable_names, values))}
            # Apply the filter function
            if not self.filter_function(**current_vars):
                continue
            # Call the body function and get updates
            updates = self.body_function(**current_vars)
            # Update the accumulators
            for key, value in updates.items():
                if key in env:
                    env[key] = value
                else:
                    raise ValueError(f"Invalid accumulator name in updates: {key}")

        # Prepare final variables for the result function
        final_vars = {**env, **{name: None for name in iterable_names}}

        # Pass all variables as keyword arguments to the result function
        return self.result_function(**final_vars)
