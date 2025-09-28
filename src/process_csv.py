import csv
from typing import Dict, List, NamedTuple, TypedDict

import pydantic


# ==================== PYDANTIC MODEL ====================
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
    def from_csv_row(cls, row: Dict[str, str]) -> "FileData":
        """Create FileData from CSV row with proper parsing."""
        # Parse working_years
        working_years_str = row.get("working_years", "").strip('"')
        working_years = (
            [int(year.strip()) for year in working_years_str.split(",")]
            if working_years_str
            else []
        )

        # Parse notes
        notes = []
        notes_years = (
            row.get("notes_year", "").split(";") if row.get("notes_year") else []
        )
        notes_months = (
            row.get("notes_working_months", "").split(";")
            if row.get("notes_working_months")
            else []
        )
        notes_satisfied = (
            row.get("notes_satisfied", "").split(";")
            if row.get("notes_satisfied")
            else []
        )

        for i, year_str in enumerate(notes_years):
            if year_str:  # Only process if year exists
                notes.append(
                    FileNote(
                        year=int(year_str.strip()),
                        working_months=int(notes_months[i].strip()),
                        satisfied=notes_satisfied[i].strip().lower() == "true",
                    )
                )

        # Parse hobbies
        hobbies_str = row.get("hobbies", "").strip('"')
        hobbies = (
            [hobby.strip() for hobby in hobbies_str.split(",")] if hobbies_str else []
        )

        return cls(
            name=row["name"].strip('"'),
            age=int(row["age"]),
            id=int(row["id"]),
            salary=int(row["salary"]),
            working_years=working_years,
            is_working=row["is_working"].lower() == "true",
            notes=notes,
            hobbies=hobbies,
        )


class DataSchema(pydantic.BaseModel):
    records: List[FileData]


def process_csv_with_pydantic() -> DataSchema:
    """Process CSV file using Pydantic."""
    records = []
    with open("data/documents.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(FileData.from_csv_row(row))

    return DataSchema(records=records)


def print_pydantic_information(data: DataSchema) -> None:
    """Print all information from Pydantic structure."""
    print("=== PROCESSING CSV DATA FILE USING PYDANTIC ===")
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
    def from_csv_row(cls, row: Dict[str, str]) -> "Person":
        """Create Person from CSV row with proper parsing."""
        # Parse working_years
        working_years_str = row.get("working_years", "").strip('"')
        working_years = (
            [int(year.strip()) for year in working_years_str.split(",")]
            if working_years_str
            else []
        )

        # Parse notes
        notes = []
        notes_years = (
            row.get("notes_year", "").split(";") if row.get("notes_year") else []
        )
        notes_months = (
            row.get("notes_working_months", "").split(";")
            if row.get("notes_working_months")
            else []
        )
        notes_satisfied = (
            row.get("notes_satisfied", "").split(";")
            if row.get("notes_satisfied")
            else []
        )

        for i, year_str in enumerate(notes_years):
            if year_str:  # Only process if year exists
                notes.append(
                    Note(
                        year=int(year_str.strip()),
                        working_months=int(notes_months[i].strip()),
                        satisfied=notes_satisfied[i].strip().lower() == "true",
                    )
                )

        # Parse hobbies
        hobbies_str = row.get("hobbies", "").strip('"')
        hobbies = (
            [hobby.strip() for hobby in hobbies_str.split(",")] if hobbies_str else []
        )

        return cls(
            name=row["name"].strip('"'),
            age=int(row["age"]),
            id=int(row["id"]),
            salary=int(row["salary"]),
            working_years=working_years,
            is_working=row["is_working"].lower() == "true",
            notes=notes,
            hobbies=hobbies,
        )


class Records(NamedTuple):
    records: List[Person]


def process_csv_with_namedtuple() -> Records:
    """Process CSV file using NamedTuple."""
    records = []
    with open("data/documents.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(Person.from_csv_row(row))

    return Records(records=records)


def print_namedtuple_information(data: Records) -> None:
    """Print all information from NamedTuple structure."""
    print("\n=== Process CSV file using NAMEDTUPLE data structure ===")
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


def parse_csv_row_to_typeddict(row: Dict[str, str]) -> PersonTypedDict:
    """Parse CSV row to TypedDict with proper data types."""
    # Parse working_years
    working_years_str = row.get("working_years", "").strip('"')
    working_years = (
        [int(year.strip()) for year in working_years_str.split(",")]
        if working_years_str
        else []
    )

    # Parse notes
    notes: List[NoteTypedDict] = []
    notes_years = row.get("notes_year", "").split(";") if row.get("notes_year") else []
    notes_months = (
        row.get("notes_working_months", "").split(";")
        if row.get("notes_working_months")
        else []
    )
    notes_satisfied = (
        row.get("notes_satisfied", "").split(";") if row.get("notes_satisfied") else []
    )

    for i, year_str in enumerate(notes_years):
        if year_str:  # Only process if year exists
            notes.append(
                {
                    "year": int(year_str.strip()),
                    "working_months": int(notes_months[i].strip()),
                    "satisfied": notes_satisfied[i].strip().lower() == "true",
                }
            )

    # Parse hobbies
    hobbies_str = row.get("hobbies", "").strip('"')
    hobbies = [hobby.strip() for hobby in hobbies_str.split(",")] if hobbies_str else []

    return {
        "name": row["name"].strip('"'),
        "age": int(row["age"]),
        "id": int(row["id"]),
        "salary": int(row["salary"]),
        "working_years": working_years,
        "is_working": row["is_working"].lower() == "true",
        "notes": notes,
        "hobbies": hobbies,
    }


def process_csv_with_typeddict() -> RecordsTypedDict:
    """Process CSV file using TypedDict."""
    records = []
    with open("data/documents.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(parse_csv_row_to_typeddict(row))

    return {"records": records}


def print_typeddict_information(data: RecordsTypedDict) -> None:
    """Print all information from TypedDict structure."""
    print("\n=== PROCESSING CSV FILE USING TYPED-DICT data structure ===")
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
    """Main function to run all CSV processing methods."""
    # Process with Pydantic
    pydantic_data = process_csv_with_pydantic()
    print_pydantic_information(pydantic_data)

    # Process with NamedTuple
    namedtuple_data = process_csv_with_namedtuple()
    print_namedtuple_information(namedtuple_data)

    # Process with TypedDict
    typeddict_data = process_csv_with_typeddict()
    print_typeddict_information(typeddict_data)


if __name__ == "__main__":
    main()
