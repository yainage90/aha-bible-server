from app.search.basic_query import EsQuery
from app.search.bible_krv.sorting_type import SortingType


class SearchQueryDsl:
    def __init__(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str | None = None,
        sorting_type: SortingType | None = SortingType.MATCH,
        books: list[str] | None = None,
        titles: list[str] | None = None,
    ):
        self._size = per_page
        self._from = per_page * (page - 1)
        self.sorting_type = sorting_type
        self._should = []
        self._filter = []

        if query:
            query = query.strip()
            self._should.append(EsQuery.match(field="text", query=query, operator="or"))

        if books:
            self._filter.append(EsQuery.terms(field="book", values=books))

        if titles:
            self._filter.append(EsQuery.terms(field="title.raw", values=titles))

    def to_dict(self):
        return {
            "track_total_hits": True,
            "from": self._from,
            "size": self._size,
            "query": {
                "bool": {
                    "should": self._should,
                    "minimum_should_match": 1 if self._should else 0,
                    "filter": self._filter,
                }
            },
            "highlight": {
                "fields": {
                    "text": {
                        "pre_tags": ["<b>"],
                        "post_tags": ["</b>"],
                    },
                },
            },
            "sort": self.sorting_type.sort_query,
        }
