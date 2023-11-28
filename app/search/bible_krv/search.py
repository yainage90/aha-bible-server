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
        book: str | None = None,
        sorting_type: SortingType | None = SortingType.MATCH,
        title: str | None = None,
    ) -> list[dict]:
        query_dsl: dict = SearchQueryDsl(
            page=page,
            per_page=per_page,
            query=query,
            book=book,
            sorting_type=sorting_type,
            title=title,
        ).to_dict()

        response = BibleKRVDocument().search().update_from_dict(query_dsl).execute()
        total = response.hits.total.value

        docs = []
        for hit in response:
            doc = hit.to_dict()
            if "highlight" in hit.meta and "text" in hit.meta.highlight:
                highlighted_text = hit.meta.highlight.text
                if highlighted_text:
                    doc["highlight"] = highlighted_text[0]
            docs.append(doc)

        return {
            "total": total,
            "docs": docs,
        }
