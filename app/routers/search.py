from fastapi import APIRouter
from app.search.bible_krv.sorting_type import SortingType
from app.es.documents.bible_krv import BibleKRVDocument
from app.search.bible_krv.search import Searcher

router = APIRouter(prefix="/search")


@router.get("/bible_krv")
def search_bible_krv(
    page: int = 1,
    per_page: int = 10,
    query: str | None = None,
    chapter: str | None = None,
    sorting_type: str | None = None,
):
    sorting_type = SortingType.find_by_name(sorting_type)
    docs = Searcher.search(
        page=page,
        per_page=per_page,
        query=query,
        chapter=chapter,
        sorting_type=sorting_type,
    )

    return docs
