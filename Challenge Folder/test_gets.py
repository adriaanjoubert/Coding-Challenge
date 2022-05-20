"""This module has the functions that get data from the database"""


import logging as log

from psycopg2.extensions import connection

from test_database import execute_queries_get_dataframes

log.basicConfig(level=log.DEBUG)
log.info('----- QRS_GETS.PY -----')


def get_table(con: connection, item_count: int, person: str):
    """Gets all data needed to display map from the desk being scanned.

    Args:
        table=None (str): determines which table to return

    Return:
        response_object (obj): python object of returned dataframes of the following:
            "users_table" (df): if arg was user
            "data_table" (df): if arg was data"""
    query = "SELECT records.id, records.person, data.text, data.json FROM records LEFT OUTER JOIN data ON records.data_id = data.id WHERE records.person = %s LIMIT %s;"

    try:
        df = execute_queries_get_dataframes(con=con, query=query, item_count=item_count, person=person)
        df = df.rename(columns={0: 'id', 1: 'person', 2: 'text', 3: 'json'})
        log.info("database response: %s", df)
        return df
    except Exception as error:
        log.info(error)
        return error
