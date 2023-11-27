class EsQuery:
    @classmethod
    def term(cls, field: str, value: int | str) -> dict:
        return {
            "term": {
                field: value,
            }
        }

    @classmethod
    def terms(cls, field: str, values: list[int] | list[str]) -> dict:
        return {
            "terms": {
                field: values,
            }
        }

    @classmethod
    def match(cls, field: str, query: str, operator: str = "or") -> dict:
        return {
            "match": {
                field: {
                    "query": query,
                    "operator": operator,
                }
            }
        }

    @classmethod
    def match_phrase(cls, field: str, query: str, slop: int = 2) -> dict:
        return {
            "match_phrase": {
                field: {
                    "query": query,
                    "slop": slop,
                }
            }
        }
