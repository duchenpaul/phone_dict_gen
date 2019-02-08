import logging_manager
import toolkit_sqlite

DB_FILE = 'phone_region.db'

query_sql = 'SELECT phone_num_region FROM vw_numer_region_priority where priority <> 0 order by priority desc;'


@logging_manager.logging_to_file
def query_phone_num_region():
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        phone_num_region = [x[0] for x in sqlitedb.query(query_sql)]
    return phone_num_region


@logging_manager.logging_to_file
def generate_dict(phone_num_region):
    with open('phone.dict', 'w') as f:
        f.write('')
        for i in phone_num_region:
            for j in range(10000):
                phone_number = i + str(j).zfill(4)
                f.write(phone_number + '\n')


@logging_manager.logging_to_file
def generate_dict_8_digits():
    digits = 8

    add_number = r'''
    1234567890
    123456789
    '''
    with open('8_digits.dict', 'w') as f:
        f.write('\n'.join([x for x in add_number.split('\n') if x]))

    with open('8_digits.dict', 'a') as f:
        f.write('\n')
        for j in range(10**digits):
            number = str(j).zfill(digits)
            f.write(number + '\n')


if __name__ == '__main__':
    phone_num_region = query_phone_num_region()
    generate_dict(phone_num_region)
    # generate_dict_8_digits()
