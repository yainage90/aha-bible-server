from fastapi import APIRouter
from app.search.bible_krv.sorting_type import SortingType
from app.search.bible_krv.search import Searcher
from app.schema.read import BibleReadResponse

router = APIRouter(prefix="/read")


@router.get("/bible_krv", response_model=BibleReadResponse)
def read_bible_krv(
    page: int = 1,
    per_page: int = 10,
    book: str | None = None,
    title: str | None = None,
    chapter: int | None = None,
    chapter_idx: int | None = None,
) -> BibleReadResponse:

    result = Searcher.search(
        page=page,
        per_page=per_page,
        books=[book] if book else None,
        titles=[title] if title else None,
        chapters=[chapter] if chapter else None,
        chapter_idx=chapter_idx if chapter_idx is not None else None,
        sorting_type=SortingType.PAGE,
    )

    total = result["total"]
    docs = result["docs"]

    chapter_idx = chapter_idx or docs[0]["chapter_idx"]
    prev_chapter_idx = chapter_idx - 1 if chapter_idx > 0 else None
    next_chapter_idx = chapter_idx + 1 if chapter_idx < 1188 else None

    return BibleReadResponse(
        total=total,
        prev_chapter_idx=prev_chapter_idx,
        next_chapter_idx=next_chapter_idx,
        verses=docs,
    )
