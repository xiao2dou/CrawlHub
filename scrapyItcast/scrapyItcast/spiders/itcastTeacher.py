# -*- coding: utf-8 -*-
import scrapy
from scrapyItcast.items import ScrapyitcastTeacherItem

class ItcastteacherSpider(scrapy.Spider):
    name = 'itcastTeacher'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # parse() 解析的方法，每个初始URL完成下载后将被调用，调用的时候传入从每一个URL传回的Response对象来作为唯一参数
        # 功能：
        # 1. 负责解析返回的网页数据(response.body)，提取结构化数据(生成item)
        # 2. 生成需要下一页的URL请求。
        # 3. 将start_urls的值修改为需要爬取的第一个url
        filename = 'teacher.html'
        with open(filename, 'wb') as f:
            # print(response.body)
            f.write(response.body)

        items = []  # 存放老师信息的集合
        for each in response.xpath("//div[@class='li_txt']"):
            item = ScrapyitcastTeacherItem()  # 将我们得到的数据封装到一个 `ItcastItem` 对象
            # extract()方法返回的都是unicode字符串
            name = each.xpath("h3/text()").extract()
            title = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()
            # xpath返回的是包含一个元素的列表
            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]
            # print(name[0])
            items.append(item)

        # 直接返回最后数据
        return items