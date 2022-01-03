import scrapy


class MoviesSpider(scrapy.Spider):
    name = "all_movies"
    start_urls = [
        'https://imsdb.com/all-scripts.html/',
    ]

    def parse(self, response):
        for movie in response.css('p'):
            yield {
                'name':
                movie.css('a::attr(title)').extract_first(),
                'link':
                'http://www.imsdb.com' +
                movie.css('a::attr(href)').extract_first().replace(' ', '%20'),
            }
