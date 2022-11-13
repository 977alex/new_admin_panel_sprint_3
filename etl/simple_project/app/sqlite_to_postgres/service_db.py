"""заданные функции для sql баз данных """

from datetime import datetime


def table_with_schema(table_name, schema_name):
    if schema_name:
        return '{0}.{1}'.format(schema_name, table_name)
    else:
        return table_name


def create_select_query(
    table_name: str, schema_name: str, fields: [], where_fields: [] = None,
) -> str:
    """создать нужный запрос в базу данных"""
    query = 'SELECT '
    query += ','.join(fields)
    query += ' FROM {0}'.format(table_with_schema(table_name, schema_name))
    where_clause = ''
    if where_fields:
        index = 0
        where_clause = ' WHERE '
        for field in where_fields:
            where_clause += '{0} = ? and '.format(field)
            index += 1
        where_clause = where_clause[:-5]

    query += '{0};'.format(where_clause)

    return query


def create_insert_query(table_name: str, schema_name: str, fields: [],) -> str:
    """создать запрос на добавление записи в базу sql без данных"""
    fields_string = ', '.join(fields)
    values_string = ('%s, ' * len(fields))[:-2]
    return 'INSERT INTO {0} ({1}) VALUES({2});'.format(
        table_with_schema(table_name, schema_name), fields_string, values_string,
    )


def create_delete_query(table_name: str, schema_name: str,) -> str:
    """формирование запроса на удаление записей таблиц"""
    return 'DELETE FROM {0};'.format(table_with_schema(table_name, schema_name))


def get_args_for_insert_query(table_name, table_data, table_set,) -> list:
    """экспорт из sql таблицы аргументов и запись в arg_list"""
    arg_list = []
    for dc_object in table_data:
        args = []
        for field in table_set['fields']:
            args.append(dc_object.__dict__[field])
        for _ in table_set['service_fields']:
            args.append(datetime.now())
        arg_list.append(args)
    return arg_list
