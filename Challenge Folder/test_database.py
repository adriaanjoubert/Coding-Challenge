"""This module does the query execution to the database"""
import logging as log

import pandas as pd
import psycopg2 as pg
from psycopg2.extensions import connection, cursor

log.basicConfig(level=log.DEBUG)


def execute_queries_get_dataframes(conn: connection, cur: cursor, query: str, item_count: int, person: str) -> pd.DataFrame:
    """Excute the list of queries as sql and returns dataframes.

    Args:
        query_string_list ([str]): list of query strings to execute on database

    Returns:
        response ([dataframe]): the data from database a dataframe for each query

    Errors:
        response ([str]): returns a list (equal in length to args list length)
                          of string message with database error"""

    try:
        cur.execute(query, (person, item_count))
        data = cur.fetchall()
        conn.commit()
        return pd.DataFrame.from_records(data)
    except pg.Error as error:
        log.error(error)
        raise error
