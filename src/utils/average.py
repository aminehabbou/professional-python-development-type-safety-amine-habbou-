import sys
from typing import Sequence


def calculate_average(numbers: Sequence[float]) -> float:
    return sum(numbers) / len(numbers) if numbers else 0.0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} number1 number2 ...")
        print("Example: python script.py 10 20 30 40")
        sys.exit(1)

    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("Error: All arguments must be numbers")
        sys.exit(1)

    result = calculate_average(numbers)
    print(f"Average: {result}")
