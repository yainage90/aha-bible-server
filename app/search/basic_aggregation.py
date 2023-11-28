class EsAggregation:
    @classmethod
    def bucket_terms(
        cls,
        bucket_name: str,
        field: str,
        filters: list[dict] | None = None,
    ) -> dict:
        return {
            "aggs": {
                bucket_name: {
                    "terms": {
                        "field": field,
                        "min_doc_count": 0,
                        "size": 10000,
                    }
                }
            },
            "filter": {
                "bool": {
                    "filter": filters,
                }
            },
        }
