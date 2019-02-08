import toolkit_sqlite

DB_FILE = 'phone_region.db'

def load_province():
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        csvFile = 'province_new.list'
        sqlitedb.load_csv(csvFile, tableName='province_priority', delimiter=',', full_refresh=True)



if __name__ == '__main__':
    update_sql = r'''UPDATE number_region
                       SET -- phone_num_region = 'phone_num_region',
                           -- city = 'city',
                           
                    priority = 8
                     WHERE province = '浙江'
                    ;'''
    
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        affected_row = sqlitedb.execute(update_sql)
        print('Affected rows: {}'.format(affected_row))
