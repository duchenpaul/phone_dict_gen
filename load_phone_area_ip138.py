import logging_manager
import logging

import os
from bs4 import BeautifulSoup
import pandas as pd

import toolkit_file
import toolkit_sqlite
import toolkit_text

DB_FILE = 'phone_region.db'
tableName = 'phone_area_ip138'

SOURCE_FOLDER = 'html_138'


# @logging_manager.logging_to_file
def extract_info(html):
    '''Extract infomation from html'''
    infoDict = {
        'phone_number_prefix': int(toolkit_file.get_basename(html)),
        'province': None,
        'city': None,
        'card_type': None,
        'area_code': None,
        'postal_code': None,
    }

    # phone_number_prefix is not registered
    with open(html, encoding='utf-8') as f:
        if '验证手机号有误' in f.read():
            return infoDict

    df = pd.read_html(html)[0]
    tmp_dict = dict()
    for index, row in df.iterrows():
        tmp_dict[row[0]] = row[1]

    # print(tmp_dict)
    try:
        infoDict['phone_number_prefix'] = int(tmp_dict['手机号码段'].replace('*', ''))
        infoDict['province'] = tmp_dict['卡号归属地'].split(' ')[0]
        infoDict['city'] = tmp_dict['卡号归属地'].split(' ')[1]
        infoDict['card_type'] = tmp_dict['卡 类 型']
        infoDict['area_code'] = tmp_dict['区 号']
        infoDict['postal_code'] = tmp_dict['邮 编']
    except Exception as e:
        logging.error('Error when loading {}'.format(html))
        logging.error('Data {}'.format(tmp_dict))
        raise
    else:
        pass
    finally:
        pass
    return infoDict


@logging_manager.logging_to_file
def batch_load_to_table(fileList):
    # fileList = toolkit_file.get_file_list(SOURCE_FOLDER)
    infoDictList = []
    for file in fileList:
        infoDictList.append(extract_info(file))

    df = pd.DataFrame(infoDictList)
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        df.to_sql(tableName, con=sqlitedb.conn,
                  index=False, if_exists='append')


# @logging_manager.logging_to_file
def load_table_in_chunks():
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        sqlitedb.execute('DELETE FROM {}'.format(tableName))

    fileList = toolkit_file.get_file_list(SOURCE_FOLDER)

    chunk_size = 100000
    start_number = 1
    file_count = len(toolkit_file.get_file_list(SOURCE_FOLDER))
    logging.info('Read {} files'.format(file_count))
    for chunk in toolkit_text.chunks(toolkit_file.get_file_list(SOURCE_FOLDER), chunk_size):
        logging.info('Loading {}-{}'.format(start_number,
                                            min(start_number + chunk_size - 1, file_count)))
        batch_load_to_table(chunk)
        start_number += chunk_size


@logging_manager.logging_to_file
def main():
    load_table_in_chunks()


if __name__ == '__main__':
    main()
