import sys


def count_letters(string: str) -> int:
    letter_count = len(string)
    print(f"The string '{string}' has {letter_count} characters.")
    return letter_count


if __name__ == "__main__":
    # Validate argument count (expecting 1 string + script name = 2 total)
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} string_to_count")
        sys.exit(1)

    # Get argument (no type conversion needed since we expect string)
    input_string = sys.argv[1]

    # Call function (return value is captured but not used since function prints)
    result = count_letters(input_string)
