import logging
import logging_manager
import toolkit_sqlite

DB_FILE = 'phone_region.db'

query_sql = 'SELECT phone_num_region FROM vw_numer_region_priority where priority <> 0 order by priority desc;'
# query_sql = '''SELECT phone_number_prefix
#   FROM phone_area_ip138
#        JOIN
#        province_priority ON phone_area_ip138.province = province_priority.province
#  WHERE priority <> 0
#  ORDER BY priority DESC;
# '''
query_sql = r'''SELECT phone_number_prefix FROM phone_area 
                -- where city like '%南京%'
                -- where province in ('江苏')
                ORDER BY phone_number_prefix;'''
output_dict_file = 'phone.dict'


@logging_manager.logging_to_file
def query_phone_num_region():
    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        phone_num_region = [x[0] for x in sqlitedb.query(query_sql)]
    return phone_num_region


@logging_manager.logging_to_file
def generate_dict(phone_num_region):
    logging.info("Generate phone dictionary...")
    with open(output_dict_file, 'w') as f:
        f.write('')
        for i in phone_num_region:
            for j in range(10000):
                phone_number = str(i) + str(j).zfill(4)
                f.write(phone_number + '\n')


@logging_manager.logging_to_file
def generate_dict_8_digits():
    logging.info("Generate 8 digits dictionary...")
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
    generate_dict_8_digits()
