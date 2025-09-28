from typing import Any, Dict, List, NamedTuple, TypedDict

import pydantic
import yaml


# ==================== PYTHONIC MODEL ====================
class FileNote(pydantic.BaseModel):
    year: int
    working_months: int
    satisfied: bool


class FileData(pydantic.BaseModel):
    name: str
    age: int
    id: int
    salary: int
    working_years: List[int]
    is_working: bool
    notes: List[FileNote] = pydantic.Field(default_factory=list)
    hobbies: List[str] = pydantic.Field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileData":
        """Create FileData from dictionary with proper parsing."""
        # Handle missing fields with defaults
        notes_data = data.get("notes", [])
        notes = [FileNote(**note) for note in notes_data]

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


class DataSchema(pydantic.BaseModel):
    records: List[FileData]


def process_yaml_with_pydantic() -> DataSchema:
    """Process YAML file using Pydantic."""
    with open("data/documents.yaml", "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    records = []
    for record_data in yaml_data["records"]:
        records.append(FileData.from_dict(record_data))

    return DataSchema(records=records)


def print_pydantic_information(data: DataSchema) -> None:
    """Print all information from Pydantic structure."""
    print("=== PROCESS YAML FILE using PYDANTIC data structure ===")
    for record in data.records:
        print(f"Name: {record.name}")
        print(f"Age: {record.age}")
        print(f"ID: {record.id}")
        print(f"Salary: {record.salary}")
        print(f"Working Years: {record.working_years}")
        print(f"Currently Working: {record.is_working}")
        print(f"Notes: {record.notes}")
        print(f"Hobbies: {record.hobbies}")
        print("-" * 40)


# ==================== NAMEDTUPLE ====================
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
        """Create Person from dictionary with proper parsing."""
        # Handle missing fields with defaults
        notes_data = data.get("notes", [])
        notes = [Note(**note) for note in notes_data]

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


def process_yaml_with_namedtuple() -> Records:
    """Process YAML file using NamedTuple."""
    with open("data/documents.yaml", "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    records = []
    for record_data in yaml_data["records"]:
        records.append(Person.from_dict(record_data))

    return Records(records=records)


def print_namedtuple_information(data: Records) -> None:
    """Print all information from NamedTuple structure."""
    print("\n=== PROCESS YAML DATA FILE Using NamedTuple data structure ===")
    for person in data.records:
        print(f"Name: {person.name}")
        print(f"Age: {person.age}")
        print(f"ID: {person.id}")
        print(f"Salary: {person.salary}")
        print(f"Working Years: {person.working_years}")
        print(f"Currently Working: {person.is_working}")
        print(f"Notes: {person.notes}")
        print(f"Hobbies: {person.hobbies}")
        print("-" * 40)


# ==================== TYPEDDICT ====================
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


def parse_dict_to_typeddict(data: Dict[str, Any]) -> PersonTypedDict:
    """Parse dictionary to TypedDict with proper data types."""
    # Handle missing fields with defaults
    notes_data = data.get("notes", [])
    notes: List[NoteTypedDict] = [
        {
            "year": note["year"],
            "working_months": note["working_months"],
            "satisfied": note["satisfied"],
        }
        for note in notes_data
    ]

    hobbies = data.get("hobbies", [])

    return {
        "name": data["name"],
        "age": data["age"],
        "id": data["id"],
        "salary": data["salary"],
        "working_years": data["working_years"],
        "is_working": data["is_working"],
        "notes": notes,
        "hobbies": hobbies,
    }


def process_yaml_with_typeddict() -> RecordsTypedDict:
    """Process YAML file using TypedDict."""
    with open("data/documents.yaml", "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    records = []
    for record_data in yaml_data["records"]:
        records.append(parse_dict_to_typeddict(record_data))

    return {"records": records}


def print_typeddict_information(data: RecordsTypedDict) -> None:
    """Print all information from TypedDict structure."""
    print("\n=== PROCESS YAML FILE Using TypedDict data structure ===")
    for person in data["records"]:
        print(f"Name: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"ID: {person['id']}")
        print(f"Salary: {person['salary']}")
        print(f"Working Years: {person['working_years']}")
        print(f"Currently Working: {person['is_working']}")
        print(f"Notes: {person['notes']}")
        print(f"Hobbies: {person['hobbies']}")
        print("-" * 40)


# ==================== MAIN EXECUTION ====================
def main() -> None:
    """Main function to run all YAML processing methods."""
    # Process with Pydantic
    pydantic_data = process_yaml_with_pydantic()
    print_pydantic_information(pydantic_data)

    # Process with NamedTuple
    namedtuple_data = process_yaml_with_namedtuple()
    print_namedtuple_information(namedtuple_data)

    # Process with TypedDict
    typeddict_data = process_yaml_with_typeddict()
    print_typeddict_information(typeddict_data)


if __name__ == "__main__":
    main()
