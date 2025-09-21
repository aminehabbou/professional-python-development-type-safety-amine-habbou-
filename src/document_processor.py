import json

import pydantic

with open("data/documents.json", "r") as f:
    d = json.load(f)


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


model = DataSchema(records=d["records"])
print(model)

for record in model.records:
    print(f"name: {record.name}")
    print(f"age: {record.age}")
    print(f"id: {(record.id)}")
    print(f"salary: {record.salary}")
    print(f"working_years: {record.working_years}")
    print(f"notes: {record.notes}")
    print(f"hobbies: {record.hobbies}")
    print("-" * 40)
