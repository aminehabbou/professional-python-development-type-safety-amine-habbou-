from typing import Any, Dict, List, Tuple

from utils.arrange import arrange_name
from utils.average import calculate_average
from utils.count_letters import count_letters
from utils.even import is_number_even


def main() -> None:
    print("1. Variables demonstration:")
    name: str = "Lea Vanne"  # string
    age: int = 24  # int
    slist: List[float] = [32.70, 19.80, 2.00, 45.78, 102.90, 88.12, 3.00]  # List
    employee: Dict[str, Any] = {
        "id": 225690,
        "name": "Luca",
        "salary": 4500,
        "age": 22,
        "profession": "cybersecurity engineer",
    }  # Dictionary

    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"slist: {slist}")
    print(f"Employee information: {employee}")

    print("2. Conditionals demonstration")
    average_slist: float = calculate_average(slist)
    print(f"average_slist: {average_slist}")

    if average_slist > 70:
        print("excellent s choice!")
    elif average_slist >= 50:
        print("mild s choice!")
    elif average_slist >= 40:
        print("acceptable s choice!")
    elif average_slist >= 30:
        print("poor s choice!")
    else:
        print("slist is broken!")

    print("3. For loop demonstration:")
    klist: List[int] = [12, 708, 78, 105, 504, 2, 15, 1205]
    print("Printing k in different positions in the klist!")
    for index in range(len(klist)):
        print(f" k{index + 1}: {klist[index]}")

    print("4. While loop demonstration:")
    j: int = 0
    while j < len(klist) and klist[j] < 1200:
        print(f"k's not satisfying the conditions: {klist[j]}")
        j = j + 1

    print("5. Data structures demonstration")
    # List
    candy: List[str] = ["haribo", "chupa-chups", "kent"]
    print(f"candy List: {candy}")
    # Tuple
    coordinates: Tuple[int, int, int] = (10, 20, 44)
    print(f"location coordinates:{coordinates}")
    # Dictionary
    motorcycle: Dict[str, Any] = {
        "name": "honda",
        "insurance": "yes",
        "distance in km": 35079,
    }
    print(f"motorcycle informartion:{motorcycle} ")
    print("6.use enumerate  built-in function:")
    for index, candy_item in enumerate(candy):
        print(f"{index}:{candy_item}")

    print("7. use of id built-in function")
    n1: int = 500
    n2: int = 450
    print(f"id of n1 (500): {id(n1)}")
    print(f"id of n2 (450): {id(n2)}")
    print("after setting n1=n2, both variables will have the same id")
    n1 = n2
    print(f"id of n1: {id(n1)}")
    print(f"id of n2: {id(n2)}")
    print("same thing happens for strings")
    print("before setting name1=name2")
    name1: str = "Bob"
    name2: str = "Alice"
    print(f"id of name1: {id(name1)}")
    print(f"id of name2: {id(name2)}")
    print("after setting name1=name2")
    name1 = name2
    print(f"id of name1: {id(name1)}")
    print(f"id of name2: {id(name2)}")

    print("8. String to int casting")
    list_strings_of_numbers: List[str] = ["8", "10", "5"]
    print(f"String numbers: {list_strings_of_numbers}")
    numbers: List[int] = []
    for num in list_strings_of_numbers:
        numbers.append(int(num))
    print(f"casted numbers:{numbers}")

    print("9. use of arrange_name function")
    full_name: str = arrange_name("Lea", "Vanne")
    print(f"complete name: {full_name}")

    print("10. Use of is_number_even function")
    list_numbers: List[int] = [2, 5, 19, 24, 1678]
    for n in list_numbers:
        if is_number_even(n):
            print(f" {n} is even!")
        else:
            print(f"{n} is odd!")
    print("11.Use of count_letters function")
    list_strings: List[str] = ["Lea", "Venta", "Kalop", "Spontaneous"]
    for string in list_strings:
        letter_count: int = count_letters(string)
        print(f"'{string}' has {letter_count} letters!")


if __name__ == "__main__":
    main()
