"""This module does the query execution to the database"""


import io
import logging as log
from typing import List

import pandas as pd
import psycopg2 as pg
from psycopg2.extensions import connection

log.basicConfig(level=log.DEBUG)


def execute_queries_get_dataframes(con: connection, query_string_list):  # TODO: rm if unused
    """Excute the list of queries as sql and returns dataframes.

    Args:
        query_string_list ([str]): list of query strings to execute on database

    Returns:
        response ([dataframe]): the data from database a dataframe for each query

    Errors:
        response ([str]): returns a list (equal in length to args list length)
                          of string message with database error"""
    response = []

    try:
        # create a cursor
        cur = con.cursor()
        # declare dataframe list
        df_list = []
        # loop through the list
        for query in query_string_list:
            # create new stringIO
            store = io.StringIO()
            # put query into sql
            sql_string = "COPY ({query}) TO STDOUT WITH CSV HEADER".format(query=query)
            # put sql response into stringio
            cur.copy_expert(str(sql_string), store)
            # prepare to read csv
            store.seek(0)
            # put csv into dataframe
            df = pd.read_csv(store, na_filter=False)
            # add dataframe to list
            df_list.append(df)

        # commit executions
        con.commit()
        # close the cursor
        cur.close()

        response = df_list

    except pg.Error as error:
        for query in query_string_list:
            response.append(error)
    finally:
        if con is not None:
            con.close()

    return response


def exc_qrs_get_dfs(con: connection, query_string_list: List[str]) -> List[pd.DataFrame]:
    """Excute the list of queries as sql and returns dataframes.

    Args:
        query_string_list ([str]): list of query strings to execute on database

    Returns:
        response ([dataframe]): the data from database a dataframe for each query

    Errors:
        response ([str]): returns a list (equal in length to args list length)
                          of string message with database error"""

    df_list = []
    response = []

    for query in query_string_list:
        try:
            cur = con.cursor()
            cur.execute(query)  # TODO: parameterize query
            data = cur.fetchall()
            cur.close()
            df = pd.DataFrame.from_records(data)
            df_list.append(df)
            response = df_list
        except pg.Error as error:
            log.error(error)
            for _ in query_string_list:
                response.append(error)

    return response
