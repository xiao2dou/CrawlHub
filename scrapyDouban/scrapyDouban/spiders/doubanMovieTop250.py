import scrapy


class Doubanmovietop250Spider(scrapy.Spider):
    name = 'doubanMovieTop250'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
