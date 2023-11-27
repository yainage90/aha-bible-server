from app.es.documents.bible_krv import BibleKRVDocument
from app.search.bible_krv.search_query_dsl import SearchQueryDsl
from app.search.bible_krv.sorting_type import SortingType


class Searcher:
    @classmethod
    def search(
        cls,
        page: int = 1,
        per_page: int = 10,
        query: str | None = None,
        sorting_type: SortingType | None = SortingType.MATCH,
        chapter: str | None = None,
    ) -> list[BibleKRVDocument]:
        query_dsl: dict = SearchQueryDsl(
            page=page,
            per_page=per_page,
            query=query,
            sorting_type=sorting_type,
            chapter=chapter,
        ).to_dict()

        response = BibleKRVDocument().search().update_from_dict(query_dsl).execute()
        total = response.hits.total.value
        docs = [hit.to_dict() for hit in response.hits]

        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if per_page * page < total else None

        return {
            "total": total,
            "page": page,
            "prev_page": prev_page,
            "next_page": next_page,
            "sorting_types": SortingType.options(),
            "docs": docs,
        }
