#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:56:37 2020

@author: liudongjin
"""


import re
from urllib import parse
from bs4 import BeautifulSoup


class HtmlParser(object):
    '''HTML页面解析
    '''

    def parser(self, page_url, html_cont):
        '''HTML页面解析
        Args:
            page_url: 待解析页面的URL
            html_cont: 待解析页面的HTML
        Returns:
            new_urls: 一个集合，解析出的新的URL
            new_data: 一个字典，解析出的数据，包括[url, title, summary]
        '''
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
    
    def _get_new_urls(self, page_url,soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/.+'))
        for link in links:
            new_url = link['href']
            new_full_url = parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
    
    def _get_new_data(self, page_url, soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', class_='lemma-summary')
        data['summary'] = summary.get_text()
        return data
