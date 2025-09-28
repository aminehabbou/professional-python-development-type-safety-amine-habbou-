import xml.etree.ElementTree as ET
from typing import List, NamedTuple, TypedDict

import pydantic


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
    def from_xml_element(cls, element: ET.Element) -> "FileData":
        """Create FileData from XML element with proper parsing."""
        # Parse basic fields
        name = element.findtext("name", "").strip()

        # FIXED: All int conversions with null checks
        age_text = element.findtext("age", "0")
        age = int(age_text) if age_text is not None else 0

        id_text = element.findtext("id", "0")
        id_num = int(id_text) if id_text is not None else 0

        salary_text = element.findtext("salary", "0")
        salary = int(salary_text) if salary_text is not None else 0

        is_working = element.findtext("is_working", "false").lower() == "true"

        # Parse working_years
        working_years_element = element.find("working_years")
        working_years = (
            [
                int(year.text)
                for year in working_years_element.findall("year")
                if year.text is not None
            ]
            if working_years_element is not None
            else []
        )

        # Parse notes
        notes = []
        notes_element = element.find("notes")
        if notes_element is not None:
            for note_element in notes_element.findall("note"):
                # FIXED: All int conversions with null checks
                year_text = note_element.findtext("year", "0")
                months_text = note_element.findtext("working_months", "0")
                satisfied_text = note_element.findtext("satisfied", "false")

                note = FileNote(
                    year=int(year_text) if year_text is not None else 0,
                    working_months=int(months_text) if months_text is not None else 0,
                    satisfied=satisfied_text.lower() == "true"
                    if satisfied_text is not None
                    else False,
                )
                notes.append(note)

        # Parse hobbies
        hobbies = []
        hobbies_element = element.find("hobbies")
        if hobbies_element is not None:
            hobbies = [
                hobby.text.strip()
                for hobby in hobbies_element.findall("hobby")
                if hobby.text is not None
            ]

        return cls(
            name=name,
            age=age,
            id=id_num,
            salary=salary,
            working_years=working_years,
            is_working=is_working,
            notes=notes,
            hobbies=hobbies,
        )


class DataSchema(pydantic.BaseModel):
    records: List[FileData]


def process_xml_with_pydantic() -> DataSchema:
    """Process XML file using Pydantic."""
    tree = ET.parse("data/documents.xml")
    root = tree.getroot()

    records = []
    for record_element in root.findall("record"):
        records.append(FileData.from_xml_element(record_element))

    return DataSchema(records=records)


def print_pydantic_information(data: DataSchema) -> None:
    """Print all information from Pydantic structure."""
    print("=== PROCESS XML FILE USING PYDANTIC data stucture ===")
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
    def from_xml_element(cls, element: ET.Element) -> "Person":
        """Create Person from XML element with proper parsing."""
        # Parse basic fields
        name = element.findtext("name", "").strip()

        # FIXED: All int conversions with null checks
        age_text = element.findtext("age", "0")
        age = int(age_text) if age_text is not None else 0

        id_text = element.findtext("id", "0")
        id_num = int(id_text) if id_text is not None else 0

        salary_text = element.findtext("salary", "0")
        salary = int(salary_text) if salary_text is not None else 0

        is_working = element.findtext("is_working", "false").lower() == "true"

        # Parse working_years
        working_years_element = element.find("working_years")
        working_years = (
            [
                int(year.text)
                for year in working_years_element.findall("year")
                if year.text is not None
            ]
            if working_years_element is not None
            else []
        )

        # Parse notes
        notes = []
        notes_element = element.find("notes")
        if notes_element is not None:
            for note_element in notes_element.findall("note"):
                # FIXED: All int conversions with null checks
                year_text = note_element.findtext("year", "0")
                months_text = note_element.findtext("working_months", "0")
                satisfied_text = note_element.findtext("satisfied", "false")

                note = Note(
                    year=int(year_text) if year_text is not None else 0,
                    working_months=int(months_text) if months_text is not None else 0,
                    satisfied=satisfied_text.lower() == "true"
                    if satisfied_text is not None
                    else False,
                )
                notes.append(note)

        # Parse hobbies
        hobbies = []
        hobbies_element = element.find("hobbies")
        if hobbies_element is not None:
            hobbies = [
                hobby.text.strip()
                for hobby in hobbies_element.findall("hobby")
                if hobby.text is not None
            ]

        return cls(
            name=name,
            age=age,
            id=id_num,
            salary=salary,
            working_years=working_years,
            is_working=is_working,
            notes=notes,
            hobbies=hobbies,
        )


class Records(NamedTuple):
    records: List[Person]


def process_xml_with_namedtuple() -> Records:
    """Process XML file using NamedTuple."""
    tree = ET.parse("data/documents.xml")
    root = tree.getroot()

    records = []
    for record_element in root.findall("record"):
        records.append(Person.from_xml_element(record_element))

    return Records(records=records)


def print_namedtuple_information(data: Records) -> None:
    """Print all information from NamedTuple structure."""
    print("\n=== PROCESS XML FILE USING NAMEDTUPLE data structure ===")
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


def parse_xml_element_to_typeddict(element: ET.Element) -> PersonTypedDict:
    """Parse XML element to TypedDict with proper data types."""
    # Parse basic fields
    name = element.findtext("name", "").strip()

    # FIXED: All int conversions with null checks
    age_text = element.findtext("age", "0")
    age = int(age_text) if age_text is not None else 0

    id_text = element.findtext("id", "0")
    id_num = int(id_text) if id_text is not None else 0

    salary_text = element.findtext("salary", "0")
    salary = int(salary_text) if salary_text is not None else 0

    is_working = element.findtext("is_working", "false").lower() == "true"

    # Parse working_years
    working_years_element = element.find("working_years")
    working_years = (
        [
            int(year.text)
            for year in working_years_element.findall("year")
            if year.text is not None
        ]
        if working_years_element is not None
        else []
    )

    # Parse notes
    notes: List[NoteTypedDict] = []
    notes_element = element.find("notes")
    if notes_element is not None:
        for note_element in notes_element.findall("note"):
            # FIXED: All int conversions with null checks
            year_text = note_element.findtext("year", "0")
            months_text = note_element.findtext("working_months", "0")
            satisfied_text = note_element.findtext("satisfied", "false")

            note: NoteTypedDict = {
                "year": int(year_text) if year_text is not None else 0,
                "working_months": int(months_text) if months_text is not None else 0,
                "satisfied": satisfied_text.lower() == "true"
                if satisfied_text is not None
                else False,
            }
            notes.append(note)

    # Parse hobbies
    hobbies = []
    hobbies_element = element.find("hobbies")
    if hobbies_element is not None:
        hobbies = [
            hobby.text.strip()
            for hobby in hobbies_element.findall("hobby")
            if hobby.text is not None
        ]

    return {
        "name": name,
        "age": age,
        "id": id_num,
        "salary": salary,
        "working_years": working_years,
        "is_working": is_working,
        "notes": notes,
        "hobbies": hobbies,
    }


def process_xml_with_typeddict() -> RecordsTypedDict:
    """Process XML file using TypedDict."""
    tree = ET.parse("data/documents.xml")
    root = tree.getroot()

    records = []
    for record_element in root.findall("record"):
        records.append(parse_xml_element_to_typeddict(record_element))

    return {"records": records}


def print_typeddict_information(data: RecordsTypedDict) -> None:
    """Print all information from TypedDict structure."""
    print("\n=== PROCESS XML file using TypedDict data structure ===")
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
    """Main function to run all XML processing methods."""
    # Process with Pydantic
    pydantic_data = process_xml_with_pydantic()
    print_pydantic_information(pydantic_data)

    # Process with NamedTuple
    namedtuple_data = process_xml_with_namedtuple()
    print_namedtuple_information(namedtuple_data)

    # Process with TypedDict
    typeddict_data = process_xml_with_typeddict()
    print_typeddict_information(typeddict_data)


if __name__ == "__main__":
    main()
