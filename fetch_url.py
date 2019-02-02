import os
import requests
from bs4 import BeautifulSoup

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


url = 'http://www.51hao.cc/index.php'
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

resp = requests.get(url, headers=headers, allow_redirects=allow_redirects)
resp.encoding = 'gb2312'

# print(resp.text)
with open('index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(resp.text)

soup = BeautifulSoup(resp.text, 'lxml')
links = [a.get('href') for a in soup.find_all('a', href=True)]
validlink = [x for x in links if x.endswith('php')]
print('\n'.join(validlink))

for link in validlink:
    print(link.split('/')[-1])
    resp = requests.get(link, headers=headers, allow_redirects=allow_redirects)
    resp.encoding = 'gb2312'
    with open('html' + os.sep + link.split('/')[-1] + '.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(resp.text)
