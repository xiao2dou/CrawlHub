#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:35:06 2020

@author: liudongjin
"""


class UrlManager(object):
    '''URL管理类    
    Attributes:
        new_urls: 未爬取的URL集合
        old_urls: 已爬去的URL集合
    '''

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''是否还有未爬取的URL  
        Returns:
            布尔值
        '''
        return len(self.new_urls) != 0

    def get_new_url(self):
        '''获取未爬取的URL  
        Returns:
            new_url: 从new_urls集合中取出的新的URL
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        '''增加一个新的URL
        Args:
            url: 待加入的新的URL
        Returns:
        '''
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''增加多个新的URL  
        Args:
            urls: 待加入的新的URL
        Returns:
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        '''待爬取的URL数量  
        Returns:
            待爬取的URL数量
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''已爬取的URL数量  
        Returns:
            已爬取的URL数量
        '''
        return len(self.old_urls)
