"""This module does the query execution to the database"""


import io
import logging as log
from typing import List

import pandas as pd
import psycopg2 as pg
from psycopg2.extensions import connection

log.basicConfig(level=log.DEBUG)


def execute_queries_get_dataframes(con: connection, query: str, item_count: int, person: str) -> pd.DataFrame:
    """Excute the list of queries as sql and returns dataframes.

    Args:
        query_string_list ([str]): list of query strings to execute on database

    Returns:
        response ([dataframe]): the data from database a dataframe for each query

    Errors:
        response ([str]): returns a list (equal in length to args list length)
                          of string message with database error"""

    try:
        cur = con.cursor()
        cur.execute(query, (person, item_count))
        data = cur.fetchall()
        cur.close()
        return pd.DataFrame.from_records(data)
    except pg.Error as error:
        log.error(error)
        raise error
