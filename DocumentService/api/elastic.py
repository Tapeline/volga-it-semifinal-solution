from elasticsearch import Elasticsearch

from document_service import settings


def connect():
    return Elasticsearch(
        hosts=[settings.ELASTIC_HOST],
        basic_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASS)
    )


_es = None


def get_connection():
    global _es
    if _es is None:
        _es = connect()
    return _es


def index_document(uid, body):
    res = get_connection().index(index="documents", id=str(uid), body=body)


def update_document(uid, body):
    res = get_connection().update(index="documents", id=str(uid), body={"doc": body})
