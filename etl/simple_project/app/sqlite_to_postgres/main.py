"""перенос данных заданных таблиц sqlite в соответсвующие таблицы postgres """

import contextlib
import logging
import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor
from tables_set import get_tables_set


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    """основная функция"""
    tables_set = get_tables_set()
    page_size = int(os.environ.get('PAGE_SIZE'))

    postgres_saver = PostgresSaver(
        pg_conn,
        tables_set,
        os.environ.get('POSTGRES_SCHEMA_NAME'),
    )
    sqlite_extract = SQLiteExtractor(sqlite_conn, tables_set)
    postgres_saver.delete_all_data()

    for table_name in list(tables_set.keys()):
        """цикл для выбора данных заданных таблиц из sqlite и сохранением в postgres"""
        table_set = tables_set[table_name]
        curs = sqlite_extract.get_cursor_for_select(table_name)

        while table_data := sqlite_extract.extract_data_from_cursor(
                curs,
                table_set['dataclass'],
                page_size,
        ):
            postgres_saver.save_all_data(table_name, table_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    dsn = {
        'dbname': os.environ.get('POSTGRES_DBNAME'),
        'user': os.environ.get('USE'),
        'password': os.environ.get('PASSWORD'),
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT'),
        }
    sqlite_dbname = os.environ.get('SQLITE_DBNAME')
    with conn_context(sqlite_dbname) as sqlite_conn, \
            contextlib.closing(psycopg2.connect(**dsn, cursor_factory=DictCursor)) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    logging.info('COMPLETE')
