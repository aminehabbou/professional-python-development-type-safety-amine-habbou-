import sys
from typing import List


def calculate_average(numbers: List[float]) -> float:
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    # Validate argument count (need at least 1 number + script name = 2 total)
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} number1 number2 ...")
        print("Example: python script.py 10 20 30 40")
        sys.exit(1)

    # Parse arguments and convert to floats
    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("Error: All arguments must be numbers")
        sys.exit(1)

    # Call function and print result
    result = calculate_average(numbers)
    print(f"Average: {result}")
