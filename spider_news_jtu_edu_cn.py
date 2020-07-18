# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:32:55 2020

@author: LiuDongjin
"""

from bs4 import BeautifulSoup
import urllib.request
import xml.etree.ElementTree as ET
import configparser
from datetime import timedelta, date
import time
import urllib.parse
import socket
from socket import timeout
from os import listdir

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
# values = {'name': 'Michael Foord',
#          'location': 'Northampton',
#          'language': 'Python' }
# data = urllib.parse.urlencode(values)
# data = data.encode('ascii')

keyword = '交'  # 用于判断乱码，一般来说，交大新闻中肯定包括了‘交’
root = 'http://news.xjtu.edu.cn'

def get_one_page_news(page_url):
    '''获取某一新闻列表页上的全部新闻摘要[date_time, url, title]
    Args:
        page_url:新闻列表页面的URL
    Returns:
        返回当前页面上所有新闻列表List[List[]]，列表中每一个元素为一条新闻的[date_time, url, title]
    '''
    # page_url = 'http://news.xjtu.edu.cn/xyzs/21.htm'
    
    req = urllib.request.Request(page_url, headers=headers)

    try:
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read()
        # print(html)
    except socket.timeout as err:
        print('socket.timeout')
        print(err)
        return [],''
    except Exception as e:
        print("-----%s:%s %s-----" % (type(e), e, page_url))
        return [],''

    soup = BeautifulSoup(html, "html.parser")

    news_pool = []
    # news_list = soup.find('div', class_='i_left')
    items = soup.find_all('div', class_='l_li')
    # print(items)
    for i, item in enumerate(items):
        if len(item) == 0:
            continue

        a = item.find('a')
        cite = item.find('cite')
        title = a.get('title')
        url = a.get('href')
        # if root in url:
        #     url = url[len(root):]
        if '..' in url:
            url = url.replace('..', root) # ../info/1004/4750.htm
        else:
            url = root + '/' +url # info/1033/137388.htm
        
        date_time = cite.get_text()
        date_time = date_time[1:-1]  # 删掉日期前的[]

        news_info = [date_time, url, title]
        news_pool.append(news_info)

    # next_url = soup.find('a', class_='Next').get('href') # zyxw/518.htm
    # next_url = root +'/' +next_url

    next = soup.find('a', class_='Next')
    if next is None:
        print('Next page is None')
        return news_pool, ''
    next_url = next.get('href') # 99.htm
    # next_url = root +'/' +next_url
    # print('Next:'+next_url)

    return news_pool, next_url


def get_news_pool(news_category):
    '''获取新闻列表池
    Args:
        news_category:为一个固定列表，指定需要爬取的新闻分类
    Returns:
        返回一个新闻列表List[List[]]，列表中每一个元素为一条新闻的[date_time, url, title]
    '''
    news_pool = []
    for category in news_category:
        url = root + '/' + category + '.htm'
        while 'htm' in url:
            one_page_news_pool, url = get_one_page_news(url)
            news_pool += one_page_news_pool
            # url = root + '/' + category + '/' +url
            if category in url:
                url = root + '/' +url
            else:
                url = root + '/' + category + '/' +url
            print('Extracting news urls at '+ url)
        # page_index = category
        # # begin = category[1]
        # end = category[2]
        # while page_index < end:
        #     # http://news.xjtu.edu.cn/xyzs/21.htm
        #     page_url = 'http://news.xjtu.edu.cn/' + \
        #         category[0]+'/'+str(page_index)+'.htm'
        #     print('Extracting news urls at '+category[0]+str(page_index))
        #     news_pool += get_one_page_news(page_url)
        #     page_index += 1
    return news_pool


def crawl_news(news_pool, min_body_len, doc_dir_path, doc_encoding):
    '''
    开始爬取新闻
    Args:
        news_pool:新闻列表池
        min_body_len:最短新闻长度限制
        doc_dir_path:结果文件存储路径
        doc_encoding:结果文件编码方式
    '''
    files = listdir(doc_dir_path)
    i = len(files)
    news_pool_len = len(news_pool)
    for n, news in enumerate(news_pool):
        print('%d/%d' % (n, news_pool_len))
        req = urllib.request.Request(news[1], headers=headers)
        try:
            response = urllib.request.urlopen(req, timeout=10)
            html = response.read()
#            response = urllib.request.urlopen(news[1])
        except socket.timeout as err:
            print('socket.timeout')
            print(err)
            print("Sleeping for 10 minute")
            time.sleep(600)
            continue
        except Exception as e:
            print("--1---%s:%s %s-----" % (type(e), e, news[1]))
            print("Sleeping for 10 minute")
            time.sleep(600)
            continue

        soup = BeautifulSoup(html, "html.parser")
        [s.extract() for s in soup('script')]  # 去除script

        try:
            ps = soup.find('div', class_="d_detail").find_all('p')
        except Exception as e:
            print("--2---%s: %s-----" % (type(e), news[1]))
            print("Sleeping for 10 minute")
            time.sleep(600)
            continue

        body = ''
        for p in ps:
            cur = p.get_text().strip()
            if cur == '':
                continue
            body += '\t' + cur + '\n'
        body = body.replace(" ", "")

        if keyword not in body:
            continue

        if len(body) <= min_body_len:
            continue

        doc = ET.Element("doc")
        # news_id = 'xjtunews ' + "%d" %(i)
        ET.SubElement(doc, "id").text = "%d" % (i)
        ET.SubElement(doc, "url").text = news[1]
        ET.SubElement(doc, "title").text = news[2]
        ET.SubElement(doc, 'datetime').text = news[0]
        ET.SubElement(doc, 'body').text = body
        tree = ET.ElementTree(doc)
        tree.write(doc_dir_path + "%d.xml" %
                   (i), encoding=doc_encoding, xml_declaration=True)
        i += 1
        if i % 500 == 0:
            print("Sleeping for 3 minute")
            time.sleep(180)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')

    # news_category = [['zyxw', 1, 518],
    #                 ['jyjx', 1, 65],
    #                 ['xyzs', 1, 21],
    #                 ['kydt', 1, 80]]

    news_category = ['zyxw','jyjx','xyzs', 'kydt']

    news_pool = get_news_pool(news_category)
    news_pool = list(set(news_pool))
    print('Starting to crawl %d xjtunews' % len(news_pool))
    # doc_dir_path = config['DEFAULT']['doc_dir_path']+'chinanews/'
    crawl_news(news_pool, 20, config['DEFAULT']
               ['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    print('done!')
