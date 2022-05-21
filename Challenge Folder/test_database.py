import logging as log

import pandas as pd
import psycopg2 as pg

from test_dbconfig import get_db_kwargs


class DBClient(object):

    def __init__(self) -> None:
        # connect to server
        self.conn = pg.connect(**get_db_kwargs())
        self.cur = self.conn.cursor()

    def get_df(self, item_count: int, person: str) -> pd.DataFrame:
        query = (
            'SELECT records.id, records.person, data.text, data.json '
            'FROM records '
            'LEFT OUTER JOIN data ON records.data_id = data.id '
            'WHERE records.person = %s LIMIT %s;'
        )
        try:
            self.cur.execute(query, (person, item_count))
            data = self.cur.fetchall()
            self.conn.commit()
            df = pd.DataFrame.from_records(data).rename(columns={0: 'id', 1: 'person', 2: 'text', 3: 'json'})
            log.info("database response: %s", df)
            return df
        except pg.Error as error:
            log.error(error)
            raise error

    def get_json(self, item_count: int, person: str) -> str:
        df = self.get_df(item_count=item_count, person=person)
        return df.to_json(orient='records')
