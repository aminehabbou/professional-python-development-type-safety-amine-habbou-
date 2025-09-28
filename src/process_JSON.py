import json
from typing import Any, Dict, List, NamedTuple, TypedDict

import pydantic

# Load JSON data
with open("data/documents.json", "r") as f:
    d = json.load(f)


# Pydantic Model
class Filenotes(pydantic.BaseModel):
    year: int
    working_months: int
    satisfied: bool


class FileData(pydantic.BaseModel):
    name: str
    age: int
    id: int
    salary: int
    working_years: list[int]
    is_working: bool
    notes: list[Filenotes] = pydantic.Field(default_factory=list)
    hobbies: list[str] = pydantic.Field(default_factory=list)


class DataSchema(pydantic.BaseModel):
    records: list[FileData]


# Process with Pydantic
print("=== PYDANTIC DATA PROCESSING ===")
model = DataSchema(records=d["records"])

for record in model.records:
    print(f"Name: {record.name}")
    print(f"Age: {record.age}")
    print(f"ID: {record.id}")
    print(f"Salary: {record.salary}")
    print(f"Working Years: {record.working_years}")
    print(f"Notes: {record.notes}")
    print(f"Hobbies: {record.hobbies}")
    print("-" * 40)


# NamedTuple Structure
class Note(NamedTuple):
    year: int
    working_months: int
    satisfied: bool


class Person(NamedTuple):
    name: str
    age: int
    id: int
    salary: int
    working_years: List[int]
    is_working: bool
    notes: List[Note]
    hobbies: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Person":
        """Create Person from dictionary with missing field handling."""
        notes = [Note(**note) for note in data.get("notes", [])]
        hobbies = data.get("hobbies", [])

        return cls(
            name=data["name"],
            age=data["age"],
            id=data["id"],
            salary=data["salary"],
            working_years=data["working_years"],
            is_working=data["is_working"],
            notes=notes,
            hobbies=hobbies,
        )


class Records(NamedTuple):
    records: List[Person]


def load_and_process_namedtuple() -> Records:
    """Load JSON data and convert to NamedTuple structure."""
    with open("data/documents.json", "r") as f:
        json_data = json.load(f)

    persons = [Person.from_dict(record) for record in json_data["records"]]
    return Records(records=persons)


def print_all_information(data: Records) -> None:
    """Print all information from the data structure."""
    print("\n=== NAMEDTUPLE DATA PROCESSING ===")
    for person in data.records:
        print(f"\n--- Person ID: {person.id} ---")
        print(f"Name: {person.name}")
        print(f"Age: {person.age}")
        print(f"Salary: ${person.salary}")
        print(f"Currently Working: {person.is_working}")
        print(f"Working Years: {person.working_years}")

        print("Notes:")
        if person.notes:
            for note in person.notes:
                status = "Satisfied" if note.satisfied else "Not Satisfied"
                print(
                    f"  - Year: {note.year}, "
                    f"Months: {note.working_months}, "
                    f"Status: {status}"
                )
        else:
            print("  No notes available")

        print("Hobbies:")
        if person.hobbies:
            for hobby in person.hobbies:
                print(f"  - {hobby}")
        else:
            print("  No hobbies listed")

        print("-" * 40)


# Process with NamedTuple
named_tuple_data = load_and_process_namedtuple()
print_all_information(named_tuple_data)


# TypedDict structure


class NoteTypedDict(TypedDict):
    year: int
    working_months: int
    satisfied: bool


class PersonTypedDict(TypedDict):
    name: str
    age: int
    id: int
    salary: int
    working_years: List[int]
    is_working: bool
    notes: List[NoteTypedDict]
    hobbies: List[str]


class RecordsTypedDict(TypedDict):
    records: List[PersonTypedDict]


def load_and_process_typeddict() -> RecordsTypedDict:
    """Load JSON data with TypedDict structure."""
    with open("data/documents.json", "r") as f:
        json_data: RecordsTypedDict = json.load(f)
    return json_data


def safe_get_notes(person: PersonTypedDict) -> List[NoteTypedDict]:
    """Safely get notes with default empty list."""
    return person.get("notes", [])


def safe_get_hobbies(person: PersonTypedDict) -> List[str]:
    """Safely get hobbies with default empty list."""
    return person.get("hobbies", [])


def print_typeddict_information(data: RecordsTypedDict) -> None:
    """Print all information from the TypedDict structure."""
    print("\n=== TYPEDDICT DATA PROCESSING ===")
    for person in data["records"]:
        print(f"\n--- Person ID: {person['id']} ---")
        print(f"Name: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"Salary: ${person['salary']}")
        print(f"Currently Working: {person['is_working']}")
        print(f"Working Years: {person['working_years']}")

        notes = safe_get_notes(person)
        print("Notes:")
        if notes:
            for note in notes:
                status = "Satisfied" if note["satisfied"] else "Not Satisfied"
                print(
                    f"  - Year: {note['year']}, "
                    f"Months: {note['working_months']}, "
                    f"Status: {status}"
                )
        else:
            print("  No notes available")

        hobbies = safe_get_hobbies(person)
        print("Hobbies:")
        if hobbies:
            for hobby in hobbies:
                print(f"  - {hobby}")
        else:
            print("  No hobbies listed")

        print("-" * 40)


# Process with TypedDict
typeddict_data = load_and_process_typeddict()
print_typeddict_information(typeddict_data)
