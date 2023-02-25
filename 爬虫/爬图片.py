import urllib.request
from lxml import etree
import time


def html(num):
    if num == 1:
        url = 'https://sc.chinaz.com/tupian/chengshijingguantupian.html'
    else:
        url = 'https://sc.chinaz.com/tupian/chengshijingguantupian_%d.html' % num
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content

alt, src = [], []
for i in range(1, 10):
    tree = etree.HTML(html(i))
    alt = alt + tree.xpath('//div[@class="tupian-list com-img-txt-list"]//img/@alt')
    src = src + tree.xpath('//div[@class="tupian-list com-img-txt-list"]//img/@data-original')
    time.sleep(1)

for i in range(len(alt)):
    name = alt[i] + '.jpg'
    url = 'https:' + src[i].replace('_s', '')
    urllib.request.urlretrieve(url=url, filename='./图片(高清)/' + name)
