import logging_manager

import os
from bs4 import BeautifulSoup
import pandas as pd

import toolkit_file
import toolkit_sqlite
import toolkit_text

DB_FILE = 'phone_region.db'
tableName = 'number_region'


@logging_manager.logging_to_file
def get_city_province(html):
    soup = BeautifulSoup(html, 'lxml')
    location = soup.findAll("div", {"class": "title"})[0].text
    province, city = location.split('- ')
    result = {
        'province': province,
        'city': city,
    }
    return result


@logging_manager.logging_to_file
def get_phone_region(html):
    phoneRegionList = toolkit_text.regex_find(r'>\d{7}<', html)
    phoneRegionList = [x.replace('<', '').replace('>', '')
                       for x in phoneRegionList]
    return phoneRegionList


@logging_manager.logging_to_file
def join_number_region(html):
    regionDict, phoneRegionList = get_city_province(
        html), get_phone_region(html)
    phoneNumRegionList = []
    for phoneNumRegion in phoneRegionList:
        regionDict['phone_num_region'] = phoneNumRegion
        phoneNumRegionList.append(regionDict.copy())

    return phoneNumRegionList


if __name__ == '__main__':
    allPhoneNumRegionList = []

    for htmlFile in toolkit_file.get_file_list('html'):
        print('Read ' + htmlFile)
        with open(htmlFile, encoding='utf-8') as f:
            html = f.read()
        allPhoneNumRegionList += join_number_region(html)

    print('Load to database...')
    df = pd.DataFrame(allPhoneNumRegionList)
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        sqlitedb.execute('DELETE FROM {}'.format(tableName))
        df.to_sql(tableName, con=sqlitedb.conn,
                  index=False, if_exists='append')
