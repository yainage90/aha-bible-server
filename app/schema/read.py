from pydantic import BaseModel


class VeresItem(BaseModel):
    id: str
    idx: int
    book: str
    title: str
    title_abbr: str
    chapter: int
    verse: int
    text: str


class BibleReadResponse(BaseModel):
    total: int
    prev_chapter_idx: int | None
    next_chapter_idx: int | None
    verses: list[VeresItem]
