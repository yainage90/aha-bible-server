from pydantic import BaseModel


class BibleChoice(BaseModel):
    key: str
    value: str
    selected: bool
    count: int
    active: bool


class BibleFilter(BaseModel):
    name: str
    choices: list[BibleChoice]


class BibleFilterResponse(BaseModel):
    total: int
    filters: list[BibleFilter]
