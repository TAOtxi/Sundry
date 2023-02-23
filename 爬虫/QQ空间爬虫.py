import urllib.request
import urllib.parse
import re
import time


def html(num):
    # 在一个叫 emotion_cgi_msglist_啥啥啥的请求网址
    url = ''
    # 换页
    url = re.sub(r'(pos=)\d+(&num)', r'\1{}\2', url).format(num)
    headers = {
        'cookie': ''
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


content = []
# 定义页数，这里设置最多爬200条
for i in range(0, 200, 20):
    json = html(i)
    content = content + re.findall('("certified":0.*?"wbid":0)', json)
    time.sleep(1)
for i in range(len(content)):
    title = re.findall(r'"commentlist".*'
                       '"content":"(.*?)",'
                       '"createTime":"(.*?)".*'
                       '"source_name":"(.*?)"', content[i])[0]

    # 组合说说内容
    title = ['[{}][{}]{}'.format(title[2], title[1], title[0])]
    if re.findall('"commentlist":(.*?),', content[i]) != ['null']:

        # 把每条评论摘出来
        comment = re.findall(r'({"IsPasswordLuckyMoneyCmtRight".*?'
                             '"private".*?"uin":\d+})', content[i])
        for j in range(len(comment)):
            # 把评论元素和每条回复抓出来
            comment[j] = re.findall(r'"content":"(.*?)".*?'
                                    '"createTime2":"(.*?)".*?'
                                    '("list_3":\[.*])?,'
                                    '"name":"(.*?)".*'
                                    '"uin":(\d+)', comment[j])[0]
            reply = comment[j][2]
            comment[j] = ['[{}]{}({}):{}'.format(comment[j][1], comment[j][3], comment[j][4], comment[j][0])]
            # 判断评论是否有回复
            if reply != "":
                # 抓回复内容的元素
                reply = re.findall(r'"content":"(.*?)".*'
                                   '"createTime2":"(.*?)".*'
                                   '"name":"(.*?)".*'
                                   '"uin":(\d+)', reply)
                for k in range(len(reply)):
                    reply[k] = '[{}]{}({})回复{}'.format(reply[k][1],
                                                         reply[k][2],
                                                         reply[k][3],
                                                         re.sub(r'@{uin:(\d+),nick:(.*?),.*}(.*)',
                                                                r'\2(\1):\3',
                                                                reply[k][0]))
                    comment[j].append(reply[k])
            title.append(comment[j])
    content[i] = title

time = time.strftime('%Y-%m-%d', time.localtime())
# 获取名字
filename = '{}-QQ空间({}).txt'.format(re.findall('.*"name":"(.*?)"', json)[0], time)
with open(filename, 'a', encoding='utf-8') as fb:
    for i in content:
        # 说说
        fb.write(i[0] + '\n')
        for j in i[1:]:
            # 评论
            fb.write('\t' + j[0] + '\n')
            for k in j[1:]:
                # 回复
                fb.write('\t\t' + k + '\n')
        fb.write('\n')
