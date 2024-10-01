import timeit
from comps.for_fold import for_fold
from comps.for_list import for_list
from comps.for_set import for_set
from comps.for_dict import for_dict
from comps.for_tuple import for_tuple
from comps.for_generator import for_generator
from comps.for_and import for_and
from comps.for_or import for_or
from comps.for_sum import for_sum
from comps.for_product import for_product
from comps.for_first import for_first
from comps.for_last import for_last
from comps.for_fold_nest import for_fold_nest
from comps.for_list_nest import for_list_nest
from comps.for_dict_nest import for_dict_nest
from comps.for_tuple_nest import for_tuple_nest
from comps.for_generator_nest import for_generator_nest
from comps.for_and_nest import for_and_nest
from comps.for_or_nest import for_or_nest
from comps.for_sum_nest import for_sum_nest
from comps.for_product_nest import for_product_nest
from comps.for_first_nest import for_first_nest
from comps.for_last_nest import for_last_nest

# Sample data for testing
numbers = list(range(1, 100))
letters = ['a', 'b', 'c', 'd']

# Define functions to benchmark
def benchmark_for_fold():
    def body(sum, n):
        return (sum + n,)
    for_fold(
        accumulators=[("sum", 0)],
        iterables=[("n", numbers)],
        body=body,
        result=lambda sum: sum
    )

def benchmark_for_list():
    for_list(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_set():
    for_set(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_dict():
    for_dict(
        iterables=[("n", numbers)],
        body=lambda n: (n, n * n)
    )

def benchmark_for_tuple():
    for_tuple(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_generator():
    list(for_generator(
        iterables=[("n", numbers)],
        body=lambda n: n
    ))

def benchmark_for_and():
    for_and(
        iterables=[("n", numbers)],
        predicate=lambda n: n % 2 == 0
    )

def benchmark_for_or():
    for_or(
        iterables=[("n", numbers)],
        predicate=lambda n: n % 2 == 0
    )

def benchmark_for_sum():
    for_sum(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_product():
    for_product(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_first():
    for_first(
        iterables=[("n", numbers)],
        body=lambda n: n,
        when=lambda n: n == 50
    )

def benchmark_for_last():
    for_last(
        iterables=[("n", numbers)],
        body=lambda n: n
    )

def benchmark_for_fold_nest():
    def body(sum, i, j):
        return (sum + ord(j) * i,)
    for_fold_nest(
        accumulators=[("sum", 0)],
        iterables=[("i", numbers), ("j", letters)],
        body=body,
        result=lambda sum: sum
    )

def benchmark_for_list_nest():
    for_list_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, j)
    )

def benchmark_for_dict_nest():
    for_dict_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, ord(j))
    )

def benchmark_for_tuple_nest():
    for_tuple_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, j)
    )

def benchmark_for_generator_nest():
    list(for_generator_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, j)
    ))

def benchmark_for_and_nest():
    for_and_nest(
        iterables=[("i", numbers), ("j", letters)],
        predicate=lambda i, j: i % 2 == 0
    )

def benchmark_for_or_nest():
    for_or_nest(
        iterables=[("i", numbers), ("j", letters)],
        predicate=lambda i, j: i % 2 == 0
    )

def benchmark_for_sum_nest():
    for_sum_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: ord(j) * i
    )

def benchmark_for_product_nest():
    for_product_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: ord(j) * i
    )

def benchmark_for_first_nest():
    for_first_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, j),
        when=lambda i, j: i == 50 and j == 'b'
    )

def benchmark_for_last_nest():
    for_last_nest(
        iterables=[("i", numbers), ("j", letters)],
        body=lambda i, j: (i, j)
    )

# List of benchmark functions
benchmarks = [
    ("for_fold", benchmark_for_fold),
    ("for_list", benchmark_for_list),
    ("for_set", benchmark_for_set),
    ("for_dict", benchmark_for_dict),
    ("for_tuple", benchmark_for_tuple),
    ("for_generator", benchmark_for_generator),
    ("for_and", benchmark_for_and),
    ("for_or", benchmark_for_or),
    ("for_sum", benchmark_for_sum),
    ("for_product", benchmark_for_product),
    ("for_first", benchmark_for_first),
    ("for_last", benchmark_for_last),
    ("for_fold_nest", benchmark_for_fold_nest),
    ("for_list_nest", benchmark_for_list_nest),
    ("for_dict_nest", benchmark_for_dict_nest),
    ("for_tuple_nest", benchmark_for_tuple_nest),
    ("for_generator_nest", benchmark_for_generator_nest),
    ("for_and_nest", benchmark_for_and_nest),
    ("for_or_nest", benchmark_for_or_nest),
    ("for_sum_nest", benchmark_for_sum_nest),
    ("for_product_nest", benchmark_for_product_nest),
    ("for_first_nest", benchmark_for_first_nest),
    ("for_last_nest", benchmark_for_last_nest),
]

# Run benchmarks
for name, func in benchmarks:
    time_taken = timeit.timeit(func, number=100)
    print(f"{name}: {time_taken:.6f} seconds (for 100 iterations)")
