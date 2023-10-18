import scrapy


class CermatiSpider(scrapy.Spider):
    name = "cermati"
    allowed_domains = ["cermati.com"]
    start_urls = ["https://cermati.com/artikel"]

    def parse(self, response):
        for article in response.css('div.margin-bottom-30 ul.panel-items-list li'):
            title = article.css('h3.item-title::text').get()
            link = response.urljoin(article.css('a::attr(href)').get())
            date = article.css('span.item-publish-date::text').getall()[-1].strip()
            category = article.css('span.item-category::text').get().strip() if article.css('span.item-category::text').get() else None

            yield {
                'title': title,
                'link': link,
                'date': date,
                'category': category
            }
