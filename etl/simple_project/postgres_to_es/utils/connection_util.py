from contextlib import contextmanager

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import RealDictCursor
from utils.backoff_util import backoff


@contextmanager
@backoff()
def elastic_search_connection(dsn: str):
    es_connection = Elasticsearch(dsn)
    try:
        yield es_connection
    finally:
        es_connection.close()


@contextmanager
@backoff()
def postgres_connection(dsn: dict):
    connection = psycopg2.connect(**dsn, cursor_factory=RealDictCursor)
    connection.set_session(autocommit=True)
    try:
        yield connection
    finally:
        connection.close()
