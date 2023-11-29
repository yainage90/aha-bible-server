from pydantic import BaseModel


class BibleSearchItem(BaseModel):
    id: str
    idx: int
    book: str
    title: str
    title_abbreviation: str
    chapter: int
    verse: int
    text: str
    highlight: str | None = None


class BibleSearchResponse(BaseModel):
    total: int
    page: int
    prev_page: int | None = None
    next_page: int | None = None
    sorting_types: list[dict[str, str]]
    docs: list[BibleSearchItem]
