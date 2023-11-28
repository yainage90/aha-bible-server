from fastapi import APIRouter
from app.es.documents.bible_krv import BibleKRVDocument
from app.es.index.bible_krv import Indexer as BibleKrvIndexer

router = APIRouter(prefix="/es")


@router.get("/full_index/bible_krv")
async def search_index() -> dict:
    result = BibleKrvIndexer.full_index(BibleKRVDocument.Index.name)
    return result
