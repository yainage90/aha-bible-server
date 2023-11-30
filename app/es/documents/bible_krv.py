from elasticsearch_dsl import Document, Text, Keyword, Integer
from app.es.analysis.korean_analysis import (
    INDEX_ANALYZER_NAME,
    SEARCH_ANALYZER_NAME,
)


class BibleKRVDocument(Document):
    class Index:
        name = "bible_krv"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    id = Keyword()
    book = Keyword()
    idx = Integer()
    title = Text(
        analyzer=INDEX_ANALYZER_NAME,
        search_analyzer=SEARCH_ANALYZER_NAME,
        fields={
            "raw": Keyword(),
        },
    )
    title_abbreviation = Keyword()
    chapter = Integer()
    chapter_idx = Integer()
    verse = Integer()
    text = Text(
        analyzer=INDEX_ANALYZER_NAME,
        search_analyzer=SEARCH_ANALYZER_NAME,
    )
