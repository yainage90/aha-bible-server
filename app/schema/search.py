from pydantic import BaseModel


class BibleSearchItem(BaseModel):
    id: str
    idx: int
    title: str
    title_abbreviation: str
    chapter: int
    verse: int
    text: str
    highlight: str | None


class BibleSearchResponse(BaseModel):
    total: int
    page: int
    prev_page: int | None
    next_page: int | None
    sorting_types: list[dict[str, str]]
    docs: list[BibleSearchItem]
