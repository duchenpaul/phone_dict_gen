import logging_manager
import logging
import os
import time
import csv

import requests
from bs4 import BeautifulSoup

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


temp_dir = 'temp'
try:
    os.mkdir(temp_dir)
except Exception as e:
    pass


# proxies = {"http": "socks5://192.168.2.211:7891", }
proxies = {"http": "http://192.168.2.211:7890", }
# proxies = None

# Sleep 1 hour if IP is banned
sleep_sec = 60 * 60 * 6

phone_region_list_csv = os.path.join(temp_dir, 'phone_region_list.csv')
csv_header = {"phone_num_region": "", "city": "", "province": ""}

root_url = 'https://www.chahaoba.com/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'www.chahaoba.com',
    'Referer': 'https://www.chahaoba.com/',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
}


def check_request_ip():
    url = 'https://api.ipify.org?format=json'
    resp = requests.get(url, proxies=proxies, timeout=30, verify=False)
    logging.info(resp.text)


def initialize_csv():
    with open(phone_region_list_csv, 'w') as f:
        f.write('')
        csv_writer = csv.DictWriter(f, csv_header.keys())
        csv_writer.writeheader()


def dump_webpage(info, webpage):
    with open(os.path.join(temp_dir, '{}.html'.format(info)), 'w', encoding='utf-8', errors='ignore') as f:
        f.write(webpage)


def get_web_page(url):
    allow_redirects = True
    resp = requests.get(url, headers=headers,
                            allow_redirects=allow_redirects, proxies=proxies, timeout=30, verify=False)
    resp.encoding = 'utf-8'

    # Check if the crawler is detected
    keyword = '抱歉，系统检测到您的访问过于密集，暂时进行了ip屏蔽'

    if keyword in resp.text:
        logging.info('crawler is detected, sleep {}s'.format(sleep_sec))
        time.sleep(sleep_sec)
        logging.info('Sleep time over, try again')
        get_web_page(url)
    return resp.text


@logging_manager.logging_to_file
def fetch_vendor_code_list():
    """Fetch all 3 digits code

    Args:
        None

    Returns:
        list: The return value. list of 3 digits code list of a telecom vendor

    """
    telecom_vendor_link = root_url + '手机号段'
    webpage = get_web_page(telecom_vendor_link)
    dump_webpage('手机号段', webpage)

    soup = BeautifulSoup(webpage, 'lxml')
    vendor_code_selector = '#mw-content-text > ul > li > a:nth-child(1)'
    vendor_code_list = soup.select(vendor_code_selector)
    vendor_code_list = [x.text for x in vendor_code_list]
    vendor_code_list = list(set(vendor_code_list))
    return vendor_code_list


@logging_manager.logging_to_file
def batch_fetch_page(fetch_list):
    '''Download all vender code page
    '''
    fetch_list.sort()
    logging.info("Get fetch list:")
    logging.info(fetch_list)
    for vendor_code in fetch_list:
        phone_code_link = root_url + vendor_code
        logging.info('Fetch web page: ' + phone_code_link)
        webpage = get_web_page(phone_code_link)
        dump_webpage(vendor_code, webpage)
        time.sleep(30)
    logging.info('batch fetch page done.')


@logging_manager.logging_to_file
def extract_vendor_region_link(vendor_code):
    with open(os.path.join(temp_dir, '{}.html'.format(vendor_code)), 'r', encoding='utf-8', errors='ignore') as f:
        webpage = f.read()
    soup = BeautifulSoup(webpage, 'lxml')
    vendor_region_index_selector = '#mw-content-text > h3'
    vendor_region_index_list = soup.select(vendor_region_index_selector)
    vendor_region_index_list = [x.text for x in vendor_region_index_list]
    return vendor_region_index_list


def extract_vendor_region_code_list(vendor_region_index):
    try:
        html_file = os.path.join(temp_dir, '{}.html'.format(vendor_region_index))
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            webpage = f.read()
        soup = BeautifulSoup(webpage, 'lxml')
        vendor_region_code_selector = '#myarticle > ol > li'
        vendor_region_code_list = soup.select(vendor_region_code_selector)
        vendor_region_code_list = [x.text for x in vendor_region_code_list]
        region = ''.join([i for i in vendor_region_index if not i.isdigit()])
        vendor_region_code_dict_list = []
        logging.info('Export to csv file')
        logging.info('Region: {}'.format(region))
        for vendor_region_code in vendor_region_code_list:
            vendor_region_code_dict_list.append({"phone_num_region": vendor_region_code, "city": "", "province": region})
        with open(phone_region_list_csv, 'a', newline='', encoding='utf-8', errors='ignore') as f:
            csv_writer = csv.DictWriter(f, csv_header.keys())
            csv_writer.writerows(vendor_region_code_dict_list)

    except Exception as e:
        logging.exception('Failed to fetch vendor_region_code_list for {}, check {}'.format(vendor_region_index, html_file))
    else:
        return vendor_region_code_list
    finally:
        pass


def trim_empty_lines(file):
    with open(file) as fd:
        contents = fd.readlines()
    new_contents = []
    # Get rid of empty lines
    for line in contents:
        # Strip whitespace, should leave nothing if empty line was just "\n"
        if not line.strip():
            continue
        # We got something, save it
        else:
            new_contents.append(line)

    with open(file, 'r') as f:
        f.write(file)


if __name__ == '__main__':
    check_request_ip()
    initialize_csv()
    vendor_code_list = fetch_vendor_code_list()
    # vendor_code_list = vendor_code_list[:3]
    batch_fetch_page(vendor_code_list)

    for vendor_code in vendor_code_list:
        vendor_region_index_list = extract_vendor_region_link(vendor_code)
        # vendor_region_index_list = vendor_region_index_list[:3]
        batch_fetch_page(vendor_region_index_list)
        for vendor_region_index in vendor_region_index_list:
            extract_vendor_region_code_list(vendor_region_index)

    # trim_empty_lines(phone_region_list_csv)
    logging.info('Finished')
