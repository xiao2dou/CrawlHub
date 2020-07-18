#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:14:40 2020

@author: liudongjin
"""

import codecs


class DataOutput(object):
    '''将爬到的数据存储
    Attributes:
        datas: 保存爬取到的所有data
    '''

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        '''将爬到的数据存储到datas中
        Args:
            data: 新爬取到的数据
        '''
       if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        '''将爬取到的所有数据写入到HTML文件
        '''
       fout = codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
