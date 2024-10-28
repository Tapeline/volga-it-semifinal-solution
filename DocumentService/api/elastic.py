from elasticsearch import Elasticsearch

from document_service import settings


def connect():
    print(f"Connecting to {settings.ELASTIC_USER}@{settings.ELASTIC_HOST}")
    return Elasticsearch(
        hosts=[settings.ELASTIC_HOST],
        basic_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASS)
    )


def index_document(uid, body):
    es = connect()
    res = es.index(index="documents", id=str(uid), body=body)
    es.close()


def update_document(uid, body):
    es = connect()
    res = es.update(index="documents", id=str(uid), body={"doc": body})
    es.close()
