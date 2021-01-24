import logging_manager
import logging
import os


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

proxies = {"http": "socks5://localhost:1080", }

root_url = 'https://www.chahaoba.com/'
headers = {
    'Host': 'www.chahaoba.com:443', 
    'Proxy-Connection': 'keep-alive', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 
}


def fetch_vendor_code_list():
    """Fetch 3 digits code list of a telecom vendor

    Args:
        None

    Returns:
        list: The return value. list of 3 digits code list of a telecom vendor

    """
    telecom_vendor_link = root_url + '手机号段'
    allow_redirects = True
    print(telecom_vendor_link)
    resp = requests.get(telecom_vendor_link, headers=headers,
                            allow_redirects=allow_redirects, proxies=proxies, timeout=30, verify=False)
    # resp.encoding = 'gb2312'
    # print(resp.text)
    with open(os.path.join(temp_dir, 'temp.html', 'w')) as f:
        f.write(resp.text)
    soup = BeautifulSoup(resp.text, 'lxml')
    code_area_selector = '#mw-content-text > ul:nth-child(12) > li:nth-child(1) > a:nth-child(1)'
    vendor_code_list = soup.select(code_area_selector)


if __name__ == '__main__':
    vendor_code_list = fetch_vendor_code_list()
    print(vendor_code_list)