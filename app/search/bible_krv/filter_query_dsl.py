from enum import StrEnum
from app.search.basic_query import EsQuery
from app.search.basic_aggregation import EsAggregation
from app.search.bible_krv.sorting_type import SortingType


class FilterQueryDsl:
    class Field(StrEnum):
        book = "book"
        title = "title.raw"

    def __init__(
        self,
        query: str | None = None,
        books: list[str] | None = None,
        titles: list[str] | None = None,
    ):
        self._should = []
        self._post_filter = []

        self.books = books
        self.titles = titles

        if query:
            query = query.strip()
            self._should.append(EsQuery.match(field="text", query=query))

        if books:
            self._post_filter.append(EsQuery.terms(field="book", values=books))

        if titles:
            self._post_filter.append(EsQuery.terms(field="title.raw", values=titles))

    def _create_aggregation_filters(self, aggregation_field: str):
        filters = []

        if aggregation_field == self.Field.book and self.titles:
            filters.append(EsQuery.terms(field=self.Field.title, values=self.titles))

        if aggregation_field == self.Field.title and self.books:
            filters.append(EsQuery.terms(field=self.Field.book, values=self.books))

        return filters

    def _book_aggregation(self):
        filters = self._create_aggregation_filters(aggregation_field=self.Field.book)
        return EsAggregation.bucket_terms(
            bucket_name=self.Field.book,
            field=self.Field.book,
            filters=filters,
        )

    def _title_aggregation(self):
        filters = self._create_aggregation_filters(aggregation_field=self.Field.title)
        return EsAggregation.bucket_terms(
            bucket_name=self.Field.title,
            field=self.Field.title,
            filters=filters,
        )

    def _aggregation(self):
        return {
            "book": self._book_aggregation(),
            "title": self._title_aggregation(),
        }

    def to_dict(self):
        return {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should": self._should,
                }
            },
            "post_filter": {
                "bool": {
                    "filter": self._post_filter,
                },
            },
            "aggs": self._aggregation(),
        }
