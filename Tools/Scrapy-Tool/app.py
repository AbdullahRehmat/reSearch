import scrapy


class TestSpider(scrapy.Spider):
	name = 'testspider'

	start_urls = [
		"http://www.shia.bs/authors/Admin.cfm",
	]

	def parse(self, response):
		scrapedData = Selector(response).css('a.articleTitleListSmall')

		for data in scrapedData:
			item = DataItem()
			item['title'] = data.css('a.articleTitleListSmall::text').get(),
			item['source'] = 'Shia.bs - Article - Abu Iyyad',
			item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
			yield item


   def parse(self, response):
	  for href in response.css('a.articleTitleListSmall::attr(href)'):
		 url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback = self.parse_dir_contents)

   def parse_dir_contents(self, response):
	  for data in response.css():
			item = DataItem()
			item['url'] = response.request.url
			item['title'] = data.css('span.articleTitle::text').get(),
			item['text'] = data.css('div.articleContent::text').get(),
			item['source'] = 'Shia.bs - Article - Abu Iyyad',
			yield item
