from app.es.documents.bible_krv import BibleKRVDocument
from app.search.bible_krv.filter_query_dsl import FilterQueryDsl
from app.search.bible_krv.filter_order import FilterOrder


class Aggregator:
    @classmethod
    def aggregate(
        cls,
        query: str | None = None,
        books: list[str] | None = None,
        titles: list[str] | None = None,
    ):
        query_dsl = FilterQueryDsl(
            query=query,
            books=books,
            titles=titles,
        ).to_dict()

        response = BibleKRVDocument().search().update_from_dict(query_dsl).execute()

        total = response.hits.total.value
        aggs = response.aggregations.to_dict()

        return {
            "total": total,
            "filters": [
                cls._get_book_filter(
                    buckets=aggs["book"][FilterQueryDsl.Field.book]["buckets"],
                    selected_values=set(books or []),
                ),
                cls._get_title_filter(
                    buckets=aggs["title"][FilterQueryDsl.Field.title]["buckets"],
                    selected_values=set(titles or []),
                ),
            ],
        }

    @classmethod
    def _get_book_filter(cls, buckets: list[dict], selected_values: set[str]):
        choices = []
        for bucket in buckets:
            choices.append(
                {
                    "key": "book",
                    "value": bucket["key"],
                    "selected": bucket["key"] in selected_values,
                    "count": bucket["doc_count"],
                    "active": bool(bucket["doc_count"]),
                }
            )

        choices.sort(
            key=lambda choice: (
                -int(choice["active"]),
                FilterOrder.get_book_order(choice["value"]),
            )
        )

        return {
            "name": "신/구약",
            "choices": choices,
        }

    @classmethod
    def _get_title_filter(cls, buckets: list[dict], selected_values: set[str]):
        choices = []
        for bucket in buckets:
            choices.append(
                {
                    "key": "title",
                    "value": bucket["key"],
                    "selected": bucket["key"] in selected_values,
                    "count": bucket["doc_count"],
                    "active": bool(bucket["doc_count"]),
                }
            )

        choices.sort(
            key=lambda choice: (
                -int(choice["active"]),
                FilterOrder.get_title_order(choice["value"]),
            )
        )

        return {
            "name": "제목",
            "choices": choices,
        }
