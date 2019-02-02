import logging_manager
import toolkit_sqlite

DB_FILE = 'phone_region.db'

query_sql = 'SELECT phone_num_region FROM number_region;'

@logging_manager.logging_to_file
def query_phone_num_region():
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        phone_num_region = [x[0] for x in sqlitedb.query(query_sql)]
    return phone_num_region


@logging_manager.logging_to_file
def generate_dict(phone_num_region):
    with open('phone.dict', 'w') as f:
        for i in phone_num_region[:10]:
            for j in range(10):
                phone_number = i + str(j).zfill(4)
                f.write(phone_number + '\n')

if __name__ == '__main__':
    phone_num_region = query_phone_num_region()
    generate_dict(phone_num_region)