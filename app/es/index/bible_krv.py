import re
import os
import pathlib
import logging
from datetime import datetime as dt
from app.es.documents.bible_krv import BibleKRVDocument
from app.es.analysis.korean_analysis import KrAnalysis
from app.search.bible_krv.filter_order import FilterOrder
from elasticsearch_dsl import Index, connections
from elasticsearch import helpers
from elasticsearch.exceptions import NotFoundError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(process)d:%(name)s:%(lineno)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
steam_handler = logging.StreamHandler()
logger.addHandler(steam_handler)


class Indexer:
    INDEX_BATCH_SIZE = 5000

    @classmethod
    def _create_index(cls, alias_name: str) -> str:
        suffix = dt.now().strftime("%Y%m%d%H%M%S")
        index_name = f"{alias_name}_{suffix}"
        index = Index(name=index_name)
        index.document(BibleKRVDocument)
        index.settings(**BibleKRVDocument.Index.settings)

        analysis = KrAnalysis()

        for analyzer in analysis.analyzers():
            index.analyzer(analyzer)

        index.create()

        return index_name

    @classmethod
    def _index_docs(cls, index_name: str) -> int:
        projct_root = pathlib.Path(
            pathlib.Path(pathlib.Path(__file__).parent).parent
        ).parent
        data_dir = f"{projct_root}/data/bible/krv"
        fnames = os.listdir(data_dir)
        fnames.sort(key=lambda x: FilterOrder.get_title_order(x.replace(".txt", "")))
        docs: list[BibleKRVDocument] = []
        prev_title_chapter = None
        chapter_idx = -1
        for fname in fnames:
            with open(f"{data_dir}/{fname}", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    p = re.compile(r"[가-힣]+")

                    title = fname.split(".")[0]
                    tokens = line.split()
                    book = tokens[0]
                    idx = tokens[1]
                    abbr = p.match(tokens[2]).group()
                    chapter, verse = tokens[2].replace(abbr, "").split(":")
                    chapter = int(chapter)
                    verse = int(verse)
                    text = " ".join(tokens[3:])

                    title_chapter = f"{title}_{chapter}"
                    if title_chapter != prev_title_chapter:
                        chapter_idx += 1
                        prev_title_chapter = title_chapter

                    docs.append(
                        BibleKRVDocument(
                            _index=index_name,
                            _id=f"{abbr}_{chapter}_{verse}",
                            id=f"{abbr}_{chapter}_{verse}",
                            book=book,
                            idx=idx,
                            title=title,
                            title_abbreviation=abbr,
                            chapter=chapter,
                            chapter_idx=chapter_idx,
                            verse=verse,
                            text=text,
                        ).to_dict(include_meta=True)
                    )

        es_conn = connections.get_connection()
        for i in range(0, len(docs), cls.INDEX_BATCH_SIZE):
            batch_docs = docs[i : i + cls.INDEX_BATCH_SIZE]
            helpers.bulk(es_conn, batch_docs)
            es_conn.indices.refresh(index=index_name, request_timeout=10)

        return len(docs)

    @classmethod
    def _switch_alias(cls, alias_name: str, new_index_name: str) -> dict | None:
        es = connections.get_connection()
        try:
            aliases = es.indices.get_alias(index=alias_name)
            old_index_names = list(aliases.keys())
            prev_index_name = old_index_names[0]
            es.indices.update_aliases(
                body={
                    "actions": [
                        {"add": {"index": new_index_name, "alias": alias_name}},
                        {"remove": {"index": prev_index_name, "alias": alias_name}},
                    ],
                }
            )

            aliases = es.indices.get_alias(index=f"{alias_name}*")
            old_index_names = list(aliases.keys())
            indices_to_delete = list(
                sorted(
                    list(set(old_index_names) - set([new_index_name, prev_index_name]))
                )
            )
            for old_index_name in indices_to_delete:
                es.indices.delete(index=old_index_name)

            return {
                "prev_alias": prev_index_name,
                "new_alias": new_index_name,
                "deleted_indices": indices_to_delete,
            }

        except NotFoundError:
            es.indices.put_alias(index=new_index_name, name=alias_name)

    @classmethod
    def full_index(cls, alias_name: str) -> dict:
        new_index_name = cls._create_index(alias_name=alias_name)
        total = cls._index_docs(index_name=new_index_name)
        result = cls._switch_alias(alias_name=alias_name, new_index_name=new_index_name)

        return {
            "total": total,
            "result": result,
        }
