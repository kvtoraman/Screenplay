import scrapy



class MoviesSpider(scrapy.Spider):
    name = "movies"
    start_urls = [
        'http://www.imsdb.com/all%20scripts/',
    ]

    def parse(self, response):
        for movie in response.css('p'):
            yield {	
                'name': movie.css('a::attr(title)').extract_first(),
                'link': 'http://www.imsdb.com' + movie.css('a::attr(href)').extract_first().replace(' ','%20'),
			}

