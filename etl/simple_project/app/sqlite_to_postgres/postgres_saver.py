"""функции взаимодействия с базой  postgres"""

import logging

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

import service_db


class PostgresSaver(object):
    def __init__(
        self, conn: _connection, tables_set: dict, schema_name: str,
    ):
        self.connection = conn
        self.tables_set = tables_set
        self.schema_name = schema_name

    def delete_data_from_table(self, table_name):
        """удаление записей из заданной таблицы"""
        sql = service_db.create_delete_query(table_name, self.schema_name)
        with self.connection.cursor() as cur:
            try:
                cur.execute(sql)
            except psycopg2.Error as err:
                logging.exception(
                    'MYError occurred while deleting data from the tables: ' + '{0}'.format(err),
                )

    def delete_all_data(self):
        """удаление записей из перечисленных таблиц"""
        for table_name in list(self.tables_set.keys())[::-1]:
            self.delete_data_from_table(table_name)

    def save_all_data(self, table_name, table_data):
        """сохранение в базу postgres переданных из базы sqlite данных"""
        table_set = self.tables_set.get(table_name)
        fields = table_set['fields'] + table_set['service_fields']
        insert_query = service_db.create_insert_query(table_name, self.schema_name, fields, )
        args_list = service_db.get_args_for_insert_query(
            table_name, table_data, table_set,
        )
        with self.connection.cursor() as cur:
            try:
                execute_batch(
                    cur, insert_query, args_list,
                )
            except psycopg2.Error as err:
                logging.exception(
                    'MYError occurred while inserting data into '
                    + '{0}: {1}'.format(table_name, err),
                )
