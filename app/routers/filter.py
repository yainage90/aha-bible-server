from fastapi import APIRouter
from app.search.bible_krv.sorting_type import SortingType
from app.search.bible_krv.filter import Aggregator
from app.schema.filter import BibleFilterResponse

router = APIRouter(prefix="/filter")


@router.get("/bible_krv", response_model=BibleFilterResponse)
def filter_bible_krv(
    query: str | None = None,
    book: str | None = None,
    title: str | None = None,
    sorting_type: str | None = None,
) -> BibleFilterResponse:
    books = None
    if book:
        books = [book for book in book.split(",")]

    titles = None
    if title:
        titles = [title for title in title.split(",")]

    sorting_type = SortingType.find_by_name(sorting_type)
    result = Aggregator.aggregate(
        query=query,
        books=books,
        titles=titles,
    )

    return BibleFilterResponse(
        total=result["total"],
        filters=result["filters"],
    )
