import scrapy
from scrapyDouban.items import ScrapydoubanMovieItem

class Doubanmovietop250Spider(scrapy.Spider):
    name = 'doubanMovieTop250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for item in response.css('.item'):
            movie = ScrapydoubanMovieItem()
            title = item.css('.hd span.title::text').extract_first()
            grade = item.css('.star span.rating_num::text').extract_first()
            actor = item.css('.bd p::text').extract_first()
            rank = item.css('.pic em::text').extract_first()
            quote = item.css('.quote span.inq::text').extract_first()
            url = item.css('.pic a::attr("href")').extract_first()
            image_url = item.css('.pic img::attr("src")').extract_first()
            # title = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]')
            # grade = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[2]')
            # actor = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()[1]')
            # rank = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[1]/em')
            # quote = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[2]/span')
            # url = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a')
            # image_url = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[1]/a/img')
            movie['title'] = title
            movie['grade'] = grade
            movie['actor'] = actor
            movie['rank'] = rank
            movie['quote'] = quote
            movie['url'] = url
            movie['image_url'] = image_url
            yield movie

            # next_url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a')
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)

