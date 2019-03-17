import time
import requests
from fake_useragent import UserAgent
from lxml import etree
import re
from handle_db import get_random_id
from handle_db import insert_mysql
import hashlib
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor


def get_md5(share_id):
    if isinstance(share_id, str):
        share_id = share_id.encode("utf-8")
    m = hashlib.md5(share_id)
    return m.hexdigest()


# web页面字体反混淆破解
def handle_font_decode(input_data):
    regex_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    for i in regex_list:
        for j in i['name']:
            input_data = re.sub(j, str(i['value']), input_data)
    share_douyin_content = etree.HTML(input_data)
    return share_douyin_content


# 将抖音用户信息插入字典并将字典插入数据库
def item_insert(share_douyin_content):
    user_info = {}
    user_info['nick_name'] = str(share_douyin_content.xpath("//p[@class='nickname']/text()")[0])
    douyin_id = re.match('抖音ID：(.*)', ''.join(share_douyin_content.xpath("//p[@class='shortid']//text()")).replace(' ', '')).group(1)
    user_info['douyin_id'] = douyin_id
    user_info['md5_id'] = get_md5(douyin_id)
    user_info['signature'] = str(share_douyin_content.xpath("//p[@class='signature']//text()")[0])
    user_info['location'] = str(share_douyin_content.xpath("//p[@class='extra-info']/span[1]/text()")[0])
    user_info['constellation'] = str(share_douyin_content.xpath("//p[@class='extra-info']/span[2]/text()")[0])
    user_info['focus_num'] = ''.join(share_douyin_content.xpath("//span[@class='focus block']/span[@class='num']//text()")).replace(' ', '')
    # 判断粉丝数是否过万
    follwer_num = ''.join(share_douyin_content.xpath("//span[@class='follower block']/span[@class='num']//text()"))
    if 'w' in follwer_num:
        user_info['follower_num'] = str(int(''.join(share_douyin_content.xpath("//span[@class='follower block']/span[@class='num']/i/text()")))/10)+'w'
    else:
        user_info['follower_num'] = ''.join(share_douyin_content.xpath("//span[@class='follower block']/span[@class='num']/i/text()"))
    # 判断点赞数是否过万
    praise_received = ''.join(share_douyin_content.xpath("//span[@class='liked-num block']/span[@class='num']//text()"))
    if 'w' in praise_received:
        user_info['praise_received'] = str(int(''.join(share_douyin_content.xpath("//span[@class='liked-num block']/span[@class='num']/i/text()")))/10)+'w'
    else:
        user_info['praise_received'] = ''.join(share_douyin_content.xpath("//span[@class='follower block']/span[@class='num']/i/text()"))
    user_info['production_num'] = int(''.join(share_douyin_content.xpath("//div[@class='user-tab active tab get-list']//i/text()")))
    user_info['liked_num'] = int(''.join(share_douyin_content.xpath("//div[@class='like-tab tab get-list']//i/text()")))
    print(user_info)
    insert_mysql(user_info)


# 处理抖音用户信息的主方法
def handle_douyin_web_share(user_id):
    share_douyin_url = 'https://www.douyin.com/share/user/{0}'.format(user_id)
    share_web_header = {
        'User-Agent': UserAgent().chrome
    }
    share_douyin_response = requests.get(url=share_douyin_url, headers=share_web_header)
    share_douyin_content = handle_font_decode(share_douyin_response.text)
    item_insert(share_douyin_content)


# 创建队列，利用多线程请求数据库的抖音ID
queue_list = Queue()
pool = ThreadPoolExecutor(max_workers=20)
for i in range(100):
    for j in range(100):
        share_id = get_random_id()['share_id']
        queue_list.put(share_id)
    while queue_list.qsize() > 0:
        try:
            pool.submit(handle_douyin_web_share, queue_list.get())
        except Exception as e:
            print(e.args)




