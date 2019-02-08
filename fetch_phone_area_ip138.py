import os
import requests

headers = {
    'Host': 'm.ip138.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://m.ip138.com/mobile.asp?mobile=1000000',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Cookie': 'ASPSESSIONIDSAQADCSR=GHCJHCODOCHPGMBPEPAHDEDH',
}

def get_phone_area(number):
    url = 'http://m.ip138.com/mobile.asp?mobile=' + number
    resp = requests.get(url, headers=headers)
    resp.encoding = 'gb2312'
    # print(resp.text)
    with open('html_138' + os.sep + number + '.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(resp.text)


if __name__ == '__main__':
    for number in range(1000000, 1000000 * 2):
        get_phone_area(number)