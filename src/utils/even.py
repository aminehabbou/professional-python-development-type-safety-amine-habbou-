import sys


def is_number_even(number: int) -> bool:
    return number % 2 == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} number")
        sys.exit(1)

    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Error: Argument must be an integer")
        sys.exit(1)

    result = is_number_even(number)
    print(f"{number} is {'even' if result else 'odd'}")
