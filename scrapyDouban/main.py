from scrapy.cmdline import execute

execute(["scrapy", "crawl", "doubanMovieTop250", "-o", "doubanMovieTop250.json"])