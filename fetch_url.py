import os
import requests
from bs4 import BeautifulSoup

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

root_url = 'http://www.51hao.cc'

headers = {
    'Host': 'www.51hao.cc',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
}
allow_redirects = True


def get_province_link_list():
    '''Extrect province_link from index page'''
    url = root_url + '/index.php'
    resp = requests.get(url, headers=headers, allow_redirects=allow_redirects)
    resp.encoding = 'gb2312'
    # print(resp.text)
    with open('index.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(resp.text)

    soup = BeautifulSoup(resp.text, 'lxml')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    provinceLinkList = [
        x for x in links if not x.endswith('php') and 'city' in x]
    return provinceLinkList


def get_city_link_list(provinceLink):
    '''Extrect city link from province page'''
    print('Get province ' + provinceLink)
    resp = requests.get(provinceLink, headers=headers,
                        allow_redirects=allow_redirects)
    resp.encoding = 'gb2312'
    soup = BeautifulSoup(resp.text, 'lxml')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    cityLinkList = [provinceLink + '/' + x for x in links if x.endswith('php')]
    return cityLinkList


def download_number_page(cityLink):
    '''Download number_page from city link'''
    print('Get city ' + cityLink.split('/')[-1])

    resp = requests.get(cityLink, headers=headers,
                        allow_redirects=allow_redirects)
    resp.encoding = 'gb2312'
    with open('html' + os.sep + cityLink.split('/')[-1] + '.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(resp.text)


if __name__ == '__main__':
    from pprint import pprint
    province_link_list = get_province_link_list()
    for province_link in province_link_list:
        cityLinkList = get_city_link_list(province_link)
        for cityLink in cityLinkList:
            download_number_page(cityLink)
