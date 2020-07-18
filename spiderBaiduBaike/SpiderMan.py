#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:32:11 2020

@author: liudongjin
"""


from URLManager import UrlManager
from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from DataOutput import DataOutput


class SpiderMan(object):
    '''爬虫调度器
    Attributes:
        manager: URL管理器
        downloader: HTML下载器
        parser: HTML解析器
        output: 数据存储器
    '''

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        '''爬虫调度函数
        Args:
            root_url: 爬虫入口URL
        Raises:
            Expection: 'NoneType' object has no attribute
        '''
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() and self.manager.old_url_size() < 100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print('已经抓取了%s个链接' % self.manager.old_url_size())
            except Exception as e:
                print('Crawl failed: %s' % e)
        self.output.output_html()


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl(
        'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711?fr=aladdin')
