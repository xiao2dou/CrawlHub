#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:49:57 2020

@author: liudongjin
"""


import requests


class HtmlDownloader(object):
    '''获取HTML页面的内容
    '''

    def download(self, url):
        '''下载URL定位的HTML页面    
        Args:
            url: 需要下载HTML页面的URL
        Returns:
            text: 下载到的HTML页面
        '''
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'        
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
