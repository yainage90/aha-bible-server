import re
import os
import pathlib
from datetime import datetime as dt
from app.es.documents.bible_krv import BibleKRVDocument
from app.es.analysis.korean_analysis import KrAnalysis
from elasticsearch_dsl import Index, connections
from elasticsearch import helpers
from elasticsearch.exceptions import NotFoundError


class Indexer:
    INDEX_BATCH_SIZE = 5000

    @classmethod
    def _create_index(cls, alias_name: str) -> str:
        suffix = dt.now().strftime("%Y%m%d%H%M%S")
        index_name = f"{alias_name}_{suffix}"
        index = Index(name=index_name)
        print(index_name)
        index.document(BibleKRVDocument)
        index.settings(**BibleKRVDocument.Index.settings)

        analysis = KrAnalysis()

        for analyzer in analysis.analyzers():
            index.analyzer(analyzer)

        index.create()

        return index_name

    @classmethod
    def _index_docs(cls, index_name: str):
        projct_root = pathlib.Path(
            pathlib.Path(pathlib.Path(__file__).parent).parent
        ).parent
        data_dir = f"{projct_root}/data/bible/krv"
        fnames = os.listdir(data_dir)
        docs: list[BibleKRVDocument] = []
        for fname in fnames:
            with open(f"{data_dir}/{fname}", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    p = re.compile(r"[가-힣]+")

                    title = fname.split(".")[0]
                    tokens = line.split()
                    idx = tokens[0]
                    abbr = p.match(tokens[1]).group()
                    chapter, verse = tokens[1].replace(abbr, "").split(":")
                    chapter = int(chapter)
                    verse = int(verse)
                    text = " ".join(tokens[2:])

                    docs.append(
                        BibleKRVDocument(
                            _index=index_name,
                            _id=f"{abbr}_{chapter}_{verse}",
                            idx=idx,
                            title=title,
                            title_abbreviation=abbr,
                            chapter=chapter,
                            verse=verse,
                            text=text,
                        ).to_dict(include_meta=True)
                    )

        es_conn = connections.get_connection()
        for i in range(0, len(docs), cls.INDEX_BATCH_SIZE):
            batch_docs = docs[i : i + cls.INDEX_BATCH_SIZE]
            helpers.bulk(es_conn, batch_docs)
            es_conn.indices.refresh(index=index_name, request_timeout=10)

    @classmethod
    def _switch_alias(cls, alias_name: str, new_index_name: str):
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
            for old_index_name in set(old_index_names) - set(
                [new_index_name, prev_index_name]
            ):
                es.indices.delete(index=old_index_name)

        except NotFoundError:
            es.indices.put_alias(index=new_index_name, name=alias_name)

    @classmethod
    def full_index(cls, alias_name: str):
        new_index_name = cls._create_index(alias_name=alias_name)
        cls._index_docs(index_name=new_index_name)
        cls._switch_alias(alias_name=alias_name, new_index_name=new_index_name)
