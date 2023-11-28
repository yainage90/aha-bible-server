from fastapi import APIRouter
from app.search.bible_krv.sorting_type import SortingType
from app.search.bible_krv.search import Searcher
from app.search.bible_krv.filter import Aggregator
from app.schema.search import BibleSearchResponse

router = APIRouter(prefix="/search")


@router.get("/bible_krv", response_model=BibleSearchResponse)
def search_bible_krv(
    page: int = 1,
    per_page: int = 10,
    query: str | None = None,
    book: str | None = None,
    title: str | None = None,
    sorting_type: str | None = None,
) -> BibleSearchResponse:
    books = None
    if book:
        books = [book for book in book.split(",")]

    titles = None
    if title:
        titles = [title for title in title.split(",")]

    sorting_type = SortingType.find_by_name(sorting_type)
    result = Searcher.search(
        page=page,
        per_page=per_page,
        query=query,
        books=books,
        titles=titles,
        sorting_type=sorting_type,
    )

    total = result["total"]
    docs = result["docs"]

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if per_page * page < total else None

    return BibleSearchResponse(
        total=total,
        page=page,
        prev_page=prev_page,
        next_page=next_page,
        sorting_types=SortingType.options(),
        docs=docs,
    )
