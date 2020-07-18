# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:32:40 2020

@author: Zhenlin
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
#data = urllib.parse.urlencode(values)
#data = data.encode('ascii')

keyword = '日'  # 用于判断乱码，一般来说，新闻中肯定包括了日期


def get_one_page_news(page_url):
    '''获取某一新闻列表页上的全部新闻摘要[date_time, url, title]
    Args:
        page_url:新闻列表页面的URL
    Returns:
        返回当前页面上所有新闻列表List[List[]]，列表中每一个元素为一条新闻的[date_time, url, title]
    '''
    #    page_url='http://www.chinanews.com/scroll-news/2020/0702/news.shtml'
    root = 'http://www.chinanews.com'
    req = urllib.request.Request(page_url, headers=headers)

    try:
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read()
    except socket.timeout as err:
        print('socket.timeout')
        print(err)
        return []
    except Exception as e:
        print("-----%s:%s %s-----" % (type(e), e, page_url))
        return []

    # http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
    soup = BeautifulSoup(html, "html.parser")

    news_pool = []
    news_list = soup.find('div', class_="content_list")
    items = news_list.find_all('li')
    for i, item in enumerate(items):
        #        print('%d/%d'%(i,len(items)))
        if len(item) == 0:  # 存在空行
            continue

        a = item.find('div', class_="dd_bt").find('a')
        title = a.string
        url = a.get('href')
        if root in url:
            url = url[len(root):]  # 切片，去掉root '/sh/2020/07-02/9227317.shtml'

        category = ''
        try:
            category = item.find('div', class_="dd_lm").find('a').string
        except Exception as e:
            continue

        if category == '图片':  # 图片新闻不爬取
            continue

        year = url.split('/')[-3]
        date_time = item.find('div', class_="dd_time").string  # 7-2 11:48
        date_time = '%s-%s:00' % (year, date_time)

        news_info = [date_time, "http://www.chinanews.com"+url, title]
        news_pool.append(news_info)
    return news_pool


def get_news_pool(start_date, end_date):
    '''获取新闻列表池
    Args:
        start_date:开始日期
        end_date:结束日期
    Returns:
        返回一个新闻列表List[List[]]，列表中每一个元素为一条新闻的[date_time, url, title]
    '''
    news_pool = []
    delta = timedelta(days=1)
    while start_date <= end_date:
        date_str = start_date.strftime("%Y/%m%d")  # 2020-07-02 --> 2020/0702
        page_url = 'http://www.chinanews.com/scroll-news/%s/news.shtml' % (  # 滚动新闻栏目
            date_str)
        print('Extracting news urls at %s' % date_str)
        news_pool += get_one_page_news(page_url)
#        print('done')
        start_date += delta
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

        # http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        soup = BeautifulSoup(html, "html.parser")
        [s.extract() for s in soup('script')]  # 去除script

        try:
            ps = soup.find('div', class_="left_zw").find_all('p')
        except Exception as e:
            print("--2---%s: %s-----" % (type(e), news[1]))
            print("Sleeping for 10 minute")
            time.sleep(600)
            continue

        body = ''
        for p in ps:
            cur = p.get_text().strip()  # 去除首尾空格
            if cur == '':
                continue
            body += '\t' + cur + '\n'
        body = body.replace(" ", "")

        if keyword not in body:  # 过滤掉乱码新闻
            continue

        if len(body) <= min_body_len:
            continue

        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d" % (i)
        ET.SubElement(doc, "url").text = news[1]
        ET.SubElement(doc, "title").text = news[2]
        ET.SubElement(doc, "datetime").text = news[0]
        ET.SubElement(doc, "body").text = body
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

    delta = timedelta(days=-5)
    end_date = date.today()
    start_date = end_date + delta  # 5天前
    news_pool = get_news_pool(start_date, end_date)
    news_pool = list(set(news_pool))
    print('Starting to crawl %d chinanews' % len(news_pool))
    # doc_dir_path = config['DEFAULT']['doc_dir_path']+'chinanews/'
    crawl_news(news_pool, 140, config['DEFAULT']
               ['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    print('done!')
