import time
from typing import Any, Callable, List, TypeVar

import numpy as np

# Add type variables for better typing
T = TypeVar("T")
R = TypeVar("R")


# FIXED: Added proper type parameters to Callable
def measure_time(func: Callable[..., R]) -> Callable[..., R]:
    # FIXED: Added type annotations for arguments
    def wrapper(*args: Any, **kwargs: Any) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time  # type: ignore

    return wrapper


# Scalar-vector multiplication with plain Python list
@measure_time
def python_scalar_multiply(scalar: float, vector: List[float]) -> List[float]:
    return [scalar * x for x in vector]


# Scalar-vector multiplication with NumPy array
@measure_time
def numpy_scalar_multiply(scalar: float, vector: np.ndarray) -> np.ndarray:
    return scalar * vector


def main() -> None:
    # Define the size of our vectors
    size = 1000000  # 1 million elements

    print(f"Comparing scalar-vector multiplication for {size:,} elements")
    print("=" * 60)

    # Create data
    print("Creating data structures...")

    # Plain Python list
    python_list = [float(i) for i in range(size)]
    print(f"Python list created with {len(python_list)} elements")

    # NumPy array
    numpy_array = np.arange(size, dtype=np.float64)
    print(f"NumPy array created with {numpy_array.size} elements")

    # Scalar value
    scalar = 2.5

    print("Data structures created successfully!\n")

    iterations = 10

    print("Python List Timings:")
    print("-" * 20)
    # Python list timing
    python_times = []
    for i in range(iterations):
        start = time.perf_counter()
        _ = python_scalar_multiply(scalar, python_list)
        end = time.perf_counter()
        iteration_time = end - start
        python_times.append(iteration_time)
        print(f"Iteration {i + 1}: {iteration_time:.6f} seconds")

    print("\nNumPy Array Timings:")
    print("-" * 20)
    # NumPy array timing
    numpy_times = []
    for i in range(iterations):
        start = time.perf_counter()
        _ = numpy_scalar_multiply(scalar, numpy_array)
        end = time.perf_counter()
        iteration_time = end - start
        numpy_times.append(iteration_time)
        print(f"Iteration {i + 1}: {iteration_time:.6f} seconds")

    # Calculate averages
    avg_python_time = sum(python_times) / len(python_times)
    avg_numpy_time = sum(numpy_times) / len(numpy_times)

    # Print the average timing values
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(
        f"Average Python list time ({iterations} runs): {avg_python_time:.6f} seconds"
    )
    print(f"Average NumPy array time ({iterations} runs): {avg_numpy_time:.6f} seconds")

    speed = avg_python_time / avg_numpy_time
    print(f"NumPy is {speed:.1f}x faster than plain Python lists!")
    print("=" * 60)


if __name__ == "__main__":
    main()
