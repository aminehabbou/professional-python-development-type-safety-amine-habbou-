import sys


def arrange_name(first: str, last: str) -> str:
    return f"{first} {last}".title()


if __name__ == "__main__":
    # Validate argument count (expecting 2 names + script name = 3 total)
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} first_name last_name")
        sys.exit(1)

    # Get arguments (no type conversion needed since we expect strings)
    first_name = sys.argv[1]
    last_name = sys.argv[2]

    # Call function and print result
    result = arrange_name(first_name, last_name)
    print(result)
