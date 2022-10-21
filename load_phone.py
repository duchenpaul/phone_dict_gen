import logging_manager
import logging

import os
from bs4 import BeautifulSoup
import pandas as pd

import toolkit_file
import toolkit_sqlite
import toolkit_text

DB_FILE = 'phone_region.db'
tableName = 'phone_area'

SOURCE_FOLDER = './'

datafile = os.path.join(SOURCE_FOLDER, 'phone.csv')


def load_table_in_chunks():
    df = pd.read_csv(datafile, header=0)
    logging.info('Load to table')
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        df.to_sql(tableName, con=sqlitedb.conn,
                  index=False, if_exists='append')


@logging_manager.logging_to_file
def main():
    load_table_in_chunks()


if __name__ == '__main__':
    main()
