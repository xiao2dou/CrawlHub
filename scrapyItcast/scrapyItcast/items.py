# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyitcastTeacherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义结构化数据字段，用来保存爬取到的数据
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
