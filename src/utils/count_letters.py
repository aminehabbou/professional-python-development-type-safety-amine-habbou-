import sys


def count_letters(string: str) -> int:
    letter_count = len(string)
    print(f"The string '{string}' has {letter_count} characters.")
    return letter_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} string_to_count")
        sys.exit(1)

    input_string = sys.argv[1]

    result = count_letters(input_string)
