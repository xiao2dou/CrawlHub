# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    grade = scrapy.Field()  # 评分
    actor = scrapy.Field()  # 主演
    rank = scrapy.Field()  # 排名
    quote = scrapy.Field()  # 描述
    url = scrapy.Field()  # 详情页URL
    image_url = scrapy.Field()  # 图片URL
