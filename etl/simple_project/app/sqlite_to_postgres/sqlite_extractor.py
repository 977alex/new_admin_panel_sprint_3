"""захват данных из таблиц sqlite и формирования целевого запроса в sqlite """

import dataclasses
import logging
import sqlite3

import psycopg2

import service_db


class SQLiteExtractor(object):
    def __init__(
        self, connection: sqlite3.Connection, table_set: dict,
    ):
        self.connection = connection
        self.table_set = table_set

    @staticmethod
    def extract_data_from_cursor(
        cursor: sqlite3.Cursor, dataclass: dataclasses, size: int,
    ) -> []:
        """выбор записей в sqlite  по запросу и сохранение в  data_list """
        data_list = []
        records = cursor.fetchmany(size=size)
        for row in records:
            row_source = dict(row)
            db_object = dataclass(**row_source)
            data_list.append(db_object)
        return data_list

        # while rows := cursor.fetchmany(size=size):
        #     yield from dataclass(**dict(rows))

        # while rows := cursor.fetchmany(size=size):
        #     yield from (dataclass(**item) for item in rows)

    def get_cursor_for_select(self, table_name: str,) -> []:
        table_set = self.table_set.get(table_name)

        curs = self.connection.cursor()
        sql = service_db.create_select_query(table_name, '', table_set['fields'], )

        try:
            curs.execute(sql)
        except psycopg2.Error as err:
            logging.exception(
                (
                    'MYError occurred while saving data from '
                    + '{0}: {1}'.format(table_name, err)
                ),
            )
            return None

        return curs
